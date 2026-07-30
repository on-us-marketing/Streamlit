# Approved Terminology

Last updated: July 2026
Status: Draft for review
Use stage: Master Content Brief

## Core Rule

Approved terminology belongs in the brief stage, not only the repurposing stage. Product naming is a governance rule, not a style choice. If the master brief gets the product name wrong, every channel output will inherit the error.

## Product Names and Inline References

When the AI reads a term in this table, it should treat the reference pointer as the next file to read if the content requires more than basic naming.

| Term | Approved usage | Reference pointer | Read the reference when | Notes |
|---|---|---|---|---|
| On-us | Always use "On-us" | `company_overview.md` | The content needs company description or positioning | Do not use ON-US, On-Us, Onus, on-us |
| Smart E-Voucher | Branded product name | `smart_e_voucher.md` | The content explains voucher product, journey, redemption, merchant choice, or campaign signals | Use for On-us' core product |
| e-voucher | Category or SEO keyword only | `smart_e_voucher.md` | The content compares category wording with the On-us branded product | Use lowercase for category/search phrases, not as product replacement |
| On-us Intelligence | Product / intelligence layer name | `on_us_intelligence.md` | The content mentions behavioral signals, analytics, AI, segmentation, retargeting, or future-facing AI capability | Keep in English across locales unless otherwise confirmed |
| Value Added Solutions (VAS) | Product group | `vas.md` | The content mentions On-us Form, Voucher Pack, Lucky Draw, event flow, or campaign add-on tools | VAS supports Smart E-Voucher campaigns |
| On-us Form | Feature / product module | `vas.md` | The content mentions lead capture, survey, registration, or form-linked reward issuance | Do not describe it as a standalone CRM |
| Voucher Pack | Feature / product module | `vas.md` | The content mentions multi-voucher package or one-link reward distribution | Use as VAS feature |
| Lucky Draw | Feature / product module | `vas.md` | The content mentions event, gamified reward, prize allocation, or employee engagement | Use as VAS feature |
| VOP | Visa Offer Platform | `vop.md`; `second_party_approval_rules.md` | The content mentions Visa, card-linked offers, issuers, cardholders, or non-cashback benefits | Use only in Visa / card-linked context |
| On-us Express | HK-only self-serve e-voucher platform | `on_us_express.md` | The content mentions SMEs, HK local campaigns, self-serve voucher setup, or Express vs Enterprise | Do not use in non-HK content unless approved |
| Incentive Intelligence | Current approved strategic term and boilerplate positioning | `official_boilerplate.md`; `company_overview.md` | The content needs company positioning, press release wording, or formal profile | Use this current positioning instead of older strategic wording such as "Agentic Growth Engine" |
| Green & ESG Solution | Umbrella solution for sustainable incentives | `green_esg_solution.md` | The content mentions Green Voucher, ESG Voucher, Wellness Voucher, sustainability, carbon, ESG, or wellness | Use as umbrella term |
| Wellness Voucher | Wellness-related reward solution | `green_esg_solution.md` | The content mentions healthy living, fitness, lifestyle, wellness, insurance wellness, or employee wellbeing | One sales and marketing angle under Green & ESG Solution |
| ESG Voucher | Social-impact reward solution | `green_esg_solution.md` | The content mentions social enterprises, community growth, inclusion, donation, or ESG commitments | One sales and marketing angle under Green & ESG Solution |
| Green Voucher | Environmental reward solution | `green_esg_solution.md` | The content mentions carbon offset, carbon footprint reduction, green finance, green projects, Verra, or Gold Standard | One sales and marketing angle under Green & ESG Solution |

## Product Reference Routing

This file controls approved naming and terminology only. It should not be used as the full product explanation.

When the AI sees a product name below, it should follow the relevant reference file before generating detailed product claims.

| Term / trigger keywords | Primary reference | Secondary reference | Read when the prompt asks about | Output guardrail |
|---|---|---|---|---|
| Smart E-Voucher, voucher journey, redemption, merchant choice, reward selection | `Tier 2 - Product Context/smart_e_voucher.md` | `Tier 1 - Factual Foundation/proof_points.md` if using scale or performance numbers | Core voucher product, redemption journey, multi-merchant selection, branded issuance, campaign signals | Do not describe it as a simple coupon, cashback-only reward, consumer app, or generic gift card |
| On-us Intelligence, behavioral signals, analytics, segmentation, retargeting, AI campaign insight | `Tier 2 - Product Context/on_us_intelligence.md` | `Tier 1 - Factual Foundation/proof_points.md` for 20+ behavioral signals | Campaign analytics, behavioral data, performance insight, future optimization, future-facing AI capability | Check the status rules inside `on_us_intelligence.md` before writing any AI-agent claim |
| VAS, On-us Form, Voucher Pack, Lucky Draw, event flow, prize allocation | `Tier 2 - Product Context/vas.md` | `Tier 1 - Factual Foundation/case_studies.md` if using event or employee reward examples | Campaign add-on tools, lead capture, survey-linked rewards, lucky draw, event reward mechanics | Do not describe VAS as the core platform; it supports Smart E-Voucher campaigns |
| VOP, Visa Offer Platform, card-linked, issuer, cardholder, non-cashback benefits, credit card reward | `Tier 2 - Product Context/vop.md` | `Tier 1 - Factual Foundation/second_party_approval_rules.md`; `Tier 1 - Factual Foundation/case_studies.md` for banking examples | Visa-related card-linked offers, bank campaigns, credit card benefits, payment-linked incentives | Do not imply Visa endorsement, exclusivity, or Visa data usage unless approved |
| On-us Express, SME, self-serve, HK local campaign, Express vs Enterprise | `Tier 2 - Product Context/on_us_express.md` | `Tier 1 - Factual Foundation/company_overview.md` if explaining client segment | HK-focused self-serve voucher platform, SME campaign, lighter local campaign | Do not use On-us Express for non-HK or enterprise custom solution content unless approved |
| Green & ESG Solution, Green Voucher, ESG Voucher, Wellness Voucher, carbon, ESG, sustainability, wellness | `Tier 2 - Product Context/green_esg_solution.md` | `Tier 1 - Factual Foundation/proof_points.md` only if using approved impact/scale numbers | Sustainable incentive campaigns, carbon contribution, ESG merchant choice, wellness benefits, social impact | Do not merge donation, tree planting, carbon credit retirement, and ESG redemption into one generic claim |
| Awards, accelerator, recognition, competition, credibility proof | `Tier 1 - Factual Foundation/awards_recognition.md` | `Tier 1 - Factual Foundation/company_overview.md` if company background is needed | Company credibility, investor/partner intro, milestone announcement | Do not turn award participation into award won; do not use awards as product performance proof |
| Official company description, boilerplate, formal intro | `Tier 1 - Factual Foundation/official_boilerplate.md` | `Tier 1 - Factual Foundation/company_overview.md` for additional factual context | Website profile, press release, company introduction, formal partner-facing text | Use exact boilerplate wording where required; do not rewrite into a new positioning |

