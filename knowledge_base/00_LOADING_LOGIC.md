# Loading Logic for On-us AI Knowledge Base

Last updated: July 2026
Owner: Erika Yu
Status: Draft for review

## Purpose

This knowledge base is designed for the On-us Master Content Generator and content repurposing workflow. It separates factual context from language and channel style, so the AI first creates an accurate and neutral master content brief before adapting it into specific channels and markets.

## Evidence and Reference Rule

The AI should only use facts, product descriptions, proof points, case examples, and terminology that are available in this knowledge base or in approved source materials referenced by the knowledge base.

Do not invent reasoning, product claims, client results, future-facing capability status, partner relationships, or campaign performance numbers.

If the required information is not found in the loaded files, the AI should write it as an open question for human review instead of filling the gap by assumption.

When a file points to another reference file, follow the reference path and read the specific file instead of loading every file in the knowledge base.

## Core Loading Rule

### Master Content Brief Stage

Always load:

- Tier 1: Factual Foundation
- Tier 2: Product Context

The master content brief should be factual, neutral, and structurally clear. It should not apply LinkedIn tone, blog tone, newsletter tone, or language-specific copywriting style too early.


Tier 3 loading boundary:

- During the Master Content Draft stage, do not load Tier 3A language rules or Tier 3B channel style files unless the task has already moved into repurposing.
- Master Content should stay factual, structured, and channel-neutral.
- If the user asks for Blog, LinkedIn, Newsletter, Webflow, ZH-HK, or ZH-TW output, first generate and review the Master Content. Load Tier 3 only after the Master Content has passed review or the human explicitly asks for repurposing.

Selective loading inside Tier 1:

- Load `awards_recognition.md` only when the topic needs award or recognition proof.
- Load `official_boilerplate.md` when the topic needs formal company description, press release copy, website profile, or investor / partner-facing company introduction.
- Use `case_studies.md` as a supporting example library, not as a requirement to mention a client name in every output.
- Load `claim_scope_hierarchy.md` whenever the output uses proof points, campaign numbers, client examples, partner claims, or performance claims.

Reference routing inside Tier 1:

The AI should not load all files by default. It should first identify the content intent, then load only the required reference files.

| Content intent / trigger | Start from | Then read | Do not read unless needed |
|---|---|---|---|
| Product naming, product term, wording check | `approved_terminology.md` | The product file listed in its Product Reference Routing table | Full product folder |
| Voucher journey, reward delivery, redemption, merchant choice, voucher status, behavior signals, reward issuance | `approved_terminology.md` | `smart_e_voucher.md`; `proof_points.md` only if using scale, merchant coverage, carbon saving, or performance numbers | Full product folder |
| General On-us company description | `company_overview.md` | `official_boilerplate.md` only if exact external wording is needed | Awards file |
| Formal company profile, press release, partner / investor intro | `official_boilerplate.md` | `company_overview.md` for factual background | Channel style files |
| Awards, credibility, competition, accelerator, recognition | `awards_recognition.md` | `company_overview.md` only for company context | Product files unless the award is product-specific |
| Performance number, scale number, proof point | `proof_points.md` | `claim_scope_hierarchy.md`; `case_studies.md` only if the number is case-specific | Awards file |
| Named client example, industry example, vertical proof | `case_studies.md` | `claim_scope_hierarchy.md`; relevant product file only if explaining the product behind the case | All case examples |
| Visa, VOP, card-linked, non-cashback benefits | `approved_terminology.md` | `second_party_approval_rules.md` + `visa_governance.md` + `vop.md` + `claim_scope_hierarchy.md` if using partner or campaign claims | Green / ESG file |
| Smart E-Voucher carbon saving, paperless voucher, 12.2g CO2, ISO 14067 | `proof_points.md` | `claim_scope_hierarchy.md` + `smart_e_voucher.md`; `green_esg_solution.md` only if ESG / Green / Wellness context is involved | Awards file |
| ESG, green, wellness, carbon, social impact | `approved_terminology.md` | `green_esg_solution.md` + `proof_points.md` + `claim_scope_hierarchy.md` if using impact numbers | VOP file |
| AI, behavioral signals, campaign analytics, segmentation | `approved_terminology.md` | `on_us_intelligence.md` + `proof_points.md` + `claim_scope_hierarchy.md` if using 20+ behavioral signals | Awards file unless credibility proof is needed |

Master Content Drafter context:

Do not load these files for simple product definition questions or factual QA. Load them only when the task is to plan or draft master content.

| Content drafting need | Read | Why |
|---|---|---|
| Decide target audience, vertical, enterprise objective, commercial application, or buyer-specific angle | `Master Content Drafter Context/enterprise_objectives_by_vertical.md` | Helps the AI write from the buyer's business objective instead of only product features |
| Decide content type, strategic pillar, drafting depth, and channel suitability | `Master Content Drafter Context/content_cluster_mapping.md` | Helps the AI classify whether the content is thought leadership, educational, proof, product, data insight, market trend, conversion, event, or talent / culture |
| Draft a complete master content source for later Blog / LinkedIn / News / EDM repurposing | `Master Content Drafter Context/master_content_drafting_guidelines.md` | Gives the master content structure, required inputs, reviewer checklist, and claim-safety workflow |

Reference trace requirement:

Every master content brief should include a short reference trace, so human reviewers can see why the AI used certain facts.

Example:

```text
Reference files used:
- approved_terminology.md: checked product naming
- on_us_intelligence.md: checked current analytics capability
- proof_points.md: checked 20+ behavioral signals
- claim_scope_hierarchy.md: checked whether the proof point is company, platform, product, campaign, or client level

Unsupported items / open questions:
- Exact ROI uplift for this campaign is not available in the loaded files.
```

### Repurposing Stage

Load selectively:

- Tier 3A: Language Rules, based on output language or market
- Tier 3B: Channel Style, based on output channel

Example:

```text
EN LinkedIn post =
Tier 1 + Tier 2 + do-not-use rules + EN American English rules + LinkedIn style + LinkedIn brand voice

ZH-HK blog =
Tier 1 + Tier 2 + ZH-HK language rules + Blog style

Webflow article =
Tier 1 + Tier 2 + selected language rules + Webflow style
```

## Why This Matters

If brand tone or channel style is applied too early, the master content may become persuasive but factually weak. The workflow should first build a reliable factual brief, then adapt it into market-specific and channel-specific content.

Repurpose governance inheritance:

- Repurpose files must read `Tier 1 - Factual Foundation/do-not-use_rules.md` again. Do not assume the Master Content review alone will prevent channel-level rewriting errors.
- `Tier 3/Tier 3B - Channel Style/brand_voice.md` is loaded only for LinkedIn repurposing. It controls voice and formatting, not facts.
- Historical channel examples are style references only. They cannot approve a claim, metric, partner reference, product capability, or case study.
- Anything marked `requires approval`, `confirm`, `pending`, `TBC`, `not approved`, `internal only`, `never use`, or `avoid` remains prohibited in public-facing clean copy until human approval changes its status.

## Master Content Brief Output Template

```text
Topic:
Target audience:
Market:
Business pain point:
Relevant On-us product:
Key factual points:
Supporting proof points:
Claim scope:
Case study reference, if useful:
Product status:
Approved terminology:
Second-party reference risk:
Do-not-use checks:
Suggested content angle:
Suggested CTA:
Open questions for human review:
```

## Repurposing Output Template

```text
Source master brief:
Output channel:
Output language:
Target audience:
Tone:
Localized terms:
Channel-specific structure:
Final draft:
Compliance / claim checks:
```
