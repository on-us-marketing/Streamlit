from __future__ import annotations

import csv
import io
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


PROMPT_ALIASES = (
    "prompt",
    "query",
    "question",
    "tracked prompt",
    "search prompt",
)
MENTION_RATE_ALIASES = (
    "mention rate",
    "brand mention rate",
    "visibility rate",
    "visibility score",
    "ai visibility",
)
MENTION_COUNT_ALIASES = ("mentions", "brand mentions", "mention count")
RESPONSE_COUNT_ALIASES = ("responses", "total responses", "response count", "runs")
COMPETITOR_ALIASES = (
    "competitors",
    "top competitors",
    "competitor mentions",
    "mentioned competitors",
)
ENGINE_ALIASES = ("engine", "model", "platform", "answer engine", "assistant")
MARKET_ALIASES = ("market", "country", "region", "location")
LANGUAGE_ALIASES = ("language", "locale")
JOURNEY_ALIASES = ("journey stage", "buyer stage", "funnel stage", "intent")


def _key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def _text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _lookup(row: dict[str, Any], aliases: tuple[str, ...]) -> Any:
    normalized = {_key(name): value for name, value in row.items()}
    for alias in aliases:
        if _key(alias) in normalized and _text(normalized[_key(alias)]):
            return normalized[_key(alias)]
    return ""


def _number(value: Any, default: float = 0.0) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or "").replace(",", ""))
    if not match:
        return default
    try:
        return float(match.group(0))
    except ValueError:
        return default


def _percent(value: Any) -> float:
    raw = _text(value)
    number = _number(raw)
    if "%" in raw:
        return max(0.0, min(100.0, number))
    if 0.0 <= number <= 1.0:
        return number * 100.0
    return max(0.0, min(100.0, number))


def parse_uploaded_records(filename: str, payload: bytes) -> list[dict[str, Any]]:
    suffix = Path(filename).suffix.lower()
    text = payload.decode("utf-8-sig", errors="replace")
    if suffix == ".json":
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            for key in ("rows", "results", "data", "prompts", "gaps"):
                if isinstance(parsed.get(key), list):
                    parsed = parsed[key]
                    break
        if not isinstance(parsed, list):
            raise ValueError("JSON must contain a list of prompt-level records.")
        return [dict(item) for item in parsed if isinstance(item, dict)]
    return [dict(row) for row in csv.DictReader(io.StringIO(text))]


def infer_content_category(prompt: str) -> str:
    lowered = prompt.lower()
    if any(term in lowered for term in ("case study", "example of", "success story")):
        return "Case Study / Use Case Proof"
    if any(term in lowered for term in ("compare", " vs ", "versus", "best ", "top ")):
        return "Thought Leadership / Industry Insight"
    if any(term in lowered for term in ("launch", "announcement", "partnership", "expansion")):
        return "Partnership / Ecosystem / Milestone Announcement"
    if any(term in lowered for term in ("how to", "strategy", "increase", "improve", "drive ")):
        return "Sales Generating / Use Case Angle"
    return "Educational / Explainer"


def infer_target_audiences(prompt: str) -> list[str]:
    lowered = prompt.lower()
    mappings = (
        (("issuer", "credit card", "card scheme", "card-linked", "card linked"), "Card Schemes & Card Issuers"),
        (("bank", "banking", "financial service", "bancassurance"), "Banks & Financial Services"),
        (("insurance", "insurer", "policyholder", "policy renewal"), "Insurance"),
        (("mpf", "pension", "scheme member"), "Pensions & MPF"),
        (("mall", "property", "real estate", "tenant"), "Property & Real Estate / Malls"),
        (("survey", "respondent", "research panel", "market research"), "Research & Insights"),
        (("employee", "staff", "hr ", "workforce"), "Enterprise Procurement / HR"),
        (("event", "mice", "attendee", "conference"), "MICE & Events"),
        (("travel", "traveller", "traveler", "hospitality", "tourism"), "Travel & Hospitality"),
        (("merchant", "redemption partner"), "Merchants & Merchant Ecosystem"),
        (("retail", "fmcg", "consumer brand"), "Retail & FMCG"),
    )
    audiences: list[str] = []
    for terms, audience in mappings:
        if any(term in lowered for term in terms) and audience not in audiences:
            audiences.append(audience)
    return audiences


