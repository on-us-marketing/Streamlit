# Master Content Drafting Guidelines

Last updated: July 2026  
Use stage: Master Content Drafter only  
Status: Working draft for review

## Purpose

This file guides the Master Content Drafter on how to turn the On-us knowledge base into a structured master content draft.

The knowledge base tells the AI what is true and what cannot be overclaimed. This file tells the AI how to use that knowledge for a specific content task.

Master Content is not the final blog, LinkedIn post, or press release. It is the source draft for downstream repurposing. It should be factual, structured, complete, and claim-safe.


## Output Cleanliness and Completeness Rules

The final master content must not include agent process notes, self-comments, revision notes, preambles, or working-log language.

Do not include phrases such as:

```text
I will revise
I'll revise
Let me
Here is
Key fixes needed
The reviewer said
I need to
```

Return only the clean master content draft.

The final output must include a final `Human Review Appendix` containing `Claim Boundaries`, `Open Questions`, and `Reference Trace`. If the draft is too long for the token limit, shorten repurposing notes or proof detail before cutting the appendix.

Do not wrap the final master content in a markdown code fence.


## Length Control Rule

Master Content should be factual and claim-safe, but it should still be human-readable. It should read like a strategic content brief or short article-style source draft that a marketing reviewer can understand before downstream repurposing.

Target length:

- Simple product explainer: 700-900 words
- Standard master content: 900-1,200 words
- Complex thought leadership or case-heavy brief: up to 1,400 words

Do not exceed the target length unless the human explicitly asks for a detailed long-form draft.

If space is limited, prioritize:

1. Product accuracy
2. Human-readable explanation of buyer context, On-us point of view, and solution story
3. Case / proof usage
4. Human Review Appendix with claim boundaries, open questions, and reference trace

Do not turn the main body into a technical routing packet. Use coherent paragraphs for the main body, and keep bullets mainly for workflows, proof lists, and the final appendix.

## Loading Rule

Use this file only after the basic KB routing has happened.

Basic sequence:

```text
Content request
-> Identify content category, target audience, objective, and writing angle
-> Load Tier 1 foundation files
-> Load relevant Tier 2 product files
-> If the task requires TA / vertical / enterprise objective routing, load enterprise_objectives_by_vertical.md
-> Load this Master Content Drafting Guidelines file
-> Draft master content
-> Run Content Reviewer / Claim Checker
-> Human review
-> Repurpose into Blog / LinkedIn / News / Newsletter / Webflow
```

Do not use this file as the source of product facts. Product facts should come from the KB files.

Related Master Content Drafter context:

```text
enterprise_objectives_by_vertical.md
```

Use `enterprise_objectives_by_vertical.md` when the task needs to decide the target audience, business objective, commercial use case, or buyer-specific writing angle.

## Required Task Inputs

The Master Content Drafter should ask for or infer the following fields before drafting:

```text
Content Category:
Target Audience / Vertical (optional; may contain multiple audiences):
Enterprise Objective:
Content Objective:
Writing Angle:
Business Pain Point:
Relevant Product / Solution:
Use Case / Scenario:
Supporting Notes:
Supporting Proof / Case Study:
Claims to Include:
Claims to Avoid:
Similar Reference:
Required Structure:
Future Repurpose Channels:
```

Target Audience is optional. If it is blank, keep the content broad and do not silently assign Banks, BFSI, insurers, or another vertical. If several audiences are supplied, write around their shared business need and add audience-specific differences only when useful.

For other missing fields, the Drafter can make a reasonable assumption, but it should mark the assumption under `Open Questions`.

## Role Split

The system should not rely on one agent to both draft and approve its own work.

Recommended split:

```text
Master Content Drafter
-> Content Reviewer / Claim Checker
-> Human Review
-> Repurpose Agents
```

### Master Content Drafter

Role:

- Create a complete, structured, factual source draft.
- Use the right KB files based on the target audience, objective, product, and use case.
- Keep the writing neutral and information-rich.
- Avoid channel-specific language too early.

It should focus on:

- Business context
- Audience-specific pain point
- On-us solution logic
- Relevant product mechanism
- Case / proof support
- Claim boundary
- Repurposing notes

### Content Reviewer / Claim Checker

Role:

- Challenge the draft.
- Check product accuracy, claim scope, proof point usage, partner governance, case study privacy, and KB reference accuracy.
- It should be a separate LLM call where possible.
- Ideally, it can use a stricter prompt or stronger model than the Drafter.

Reviewer output should include:

```text
Pass / Fail:
Key issues:
Required fixes:
Claim scope risks:
Partner / second-party risks:
Case study privacy risks:
Missing KB references:
Suggested human review questions:
```


### Review Gate

