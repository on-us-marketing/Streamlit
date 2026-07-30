from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from on_us_content_agent.crew import (
    RunConfig,
    _safe_float,
    _safe_int,
    approved_research_context,
    build_fast_review_finalize_prompt,
    build_repurpose_prompt,
    repurpose_quality_issues,
    request_to_text,
    run_master_content_workflow,
)
from on_us_content_agent.tools.retrieval_tool import FOUNDATION_FILES, REVIEWER_FILES, select_relevant_files
from on_us_content_agent.tools.research_tool import build_research_brief, run_tavily_research


class ResearchToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = {
            "content_category": "Thought Leadership / Industry Insight",
            "target_audience": "Banks & Financial Services",
            "content_objective": "Explain current card-linked incentive trends for bank campaign managers.",
            "supporting_notes": "Focus on non-cashback benefits, spend qualification, and real-time transaction verification in APAC.",
            "future_repurpose_channels": ["Blog", "LinkedIn"],
        }

    def test_empty_log_metrics_are_zero(self) -> None:
        self.assertEqual(_safe_float(""), 0.0)
        self.assertEqual(_safe_float(None), 0.0)
        self.assertEqual(_safe_int(""), 0)
        self.assertEqual(_safe_int(None), 0)

    def test_repurpose_prompt_uses_shorter_blog_and_linkedin_limits(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb = Path(temp_dir)
            voice_file = kb / "Tier 3" / "Tier 3B - Channel Style" / "brand_voice.md"
            voice_file.parent.mkdir(parents=True)
            voice_file.write_text("LINKEDIN BRAND VOICE TEST MARKER", encoding="utf-8")
            prompt = build_repurpose_prompt(
                {
                    **self.request,
                    "channel": "Blog, LinkedIn",
                    "future_repurpose_channels": ["Blog", "LinkedIn"],
                },
                kb,
                "Master content",
                "Reviewer result",
                "",
                quality_passed=True,
                approved=False,
            )
            self.assertIn("standard Blog 400-600 words", prompt)
            self.assertIn("standard LinkedIn should aim for 140-190 words", prompt)
        self.assertIn("must not exceed 220 words", prompt)
        self.assertIn("Blog is an SEO/AEO retrieval asset", prompt)
        self.assertIn("LinkedIn is a marketing distribution asset", prompt)
        self.assertIn("Priority LinkedIn brand voice context", prompt)
        self.assertIn("authoritative for LinkedIn voice", prompt)
        self.assertIn("Emoji direction for this topic: 💳 or 📈", prompt)
        self.assertIn("Do not default to `🔹`", prompt)
        self.assertIn("This piece argues", prompt)
        self.assertIn("Answer the primary search intent directly", prompt)
        self.assertIn("LINKEDIN BRAND VOICE TEST MARKER", prompt)
        self.assertIn("Repurpose Governance Handoff", prompt)
        self.assertIn("first 210 characters", prompt)
        self.assertIn("Never use em dashes", prompt)

    def test_reviewer_loads_real_do_not_use_filename(self) -> None:
        expected = "Tier 1 - Factual Foundation/do-not-use_rules.md"
        self.assertIn(expected, FOUNDATION_FILES)
        self.assertIn(expected, REVIEWER_FILES)
        self.assertNotIn("Tier 1 - Factual Foundation/do_not_use.md", FOUNDATION_FILES)
        self.assertNotIn("Tier 1 - Factual Foundation/do_not_use.md", REVIEWER_FILES)

    def test_web_research_content_does_not_trigger_unrelated_kb_files(self) -> None:
        files = select_relevant_files(
            {
                "content_category": "Partnership / Ecosystem / Milestone Announcement",
                "target_audience": "Banks & Financial Services",
                "content_objective": "Announce Korea merchant network expansion and broader merchant choice.",
                "supporting_notes": "Focus on Korea travel and cross-border incentive campaigns.",
                "channel": "LinkedIn",
                "future_repurpose_channels": ["LinkedIn"],
                "web_research_bundle": {
                    "eligible_sources": [
                        {
                            "content": "VOP On-us Intelligence VAS On-us Express green ESG awards blog newsletter",
                        }
                    ]
                },
            },
            "",
        )
        self.assertIn("Tier 2 - Product Context/smart_e_voucher.md", files)
        self.assertIn("Tier 3/Tier 3B - Channel Style/linkedin.md", files)
        self.assertNotIn("Tier 2 - Product Context/vop.md", files)
        self.assertNotIn("Tier 2 - Product Context/on_us_intelligence.md", files)
        self.assertNotIn("Tier 2 - Product Context/vas.md", files)
        self.assertNotIn("Tier 3/Tier 3B - Channel Style/blog.md", files)
        self.assertNotIn("Tier 3/Tier 3B - Channel Style/newsletter.md", files)

    def test_fast_reviewer_judges_corrected_final_and_protects_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            prompt = build_fast_review_finalize_prompt(
                Path(temp_dir),
                self.request,
                "Routing context",
                "Draft content",
                [],
            )
        self.assertIn("against the corrected Final Revised Master Content", prompt)
        self.assertIn("under 350 words", prompt)
        self.assertIn("Never shorten, abbreviate, or stop the final master mid-section", prompt)

    def test_repurpose_quality_check_catches_mentor_flags(self) -> None:
        output = """# Repurpose Agent Output

## Publish-Ready Clean Copy
### LinkedIn Clean Copy
This piece argues that incentives outperform cashback — without adding complexity.

Infrequent. Hard to personalise. Even harder to measure.

#Onus #Rewards
"""
        issues = repurpose_quality_issues(
            output,
            {
                "channel": "LinkedIn",
                "future_repurpose_channels": ["LinkedIn"],
            },
            draft_text="Reviewed master content without comparative proof.",
            review_text="The outperformance comparison requires approval.",
        )
        joined = "\n".join(issues)
        self.assertIn("Academic or self-referential", joined)
        self.assertIn("Em dash", joined)
        self.assertIn("Forbidden hashtag #Onus", joined)
        self.assertIn("British English", joined)
        self.assertIn("Comparative outperformance", joined)
        self.assertIn("Fragmented or staccato", joined)

    def test_repurpose_quality_check_rejects_heavy_repeated_linkedin_template(self) -> None:
        output = """# Repurpose Agent Output

## Publish-Ready Clean Copy
### LinkedIn Clean Copy
One concise idea should lead the post.

🔹 First detailed benefit with 20+ signals.
🔹 Second detailed benefit with 85% performance.
🔹 Third detailed benefit that turns the post into a feature inventory.

#SmartEVoucher #Incentives #Marketing
"""
        issues = repurpose_quality_issues(
            output,
            {
                "channel": "LinkedIn",
                "future_repurpose_channels": ["LinkedIn"],
            },
            draft_text="20+ signals and 85% performance are approved for this test.",
            review_text="Approved for this test.",
        )
        joined = "\n".join(issues)
        self.assertIn("keep at most 2", joined)
        self.assertIn("repeated `🔹`", joined)
        self.assertIn("multiple proof points", joined)

    @patch("on_us_content_agent.crew.run_stage")
    def test_fast_mode_uses_three_llm_stages_and_skips_planning_and_visual(self, mock_stage) -> None:
        section_names = [
            "Executive Narrative",
            "Audience Context and Business Tension",
            "On-us Point of View",
            "Solution Story and Product Mechanism",
            "Proof / Case Support",
            "Why This Matters For The Buyer",
            "Repurpose Direction",
            "Human Review Appendix",
            "Claim Boundaries",
            "Open Questions",
            "Reference Trace",
        ]
        paragraph = " ".join(["Supported business context for human review."] * 18)
        master = "# Master Content Draft\n\n" + "\n\n".join(
            f"## {name}\n\n{paragraph}" for name in section_names
        )

        def fake_stage(**kwargs):
            stage = kwargs["stage"]
            if stage == "writer_agent":
                text = master
            elif stage == "evaluation_safeguarding_and_finalizer":
                text = (
                    "# Fast Review Result\n\nPass / Fail: PASS\n\n"
                    "## Key Issues Found\n- None.\n\n"
                    "## Fixes Applied\n- None required.\n\n"
                    "## Remaining Human Decisions\n- Final human approval.\n\n"
                    "## Final Recommendation\n- Proceed to human review.\n\n"
                    "# Final Revised Master Content\n\n"
                    + master
                )
            elif stage == "repurpose_agents":
                text = """# Repurpose Agent Output

## Safety Status
Preview only.

## Publish-Ready Clean Copy
### Blog Clean Copy
Testing copy for the Blog channel.

### LinkedIn Clean Copy
Bank campaign teams are looking for reward experiences that feel relevant without adding unnecessary complexity to campaign delivery.
Clearer reward choice can help create a stronger customer moment while keeping the campaign message focused.

At On-us, we help marketers connect campaign design with practical reward journeys. Smart E-Vouchers can give recipients a choice of participating merchants while providing campaign teams with a more consistent way to deliver and review the reward experience.

For campaign managers, the opportunity is to move beyond one-size-fits-all rewards and make each incentive more useful to the recipient. A more relevant reward experience can support stronger attention at the moment the campaign reaches the customer.

Explore the right incentive approach for your next customer engagement campaign with On-us.

#SmartEVoucher #CustomerEngagement #IncentiveMarketing

## Channel Review Notes
- Human approval is still required.
"""
            else:
                raise AssertionError(f"Unexpected LLM stage in fast mode: {stage}")
            log = {
                "stage": stage,
                "provider": "anthropic",
                "model": "test-model",
                "input_tokens": 10,
                "output_tokens": 20,
                "total_tokens": 30,
                "time_seconds": 0.1,
            }
            return text, log

        mock_stage.side_effect = fake_stage
        with tempfile.TemporaryDirectory() as temp_dir, patch.dict(os.environ, {"LLM_API_KEY": "test-key"}):
            root = Path(temp_dir)
            kb = root / "knowledge_base"
            kb.mkdir()
            run_dir = run_master_content_workflow(
                self.request,
                RunConfig(
                    kb_path=kb,
                    output_dir=root / "runs",
                    project_root=root,
                    fast_mode=True,
                    repurpose_draft=True,
                ),
            )
            planning_exists = (run_dir / "01_planning_agent_output.md").exists()
            visual_exists = (run_dir / "03_visual_recommendation_output.md").exists()
            final_exists = (run_dir / "final_master_content.md").exists()
            review_exists = (run_dir / "content_review.md").exists()
            selected_kb_exists = (run_dir / "selected_kb_files.md").exists()
            prompt_dir_exists = (run_dir / "prompts").exists()
            repurpose_exists = (run_dir / "repurpose_content.md").exists()

        stages = [call.kwargs["stage"] for call in mock_stage.call_args_list]
        self.assertEqual(
            stages,
            ["writer_agent", "evaluation_safeguarding_and_finalizer", "repurpose_agents"],
        )
        self.assertFalse(planning_exists)
        self.assertFalse(visual_exists)
        self.assertFalse(selected_kb_exists)
        self.assertFalse(prompt_dir_exists)
        self.assertTrue(final_exists)
        self.assertTrue(review_exists)
        self.assertTrue(repurpose_exists)

    @staticmethod
    def fake_post(url: str, api_key: str, payload: dict) -> dict:
        if url.endswith("/search") and "safe_search" in payload:
            raise AssertionError("Free Tavily requests must not include the Enterprise-only safe_search parameter")
        if url.endswith("/extract"):
            return {"results": [], "usage": {"credits": 0}}
        if payload.get("topic") == "news":
            return {
                "results": [
                    {
                        "title": "APAC payments outlook July 2026",
                        "url": "https://example.org/reports/payments-outlook-2026",
                        "content": "Published July 12, 2026. Issuers are testing new reward formats.",
                        "raw_content": "# APAC payments outlook\nPublished July 12, 2026.",
                        "score": 0.91,
                    },
                    {
                        "title": "Forum thread about rewards 2026",
                        "url": "https://reddit.com/r/payments/example",
                        "content": "A discussion.",
                        "score": 0.95,
                    },
                ],
                "usage": {"credits": 1},
            }
        return {
            "results": [
                {
                    "title": "Undated incentive overview",
                    "url": "https://example.com/incentives",
                    "content": "No publication date is shown.",
                    "score": 0.8,
                },
                {
                    "title": "Unrelated executive appointment July 2026",
                    "url": "https://example.com/executive-appointment",
                    "content": "Published July 4, 2026. A company appointed a new chief executive.",
                    "score": 0.89,
                }
            ],
            "usage": {"credits": 1},
        }

    @patch("on_us_content_agent.tools.research_tool._post_json", side_effect=fake_post.__func__)
    def test_search_filters_and_credit_limit(self, _mock_post) -> None:
        bundle = run_tavily_research(
            api_key="test-key",
            request=self.request,
            focus=["Industry trends and market change", "Latest news"],
            query_count=2,
            max_sources=5,
        )
        self.assertEqual(bundle["query_count"], 2)
        self.assertEqual(bundle["credits_used_reported"], 2)
        self.assertTrue(all(len(item["query"]) <= 400 for item in bundle["queries"]))
        self.assertIn("non-cashback benefits", bundle["queries"][0]["query"])
        self.assertIn("real-time transaction verification", bundle["queries"][1]["query"])
        self.assertTrue(bundle["queries"][0]["query"].startswith("current card-linked incentive trends"))
        self.assertIn("Content Objective and Supporting Notes drive the search", bundle["input_alignment"]["priority_rule"])
        self.assertEqual(len(bundle["eligible_sources"]), 1)
        self.assertEqual(bundle["eligible_sources"][0]["url"], "https://example.org/reports/payments-outlook-2026")
        reasons = " ".join(source["excluded_reason"] for source in bundle["excluded_sources"])
        self.assertIn("No publication", reasons)
        self.assertIn("Blocked low-governance domain", reasons)
        self.assertIn("Low relevance to Content Objective and Supporting Notes", reasons)

    @patch("on_us_content_agent.tools.research_tool._post_json", side_effect=fake_post.__func__)
    def test_only_approved_source_enters_brief_and_run(self, _mock_post) -> None:
        bundle = run_tavily_research(
            api_key="test-key",
            request=self.request,
            focus=["Latest news"],
            query_count=2,
            max_sources=5,
        )
        approved_url = bundle["eligible_sources"][0]["url"]
        brief = build_research_brief(bundle, approved_urls={approved_url})
        self.assertIn(approved_url, brief)
        self.assertIn("Human-approved external sources", brief)

        request = dict(self.request)
        request["web_research_bundle"] = bundle
        request["approved_web_research_urls"] = [approved_url]
        text = request_to_text(request)
        self.assertNotIn("raw_responses", text)
        self.assertIn("approved_external_source_count: 1", text)
        self.assertIn(approved_url, approved_research_context(request))

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            kb = root / "knowledge_base"
            kb.mkdir()
            output = root / "runs"
            run_dir = run_master_content_workflow(
                request,
                RunConfig(kb_path=kb, output_dir=output, project_root=root, dry_run=True),
            )
            self.assertTrue((run_dir / "web_research_brief.md").exists())
            saved_request = json.loads((run_dir / "request.json").read_text(encoding="utf-8"))
            self.assertNotIn("raw_responses", json.dumps(saved_request))


if __name__ == "__main__":
    unittest.main()