def infer_target_audience(prompt: str) -> str:
    """Backward-compatible primary audience helper.

    An empty string is intentional. Broad, promotional, event, and company-level
    topics must not be silently routed to Banks & Financial Services.
    """
    audiences = infer_target_audiences(prompt)
    return audiences[0] if audiences else ""


def infer_products(prompt: str) -> list[str]:
    lowered = prompt.lower()
    products: list[str] = []
    mappings = (
        (("card-linked", "card linked", "issuer", "spend qualification", "visa offer"), "VOP"),
        (("intelligence", "behavioral", "behavioural", "analytics", "retarget"), "On-us Intelligence"),
        (("express", "self-serve", "sme"), "On-us Express"),
        (("wellness", "green voucher", "esg", "carbon"), "Green & ESG Solution"),
        (("survey", "form", "lucky draw", "event", "lead capture"), "VAS"),
        (("voucher", "reward", "incentive", "fulfilment", "fulfillment", "merchant choice"), "Smart E-Voucher"),
    )
    for terms, product in mappings:
        if any(term in lowered for term in terms) and product not in products:
            products.append(product)
    return products or ["Smart E-Voucher"]


def normalize_geovector_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, row in enumerate(records, start=1):
        prompt = _text(_lookup(row, PROMPT_ALIASES))
        if not prompt:
            continue
        mention_count = _number(_lookup(row, MENTION_COUNT_ALIASES))
        response_count = _number(_lookup(row, RESPONSE_COUNT_ALIASES))
        raw_rate = _lookup(row, MENTION_RATE_ALIASES)
        mention_rate = _percent(raw_rate)
        if not _text(raw_rate) and response_count > 0:
            mention_rate = max(0.0, min(100.0, mention_count / response_count * 100.0))
        competitors = _text(_lookup(row, COMPETITOR_ALIASES))
        gap_score = round(max(0.0, 100.0 - mention_rate), 1)
        if competitors:
            gap_score = min(100.0, gap_score + 5.0)
        normalized.append(
            {
                "gap_id": _text(row.get("gap_id")) or f"GEO-{index:03d}",
                "prompt": prompt,
                "mention_rate": round(mention_rate, 1),
                "gap_score": gap_score,
                "competitors": competitors,
                "engine": _text(_lookup(row, ENGINE_ALIASES)) or "Multiple / not specified",
                "market": _text(_lookup(row, MARKET_ALIASES)) or "APAC / not specified",
                "language": _text(_lookup(row, LANGUAGE_ALIASES)) or "EN / not specified",
                "journey_stage": _text(_lookup(row, JOURNEY_ALIASES)) or "Not specified",
                "content_category": infer_content_category(prompt),
                "target_audience": infer_target_audiences(prompt),
                "relevant_products": infer_products(prompt),
                "source": "GeoVector",
            }
        )
    return sorted(normalized, key=lambda item: (-item["gap_score"], item["prompt"].lower()))


