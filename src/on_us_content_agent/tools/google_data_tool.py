from __future__ import annotations

import csv
import io
import json
import re
from datetime import date, timedelta
from typing import Any


GA4_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
GOOGLE_ADS_SCOPE = "https://www.googleapis.com/auth/adwords"


def _key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def _number(value: Any) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or "").replace(",", ""))
    return float(match.group(0)) if match else 0.0


def _lookup(row: dict[str, Any], *aliases: str) -> Any:
    normalized = {_key(name): value for name, value in row.items()}
    for alias in aliases:
        if _key(alias) in normalized:
            return normalized[_key(alias)]
    return ""


def parse_csv_records(payload: bytes) -> list[dict[str, Any]]:
    text = payload.decode("utf-8-sig", errors="replace")
    parsed_rows = list(csv.reader(io.StringIO(text)))
    header_markers = {
        "search term",
        "keyword",
        "landing page",
        "landing page query string",
        "landing page query string class",
        "page path",
        "page",
    }
    header_index = 0
    for index, row in enumerate(parsed_rows[:30]):
        normalized = {_key(cell) for cell in row}
        if normalized & header_markers:
            header_index = index
            break

    if not parsed_rows or header_index >= len(parsed_rows):
        return []
    headers = [str(value or "").strip() for value in parsed_rows[header_index]]
    output: list[dict[str, Any]] = []
    for row in parsed_rows[header_index + 1 :]:
        if not any(str(value or "").strip() for value in row):
            continue
        padded = list(row) + [""] * max(0, len(headers) - len(row))
        output.append(dict(zip(headers, padded[: len(headers)])))
    return output


def normalize_google_ads_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in records:
        search_term = str(
            _lookup(row, "search term", "query", "keyword", "search keyword") or ""
        ).strip()
        if not search_term or search_term.lower().startswith("total:"):
            continue
        output.append(
            {
                "search_term": search_term,
                "campaign": str(_lookup(row, "campaign", "campaign name") or "").strip(),
                "impressions": _number(_lookup(row, "impressions", "impr", "impr.")),
                "avg_monthly_searches": _number(
                    _lookup(row, "avg. monthly searches", "average monthly searches", "monthly searches")
                ),
                "clicks": _number(_lookup(row, "clicks")),
                "ctr": _number(_lookup(row, "ctr", "click through rate")),
                "conversions": _number(_lookup(row, "conversions", "all conversions")),
                "conversion_rate": _number(_lookup(row, "conversion rate", "conv rate")),
                "cost": _number(_lookup(row, "cost", "cost micros")),
                "competition": str(_lookup(row, "competition", "competition level") or "").strip(),
                "top_of_page_bid_low": _number(
                    _lookup(row, "top of page bid low range", "top of page bid low")
                ),
                "top_of_page_bid_high": _number(
                    _lookup(row, "top of page bid high range", "top of page bid high")
                ),
            }
        )
    return output


def normalize_ga4_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in records:
        landing_page = str(
            _lookup(row, "landing page", "landing page query string", "page path", "page") or ""
        ).strip()
        if not landing_page:
            continue
        output.append(
            {
                "landing_page": landing_page,
                "sessions": _number(_lookup(row, "sessions")),
                "active_users": _number(_lookup(row, "active users", "users")),
                "engaged_sessions": _number(_lookup(row, "engaged sessions")),
                "engagement_rate": _number(_lookup(row, "engagement rate")),
                "average_engagement_time": _number(
                    _lookup(row, "average engagement time", "average session duration")
                ),
                "key_events": _number(_lookup(row, "key events", "conversions")),
            }
        )
    return output


def _authorized_session(
    *,
    scopes: list[str],
    service_account_info: dict[str, Any] | None = None,
    oauth_config: dict[str, str] | None = None,
):
    try:
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2.credentials import Credentials
        from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    except ImportError as exc:
        raise RuntimeError(
            "Google API support is not installed. Run `pip install google-auth requests`."
        ) from exc

    if service_account_info:
        credentials = ServiceAccountCredentials.from_service_account_info(
            service_account_info, scopes=scopes
        )
    elif oauth_config:
        credentials = Credentials(
            token=None,
            refresh_token=oauth_config.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=oauth_config.get("client_id"),
            client_secret=oauth_config.get("client_secret"),
            scopes=scopes,
        )
    else:
        raise RuntimeError("No Google service account or OAuth credentials were configured.")
    return AuthorizedSession(credentials)


