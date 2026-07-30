from __future__ import annotations

import unittest

from on_us_content_agent.tools.gap_tool import (
    build_gap_brief,
    build_google_data_gap_candidates,
    enrich_gap_opportunity,
    infer_target_audiences,
    normalize_geovector_records,
)
from on_us_content_agent.tools.google_data_tool import (
    normalize_google_ads_records,
    parse_csv_records,
)


class GapToolTests(unittest.TestCase):
    def test_geovector_aliases_and_percentage_are_normalized(self) -> None:
        gaps = normalize_geovector_records(
            [
                {
                    "Query": "What are the best card-linked rewards for issuers?",
                    "Visibility Rate": "10%",
                    "Platform": "ChatGPT",
                    "Top Competitors": "Example competitor",
                }
            ]
        )
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["mention_rate"], 10.0)
        self.assertEqual(gaps[0]["target_audience"], ["Card Schemes & Card Issuers"])
        self.assertIn("VOP", gaps[0]["relevant_products"])

    def test_target_audience_is_optional_and_can_be_multiple(self) -> None:
        self.assertEqual(infer_target_audiences("What is an electronic voucher platform?"), [])
        self.assertEqual(
            infer_target_audiences("How can banks and insurers improve employee rewards?"),
            ["Banks & Financial Services", "Insurance", "Enterprise Procurement / HR"],
        )

    def test_keyword_planner_columns_are_supported(self) -> None:
        rows = normalize_google_ads_records(
            [
                {
                    "Keyword": "card linked rewards",
                    "Avg. monthly searches": "1,000",
                    "Competition": "High",
                    "Top of page bid (high range)": "18.50",
                }
            ]
        )
        self.assertEqual(rows[0]["avg_monthly_searches"], 1000.0)
        self.assertEqual(rows[0]["competition"], "High")
        self.assertEqual(rows[0]["top_of_page_bid_high"], 18.5)

    def test_google_ads_metadata_lines_before_header_are_skipped(self) -> None:
        payload = (
            "Search terms report\n"
            '"June 1, 2026 - June 30, 2026"\n'
            "Search term,Campaign,Clicks,Impr.,CTR,Conversions\n"
            "digital coupon platform,PMAX for HK,2,13,15.38%,1\n"
        ).encode("utf-8")
        rows = normalize_google_ads_records(parse_csv_records(payload))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["search_term"], "digital coupon platform")
        self.assertEqual(rows[0]["impressions"], 13.0)

    def test_gap_enrichment_prioritizes_demand_and_generates_editable_brief(self) -> None:
        gap = normalize_geovector_records(
            [{"Prompt": "How can banks use card-linked rewards?", "Mention Rate": "5%"}]
        )[0]
        enriched = enrich_gap_opportunity(
            gap,
            related_google_ads_rows=[
                {"search_term": "card linked rewards", "avg_monthly_searches": 1000, "conversions": 3}
            ],
            related_ga4_rows=[],
        )
        brief = build_gap_brief(enriched)
        self.assertGreater(enriched["opportunity_score"], 80)
        self.assertEqual(enriched["recommended_action"], "Create a new SEO/AEO pillar or explainer")
        self.assertIn("card linked rewards", brief["supporting_notes"])
        self.assertIn("directly answers", brief["content_objective"])

    def test_ads_can_create_a_gap_without_geovector(self) -> None:
        gaps = build_google_data_gap_candidates(
            google_ads_rows=[
                {
                    "search_term": "企業福利平台",
                    "impressions": 120,
                    "clicks": 8,
                    "conversions": 2,
                }
            ],
            ga4_rows=[],
        )
        employee_gap = next(item for item in gaps if item["gap_id"] == "DATA-EMPLOYEE_REWARDS")
        self.assertEqual(employee_gap["source"], "Google Ads")
        self.assertEqual(employee_gap["target_audience"], ["Enterprise Procurement / HR"])
        self.assertEqual(employee_gap["recommended_action"], "Create a new SEO/AEO pillar or explainer")


if __name__ == "__main__":
    unittest.main()