If the relevant reference file does not support a claim, do not create the claim from reasoning. Put it under open questions for human review.

Suggested reference trace format:

```text
Terminology checked:
- Term: On-us Intelligence
- Primary reference: on_us_intelligence.md
- Secondary reference: proof_points.md, only when using 20+ behavioral signals or other approved metrics
- Claim allowed: campaign analytics and 20+ behavioral signals
- Claim not supported: fully autonomous loyalty operations as a live product
```

## Incentive Ecosystem

Use **incentive ecosystem** only when referring to the On-us ecosystem, not as a generic replacement for "reward program".

On-us' incentive ecosystem connects three stakeholder groups:

1. Marketers: enterprise clients and campaign owners
2. Merchants: redemption partners in the Smart E-Voucher network
3. Consumers: end users who receive, select, and redeem rewards

Approved meaning:

```text
On-us' incentive ecosystem connects marketers, merchants, and consumers through Smart E-Voucher campaigns, redemption journeys, and campaign data.
```

Do not write:

```text
Every brand should build an incentive ecosystem.
```

Reason:

This makes the term sound generic. In On-us content, "incentive ecosystem" should refer to the On-us model where marketer demand, merchant participation, and consumer redemption are connected.

## Smart E-Voucher vs e-voucher

Use **Smart E-Voucher** when referring to the On-us branded product.

Examples:

```text
On-us Smart E-Voucher supports multi-merchant redemption.
Smart E-Vouchers help marketers track redemption behavior.
```

Use **e-voucher** only when referring to the general category, market, or SEO keyword.

Examples:

```text
e-voucher solution for banks
digital rewards and e-voucher platforms in Asia
```

Do not use "e-voucher" as a direct substitute for the branded product in product descriptions.

## Green & ESG Solution Terms

Use **Green & ESG Solution** as the umbrella term when referring to the full On-us sustainability rewards offering.

Use **Wellness Voucher** when the campaign is focused on fitness, lifestyle, health, and wellness product benefits.

Use **ESG Voucher** when the campaign is focused on social enterprises, community growth, inclusion, or broader ESG commitments.

Use **Green Voucher** when the campaign is specifically linked to carbon offset, carbon footprint reduction, green finance, eco-friendly projects, or environmental contribution.

Do not merge donation, tree planting, carbon credit retirement, and ESG merchant redemption into one generic claim. They are related but operationally different.

Use the 12.2g CO2 per Smart E-Voucher proof point only as a digital voucher carbon-saving comparison. It is not the same as Green Voucher carbon offset, VCU retirement, donation amount, tree planting, or campaign-specific impact certification.

## Audience Terms

| Term | Meaning |
|---|---|
| Marketer | Enterprise buyer or campaign owner using On-us |
| Client | B2B customer of On-us |
| Consumer | End user receiving, opening, selecting, and redeeming the voucher |
| Merchant | Redemption partner where Smart E-Vouchers can be used |
| Cardholder | Consumer in banking or card-linked offer context |
| Issuer | Bank or card issuer |
| BFSI | Banking, financial services, and insurance |
| FMCG | Fast-moving consumer goods |
| ROI | Return on investment. Spell out on first use in formal copy |
| LTV | Customer lifetime value |
| Omni-channel | Use "omni-channel distribution" when describing delivery across channels |
| Redemption | Preferred formal B2B term. Avoid "use" when describing voucher redemption |

## Avoided Substitutes

| Approved | Avoid |
|---|---|
| Smart E-Voucher | smart voucher, e-voucher system, generic digital voucher when describing the On-us product |
| On-us Intelligence | our analytics tool |
| Strategic partner | vendor / supplier |
| Incentive ecosystem | reward program, loyalty program, campaign, unless referring to the On-us three-party ecosystem |
| Customer engagement and retention | customer management |

## Terms to Use Carefully

| Term | Guidance |
|---|---|
| AI | Explain what it does. Avoid using as empty buzzword |
| Behavioral signals | Use instead of raw data sale framing |
| Retargeting | Use in marketing context, but avoid surveillance tone |
| Location-based offers | Prefer over "geo-fenced" in consumer-facing content |
| Insight-as-a-Service | Use only if approved for the specific content |