def build_gap_brief(gap: dict[str, Any]) -> dict[str, Any]:
    prompt = _text(gap.get("prompt"))
    mention_rate = float(gap.get("mention_rate", 0.0) or 0.0)
    competitors = _text(gap.get("competitors")) or "Not supplied"
    products = ", ".join(gap.get("relevant_products") or ["Smart E-Voucher"])
    opportunity_score = float(gap.get("opportunity_score", gap.get("gap_score", 0.0)) or 0.0)
    recommendation = _text(gap.get("recommended_action")) or "Create a focused GEO answer asset"
    ads_terms = [
        _text(row.get("search_term"))
        for row in gap.get("related_google_ads_rows", [])[:5]
        if _text(row.get("search_term"))
    ]
    ga4_pages = [
        _text(row.get("landing_page"))
        for row in gap.get("related_ga4_rows", [])[:3]
        if _text(row.get("landing_page"))
    ]
    source = _text(gap.get("source")) or "GeoVector"
    is_geo = "geovector" in source.lower()
    objective = (
        f"Create a master content source draft that directly answers: \"{prompt}\". "
        "Use the identified search and website opportunity to produce a factual, useful On-us content asset, "
        "then prepare it for the selected repurpose channels."
    )
    notes_parts = [
        f"Gap source: {source}.",
        f"Combined opportunity score: {opportunity_score:.1f}/100.",
        f"Recommended action: {recommendation}.",
        f"Relevant product context to verify: {products}.",
    ]
    if is_geo:
        notes_parts.extend(
            [
                f"Current On-us mention rate: {mention_rate:.1f}%.",
                f"Tracked engine: {gap.get('engine', 'Not specified')}.",
                f"Market: {gap.get('market', 'Not specified')}.",
                f"Competitors appearing in responses: {competitors}.",
            ]
        )
    notes_parts.append(
        "Answer the primary intent early. Explain the problem, relevant On-us mechanism, supported evidence, limitations, "
        "and practical next step. Treat demand and analytics data as planning evidence, not as public product proof."
    )
    notes = " ".join(notes_parts)
    if ads_terms:
        notes += f" Related Google Ads search terms: {', '.join(ads_terms)}."
    if ga4_pages:
        notes += f" Related GA4 landing pages to assess before creating a new page: {', '.join(ga4_pages)}."
    return {
        "content_category": gap.get("content_category") or infer_content_category(prompt),
        "target_audience": gap.get("target_audience") or infer_target_audiences(prompt),
        "content_objective": objective,
        "supporting_notes": notes,
        "similar_reference": (
            f"GeoVector tracked prompt: {prompt}\nMention rate: {mention_rate:.1f}%\nCompetitors: {competitors}"
            if is_geo
            else f"Search / analytics opportunity: {prompt}\nSource: {source}\nRecommended action: {recommendation}"
        ),
    }


