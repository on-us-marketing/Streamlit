from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def fake_tavily_post(url: str, api_key: str, payload: dict) -> dict:
    return {
        "results": [
            {
                "title": "APAC card rewards report July 2026",
                "url": "https://example.org/reports/card-rewards-2026",
                "content": "Published July 12, 2026. A dated research summary.",
                "raw_content": "# APAC card rewards report\nPublished July 12, 2026.",
                "score": 0.9,
            }
        ],
        "usage": {"credits": 1},
    }


class StreamlitResearchFlowTests(unittest.TestCase):
    def test_company_keys_load_automatically_and_research_precedes_generation_settings(self) -> None:
        env_updates = {
            "LLM_API_KEY": "test-company-llm-key",
            "TAVILY_API_KEY": "test-company-tavily-key",
        }
        with patch.dict(os.environ, env_updates, clear=False):
            app = AppTest.from_file(str(APP_PATH)).run(timeout=30)

        self.assertEqual(len(app.exception), 0)
        headers = [item.value for item in app.header]
        self.assertLess(headers.index("Web Research"), headers.index("Generation Settings"))
        success_messages = [item.value for item in app.success]
        self.assertIn("Company LLM API loaded automatically", success_messages)
        self.assertIn("Company Tavily key loaded automatically", success_messages)

    def test_target_audience_is_optional_and_multi_select(self) -> None:
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        app.radio[0].set_value("Generate New Content").run(timeout=30)
        audience = next(
            item for item in app.multiselect
            if item.label == "Target Audience (optional, select more than one if needed)"
        )
        self.assertEqual(audience.value, [])
        audience.set_value(["Banks & Financial Services", "Insurance"]).run(timeout=30)
        self.assertEqual(
            next(
                item for item in app.multiselect
                if item.label == "Target Audience (optional, select more than one if needed)"
            ).value,
            ["Banks & Financial Services", "Insurance"],
        )

    @patch("on_us_content_agent.tools.research_tool._post_json", side_effect=fake_tavily_post)
    def test_research_pauses_for_source_approval(self, _mock_post) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            previous_root = os.environ.get("ON_US_PROJECT_ROOT")
            os.environ["ON_US_PROJECT_ROOT"] = temp_dir
            try:
                app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
                app.radio[0].set_value("Generate New Content").run(timeout=30)
                next(item for item in app.text_input if item.label == "LLM API key").set_value("test-llm-key")
                next(item for item in app.text_input if item.label == "Tavily API key").set_value("test-tavily-key")
                next(
                    item for item in app.checkbox
                    if item.label == "Run Web Research before generation"
                ).set_value(True).run(timeout=30)
                next(item for item in app.text_area if item.label == "Content Objective").set_value(
                    "Explain current card-linked incentive trends for APAC bank campaign managers."
                )
                app.button[0].click().run(timeout=30)
            finally:
                if previous_root is None:
                    os.environ.pop("ON_US_PROJECT_ROOT", None)
                else:
                    os.environ["ON_US_PROJECT_ROOT"] = previous_root

            self.assertEqual(len(app.exception), 0)
            headings = [item.value for item in app.subheader]
            self.assertIn("Web Research Source Approval", headings)
            self.assertTrue(any(item.label == "Approve this source for Master Content" for item in app.checkbox))
            self.assertTrue(any(item.label == "Continue to Content Generation" for item in app.button))


if __name__ == "__main__":
    unittest.main()