If the Content Reviewer / Claim Checker returns `Fail`, the workflow should stop before repurposing. Do not generate Blog, LinkedIn, Newsletter, Webflow, or localized outputs from a failed master content draft unless a human explicitly overrides the review gate.


## Topic-Specific Failure Prevention Notes

Use these notes when drafting or reviewing topics that matched testing failure patterns.

| Topic | Prevent this error | Safer handling |
|---|---|---|
| VOP / Card Issuer | Do not merge VOP qualification mechanics with Smart E-Voucher redemption mechanics. Do not imply Visa endorsement, exclusivity, raw Visa data access, or automatic merchant choice inside VOP. | Treat VOP as the card-linked / transaction-qualification context. Treat Smart E-Voucher as a configurable non-cashback fulfillment layer after qualification. Use `visa_governance.md` for the full never-use list. |
| Smart E-Voucher | Do not turn it into a generic coupon, cashback-only reward, CRM replacement, or every-feature-by-default product. Do not attach BOC Life or other case studies to a generic explainer unless the task asks for proof. | Explain core journey, merchant choice, redemption, status tracking, and campaign signals where configured. Use case studies only when the topic asks for vertical proof or named examples. |
| On-us Intelligence | Do not present future-facing AI, autonomous loyalty operations, respondent scoring, fraud scoring, or fully autonomous optimization as live unless approved. Do not use defensive phrases such as "not surveillance" as marketing claims. | Current capability should be framed as campaign analytics, behavioral signals, segmentation support, retargeting planning, and performance visibility. Future-facing AI should be explicitly labeled future-facing or open for confirmation. |
| Green & ESG Solution | Do not mix Smart E-Voucher carbon saving, Green Voucher carbon offset, ESG Voucher social impact, and Wellness Voucher wellbeing into one generic claim. | Separate Wellness, ESG Voucher, and Green Voucher angles. The 12.2g CO2 proof point belongs to Smart E-Voucher digital-format carbon saving only. |
| On-us Express vs Enterprise | Do not turn open questions into confirmed facts. Do not use "likely Enterprise-tier" as a claim in the body. | Use On-us Express only for HK self-serve / SME / lighter local campaign context. Use Enterprise for customized, cross-market, API, dedicated-support, or complex campaign context. Put uncertainty under Open Questions. |
| Property / Hysan POC | Do not present Hysan as a completed case. Do not use Swire event/community proof as mall loyalty proof. Do not expose CONFIRM internal metrics. | Hysan is proposal / POC context only. Swire is an approved event/community engagement reference only, not proof of mall loyalty performance unless approved. |
| Insurance Wellness Lead Conversion | Do not invent policy activation milestones. Do not reposition BOC Life as a lead conversion or policy activation case. Do not claim On-us has proven LTV uplift. | Use BOC Life only within its approved loyalty / wellness reward fulfillment scope. Treat LTV as an enterprise objective, not a proven result, unless an approved proof point supports it. |
| Research Survey Incentive | Do not misframe ShareParty as a generic MarTech example when the task is Research & Insights. Do not mix APPROVED and CONFIRM cases without labels. Do not claim respondent scoring or fraud scoring as live. | Use ShareParty as the approved cross-border API automation / research incentive case. Use Ipsos, NTU, and BCT as CONFIRM-only internal references unless re-approved. |

## Enterprise Objective and Target Audience Routing

When a target audience is supplied, the Master Content Drafter should start from the audience and business objective, not from product features. For broad SEO, company, promotional, event, or announcement content with no selected audience, start from the Content Objective and category instead of inventing a vertical.

Correct order:

```text
Target audience / vertical
-> enterprise objective
-> commercial application
-> relevant On-us product or solution
-> proof / case / claim boundary
```

For a broad request with no selected audience:

```text
Content objective / category
-> business or market context
-> relevant On-us product or solution
-> proof / case / claim boundary
```

## Vertical / TA Reference