SEARCH_DATA_TOPICS: tuple[dict[str, Any], ...] = (
    {
        "id": "EVOUCHER_PLATFORM",
        "prompt": "How should enterprises evaluate an electronic voucher platform?",
        "keywords": (
            "electronic voucher platform", "e-voucher platform", "evoucher platform",
            "digital voucher platform", "digital coupon platform", "電子禮券平台",
            "电子礼券平台", "禮券平台", "礼券平台", "gift card platform",
        ),
        "content_category": "Educational / Explainer",
        "target_audience": [],
        "relevant_products": ["Smart E-Voucher"],
    },
    {
        "id": "VOUCHER_COMPARISON",
        "prompt": "What is the difference between an e-voucher, gift card, cash voucher, and coupon?",
        "keywords": (
            "e voucher", "e-voucher", "egift", "e gift", "gift card", "gift voucher",
            "電子禮券", "电子礼券", "現金券", "现金券", "禮券", "礼券",
        ),
        "content_category": "Educational / Explainer",
        "target_audience": [],
        "relevant_products": ["Smart E-Voucher"],
    },
    {
        "id": "PLATFORM_EVALUATION",
        "prompt": "What should enterprises compare when choosing an e-voucher or employee rewards platform?",
        "keywords": (
            "edenred", "宜睿", "mezzofy", "reward gateway", "ocard", "eber",
            "payeasy", "stayfun", "echoss", "voucher platform comparison",
        ),
        "content_category": "Thought Leadership / Industry Insight",
        "target_audience": [],
        "relevant_products": ["Smart E-Voucher"],
    },
    {
        "id": "EMPLOYEE_REWARDS",
        "prompt": "How can enterprises simplify employee rewards and corporate gifting with e-vouchers?",
        "keywords": (
            "employee reward", "employee benefit", "staff reward", "corporate gifting",
            "corporate gift", "企業福利", "企业福利", "員工福利", "员工福利",
            "員工禮品", "员工礼品", "企業贈禮", "企业赠礼", "企業禮券", "企业礼券",
        ),
        "content_category": "Sales Generating / Use Case Angle",
        "target_audience": ["Enterprise Procurement / HR"],
        "relevant_products": ["Smart E-Voucher", "VAS"],
    },
    {
        "id": "LOYALTY_REWARDS",
        "prompt": "How can Smart E-Vouchers complement an existing membership or loyalty program?",
        "keywords": (
            "loyalty platform", "loyalty program", "membership system", "member reward",
            "會員系統", "会员系统", "會員平台", "会员平台", "會員卡", "会员卡",
            "會員積分", "会员积分", "集點系統", "集点系统",
        ),
        "content_category": "Educational / Explainer",
        "target_audience": [],
        "relevant_products": ["Smart E-Voucher", "On-us Intelligence"],
    },
    {
        "id": "ON_US_EXPRESS",
        "prompt": "When should a Hong Kong SME use On-us Express instead of an enterprise voucher solution?",
        "keywords": (
            "on us express", "on-us express", "onus express", "small business voucher",
            "sme voucher", "self serve voucher", "self-service voucher",
        ),
        "content_category": "Product Education / Solution Explainer",
        "target_audience": [],
        "relevant_products": ["On-us Express", "Smart E-Voucher"],
    },
    {
        "id": "MERCHANT_CHOICE",
        "prompt": "How does a multi-merchant e-voucher give recipients more reward choice?",
        "keywords": (
            "multi merchant", "multi-merchant", "merchant choice", "merchant network",
            "where to redeem", "redemption locations", "多商戶", "多商户", "商戶選擇", "商户选择",
        ),
        "content_category": "Product Education / Solution Explainer",
        "target_audience": [],
        "relevant_products": ["Smart E-Voucher"],
    },
    {
        "id": "CARD_LINKED",
        "prompt": "How can card-linked non-cashback incentives support issuer engagement campaigns?",
        "keywords": (
            "card linked", "card-linked", "credit card reward", "issuer reward",
            "visa offer platform", "spend qualification", "信用卡獎賞", "信用卡奖励",
        ),
        "content_category": "Educational / Explainer",
        "target_audience": ["Card Schemes & Card Issuers"],
        "relevant_products": ["VOP", "Smart E-Voucher"],
    },
    {
        "id": "SURVEY_INCENTIVES",
        "prompt": "How can automated e-voucher incentives improve survey reward fulfillment?",
        "keywords": (
            "survey incentive", "survey reward", "respondent reward", "research incentive",
            "問卷獎勵", "问卷奖励", "問卷禮券", "问卷礼券",
        ),
        "content_category": "Sales Generating / Use Case Angle",
        "target_audience": ["Research & Insights"],
        "relevant_products": ["On-us Form", "Smart E-Voucher"],
    },
    {
        "id": "GREEN_REWARDS",
        "prompt": "How can enterprises use sustainability-linked vouchers without overstating environmental impact?",
        "keywords": (
            "green voucher", "esg voucher", "sustainable reward", "wellness voucher",
            "綠色禮券", "绿色礼券", "永續獎勵", "可持續獎賞",
        ),
        "content_category": "ESG / Green / Wellness Content",
        "target_audience": [],
        "relevant_products": ["Green & ESG Solution", "Smart E-Voucher"],
    },
)


def _matches_topic(value: Any, keywords: tuple[str, ...]) -> bool:
    compact_value = re.sub(r"\s+", "", _text(value).lower())
    return any(re.sub(r"\s+", "", keyword.lower()) in compact_value for keyword in keywords)


