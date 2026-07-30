from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from on_us_content_agent.crew import DEFAULT_API_URL, DEFAULT_MODEL, DEFAULT_PROVIDER, RunConfig, run_master_content_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the On-us Content Agent workflow.")
    parser.add_argument("--request", default="on_us_content_agent/sample_request.json", help="Path to request JSON.")
    parser.add_argument("--kb", default=os.getenv("ON_US_KB_PATH", "on_us_content_agent/knowledge_base"), help="Knowledge base root directory.")
    parser.add_argument("--output-dir", default="on_us_content_agent/outputs/runs", help="Output directory for run artifacts.")
    parser.add_argument("--project-root", default="on_us_content_agent", help="Project root for config, local CrewAI storage, and runtime files.")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default=os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER), help="API provider: anthropic or openai-compatible.")
    parser.add_argument("--api-url", default=os.getenv("LLM_API_URL", os.getenv("ANTHROPIC_API_URL", DEFAULT_API_URL)), help="API base URL or endpoint.")
    parser.add_argument("--model", default=os.getenv("LLM_MODEL", os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)), help="Model name.")
    parser.add_argument("--review-model", default=os.getenv("LLM_REVIEW_MODEL", os.getenv("ANTHROPIC_REVIEW_MODEL", "")), help="Optional separate reviewer model.")
    parser.add_argument("--engine", choices=["controller", "compact", "crewai"], default="controller", help="Use the usable workflow controller, compact alias, or experimental CrewAI workflow.")
    parser.add_argument("--approved", action="store_true", help="Run repurpose / formatting stages after human approval.")
    parser.add_argument("--repurpose-draft", action="store_true", help="Generate testing-only repurpose output even if the quality gate fails.")
    parser.add_argument("--max-revision-rounds", type=int, default=1, help="Maximum automatic revision rounds when quality check fails.")
    parser.add_argument("--fast-mode", action="store_true", help="Use the three-call Drafter -> Reviewer/Finalizer -> Repurpose workflow.")
    parser.add_argument("--debug-artifacts", action="store_true", help="Keep prompts and intermediate Markdown files in fast mode.")
    parser.add_argument("--temperature", type=float, default=0.2, help="Generation temperature.")
    parser.add_argument("--planning-tokens", type=int, default=1800, help="Max tokens for planning stage.")
    parser.add_argument("--draft-tokens", type=int, default=2200, help="Max tokens for drafting stage.")
    parser.add_argument("--review-tokens", type=int, default=1800, help="Max tokens for review stage.")
    parser.add_argument("--dry-run", action="store_true", help="Build prompts and selected files without calling the API.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    request_path = Path(args.request)
    if not request_path.exists():
        raise SystemExit(f"Request file not found: {request_path}")

    request = json.loads(request_path.read_text(encoding="utf-8"))
    config = RunConfig(
        kb_path=Path(args.kb),
        output_dir=Path(args.output_dir),
        project_root=Path(args.project_root),
        api_url=args.api_url,
        model=args.model,
        review_model=args.review_model,
        provider=args.provider,
        engine=args.engine,
        approved=args.approved,
        repurpose_draft=args.repurpose_draft,
        max_revision_rounds=args.max_revision_rounds,
        fast_mode=args.fast_mode,
        lean_artifacts=not args.debug_artifacts,
        temperature=args.temperature,
        planning_tokens=args.planning_tokens,
        draft_tokens=args.draft_tokens,
        review_tokens=args.review_tokens,
        dry_run=args.dry_run,
    )
    run_dir = run_master_content_workflow(request, config)
    if args.dry_run:
        print(f"Dry run complete: {run_dir}")
        print("Prompts and selected files were written, no API call was made.")
    else:
        print(f"Run complete: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