| Vertical / TA | What this audience cares about | Common writing angles | Relevant On-us context |
|---|---|---|---|
| Banks & Financial Services | Customer lifetime value, acquisition, retention, digital banking engagement, cross-product relationship growth | From reward distribution to customer intelligence; using incentives to deepen financial relationships; loyalty beyond one-off rewards | Smart E-Voucher, On-us Intelligence, VAS, banking case studies |
| Card Schemes & Card Issuers | Card activation, top-of-wallet, spend uplift, cross-border spend, non-cashback reward differentiation | Cashback is not the only cardholder benefit; card-linked non-cashback benefits; overseas dining / travel spend activation; real-time transaction-based rewards | VOP, Smart E-Voucher, Visa governance, DBS VOP cross-border case |
| Insurance | Lead conversion, policy activation, renewal, retention, wellness engagement, customer lifetime value | Incentives for lead-to-policy conversion; wellness rewards for long-term engagement; using rewards to support renewal and retention | Smart E-Voucher, VAS, Green & ESG Solution, On-us Intelligence |
| Pensions & MPF | Scheme member engagement, survey participation, feedback collection, member retention, account activation | Incentivized survey participation; improving member response quality; reward-led member education and feedback | On-us Form, Smart E-Voucher, VAS, Research & Insights overlap |
| Retail & FMCG | Product trial, customer acquisition, seasonal promotion, loyalty, campaign effectiveness | From discounting to measurable engagement; product launch activation; multi-brand reward strategy | Smart E-Voucher, merchant choice, On-us Intelligence |
| Property & Real Estate / Malls | Footfall growth, dwell-time, tenant co-marketing, shopper loyalty, member conversion, paperless engagement | Convert mall traffic into active spending; direct traffic to target tenants; turn redemption into mall-level insight; app-less engagement for pass-by traffic | Smart E-Voucher, VAS, On-us Intelligence, Hysan POC as proposal context |
| Travel & Hospitality | Traveler acquisition, destination spend, cross-border growth, repeat visitation, travel loyalty | Winning travel spend before the transaction; destination-specific rewards; cross-border merchant rewards | Smart E-Voucher, VOP where card-linked, travel reward content |
| MICE & Events | Attendee acquisition, participation, sponsor value, post-event community, event operations | Event engagement from check-in to reward fulfillment; zero-waste event rewards; sponsor and exhibitor engagement | VAS, Lucky Draw, Voucher Pack, On-us Form, Smart E-Voucher |
| Research & Insights | Panel participation, verified response, reward fulfillment, response quality, multi-market fieldwork | Incentivized data collection; verified respondent rewards; API reward fulfillment for research platforms | On-us Form, Smart E-Voucher, VAS, pass code / fraud-resistant reward gating |
| Enterprise Procurement / HR | Employee engagement, wellbeing, recognition, corporate event rewards, employer brand | Automating staff rewards; employee benefits with merchant choice; annual dinner / lucky draw fulfillment | VAS, Lucky Draw, Voucher Pack, Smart E-Voucher, Wellness Voucher |
| Merchants & Merchant Ecosystem | Incremental footfall, marketer-funded demand, simple redemption, settlement, co-marketing exposure | Zero-integration merchant participation; turning reward campaigns into tenant traffic; merchant network value | Use as ecosystem participant / partner context, not always a marketer vertical |

## Merchant Row Recommendation

The merchant row is valuable, but it should not be treated exactly the same as marketer verticals.

Reason:

- Most content is written for marketer clients.
- Merchants are usually ecosystem participants and redemption partners.
- Merchant content has a different objective: merchant onboarding, tenant participation, redemption acceptance, settlement simplicity, and co-marketing exposure.

Recommended handling:

```text
Keep merchant as a separate "Merchant Ecosystem Context" section.
Load it only when the content is about merchant onboarding, tenant engagement, mall tenants, merchant network, redemption acceptance, or settlement.
```

Do not load merchant context for every marketer-facing content draft unless merchant participation is central to the story.

## Property & Real Estate / Mall Angle From Hysan POC

Use Hysan POC as vertical context, not as a confirmed case study.

Useful mall/property content angles:

- Convert traffic into active spending
- Engage pass-by traffic and non-members without app installation
- Use QR / NFC / URL-based distribution for on-site and digital acquisition
- Direct spending to selected tenants
- Track campaign channels from acquisition to redemption
- Use redemption data, tenant redemption statistics, and heatmap-style analysis for mall insight
- Support merchant onboarding with low IT effort
- Retarget shoppers after redemption with follow-up offers or CRM conversion
- Use On-us Form, Voucher Pack, Lucky Draw, and gamified data collection for loyalty conversion

Safe boundary:

```text
Do not present Hysan as a completed campaign or approved case study unless confirmed.
Use it as a POC / proposal reference for the Property & Real Estate vertical.
```

## Content Clusters

### 1. Thought Leadership / Industry Insight

Purpose:

Explain an industry shift and position On-us' point of view.

Master content structure:

```text
Cluster:
Target audience:
Enterprise objective:
Industry context / why now:
Core tension / problem:
Audience-specific pain point:
On-us point of view:
Relevant product context:
How the solution works at a high level:
Supporting proof point or external reference:
Business implication:
Safe claim boundary:
Suggested Blog angle:
Suggested LinkedIn angle:
Suggested News angle:
CTA options:
Open questions:
```

### 2. Product Education / Solution Explainer

Purpose:

Explain what a product is, what it solves, and how it works.

Master content structure:

```text
Cluster:
Product:
Target audience:
Plain definition:
What problem it solves:
Who uses it:
How it works:
Typical workflow:
Key features:
Business value:
Common use cases:
Proof points:
What it is not:
Claim boundaries:
FAQ-style answers:
Recommended CTA:
Open questions:
```

### 3. Sales Generating / Use Case Angle

Purpose:

Turn product capability into a business use case for a target audience.

Master content structure:

```text
Cluster:
Target audience:
Enterprise objective:
Use case:
Current pain point:
Why existing approach is not enough:
Relevant On-us product:
Campaign mechanism:
Expected business value:
Supporting proof point:
Suggested case study:
Claim scope:
Implementation considerations:
CTA:
Repurposing notes:
Open questions:
```

### 4. Case Study / Use Case Proof

Purpose:

Use a real or anonymized case to prove relevance.

Master content structure:

```text
Cluster:
Case name:
Usage mode: named / anonymized / internal only / backup
Vertical:
Region:
Scenario:
Client objective:
Challenge:
On-us solution:
Execution process:
Redemption / fulfillment mechanism:
Impact:
Approved metrics:
Confirm metrics:
Privacy notes:
Partner approval notes:
Safe sentence:
Avoid:
Repurposing notes:
Open questions:
```

### 5. Partnership / Ecosystem / Milestone Announcement

Purpose:

Announce a partner, platform integration, accelerator, delegation, or market milestone.

Master content structure:

```text
Cluster:
Announcement:
Date:
Partner / platform:
Approval status:
Why this matters:
On-us role:
Relevant product:
Target audience impact:
Strategic significance:
Proof / credibility point:
Partner wording risk:
Safe wording:
CTA:
Repurposing notes:
Open questions:
```

### 6. Event / Award / Recognition

Purpose:

Use events and recognition to show market validation and credibility.

Master content structure:

```text
Cluster:
Event / recognition:
Date / location:
Organizer:
Why On-us participated:
What On-us showcased:
Audience / stakeholders engaged:
Key takeaway:
Strategic relevance:
Product relevance:
Proof / credibility:
Safe claim boundary:
CTA:
Repurposing notes:
Open questions:
```

### 7. ESG / Green / Wellness Content

Purpose:

Explain sustainability-linked incentives and purpose-led rewards.

Master content structure:

```text
Cluster:
Sustainability angle: Green / ESG / Wellness
Target audience:
Enterprise objective:
Campaign scenario:
Relevant reward options:
Smart E-Voucher foundation:
Impact / contribution mechanism:
Proof point:
Carbon claim boundary:
Post-campaign reporting:
Use case examples:
Safe wording:
Avoid:
CTA:
Open questions:
```

### 8. Talent / Culture / Mentorship

Purpose:

Support employer branding and talent engagement.

Master content structure:

```text
Cluster:
Talent / culture topic:
Audience:
Human story:
Business relevance:
What On-us is building:
Skills / mindset emphasized:
Program / opportunity:
CTA:
Repurposing notes:
Open questions:
```

## Master Content Output Template

Use this human-readable standard output format for the Master Content Drafter:

```text
Working title:
Content cluster:
Target audience / vertical:
Enterprise objective:
Content objective:
Writing angle:
Relevant product(s):

1. Executive Narrative (2 short paragraphs, around 220-300 words total)
2. Audience Context and Business Tension
3. On-us Point of View
4. Solution Story and Product Mechanism
5. Proof / Case Support
6. Why This Matters For The Buyer
7. Repurpose Direction
8. Human Review Appendix
   - Claim Boundaries
   - Open Questions
   - Reference Trace
```

The main body should be paragraph-led and useful for a human marketing reviewer. Do not write the final Blog, LinkedIn post, newsletter, or press release yet. The final `Human Review Appendix` should carry governance details so the main body stays readable while the reviewer can still check claim safety.

## Reviewer Checklist

The Content Reviewer / Claim Checker should check:

- Did the Drafter identify the correct target audience and vertical?
- Did it use a clear enterprise objective?
- Did it select the correct Tier 2 product file?
- Did it use the right case study or proof point?
- Did it confuse company-level, product-level, campaign-level, and client-level claims?
- Did it overstate AI capability as live when it is future-facing?
- Did it misuse Visa, Mastercard, Google Wallet, Microsoft, or other partner references?
- Did it combine client name and sensitive metric when not approved?
- Did it treat Hysan POC as a completed case without approval?
- Did it use merchant context only when relevant?
- Did it create unsupported ROI or performance claims?
- Did it include open questions for missing approval?

## Why This Matters

The goal is not only to make content sound better. The goal is to make content more accurate, more business-led, and safer to repurpose.

The KB provides the factual foundation. This file provides the drafting logic.