def build_google_data_gap_candidates(
    google_ads_rows: list[dict[str, Any]] | None = None,
    ga4_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build concentrated, deterministic SEO/AEO opportunities from Ads and GA4.

    Google Ads contributes search-demand evidence. GA4 contributes existing-page
    coverage and engagement evidence. The result is planning guidance, not proof
    of product performance or a forecast of organic ranking.
    """
    ads = google_ads_rows or []
    analytics = ga4_rows or []
    candidates: list[dict[str, Any]] = []
    matched_ga4_ids: set[int] = set()
    for topic in SEARCH_DATA_TOPICS:
        topic_ads = [
            row for row in ads if _matches_topic(row.get("search_term", ""), topic["keywords"])
        ]
        topic_ga4 = [
            row for row in analytics if _matches_topic(row.get("landing_page", ""), topic["keywords"])
        ]
        matched_ga4_ids.update(id(row) for row in topic_ga4)
        impressions = sum(float(row.get("impressions", 0.0) or 0.0) for row in topic_ads)
        clicks = sum(float(row.get("clicks", 0.0) or 0.0) for row in topic_ads)
        conversions = sum(float(row.get("conversions", 0.0) or 0.0) for row in topic_ads)
        has_ads_signal = bool(topic_ads) and (impressions >= 5 or clicks > 0 or conversions > 0)

        ga4_sessions = sum(float(row.get("sessions", 0.0) or 0.0) for row in topic_ga4)
        engagement_rates = [
            float(row.get("engagement_rate", 0.0) or 0.0)
            for row in topic_ga4
            if float(row.get("engagement_rate", 0.0) or 0.0) > 0
        ]
        avg_engagement = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0.0
        if avg_engagement > 1.0:
            avg_engagement /= 100.0
        has_ga4_gap = bool(topic_ga4) and (ga4_sessions < 100 or avg_engagement < 0.35)
        if not has_ads_signal and not has_ga4_gap:
            continue

        source_parts = []
        if has_ads_signal:
            source_parts.append("Google Ads")
        if topic_ga4:
            source_parts.append("GA4")
        source = " + ".join(source_parts) or "GA4"
        base = {
            "gap_id": f"DATA-{topic['id']}",
            "prompt": topic["prompt"],
            "mention_rate": 0.0,
            "gap_score": 0.0,
            "competitors": "",
            "engine": "Not applicable",
            "market": "Based on imported Google data",
            "language": "Infer from search terms / page",
            "journey_stage": "Search and website opportunity",
            "content_category": topic["content_category"],
            "target_audience": list(topic["target_audience"]),
            "relevant_products": list(topic["relevant_products"]),
            "source": source,
            "related_google_ads_rows": sorted(
                topic_ads,
                key=lambda row: (
                    -float(row.get("conversions", 0.0) or 0.0),
                    -float(row.get("impressions", 0.0) or 0.0),
                ),
            )[:8],
            "related_ga4_rows": sorted(
                topic_ga4,
                key=lambda row: -float(row.get("sessions", 0.0) or 0.0),
            )[:5],
        }
        candidates.append(
            enrich_gap_opportunity(
                base,
                related_google_ads_rows=base["related_google_ads_rows"],
                related_ga4_rows=base["related_ga4_rows"],
            )
        )

    weak_unmatched_pages: list[dict[str, Any]] = []
    for row in analytics:
        if id(row) in matched_ga4_ids:
            continue
        landing_page = _text(row.get("landing_page"))
        if not landing_page or landing_page in {"/", "(not set)", "not set"}:
            continue
        sessions = float(row.get("sessions", 0.0) or 0.0)
        engagement = float(row.get("engagement_rate", 0.0) or 0.0)
        if engagement > 1.0:
            engagement /= 100.0
        if sessions >= 100 and engagement >= 0.35:
            continue
        weak_unmatched_pages.append(row)

    for index, row in enumerate(
        sorted(weak_unmatched_pages, key=lambda item: -float(item.get("sessions", 0.0) or 0.0))[:8],
        start=1,
    ):
        landing_page = _text(row.get("landing_page"))
        clean_path = landing_page.split("?", 1)[0].strip("/")
        page_topic = re.sub(r"[-_/]+", " ", clean_path.split("/")[-1]).strip() or "existing page"
        base = {
            "gap_id": f"DATA-GA4-{index:02d}",
            "prompt": f"How should On-us refresh the existing {page_topic} page for clearer SEO/AEO intent?",
            "mention_rate": 0.0,
            "gap_score": 0.0,
            "competitors": "",
            "engine": "Not applicable",
            "market": "Based on imported GA4 data",
            "language": "Infer from landing page",
            "journey_stage": "Existing-page refresh",
            "content_category": infer_content_category(page_topic),
            "target_audience": infer_target_audiences(page_topic),
            "relevant_products": infer_products(page_topic),
            "source": "GA4",
            "related_google_ads_rows": [],
            "related_ga4_rows": [row],
        }
        candidates.append(
            enrich_gap_opportunity(base, related_google_ads_rows=[], related_ga4_rows=[row])
        )
    return sorted(candidates, key=lambda item: (-item["opportunity_score"], item["prompt"].lower()))


def enrich_gap_opportunity(
    gap: dict[str, Any],
    *,
    related_google_ads_rows: list[dict[str, Any]] | None = None,
    related_ga4_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Combine GEO visibility, paid-search demand, and existing-site coverage.

    The score is a prioritisation aid, not a performance forecast. GEO remains the
    dominant signal. Google Ads adds evidence of active search demand, while GA4
    changes the recommended action from net-new creation to refresh/expansion when
    a related landing page already exists.
    """
    ads_rows = related_google_ads_rows or []
    ga4_rows = related_ga4_rows or []
    geo_gap = float(gap.get("gap_score", 0.0) or 0.0)

    impressions = sum(float(row.get("impressions", 0.0) or 0.0) for row in ads_rows)
    monthly_searches = sum(float(row.get("avg_monthly_searches", 0.0) or 0.0) for row in ads_rows)
    conversions = sum(float(row.get("conversions", 0.0) or 0.0) for row in ads_rows)
    demand_score = min(
        100.0,
        impressions / 20.0 + monthly_searches / 20.0 + conversions * 10.0,
    )

    sessions = sum(float(row.get("sessions", 0.0) or 0.0) for row in ga4_rows)
    engagement_rates = [
        float(row.get("engagement_rate", 0.0) or 0.0)
        for row in ga4_rows
        if float(row.get("engagement_rate", 0.0) or 0.0) > 0
    ]
    average_engagement = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0.0
    if average_engagement > 1.0:
        average_engagement /= 100.0

    if not ga4_rows:
        coverage_gap_score = 100.0
        recommended_action = "Create a new SEO/AEO pillar or explainer"
    elif sessions < 100 or average_engagement < 0.35:
        coverage_gap_score = 70.0
        recommended_action = "Refresh and expand the closest existing page"
    else:
        coverage_gap_score = 35.0
        recommended_action = "Strengthen the existing page for GEO citation and buyer intent"

    source = _text(gap.get("source")).lower()
    if "geovector" in source:
        opportunity_score = round(
            geo_gap * 0.60 + demand_score * 0.25 + coverage_gap_score * 0.15,
            1,
        )
    elif ads_rows:
        opportunity_score = round(demand_score * 0.65 + coverage_gap_score * 0.35, 1)
    else:
        opportunity_score = round(coverage_gap_score, 1)
    return {
        **gap,
        "opportunity_score": opportunity_score,
        "search_demand_score": round(demand_score, 1),
        "site_coverage_gap_score": round(coverage_gap_score, 1),
        "recommended_action": recommended_action,
        "related_google_ads_rows": ads_rows,
        "related_ga4_rows": ga4_rows,
    }


def save_gap_snapshot(root: Path, gaps: list[dict[str, Any]]) -> Path:
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_dir = root / "outputs" / "gap_sessions" / session_id
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "normalized_geo_gaps.json").write_text(
        json.dumps(gaps, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return output_dir