def fetch_ga4_landing_pages(
    *,
    property_id: str,
    service_account_json: str = "",
    oauth_config: dict[str, str] | None = None,
    days: int = 180,
) -> list[dict[str, Any]]:
    service_account_info = json.loads(service_account_json) if service_account_json.strip() else None
    session = _authorized_session(
        scopes=[GA4_SCOPE],
        service_account_info=service_account_info,
        oauth_config=oauth_config,
    )
    endpoint = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    payload = {
        "dateRanges": [
            {
                "startDate": (date.today() - timedelta(days=days)).isoformat(),
                "endDate": "yesterday",
            }
        ],
        "dimensions": [{"name": "landingPage"}, {"name": "sessionDefaultChannelGroup"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "activeUsers"},
            {"name": "engagedSessions"},
            {"name": "engagementRate"},
            {"name": "averageSessionDuration"},
            {"name": "keyEvents"},
        ],
        "dimensionFilter": {
            "filter": {
                "fieldName": "sessionDefaultChannelGroup",
                "stringFilter": {"matchType": "EXACT", "value": "Organic Search"},
            }
        },
        "limit": "1000",
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
    }
    response = session.post(endpoint, json=payload, timeout=90)
    if response.status_code >= 400:
        raise RuntimeError(f"GA4 Data API HTTP {response.status_code}: {response.text}")
    body = response.json()
    output: list[dict[str, Any]] = []
    for row in body.get("rows", []):
        dimensions = row.get("dimensionValues", [])
        metrics = row.get("metricValues", [])
        output.append(
            {
                "landing_page": dimensions[0].get("value", "") if dimensions else "",
                "channel_group": dimensions[1].get("value", "") if len(dimensions) > 1 else "",
                "sessions": _number(metrics[0].get("value")) if len(metrics) > 0 else 0,
                "active_users": _number(metrics[1].get("value")) if len(metrics) > 1 else 0,
                "engaged_sessions": _number(metrics[2].get("value")) if len(metrics) > 2 else 0,
                "engagement_rate": _number(metrics[3].get("value")) if len(metrics) > 3 else 0,
                "average_engagement_time": _number(metrics[4].get("value")) if len(metrics) > 4 else 0,
                "key_events": _number(metrics[5].get("value")) if len(metrics) > 5 else 0,
            }
        )
    return output


def fetch_google_ads_search_terms(
    *,
    customer_id: str,
    developer_token: str,
    oauth_config: dict[str, str],
    login_customer_id: str = "",
    api_version: str = "v23",
) -> list[dict[str, Any]]:
    session = _authorized_session(scopes=[GOOGLE_ADS_SCOPE], oauth_config=oauth_config)
    clean_customer_id = re.sub(r"\D", "", customer_id)
    endpoint = (
        f"https://googleads.googleapis.com/{api_version}/customers/"
        f"{clean_customer_id}/googleAds:searchStream"
    )
    query = """
        SELECT
          campaign.name,
          campaign_search_term_view.search_term,
          metrics.impressions,
          metrics.clicks,
          metrics.ctr,
          metrics.conversions,
          metrics.cost_micros
        FROM campaign_search_term_view
        WHERE segments.date DURING LAST_90_DAYS
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.impressions DESC
        LIMIT 1000
    """
    headers = {"developer-token": developer_token}
    if login_customer_id.strip():
        headers["login-customer-id"] = re.sub(r"\D", "", login_customer_id)
    response = session.post(endpoint, headers=headers, json={"query": query}, timeout=90)
    if response.status_code >= 400:
        raise RuntimeError(f"Google Ads API HTTP {response.status_code}: {response.text}")
    output: list[dict[str, Any]] = []
    for batch in response.json():
        for row in batch.get("results", []):
            metrics = row.get("metrics", {})
            output.append(
                {
                    "search_term": row.get("campaignSearchTermView", {}).get("searchTerm", ""),
                    "campaign": row.get("campaign", {}).get("name", ""),
                    "impressions": _number(metrics.get("impressions")),
                    "clicks": _number(metrics.get("clicks")),
                    "ctr": _number(metrics.get("ctr")),
                    "conversions": _number(metrics.get("conversions")),
                    "cost": _number(metrics.get("costMicros")) / 1_000_000,
                }
            )
    return [row for row in output if row["search_term"]]
