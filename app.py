from __future__ import annotations

import html
import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("ON_US_PROJECT_ROOT", str(APP_DIR))).resolve()
SRC = APP_DIR / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from on_us_content_agent.crew import (
    DEFAULT_API_URL,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    RunConfig,
    run_master_content_workflow,
)
from on_us_content_agent.tools.research_tool import (
    build_research_brief,
    run_tavily_research,
    save_research_artifacts,
)
from on_us_content_agent.tools.gap_tool import (
    build_gap_brief,
    build_google_data_gap_candidates,
    enrich_gap_opportunity,
    normalize_geovector_records,
    parse_uploaded_records,
    save_gap_snapshot,
)
from on_us_content_agent.tools.google_data_tool import (
    fetch_ga4_landing_pages,
    fetch_google_ads_search_terms,
    normalize_ga4_records,
    normalize_google_ads_records,
    parse_csv_records,
)


CATEGORY_OPTIONS = [
    "Thought Leadership / Industry Insight",
    "Educational / Explainer",
    "Product Education / Solution Explainer",
    "Sales Generating / Use Case Angle",
    "Case Study / Use Case Proof",
    "Partnership / Ecosystem / Milestone Announcement",
    "Event / Award / Recognition",
    "ESG / Green / Wellness Content",
    "Talent / Culture / Community",
]

TA_OPTIONS = [
    "Banks & Financial Services",
    "Card Schemes & Card Issuers",
    "Insurance",
    "Pensions & MPF",
    "Retail & FMCG",
    "Property & Real Estate / Malls",
    "Travel & Hospitality",
    "MICE & Events",
    "Research & Insights",
    "Enterprise Procurement / HR",
    "Merchants & Merchant Ecosystem",
]

CHANNEL_OPTIONS = ["Blog", "LinkedIn", "Newsletter", "Webflow"]
LANGUAGE_OPTIONS = ["EN", "ZH-HK", "ZH-TW"]

RESEARCH_FOCUS_OPTIONS = [
    "Industry trends and market change",
    "External statistics and research reports",
    "Competitor content",
    "Latest news",
    "SEO/GEO content gap",
]

PROVIDER_OPTIONS = ["anthropic", "openai"]
PROVIDER_PRESETS = {
    "Claude / devaicode": {
        "provider": "anthropic",
        "api_url": "https://devaicode.dev/v1/messages",
        "model": "claude-sonnet-5",
    },
    "NVIDIA / Llama 3.2 3B": {
        "provider": "openai",
        "api_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "meta/llama-3.2-3b-instruct",
    },
    "NVIDIA / GPT-OSS 20B": {
        "provider": "openai",
        "api_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "openai/gpt-oss-20b",
    },
    "Custom": {
        "provider": DEFAULT_PROVIDER,
        "api_url": DEFAULT_API_URL,
        "model": DEFAULT_MODEL,
    },
}


