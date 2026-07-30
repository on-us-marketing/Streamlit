from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PLANNING_CONTEXT_FILES = [
    "00_LOADING_LOGIC.md",
    "Master Content Drafter Context/enterprise_objectives_by_vertical.md",
    "Master Content Drafter Context/content_cluster_mapping.md",
    "Master Content Drafter Context/master_content_drafting_guidelines.md",
    "Tier 1 - Factual Foundation/approved_terminology.md",
]

FOUNDATION_FILES = [
    "00_LOADING_LOGIC.md",
    "Tier 1 - Factual Foundation/approved_terminology.md",
    "Tier 1 - Factual Foundation/company_overview.md",
    "Tier 1 - Factual Foundation/business_model.md",
    "Tier 1 - Factual Foundation/claim_scope_hierarchy.md",
    "Tier 1 - Factual Foundation/proof_points.md",
    "Tier 1 - Factual Foundation/do-not-use_rules.md",
    "Master Content Drafter Context/master_content_drafting_guidelines.md",
    "Master Content Drafter Context/enterprise_objectives_by_vertical.md",
    "Master Content Drafter Context/content_cluster_mapping.md",
]

REVIEWER_FILES = [
    "00_LOADING_LOGIC.md",
    "Tier 1 - Factual Foundation/approved_terminology.md",
    "Tier 1 - Factual Foundation/claim_scope_hierarchy.md",
    "Tier 1 - Factual Foundation/proof_points.md",
    "Tier 1 - Factual Foundation/do-not-use_rules.md",
    "Tier 1 - Factual Foundation/second_party_approval_rules.md",
    "Master Content Drafter Context/master_content_drafting_guidelines.md",
]

PRODUCT_TRIGGER_MAP = {
    "Tier 2 - Product Context/smart_e_voucher.md": [
        "smart e-voucher",
        "redemption",
        "reward delivery",
        "merchant choice",
        "merchant selection",
        "reward issuance",
        "voucher journey",
    ],
    "Tier 2 - Product Context/on_us_intelligence.md": [
        "on-us intelligence",
        "behavioral signals",
        "campaign analytics",
        "retargeting",
        "segmentation",
        "customer intelligence",
        "data insight",
    ],
    "Tier 2 - Product Context/vop.md": [
        "vop",
        "visa offer platform",
        "card-linked",
        "non-cashback",
        "transaction qualification",
        "spend-qualified",
        "mcc-based",
        "bin-based",
    ],
    "Tier 2 - Product Context/vas.md": [
        "vas",
        "on-us form",
        "voucher pack",
        "lucky draw",
        "survey",
        "lead capture",
        "registration",
    ],
    "Tier 2 - Product Context/on_us_express.md": [
        "on-us express",
        "sme",
        "self-serve",
        "hong kong local",
        "hk local",
    ],
    "Tier 2 - Product Context/green_esg_solution.md": [
        "green",
        "esg",
        "wellness",
        "carbon",
        "sustainability",
        "paperless",
        "donation",
    ],
}

SPECIAL_TRIGGER_MAP = {
    "Tier 1 - Factual Foundation/case_studies.md": [
        "case study",
        "proof",
        "client",
        "dbs",
        "boc life",
        "sun life",
        "swire",
        "l'oreal",
        "shareparty",
        "ipsos",
        "hysan",
    ],
    "Tier 1 - Factual Foundation/visa_governance.md": [
        "visa",
        "vop",
        "card-linked",
        "issuer",
        "cardholder",
    ],
    "Tier 1 - Factual Foundation/second_party_approval_rules.md": [
        "visa",
        "mastercard",
        "google wallet",
        "microsoft",
        "partner",
    ],
    "Tier 1 - Factual Foundation/awards_recognition.md": [
        "award",
        "recognition",
        "accelerator",
        "competition",
        "finalist",
    ],
    "Tier 1 - Factual Foundation/official_boilerplate.md": [
        "boilerplate",
        "company profile",
        "press release",
        "formal intro",
    ],
    "Tier 3/Tier 3B - Channel Style/blog.md": [
        "blog",
    ],
    "Tier 3/Tier 3B - Channel Style/linkedin.md": [
        "linkedin",
    ],
    "Tier 3/Tier 3B - Channel Style/newsletter.md": [
        "newsletter",
    ],
    "Tier 3/Tier 3B - Channel Style/webflow.md": [
        "webflow",
    ],
}


def unique(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out


def trigger_matches(haystack: str, trigger: str) -> bool:
    if len(trigger) <= 4 and trigger.replace("-", "").isalnum():
        pattern = rf"(?<![a-z0-9-]){re.escape(trigger)}(?![a-z0-9-])"
        return re.search(pattern, haystack) is not None
    return trigger in haystack


def select_relevant_files(request: dict[str, Any], planning_text: str = "") -> list[str]:
    routing_request = {
        key: value
        for key, value in request.items()
        if key
        not in {
            "web_research_bundle",
            "approved_web_research_urls",
            "research_source_urls",
            "human_input_policy",
        }
    }
    haystack = (json.dumps(routing_request, ensure_ascii=False) + "\n" + planning_text).lower()
    files = list(FOUNDATION_FILES)
    for rel, triggers in PRODUCT_TRIGGER_MAP.items():
        if any(trigger_matches(haystack, trigger) for trigger in triggers):
            files.append(rel)
    for rel, triggers in SPECIAL_TRIGGER_MAP.items():
        if any(trigger_matches(haystack, trigger) for trigger in triggers):
            files.append(rel)
    return unique(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_files(kb: Path, files: list[str]) -> str:
    blocks = []
    for rel in unique(files):
        path = kb / rel
        if path.exists():
            blocks.append(f"\n\n--- FILE: {rel} ---\n{read_text(path)}\n--- END FILE: {rel} ---")
        else:
            blocks.append(f"\n\n--- MISSING FILE: {rel} ---")
    return "\n".join(blocks)