def text_or_empty(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def secret_value(name: str) -> str:
    try:
        return str(st.secrets.get(name, "") or "").strip()
    except Exception:
        return ""


def secret_or_env(*names: str) -> str:
    for name in names:
        value = secret_value(name) or os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def parse_urls(*values: str) -> list[str]:
    urls: list[str] = []
    for value in values:
        for item in re.split(r"[\s,]+", value or ""):
            cleaned = item.strip()
            if cleaned.startswith(("http://", "https://")) and cleaned not in urls:
                urls.append(cleaned)
    return urls[:5]


def create_research_session_dir() -> Path:
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = ROOT / "outputs" / "research_sessions" / session_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_research_stage(
    request: dict[str, Any],
    *,
    tavily_api_key: str,
    focus: list[str],
    query_count: int,
    max_sources: int,
    provided_urls: list[str],
) -> tuple[dict[str, Any], Path]:
    bundle = run_tavily_research(
        api_key=tavily_api_key,
        request=request,
        focus=focus,
        query_count=query_count,
        max_sources=max_sources,
        provided_urls=provided_urls,
    )
    session_dir = create_research_session_dir()
    save_research_artifacts(session_dir, bundle, approved_urls=None)
    return bundle, session_dir


def list_md_files(run_dir: Path) -> list[Path]:
    if not run_dir.exists():
        return []
    return sorted(run_dir.glob("*.md"))


def zip_run_dir(run_dir: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(run_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(run_dir.parent))
    buffer.seek(0)
    return buffer.read()


def build_request(form: dict[str, Any]) -> dict[str, Any]:
    target_audiences = form.get("target_audience") or []
    if isinstance(target_audiences, str):
        target_audiences = [target_audiences] if target_audiences.strip() else []
    return {
        "content_category": form["content_category"],
        "target_audience": target_audiences,
        "audience_scope": "selected" if target_audiences else "broad / not specified",
        "content_objective": form["content_objective"],
        "channel": ", ".join(form["channels"]),
        "supporting_notes": form["supporting_notes"],
        "claims_to_include": form["claims_to_include"],
        "claims_to_avoid": form["claims_to_avoid"],
        "similar_reference": form["similar_reference"],
        "similar_reference_url": form["similar_reference_url"],
        "research_focus": form.get("research_focus", RESEARCH_FOCUS_OPTIONS),
        "research_source_urls": form.get("research_source_urls", []),
        "future_repurpose_channels": form["channels"],
        "target_languages": form["languages"],
        "human_input_policy": {
            "human_provided": [
                "content_category",
                "target_audience",
                "content_objective",
                "supporting_notes",
                "claims_to_include",
                "claims_to_avoid",
                "similar_reference",
                "research_focus",
                "research_source_urls",
            ],
            "llm_should_infer": [
                "writing_angle",
                "relevant_product_solution",
                "relevant_case_study",
                "required_structure",
                "selected_kb_files",
                "repurpose_structure",
            ],
        },
    }


def run_generator(request: dict[str, Any], settings: dict[str, Any]) -> Path:
    previous_env = {
        "LLM_API_KEY": os.environ.get("LLM_API_KEY"),
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY"),
        "LLM_PROVIDER": os.environ.get("LLM_PROVIDER"),
        "LLM_API_URL": os.environ.get("LLM_API_URL"),
        "LLM_MODEL": os.environ.get("LLM_MODEL"),
    }

    os.environ["LLM_API_KEY"] = settings["api_key"]
    os.environ["ANTHROPIC_API_KEY"] = settings["api_key"]
    os.environ["LLM_PROVIDER"] = settings["provider"]
    os.environ["LLM_API_URL"] = settings["api_url"]
    os.environ["LLM_MODEL"] = settings["model"]
    try:
        config = RunConfig(
            kb_path=ROOT / "knowledge_base",
            output_dir=ROOT / "outputs" / "runs",
            project_root=ROOT,
            api_url=settings["api_url"],
            provider=settings["provider"],
            model=settings["model"],
            review_model=settings["review_model"],
            approved=settings.get("human_approved", False),
            repurpose_draft=True,
            max_revision_rounds=settings["max_revision_rounds"],
            fast_mode=settings.get("fast_mode", True),
            lean_artifacts=settings.get("lean_artifacts", True),
            temperature=settings["temperature"],
            planning_tokens=settings["planning_tokens"],
            draft_tokens=settings["draft_tokens"],
            review_tokens=settings["review_tokens"],
            dry_run=False,
        )
        return run_master_content_workflow(request, config)
    finally:
        for key, value in previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def latest_file(run_dir: Path, pattern: str) -> Path | None:
    matches = sorted(run_dir.glob(pattern))
    return matches[-1] if matches else None


def best_master_file(run_dir: Path) -> Path | None:
    candidates = [
        run_dir / "final_master_content.md",
        latest_file(run_dir, "*master_content_revision_round_*.md"),
        run_dir / "draft_needs_revision.md",
        run_dir / "02_master_content_draft_v1.md",
    ]
    for candidate in candidates:
        if candidate and candidate.exists() and candidate.read_text(encoding="utf-8", errors="replace").strip():
            return candidate
    return None


def best_repurpose_file(run_dir: Path) -> Path | None:
    candidates = [
        run_dir / "repurpose_content.md",
        run_dir / "90_repurpose_agent_output.md",
        run_dir / "90_repurpose_preview.md",
        run_dir / "90_repurpose_draft_for_testing.md",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.read_text(encoding="utf-8", errors="replace").strip():
            return candidate
    return None


def best_reviewer_file(run_dir: Path) -> Path | None:
    lean_review = run_dir / "content_review.md"
    if lean_review.exists() and lean_review.read_text(encoding="utf-8", errors="replace").strip():
        return lean_review
    return latest_file(run_dir, "*_evaluation_safeguarding_output.md")


def workflow_state(run_dir: Path) -> dict[str, Any]:
    state_path = run_dir / "workflow_state.json"
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def split_sections(markdown_text: str, level: int = 2) -> list[tuple[str, str]]:
    marker = "#" * level
    pattern = re.compile(rf"^{re.escape(marker)}\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(markdown_text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
        sections.append((match.group(1).strip(), markdown_text[start:end].strip()))
    return sections


def frontmatter_value(master: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s*(.+)$", master, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def master_title(master: str) -> str:
    return frontmatter_value(master, "Working title") or "Master Content Draft"


def subsection(markdown_text: str, title_pattern: str) -> str:
    pattern = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(markdown_text))
    for index, match in enumerate(matches):
        if re.search(title_pattern, match.group(1), re.IGNORECASE):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
            return markdown_text[start:end].strip()
    return ""


def bullet_items(text: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^[-*]\s+", line):
            if current:
                items.append(" ".join(current).strip())
            current = [re.sub(r"^[-*]\s+", "", line).strip()]
        elif current:
            current.append(line)
    if current:
        items.append(" ".join(current).strip())
    return items


def classify_claim_boundaries(claim_text: str) -> dict[str, list[str]]:
    groups = {"safe": [], "warn": [], "never": []}
    current = "warn"
    for raw in claim_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        lower = line.lower()
        if "can be said" in lower or "safe" in lower:
            current = "safe"
            continue
        if "must be avoided" in lower or "never" in lower or "avoid" == lower.strip(":"):
            current = "never"
            continue
        if "requires approval" in lower or "requires human" in lower or "requires confirmation" in lower:
            current = "warn"
            continue
        if re.match(r"^[-*]\s+", line):
            item = re.sub(r"^[-*]\s+", "", line).strip()
            if item:
                groups[current].append(item)
    if not any(groups.values()) and claim_text.strip():
        groups["warn"] = bullet_items(claim_text) or [claim_text.strip()]
    return groups


def reference_items(reference_text: str) -> list[str]:
    items = bullet_items(reference_text)
    if items:
        return items
    return [line.strip() for line in reference_text.splitlines() if line.strip()]


def read_request(run_dir: Path) -> dict[str, Any]:
    request_path = run_dir / "request.json"
    if not request_path.exists():
        return {}
    try:
        return json.loads(request_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def requested_channel_names(run_dir: Path) -> set[str]:
    request = read_request(run_dir)
    values: list[str] = []
    for key in ["future_repurpose_channels", "target_channels"]:
        value = request.get(key, [])
        if isinstance(value, list):
            values.extend(str(item) for item in value)
    channel = request.get("channel", "")
    if isinstance(channel, str):
        values.append(channel)
    lowered = " ".join(values).lower()
    result: set[str] = set()
    if "blog" in lowered:
        result.add("blog")
    if "linkedin" in lowered or "linked in" in lowered:
        result.add("linkedin")
    return result


def section_by_heading(markdown_text: str, heading_patterns: list[str]) -> str:
    pattern = re.compile(r"^(#{2,4})\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(markdown_text))
    for index, match in enumerate(matches):
        heading = match.group(2).strip()
        if any(re.search(item, heading, re.IGNORECASE) for item in heading_patterns):
            start = match.end()
            end = len(markdown_text)
            current_level = len(match.group(1))
            for next_match in matches[index + 1 :]:
                if len(next_match.group(1)) <= current_level:
                    end = next_match.start()
                    break
            return markdown_text[start:end].strip()
    return ""


def clean_publish_copy(text: str) -> str:
    text = re.sub(r"^```[a-zA-Z]*\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text.strip())
    lines = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if re.match(r"^\s*#{1,6}\s+", line):
            line = re.sub(r"^\s*#{1,6}\s+", "", line)
        if re.match(r"^\s*(status|notes?|safety status)\s*:", line, re.IGNORECASE):
            continue
        if re.match(r"^\s*(testing only|preview only|not requested)\b", line, re.IGNORECASE):
            continue
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        lines.append(line)
    return "\n".join(lines).strip()


def extract_clean_channel_copy(repurpose: str, channel: str) -> str:
    if channel == "blog":
        patterns = [
            r"Blog\s+Clean\s+Copy",
            r"Blog\s+Publish[- ]Ready\s+Copy",
            r"Blog\s+Ready[- ]to[- ]Publish\s+Copy",
            r"Blog\s+Draft\s*/\s*Notes",
        ]
    else:
        patterns = [
            r"LinkedIn\s+Clean\s+Copy",
            r"LinkedIn\s+Publish[- ]Ready\s+Copy",
            r"LinkedIn\s+Ready[- ]to[- ]Publish\s+Copy",
            r"LinkedIn\s+Draft\s*/\s*Notes",
        ]
    return clean_publish_copy(section_by_heading(repurpose, patterns))


def markdown_to_plain_excerpt(markdown_text: str, limit: int = 260) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", markdown_text)
    text = re.sub(r"[*_#>-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + ("..." if len(text) > limit else "")


def inject_review_css() -> None:
    st.markdown(
        """
        <style>
        .brief-card {
            border-top: 3px solid #000;
            border-bottom: 1px solid #E6E8EC;
            padding: 1.35rem 0 1rem 0;
            margin-bottom: .75rem;
        }
        .brief-eyebrow {
            color: #FE004B;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin-bottom: .35rem;
        }
        .brief-title {
            color: #000;
            font-size: 1.65rem;
            line-height: 1.25;
            font-weight: 500;
            margin-bottom: .85rem;
        }
        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: .4rem;
            margin: .18rem .25rem .18rem 0;
            padding: .32rem .65rem;
            border-radius: 99px;
            font-size: .78rem;
            font-weight: 700;
        }
        .chip-safe { background: #E9F6EF; color: #0E7A4B; }
        .chip-warn { background: #FCF3E0; color: #9A6400; }
        .chip-never { background: #FBEAEC; color: #B00020; }
        .chip-open { background: #F6F7F9; color: #40454F; }
        .claim-card {
            border: 1px solid #E6E8EC;
            border-left: 4px solid #999;
            padding: .7rem .85rem;
            margin: .42rem 0;
            color: #111;
            font-size: .9rem;
            line-height: 1.45;
        }
        .claim-safe { border-left-color: #0E7A4B; background: #E9F6EF; }
        .claim-warn { border-left-color: #9A6400; background: #FCF3E0; }
        .claim-never { border-left-color: #B00020; background: #FBEAEC; }
        .claim-label {
            display: inline-block;
            margin-right: .45rem;
            font-size: .68rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .small-muted { color: #8A8F99; font-size: .82rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_chip(label: str, kind: str) -> str:
    return f'<span class="status-chip chip-{kind}">{html.escape(label)}</span>'


def render_claim_card(text: str, kind: str, label: str) -> None:
    st.markdown(
        f'<div class="claim-card claim-{kind}"><span class="claim-label">{html.escape(label)}</span>{html.escape(text)}</div>',
        unsafe_allow_html=True,
    )


def render_brief_card(master: str, run_dir: Path, master_file: Path | None, reviewer_file: Path | None) -> None:
    state = workflow_state(run_dir)
    quality_pass = state.get("quality_pass")
    status = "PASS" if quality_pass else "NEEDS REVISION"
    status_kind = "safe" if quality_pass else "warn"
    st.markdown(
        f"""
        <div class="brief-card">
            <div class="brief-eyebrow">Master Content Review · {html.escape(status)}</div>
            <div class="brief-title">{html.escape(master_title(master))}</div>
        </div>
        <div>
            {status_chip(status, status_kind)}
            {status_chip('Revision view', 'open')}
            {status_chip('Human review required', 'warn')}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_master_review(run_dir: Path, master: str, reviewer: str, selected_files: str, master_file: Path | None) -> None:
    inject_review_css()
    reviewer_file = best_reviewer_file(run_dir)
    render_brief_card(master, run_dir, master_file, reviewer_file)

    sections = split_sections(master, level=2)
    appendix = ""
    narrative_sections: list[tuple[str, str]] = []
    for title, body in sections:
        if "human review appendix" in title.lower():
            appendix = body
        else:
            narrative_sections.append((title, body))

    claim_groups = classify_claim_boundaries(subsection(appendix, r"Claim Boundaries"))
    open_questions = bullet_items(subsection(appendix, r"Open Questions"))
    references = reference_items(subsection(appendix, r"Reference Trace"))

    st.markdown(
        "".join(
            [
                status_chip(f"{len(claim_groups['safe'])} safe claims", "safe"),
                status_chip(f"{len(claim_groups['warn'])} approval / confirm items", "warn"),
                status_chip(f"{len(claim_groups['never'])} avoid items", "never"),
                status_chip(f"{len(open_questions)} open questions", "open"),
            ]
        ),
        unsafe_allow_html=True,
    )

    tab_narrative, tab_claims, tab_review = st.tabs(["Narrative", "Claim Boundaries", "Review & Trace"])

    with tab_narrative:
        st.caption("This is the revisioned master content shown in human-readable sections. Each section can be opened or collapsed for review.")
        for index, (title, body) in enumerate(narrative_sections, start=1):
            expanded = index == 1
            with st.expander(f"{index:02d} · {title}", expanded=expanded):
                st.markdown(body)

    with tab_claims:
        st.caption("Claim boundaries are separated by usage risk so reviewers can quickly see what is safe, what needs approval, and what should not be used.")
        left, middle, right = st.columns(3)
        with left:
            st.subheader("Safe")
            if claim_groups["safe"]:
                for item in claim_groups["safe"]:
                    render_claim_card(item, "safe", "SAFE")
            else:
                st.info("No safe claims detected in the appendix.")
        with middle:
            st.subheader("Needs Approval")
            if claim_groups["warn"]:
                for item in claim_groups["warn"]:
                    render_claim_card(item, "warn", "CHECK")
            else:
                st.info("No approval-needed claims detected in the appendix.")
        with right:
            st.subheader("Avoid")
            if claim_groups["never"]:
                for item in claim_groups["never"]:
                    render_claim_card(item, "never", "AVOID")
            else:
                st.info("No avoid items detected in the appendix.")

    with tab_review:
        st.caption("Open questions are checkable for human review. Reference trace and reviewer output are included for audit.")
        st.subheader("Human Review Checklist")
        if open_questions:
            for index, question in enumerate(open_questions, start=1):
                st.checkbox(question, key=f"open_q_{run_dir.name}_{index}")
        else:
            st.info("No open questions detected.")

        with st.expander("Reviewer Result", expanded=True):
            st.markdown(reviewer or "_No reviewer result found._")

        with st.expander("Reference Trace", expanded=False):
            if references:
                for index, item in enumerate(references, start=1):
                    checked = st.checkbox(
                        markdown_to_plain_excerpt(item, limit=160),
                        key=f"ref_{run_dir.name}_{index}",
                    )
                    if checked:
                        st.caption("Marked as reviewed in this session.")
            elif selected_files:
                st.markdown(selected_files)
            else:
                st.info("No reference trace found.")


def stable_key(prefix: str, run_dir: Path, suffix: str = "") -> str:
    raw = re.sub(r"[^A-Za-z0-9_]+", "_", str(run_dir))
    if len(raw) > 120:
        raw = raw[-120:]
    return f"{prefix}_{raw}_{suffix}".strip("_")


def render_repurpose_editor(run_dir: Path, repurpose: str, repurpose_file: Path | None) -> None:
    if not repurpose:
        st.info("No repurpose output found.")
        return

    source_name = repurpose_file.name if repurpose_file else "repurpose_output.md"
    requested = requested_channel_names(run_dir)
    blog_copy = extract_clean_channel_copy(repurpose, "blog")
    linkedin_copy = extract_clean_channel_copy(repurpose, "linkedin")
    quality_check = text_or_empty(run_dir / "repurpose_quality_check.md") or text_or_empty(
        run_dir / "91_repurpose_quality_check.md"
    )

    if quality_check:
        quality_failed = bool(re.search(r"(?im)^Pass / Fail:\s*FAIL\b", quality_check))
        if quality_failed:
            st.warning("Repurpose Quality Check: needs revision before publishing.")
        else:
            st.success("Repurpose Quality Check: automated checks passed. Human review is still required.")
        with st.expander("Repurpose Quality Check", expanded=quality_failed):
            st.markdown(quality_check)

    st.caption("Only Blog and LinkedIn publish-ready copy is editable here. These boxes are clean text for copy/paste, not markdown notes.")

    shown_any = False
    if "blog" in requested or blog_copy:
        shown_any = True
        blog_key = stable_key("blog_clean_editor", run_dir, source_name)
        if st.session_state.get(f"{blog_key}_source") != source_name:
            st.session_state[blog_key] = blog_copy
            st.session_state[f"{blog_key}_source"] = source_name
        st.subheader("Blog Clean Copy")
        edited_blog = st.text_area("Edit Blog copy", key=blog_key, height=520, label_visibility="collapsed")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button("Download edited Blog copy", edited_blog, file_name="edited_blog_copy.txt", mime="text/plain")
        with col2:
            if st.button("Save edited Blog copy to this run", key=stable_key("save_blog", run_dir, source_name)):
                output_path = run_dir / "edited_blog_copy.txt"
                output_path.write_text(edited_blog, encoding="utf-8")
                st.success(f"Saved: {output_path.name}")

    if "linkedin" in requested or linkedin_copy:
        shown_any = True
        linkedin_key = stable_key("linkedin_clean_editor", run_dir, source_name)
        if st.session_state.get(f"{linkedin_key}_source") != source_name:
            st.session_state[linkedin_key] = linkedin_copy
            st.session_state[f"{linkedin_key}_source"] = source_name
        st.subheader("LinkedIn Clean Copy")
        edited_linkedin = st.text_area("Edit LinkedIn copy", key=linkedin_key, height=420, label_visibility="collapsed")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button("Download edited LinkedIn copy", edited_linkedin, file_name="edited_linkedin_copy.txt", mime="text/plain")
        with col2:
            if st.button("Save edited LinkedIn copy to this run", key=stable_key("save_linkedin", run_dir, source_name)):
                output_path = run_dir / "edited_linkedin_copy.txt"
                output_path.write_text(edited_linkedin, encoding="utf-8")
                st.success(f"Saved: {output_path.name}")

    if not shown_any:
        st.warning("No Blog or LinkedIn clean copy section was detected in the repurpose output.")

    with st.expander("Full repurpose output (raw, read-only)", expanded=False):
        st.markdown(repurpose)


def source_excerpt(source: dict[str, Any], limit: int = 650) -> str:
    text = source.get("content") or source.get("raw_content") or ""
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text[:limit] + ("..." if len(text) > limit else "")


def render_pending_research_approval(
    bundle: dict[str, Any],
    session_dir: Path,
) -> tuple[bool, list[str]]:
    eligible = bundle.get("eligible_sources", [])
    excluded = bundle.get("excluded_sources", [])

    st.divider()
    st.subheader("Web Research Source Approval")
    st.caption(
        "Research is complete. Select the external sources the Master Content Drafter may use. "
        "On-us facts and claims will still come from the internal KB."
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Search calls", bundle.get("query_count", 0))
    col2.metric("Reported credits", bundle.get("credits_used_reported", 0))
    col3.metric("Eligible sources", len(eligible))
    col4.metric("Auto-excluded", len(excluded))

    alignment = bundle.get("input_alignment", {})
    if alignment:
        with st.expander("Research input alignment", expanded=True):
            st.markdown(f"**Content Objective:** {alignment.get('content_objective', '')}")
            st.markdown(f"**Supporting Notes:** {alignment.get('supporting_notes', '')}")
            st.caption(alignment.get("priority_rule", ""))
            anchors = alignment.get("anchors", [])
            if anchors:
                st.markdown(f"**Extracted search anchors:** {', '.join(anchors)}")

    with st.expander("Search queries", expanded=False):
        for index, query in enumerate(bundle.get("queries", []), start=1):
            st.markdown(f"**{index}. {query.get('purpose', '')}**")
            st.code(query.get("query", ""), language=None)

    selected_urls: list[str] = []
    if eligible:
        for index, source in enumerate(eligible, start=1):
            with st.container(border=True):
                st.markdown(f"**{index}. [{source.get('title', 'Untitled source')}]({source.get('url', '')})**")
                st.caption(
                    f"Published / updated: {source.get('published_date', '')} · "
                    f"Type: {source.get('source_type', 'search')} · "
                    f"Purpose: {source.get('query_purpose', '')}"
                )
                matched_anchors = source.get("matched_input_anchors", [])
                if matched_anchors:
                    st.caption(
                        f"Matched input terms: {', '.join(matched_anchors)} · "
                        f"Input relevance: {float(source.get('input_relevance_score') or 0):.0%}"
                    )
                st.write(source_excerpt(source))
                approve_key = stable_key("approve_source", session_dir, str(index))
                if st.checkbox("Approve this source for Master Content", key=approve_key):
                    selected_urls.append(source.get("url", ""))
    else:
        st.warning("No dated, eligible source remained after filtering. Adjust the topic or reference URLs and run research again.")

    if excluded:
        with st.expander(f"Auto-excluded sources ({len(excluded)})", expanded=False):
            for source in excluded:
                st.markdown(f"- [{source.get('title', 'Untitled')}]({source.get('url', '')})")
                st.caption(source.get("excluded_reason", "Excluded by source policy"))

    with st.expander("Candidate research brief", expanded=False):
        st.markdown(build_research_brief(bundle, approved_urls=None))

    clicked = st.button(
        "Continue to Content Generation",
        type="primary",
        key=stable_key("continue_research", session_dir),
    )
    return clicked, selected_urls


def render_saved_research(run_dir: Path) -> None:
    sources_path = run_dir / "web_research_sources.json"
    brief_path = run_dir / "web_research_brief.md"
    raw_path = run_dir / "web_research_raw_response.json"
    if not sources_path.exists():
        st.info("No web research was used in this run.")
        return

    try:
        payload = json.loads(sources_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}
    approved = set(payload.get("approved_urls", []))
    eligible = payload.get("eligible_sources", [])
    approved_sources = [source for source in eligible if source.get("url") in approved]
    excluded = payload.get("excluded_sources", [])

    col1, col2, col3 = st.columns(3)
    col1.metric("Approved sources", len(approved_sources))
    col2.metric("Search calls", payload.get("query_count", 0))
    col3.metric("Reported credits", payload.get("credits_used_reported", 0))

    for index, source in enumerate(approved_sources, start=1):
        with st.expander(f"{index}. {source.get('title', 'Untitled source')}", expanded=index == 1):
            st.markdown(f"[{source.get('url', '')}]({source.get('url', '')})")
            st.caption(f"Published / updated: {source.get('published_date', '')}")
            st.write(source_excerpt(source, limit=1200))

    if not approved_sources:
        st.warning("Research ran, but no external source was approved for this generation.")

    if excluded:
        with st.expander(f"Auto-excluded sources ({len(excluded)})", expanded=False):
            for source in excluded:
                st.markdown(f"- [{source.get('title', 'Untitled')}]({source.get('url', '')})")
                st.caption(source.get("excluded_reason", "Excluded by source policy"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "Download research brief",
            text_or_empty(brief_path),
            file_name="web_research_brief.md",
            mime="text/markdown",
        )
    with col2:
        st.download_button(
            "Download source log",
            text_or_empty(sources_path),
            file_name="web_research_sources.json",
            mime="application/json",
        )
    with col3:
        if raw_path.exists():
            st.download_button(
                "Download raw response",
                raw_path.read_bytes(),
                file_name="web_research_raw_response.json",
                mime="application/json",
            )


def apply_gap_to_content_form(gap: dict[str, Any]) -> None:
    brief = build_gap_brief(gap)
    audiences = brief.get("target_audience") or []
    if isinstance(audiences, str):
        audiences = [audiences] if audiences else []
    st.session_state["content_category_input"] = brief["content_category"]
    st.session_state["target_audience_input"] = [item for item in audiences if item in TA_OPTIONS]
    st.session_state["content_objective_input"] = brief["content_objective"]
    st.session_state["supporting_notes_input"] = brief["supporting_notes"]
    st.session_state["similar_reference_input"] = brief["similar_reference"]
    st.session_state["use_web_research_input"] = False
    st.session_state["mode"] = "Generate New Content"


def _prompt_tokens(value: str) -> set[str]:
    stop_words = {
        "about", "and", "are", "best", "can", "for", "from", "how", "the", "this",
        "what", "which", "with", "your", "their", "into", "help", "using",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) >= 3 and token not in stop_words
    }


def _related_google_ads_rows(prompt: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt_terms = _prompt_tokens(prompt)
    matches: list[tuple[float, dict[str, Any]]] = []
    for row in rows:
        term_tokens = _prompt_tokens(str(row.get("search_term", "")))
        overlap = len(prompt_terms & term_tokens)
        if not overlap:
            continue
        score = overlap / max(len(term_tokens), 1)
        if score >= 0.25:
            matches.append((score, row))
    matches.sort(
        key=lambda item: (
            -float(item[1].get("conversions", 0) or 0),
            -float(item[1].get("impressions", 0) or 0),
            -item[0],
        )
    )
    return [row for _, row in matches[:8]]


def _related_ga4_rows(prompt: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt_terms = _prompt_tokens(prompt)
    matches: list[tuple[int, dict[str, Any]]] = []
    for row in rows:
        path_tokens = _prompt_tokens(str(row.get("landing_page", "")).replace("-", " "))
        overlap = len(prompt_terms & path_tokens)
        if overlap:
            matches.append((overlap, row))
    matches.sort(key=lambda item: (-item[0], -float(item[1].get("sessions", 0) or 0)))
    return [row for _, row in matches[:5]]


def render_gap_finder_page(
    *,
    ga4_property_id: str,
    google_service_account_json: str,
    google_oauth_config: dict[str, str],
    google_ads_config: dict[str, str],
) -> None:
    st.header("GEO / SEO Gap Finder")
    st.caption(
        "Use GeoVector to identify low AI visibility prompts. Google Ads validates search and commercial demand; "
        "GA4 shows whether related landing pages already attract and engage visitors."
    )

    geo_tab, google_tab = st.tabs(
        ["GeoVector / Manual Gaps", "Google Ads & GA4"]
    )
    with geo_tab:
        upload = st.file_uploader(
            "Upload a GeoVector prompt-level export",
            type=["csv", "json"],
            help="Expected fields include a prompt or query plus mention rate/visibility. Column names are matched flexibly.",
            key="geovector_upload",
        )
        if st.button("Import and Rank GEO Gaps", disabled=upload is None, type="primary"):
            try:
                records = parse_uploaded_records(upload.name, upload.getvalue())
                gaps = normalize_geovector_records(records)
                if not gaps:
                    raise ValueError("No prompt column was detected in the uploaded file.")
                st.session_state["geo_gaps"] = gaps
                st.session_state["gap_snapshot_dir"] = str(save_gap_snapshot(ROOT, gaps))
                st.success(f"Imported {len(gaps)} prompt-level gaps.")
            except Exception as exc:
                st.error(f"GeoVector import failed: {exc}")

        with st.expander("Add one gap manually", expanded=False):
            with st.form("manual_gap_form"):
                manual_prompt = st.text_area("Buyer prompt / question")
                col1, col2 = st.columns(2)
                manual_rate = col1.number_input("On-us mention rate (%)", 0.0, 100.0, 0.0, 1.0)
                manual_engine = col2.text_input("Answer engine", value="Multiple / not specified")
                manual_competitors = st.text_input("Competitors mentioned")
                add_gap = st.form_submit_button("Add Gap")
            if add_gap and manual_prompt.strip():
                manual_records = [{
                    "prompt": manual_prompt.strip(),
                    "mention rate": manual_rate,
                    "engine": manual_engine,
                    "competitors": manual_competitors,
                }]
                new_gaps = normalize_geovector_records(manual_records)
                existing = list(st.session_state.get("geo_gaps", []))
                st.session_state["geo_gaps"] = existing + new_gaps
                st.rerun()

        gaps = st.session_state.get("geo_gaps", [])
        if not gaps:
            st.info("Upload a GeoVector export or add a prompt manually to build the gap dashboard.")
        else:
            enriched_gaps = []
            for gap in gaps:
                ads_matches = _related_google_ads_rows(
                    gap["prompt"], st.session_state.get("google_ads_rows", [])
                )
                ga_matches = _related_ga4_rows(
                    gap["prompt"], st.session_state.get("ga4_rows", [])
                )
                enriched_gaps.append(
                    enrich_gap_opportunity(
                        gap,
                        related_google_ads_rows=ads_matches,
                        related_ga4_rows=ga_matches,
                    )
                )
            enriched_gaps.sort(key=lambda item: (-item["opportunity_score"], item["prompt"].lower()))

            st.subheader("Prioritised Gaps")
            st.dataframe(
                [
                    {
                        "Gap": gap["gap_id"],
                        "Prompt": gap["prompt"],
                        "Mention rate": f"{gap['mention_rate']:.1f}%",
                        "Priority": gap["opportunity_score"],
                        "Recommended action": gap["recommended_action"],
                        "Audience": ", ".join(gap["target_audience"]) if isinstance(gap["target_audience"], list) else gap["target_audience"],
                        "Category": gap["content_category"],
                    }
                    for gap in enriched_gaps
                ],
                width="stretch",
                hide_index=True,
            )
            labels = [
                f"{gap['gap_id']} | Priority {gap['opportunity_score']:.1f} | {gap['prompt']}"
                for gap in enriched_gaps
            ]
            selected_label = st.selectbox("Select a gap to review", labels)
            selected_gap = enriched_gaps[labels.index(selected_label)]
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("On-us mention rate", f"{selected_gap['mention_rate']:.1f}%")
                col2.metric("Priority score", f"{selected_gap['opportunity_score']:.1f}")
                col3.metric("Search demand", f"{selected_gap['search_demand_score']:.1f}")
                col4.metric("Site coverage gap", f"{selected_gap['site_coverage_gap_score']:.1f}")
                st.markdown(f"**Prompt:** {selected_gap['prompt']}")
                st.markdown(f"**Recommended action:** {selected_gap['recommended_action']}")
                st.caption(f"Tracked engine: {selected_gap.get('engine', 'Not specified')}")
                audience_value = selected_gap.get("target_audience") or []
                if isinstance(audience_value, str):
                    audience_value = [audience_value] if audience_value else []
                st.markdown(f"**Suggested audience:** {', '.join(audience_value) or 'Broad / optional'}")
                st.markdown(f"**Suggested category:** {selected_gap['content_category']}")
                st.markdown(f"**Relevant products to verify:** {', '.join(selected_gap['relevant_products'])}")
                if selected_gap.get("competitors"):
                    st.markdown(f"**Competitors appearing:** {selected_gap['competitors']}")

                ads_matches = selected_gap["related_google_ads_rows"]
                ga_matches = selected_gap["related_ga4_rows"]
                if ads_matches:
                    with st.expander("Supporting Google Ads search terms", expanded=False):
                        st.dataframe(ads_matches, width="stretch", hide_index=True)
                else:
                    st.caption("No matching Google Ads search-term signal has been loaded yet.")
                if ga_matches:
                    with st.expander("Related GA4 landing pages", expanded=False):
                        st.dataframe(ga_matches, width="stretch", hide_index=True)
                else:
                    st.caption("No related GA4 landing-page signal has been detected yet.")

            st.button(
                "Use This Gap in Content Generator",
                type="primary",
                on_click=apply_gap_to_content_form,
                args=(selected_gap,),
            )
            st.caption("The generated content category, audience, objective and notes remain fully editable before generation.")

    with google_tab:
        st.subheader("Google Ads")
        ads_ready = all(
            google_ads_config.get(key)
            for key in ("customer_id", "developer_token", "client_id", "client_secret", "refresh_token")
        )
        if ads_ready:
            st.success("Google Ads API secrets are configured.")
            if st.button("Sync Google Ads Search Terms"):
                try:
                    rows = fetch_google_ads_search_terms(
                        customer_id=google_ads_config["customer_id"],
                        developer_token=google_ads_config["developer_token"],
                        login_customer_id=google_ads_config.get("login_customer_id", ""),
                        api_version=google_ads_config.get("api_version", "v21"),
                        oauth_config={
                            "client_id": google_ads_config["client_id"],
                            "client_secret": google_ads_config["client_secret"],
                            "refresh_token": google_ads_config["refresh_token"],
                        },
                    )
                    st.session_state["google_ads_rows"] = rows
                    st.success(f"Synced {len(rows)} Google Ads search terms from the last 90 days.")
                except Exception as exc:
                    st.error(f"Google Ads sync failed: {exc}")
        else:
            st.warning("Google Ads API is not configured. A Search Terms or Keyword Planner CSV works immediately.")
        ads_upload = st.file_uploader(
            "Upload Google Ads Search Terms or Keyword Planner CSV",
            type=["csv"],
            key="ads_upload",
        )
        if st.button("Import Google Ads CSV", disabled=ads_upload is None):
            try:
                raw_rows = parse_csv_records(ads_upload.getvalue())
                rows = normalize_google_ads_records(raw_rows)
                if not rows:
                    detected_columns = ", ".join(raw_rows[0].keys()) if raw_rows else "No columns detected"
                    raise ValueError(
                        "No Google Ads keyword rows were detected. Export a Google Ads Search Terms report "
                        "with a `Search term` column, or a Keyword Planner report with a `Keyword` column. "
                        f"Detected columns: {detected_columns}"
                    )
                st.session_state["google_ads_rows"] = rows
                st.success(f"Imported {len(rows)} Google Ads keyword/search-term rows.")
            except Exception as exc:
                st.error(f"Google Ads CSV import failed: {exc}")
        if st.session_state.get("google_ads_rows"):
            st.dataframe(st.session_state["google_ads_rows"][:100], width="stretch", hide_index=True)

        st.divider()
        st.subheader("Google Analytics 4")
        ga4_ready = bool(ga4_property_id and (google_service_account_json or all(google_oauth_config.values())))
        if ga4_ready:
            st.success("GA4 Data API secrets are configured.")
            if st.button("Sync GA4 Organic Landing Pages"):
                try:
                    rows = fetch_ga4_landing_pages(
                        property_id=ga4_property_id,
                        service_account_json=google_service_account_json,
                        oauth_config=google_oauth_config if all(google_oauth_config.values()) else None,
                    )
                    st.session_state["ga4_rows"] = rows
                    st.success(f"Synced {len(rows)} organic landing pages from GA4.")
                except Exception as exc:
                    st.error(f"GA4 sync failed: {exc}")
        else:
            st.warning("GA4 Data API is not configured. Uploading a Landing Page CSV works immediately.")
        ga4_upload = st.file_uploader("Upload GA4 Landing Page CSV", type=["csv"], key="ga4_upload")
        if st.button("Import GA4 CSV", disabled=ga4_upload is None):
            try:
                raw_rows = parse_csv_records(ga4_upload.getvalue())
                rows = normalize_ga4_records(raw_rows)
                if not rows:
                    detected_columns = ", ".join(raw_rows[0].keys()) if raw_rows else "No columns detected"
                    raise ValueError(
                        "No GA4 landing-page rows were detected. Export a GA4 report containing "
                        "`Landing page`, `Landing page + query string`, or `Page path`. "
                        f"Detected columns: {detected_columns}"
                    )
                st.session_state["ga4_rows"] = rows
                st.success(f"Imported {len(rows)} GA4 landing pages.")
            except Exception as exc:
                st.error(f"GA4 CSV import failed: {exc}")
        if st.session_state.get("ga4_rows"):
            st.dataframe(st.session_state["ga4_rows"][:100], width="stretch", hide_index=True)

    with google_tab:
        st.subheader("Concentrated Opportunities from Google Ads and GA4")
        st.caption(
            "Google Ads identifies concentrated search demand. GA4 shows whether a related organic landing page is missing, weak, or already healthy. "
            "You can use either source independently or combine both."
        )
        data_gaps = build_google_data_gap_candidates(
            st.session_state.get("google_ads_rows", []),
            st.session_state.get("ga4_rows", []),
        )
        if not data_gaps:
            st.info(
                "Import or sync Google Ads and/or GA4 data above. "
                "The app will then group related terms and pages into selectable content opportunities."
            )
        else:
            st.dataframe(
                [
                    {
                        "Opportunity": gap["prompt"],
                        "Source": gap["source"],
                        "Priority": gap["opportunity_score"],
                        "Search demand": gap["search_demand_score"],
                        "Site coverage gap": gap["site_coverage_gap_score"],
                        "Recommended action": gap["recommended_action"],
                        "Audience": ", ".join(gap.get("target_audience") or []) or "Broad / optional",
                    }
                    for gap in data_gaps
                ],
                width="stretch",
                hide_index=True,
            )
            labels = [
                f"{gap['gap_id']} | Priority {gap['opportunity_score']:.1f} | {gap['prompt']}"
                for gap in data_gaps
            ]
            selected_label = st.selectbox(
                "Select an Ads / GA4 opportunity to review",
                labels,
                key="selected_google_data_gap",
            )
            selected_gap = data_gaps[labels.index(selected_label)]
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Priority", f"{selected_gap['opportunity_score']:.1f}")
                col2.metric("Search demand", f"{selected_gap['search_demand_score']:.1f}")
                col3.metric("Site coverage gap", f"{selected_gap['site_coverage_gap_score']:.1f}")
                col4.metric("Source", selected_gap["source"])
                st.markdown(f"**Suggested content question:** {selected_gap['prompt']}")
                st.markdown(f"**Recommended action:** {selected_gap['recommended_action']}")
                st.markdown(
                    f"**Suggested audience:** {', '.join(selected_gap.get('target_audience') or []) or 'Broad / optional'}"
                )
                st.markdown(f"**Suggested category:** {selected_gap['content_category']}")
                st.markdown(f"**Relevant products to verify:** {', '.join(selected_gap['relevant_products'])}")
                if selected_gap.get("related_google_ads_rows"):
                    with st.expander("Supporting Google Ads terms", expanded=False):
                        st.dataframe(
                            selected_gap["related_google_ads_rows"],
                            width="stretch",
                            hide_index=True,
                        )
                if selected_gap.get("related_ga4_rows"):
                    with st.expander("Related GA4 landing pages", expanded=False):
                        st.dataframe(
                            selected_gap["related_ga4_rows"],
                            width="stretch",
                            hide_index=True,
                        )
            st.button(
                "Use This Opportunity in Content Generator",
                type="primary",
                key="use_google_data_gap",
                on_click=apply_gap_to_content_form,
                args=(selected_gap,),
            )
            st.caption(
                "The category, optional audiences, objective, and supporting notes remain editable before generation."
            )


def display_run(run_dir: Path) -> None:
    st.success(f"Run saved: {run_dir}")

    selected_files = text_or_empty(run_dir / "selected_kb_files.md")
    planning = text_or_empty(run_dir / "01_planning_agent_output.md")
    master_file = best_master_file(run_dir)
    master = text_or_empty(master_file) if master_file else ""
    reviewer_file = best_reviewer_file(run_dir)
    reviewer = text_or_empty(reviewer_file) if reviewer_file else ""
    repurpose_file = best_repurpose_file(run_dir)
    repurpose = text_or_empty(repurpose_file) if repurpose_file else ""
    visual = text_or_empty(run_dir / "03_visual_recommendation_output.md")
    state = text_or_empty(run_dir / "workflow_state.json")
    state_data = workflow_state(run_dir)
    log = text_or_empty(run_dir / "run_log.csv")

    tab_names = ["Master Review", "Master Raw", "Reviewer Result", "Repurpose", "Web Research"]
    if not state_data.get("fast_mode"):
        tab_names.extend(["Selected KB", "Planning", "Visual", "Run Log"])
    tab_names.append("Files")
    tabs = dict(zip(tab_names, st.tabs(tab_names)))

    with tabs["Master Review"]:
        if master:
            st.download_button(
                "Download master content revision",
                master,
                master_file.name if master_file else "master_content_revision.md",
                mime="text/markdown",
            )
            render_master_review(run_dir, master, reviewer, selected_files, master_file)
        else:
            st.warning("No master content revision found.")

    with tabs["Master Raw"]:
        st.download_button(
            "Download raw master markdown",
            master,
            master_file.name if master_file else "master_content.md",
            mime="text/markdown",
        )
        st.markdown(master or "_No master content file found._")

    with tabs["Reviewer Result"]:
        st.download_button("Download reviewer_result.md", reviewer, "reviewer_result.md", mime="text/markdown")
        st.markdown(reviewer or "_No reviewer result found._")

    with tabs["Repurpose"]:
        render_repurpose_editor(run_dir, repurpose, repurpose_file)

    with tabs["Web Research"]:
        render_saved_research(run_dir)

    if "Selected KB" in tabs:
        with tabs["Selected KB"]:
            st.markdown(selected_files or "_No selected KB file list found._")

        with tabs["Planning"]:
            st.markdown(planning or "_No planning output found._")

        with tabs["Visual"]:
            st.markdown(visual or "_No visual recommendation found._")

        with tabs["Run Log"]:
            if state:
                st.code(state, language="json")
            if log:
                st.code(log, language="csv")

    with tabs["Files"]:
        st.download_button(
            "Download full run ZIP",
            zip_run_dir(run_dir),
            file_name=f"{run_dir.name}.zip",
            mime="application/zip",
        )
        for path in list_md_files(run_dir):
            st.write(f"- `{path.name}`")


def render_recent_runs() -> None:
    runs_root = ROOT / "outputs" / "runs"
    run_dirs: list[Path] = []
    for path in sorted(runs_root.rglob("*"), reverse=True):
        if path.is_dir() and (path / "workflow_state.json").exists():
            run_dirs.append(path)
    if not run_dirs:
        st.info("No previous runs yet.")
        return

    labels = [str(path.relative_to(runs_root)) for path in run_dirs[:60]]
    selected = st.selectbox("Open previous run", labels)
    display_run(runs_root / selected)


st.set_page_config(page_title="On-us Master Content Generator", layout="wide")
st.title("On-us Master Content Generator")
st.caption("Internal MVP for Marketing: GEO/SEO gaps -> editable content brief -> optional research -> master content -> reviewer -> repurpose.")

SESSION_DEFAULTS = {
    "mode": "Find Content Gaps",
    "last_run_dir": "",
    "pending_research_bundle": {},
    "pending_research_session_dir": "",
    "pending_request": {},
    "pending_settings": {},
    "geo_gaps": [],
    "google_ads_rows": [],
    "ga4_rows": [],
    "gap_snapshot_dir": "",
    "content_category_input": CATEGORY_OPTIONS[1],
    "target_audience_input": [],
    "channels_input": ["Blog", "LinkedIn"],
    "languages_input": ["EN"],
    "use_web_research_input": False,
    "research_focus_input": [
        "Industry trends and market change",
        "External statistics and research reports",
    ],
}
for state_key, default_value in SESSION_DEFAULTS.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value
if isinstance(st.session_state.get("target_audience_input"), str):
    previous_audience = st.session_state["target_audience_input"].strip()
    st.session_state["target_audience_input"] = [previous_audience] if previous_audience in TA_OPTIONS else []

company_llm_key = secret_or_env("LLM_API_KEY", "ANTHROPIC_API_KEY")
company_llm_provider = secret_or_env("LLM_PROVIDER") or DEFAULT_PROVIDER
company_llm_api_url = secret_or_env("LLM_API_URL", "ANTHROPIC_API_URL") or DEFAULT_API_URL
company_llm_model = secret_or_env("LLM_MODEL", "ANTHROPIC_MODEL") or DEFAULT_MODEL
company_review_model = secret_or_env("LLM_REVIEW_MODEL")
company_tavily_key = secret_or_env("TAVILY_API_KEY")
ga4_property_id = secret_or_env("GA4_PROPERTY_ID")
google_service_account_json = secret_or_env("GOOGLE_SERVICE_ACCOUNT_JSON")
google_oauth_config = {
    "client_id": secret_or_env("GOOGLE_OAUTH_CLIENT_ID"),
    "client_secret": secret_or_env("GOOGLE_OAUTH_CLIENT_SECRET"),
    "refresh_token": secret_or_env("GOOGLE_OAUTH_REFRESH_TOKEN"),
}
google_ads_config = {
    **google_oauth_config,
    "developer_token": secret_or_env("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "customer_id": secret_or_env("GOOGLE_ADS_CUSTOMER_ID"),
    "login_customer_id": secret_or_env("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
    "api_version": secret_or_env("GOOGLE_ADS_API_VERSION") or "v23",
}

provider_presets = dict(PROVIDER_PRESETS)
if company_llm_key:
    provider_presets = {
        "Company default": {
            "provider": company_llm_provider,
            "api_url": company_llm_api_url,
            "model": company_llm_model,
        },
        **provider_presets,
    }

with st.sidebar:
    st.header("API Settings")
    if company_llm_key:
        st.success("Company LLM API loaded automatically")
    else:
        st.warning("Add LLM_API_KEY to Streamlit Secrets once to stop entering it for every run.")
    with st.expander("Provider and API settings", expanded=not bool(company_llm_key)):
        preset_name = st.selectbox("Provider Preset", list(provider_presets.keys()))
        preset = provider_presets[preset_name]
        provider = st.selectbox(
            "API Format",
            PROVIDER_OPTIONS,
            index=PROVIDER_OPTIONS.index(preset["provider"]),
            help="Use anthropic for Claude Messages endpoints. Use openai for NVIDIA/OpenAI-compatible chat completions.",
        )
        api_url = st.text_input("API URL", value=preset["api_url"], key=f"api_url_{preset_name}")
        api_key_override = st.text_input(
            "LLM API key",
            type="password",
            key="api_key_input",
            help="Leave blank to use the company default key. A temporary override is not saved.",
        )
        model = st.text_input("Drafter Model", value=preset["model"], key=f"model_{preset_name}")
        review_model = st.text_input(
            "Reviewer Model",
            value=company_review_model or preset["model"],
            key="review_model_input",
            help="Defaults to the same model as the Drafter Model.",
        )
    api_key = api_key_override.strip() or company_llm_key
    st.divider()
    st.header("Web Research")
    if company_tavily_key:
        st.success("Company Tavily key loaded automatically")
    else:
        st.warning("Add TAVILY_API_KEY to Streamlit Secrets once to stop entering it for every run.")
    tavily_key_override = st.text_input(
        "Tavily API key",
        type="password",
        key="tavily_api_key_override",
        help="Leave blank to use the company key. A value entered here is used for this session only and is not saved.",
    )
    tavily_api_key = tavily_key_override.strip() or company_tavily_key
    research_query_count = st.number_input(
        "Basic search calls per generation",
        min_value=1,
        max_value=2,
        value=2,
        step=1,
        key="research_query_count",
        help="Two basic Tavily searches normally use two credits.",
    )
    research_max_sources = st.number_input(
        "Maximum candidate sources",
        min_value=1,
        max_value=8,
        value=5,
        step=1,
        key="research_max_sources",
    )
    st.caption("Default scope: APAC / Hong Kong, English, last 12 months. Reddit, forums, personal-blog platforms, and undated pages are excluded.")
    st.divider()
    st.header("Generation Settings")
    fast_mode = st.checkbox(
        "Fast generation",
        value=True,
        key="fast_mode_input",
        help="Recommended: Master Drafter -> Reviewer/Finalizer -> Repurpose. Planning and Visual agents do not call the LLM.",
    )
    st.caption("Fast mode uses the minimum 3 LLM calls: master draft, independent review/finalization, and repurpose.")
    with st.expander("Advanced generation settings", expanded=False):
        planning_tokens = st.number_input("Planning tokens", min_value=500, max_value=8000, value=1800, step=100, key="planning_tokens_input")
        draft_tokens = st.number_input("Draft / repurpose tokens", min_value=1000, max_value=12000, value=3000, step=250, key="draft_tokens_input")
        review_tokens = st.number_input("Review tokens", min_value=500, max_value=8000, value=2000, step=100, key="review_tokens_input")
        max_revision_rounds = st.number_input("Auto revision rounds", min_value=0, max_value=3, value=1, step=1, key="max_revision_rounds_input")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05, key="temperature_input")
    human_approved = st.checkbox(
        "Human approved for official repurpose",
        value=False,
        key="human_approved_input",
        help="Leave off for testing-only repurpose drafts. Turn on only after human review approval.",
    )
    st.divider()
    st.write("Knowledge base")
    st.code(str(ROOT / "knowledge_base"))

page = st.radio(
    "Mode",
    ["Find Content Gaps", "Generate New Content", "View Previous Runs"],
    horizontal=True,
    key="mode",
)

if page == "Find Content Gaps":
    render_gap_finder_page(
        ga4_property_id=ga4_property_id,
        google_service_account_json=google_service_account_json,
        google_oauth_config=google_oauth_config,
        google_ads_config=google_ads_config,
    )
elif page == "View Previous Runs":
    render_recent_runs()
else:
    with st.form("content_request_form"):
        left, right = st.columns(2)
        with left:
            content_category = st.selectbox("Content Category", CATEGORY_OPTIONS, key="content_category_input")
            target_audience = st.multiselect(
                "Target Audience (optional, select more than one if needed)",
                TA_OPTIONS,
                key="target_audience_input",
                help="Leave blank for broad SEO content, company announcements, events, or promotional content. The model must not invent a vertical when this is blank.",
            )
            channels = st.multiselect("Repurpose Channels", CHANNEL_OPTIONS, key="channels_input")
            languages = st.multiselect("Languages", LANGUAGE_OPTIONS, key="languages_input")
        with right:
            similar_reference_url = st.text_input("Similar Reference URL (optional)", key="similar_reference_url_input")
            similar_reference = st.text_area("Similar Reference Notes (optional)", height=96, key="similar_reference_input")
            claims_to_include_raw = st.text_area("Claims To Include (optional, one per line)", height=96, key="claims_to_include_input")
            claims_to_avoid_raw = st.text_area("Claims To Avoid (optional, one per line)", height=96, key="claims_to_avoid_input")

        content_objective = st.text_area(
            "Content Objective",
            height=110,
            key="content_objective_input",
            placeholder="Example: Create a master content source draft explaining how Smart E-Voucher helps banks improve campaign engagement.",
        )
        supporting_notes = st.text_area(
            "Supporting Notes",
            height=140,
            key="supporting_notes_input",
            placeholder="Add product focus, audience context, campaign scenario, proof points to consider, and things to avoid.",
        )
        use_web_research = st.checkbox(
            "Run Web Research before generation",
            key="use_web_research_input",
            help="Optional. Leave off to generate directly from the internal KB and human inputs.",
        )
        research_focus = st.multiselect(
            "Web Research Focus",
            RESEARCH_FOCUS_OPTIONS,
            key="research_focus_input",
            disabled=not use_web_research,
        )
        research_urls_raw = st.text_area(
            "Additional Source URLs (optional, up to 5)",
            height=90,
            key="research_urls_input",
            placeholder="Enter one URL per line. The Similar Reference URL above is included automatically.",
            disabled=not use_web_research,
        )

        submitted = st.form_submit_button(
            "Run Web Research" if use_web_research else "Generate Content",
            type="primary",
        )

    if submitted:
        if use_web_research and not tavily_api_key:
            st.error("Please configure the company Tavily key in Streamlit Secrets or enter a temporary override key.")
            st.stop()
        if not api_key.strip():
            st.error("Please configure the company LLM API key in Streamlit Secrets or enter a temporary override key.")
            st.stop()
        if not content_objective.strip():
            st.error("Please enter a content objective.")
            st.stop()
        if not channels:
            st.error("Please select at least one repurpose channel.")
            st.stop()
        if not languages:
            st.error("Please select at least one language.")
            st.stop()
        research_source_urls = parse_urls(similar_reference_url, research_urls_raw)
        form = {
            "content_category": content_category,
            "target_audience": target_audience,
            "content_objective": content_objective.strip(),
            "supporting_notes": supporting_notes.strip(),
            "claims_to_include": [x.strip() for x in claims_to_include_raw.splitlines() if x.strip()],
            "claims_to_avoid": [x.strip() for x in claims_to_avoid_raw.splitlines() if x.strip()],
            "similar_reference": similar_reference.strip(),
            "similar_reference_url": similar_reference_url.strip(),
            "research_focus": research_focus,
            "research_source_urls": research_source_urls,
            "channels": channels,
            "languages": languages,
        }
        request = build_request(form)

        settings = {
            "provider": provider,
            "api_url": api_url.strip(),
            "api_key": api_key.strip(),
            "model": model.strip() or DEFAULT_MODEL,
            "review_model": review_model.strip(),
            "planning_tokens": int(planning_tokens),
            "draft_tokens": int(draft_tokens),
            "review_tokens": int(review_tokens),
            "max_revision_rounds": int(max_revision_rounds),
            "temperature": float(temperature),
            "human_approved": bool(human_approved),
            "fast_mode": bool(fast_mode),
            "lean_artifacts": True,
        }

        if use_web_research:
            with st.spinner("Searching the web and filtering candidate sources..."):
                try:
                    research_bundle, research_session_dir = run_research_stage(
                        request,
                        tavily_api_key=tavily_api_key,
                        focus=research_focus,
                        query_count=int(research_query_count),
                        max_sources=int(research_max_sources),
                        provided_urls=research_source_urls,
                    )
                except Exception as exc:
                    st.error(f"Web research failed: {exc}")
                    st.stop()

            st.session_state.pending_research_bundle = research_bundle
            st.session_state.pending_research_session_dir = str(research_session_dir)
            st.session_state.pending_request = request
            st.session_state.pending_settings = settings
        else:
            with st.spinner("Generating master content, running reviewer, and creating repurpose output..."):
                try:
                    run_dir = run_generator(request, settings)
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                    st.stop()
            st.session_state.last_run_dir = str(run_dir)
            st.rerun()

    if st.session_state.pending_research_bundle and st.session_state.pending_research_session_dir:
        pending_bundle = st.session_state.pending_research_bundle
        pending_session_dir = Path(st.session_state.pending_research_session_dir)
        continue_clicked, approved_urls = render_pending_research_approval(pending_bundle, pending_session_dir)
        if continue_clicked:
            if not api_key.strip():
                st.error("Configure the company LLM API key in Streamlit Secrets or enter a temporary override before continuing.")
            else:
                approved_request = dict(st.session_state.pending_request)
                approved_request["web_research_bundle"] = pending_bundle
                approved_request["approved_web_research_urls"] = approved_urls
                generation_settings = dict(st.session_state.pending_settings)
                generation_settings.update(
                    {
                        "provider": provider,
                        "api_url": api_url.strip(),
                        "api_key": api_key.strip(),
                        "model": model.strip() or DEFAULT_MODEL,
                        "review_model": review_model.strip(),
                        "planning_tokens": int(planning_tokens),
                        "draft_tokens": int(draft_tokens),
                        "review_tokens": int(review_tokens),
                        "max_revision_rounds": int(max_revision_rounds),
                        "temperature": float(temperature),
                        "human_approved": bool(human_approved),
                        "fast_mode": bool(fast_mode),
                        "lean_artifacts": True,
                    }
                )
                save_research_artifacts(pending_session_dir, pending_bundle, approved_urls=set(approved_urls))
                with st.spinner("Generating master content, running reviewer, and creating repurpose output..."):
                    try:
                        run_dir = run_generator(approved_request, generation_settings)
                    except Exception as exc:
                        st.error(f"Generation failed: {exc}")
                        st.stop()
                st.session_state.last_run_dir = str(run_dir)
                st.session_state.pending_research_bundle = {}
                st.session_state.pending_research_session_dir = ""
                st.session_state.pending_request = {}
                st.session_state.pending_settings = {}
                st.rerun()

    if st.session_state.last_run_dir:
        latest_run_dir = Path(st.session_state.last_run_dir)
        if latest_run_dir.exists():
            st.divider()
            st.subheader("Latest Generation")
            display_run(latest_run_dir)
        else:
            st.session_state.last_run_dir = ""
