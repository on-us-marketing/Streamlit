# Case Studies

Last updated: July 2026
Status: Draft for review
Use stage: Master Content Brief

## Purpose

This file helps the AI use On-us case studies as controlled supporting evidence inside a master content brief.

The AI should not treat this file as a random client-name list. It should first identify the relevant business vertical, scenario, region, product, and approval status. Then it can select a case as a supporting example.

## Source Reference

Primary source:

```text
On-us_Case_Study_Knowledge_Base_Erika_v1.pdf
```

This PDF organizes case studies by region:

- Part A: Hong Kong client campaigns
- Part B: Taiwan client campaigns
- Part C: Cross-border / multi-market client campaigns

Each case follows the same logic:

```text
Business vertical -> use case -> campaign year / period -> what happened -> how On-us executed -> impact -> approval status
```

## Approval Status Rules

Every case and metric must follow its approval status.

| Status | Meaning | How AI can use it |
|---|---|---|
| APPROVED | Published on On-us website, case study, or news page. Numbers are approved for publication. | Can be used externally with client name and approved metrics if the campaign year / period is stated. |
| CONFIRM | Sourced from internal decks, internal drafts, screenshots, or non-public materials. | Internal brief only. For external content, flag for confirmation with account owner / client before use. |
| MIXED | Some parts are approved, but some metrics or details are internal-only. | Split approved framing from confirm metrics. Do not blend them without review. |
| PENDING / TBC | Case is incomplete or partnership details are not finalized. | Do not generate client-facing content using this client yet. |
| EXCLUDED | Case should not be used as a separate reference. | Do not use. |

## Client Name and Metric Rule

The old simple rule "client names and metrics must not coexist" is too broad. Use this improved rule:

### Client name + metric is allowed only when both are approved

Allowed:

```text
BOC Life's Live Young Rewards Program reached 140,000+ users through targeted in-app campaigns since 2022.
```

Reason: BOC Life case and the metric are marked APPROVED.

### For CONFIRM / MIXED metrics, use safer modes

Use named-client mode:

```text
On-us supported DBS in a card-linked overseas spending reward campaign using Smart E-Voucher with VOP.
```

Use anonymized-metric mode:

```text
In a banking card-linked reward campaign, On-us supported 3,000+ enrollments within 2 weeks.
```

Avoid:

```text
DBS achieved 3,000+ enrollments within 2 weeks.
```

Reason: the DBS metric is CONFIRM, so the exact client + metric combination needs approval before external use.

## Privacy Usage Rule

Case studies may include client names, campaign mechanics, internal metrics, and operational details. The AI should use only the level of detail supported by the approval status.

For external content:

- Use client names only when the case status and usage rule allow it.
- Use internal or CONFIRM metrics only in anonymized form unless re-approved.
- Do not reveal masked client names, internal campaign IDs, unpublished operational details, employee-level details, customer-level data, or partner-sensitive mechanics.
- If the case is marked MIXED, separate approved public framing from internal metrics.
- If privacy or approval status is unclear, write the item as an open question for human review.


CONFIRM-only metrics placement rule:

- CONFIRM-only metrics are internal validation references.
- Do not place CONFIRM-only metrics in the public-facing master content body unless human approval is confirmed.
- If useful, place them under `Open Questions`, `Internal Notes`, or use anonymized-metric mode without the client name.
- Do not use CONFIRM metrics in repurposed Blog, LinkedIn, Newsletter, Webflow, or localized copy unless approval is updated.

Default privacy note for catalog-only / backup cases:

```text
Privacy usage note: Treat this as a scenario reference only. Do not use client name, internal metrics, or detailed execution mechanics externally unless the case has explicit approval.
```

## Special Handling Rules

| Case / group | Rule |
|---|---|
| DBS VOP | Use as both Hong Kong banking case and cross-border / overseas spending case. Metrics are CONFIRM unless re-approved. Visa-related wording also requires Visa governance. |
| Swire Properties | Always frame as an ongoing multi-year partnership from 2023 to 2026 / four consecutive editions. Do not frame as a one-off event. |
| Masked community volunteer case | Never output the original client name. Always mask it as "a Hong Kong community organization" or similar. |
| EK2A | Remove as a separate reference. It belongs to the same group as ShareParty, and ShareParty is the preferred approved case. |
| Chubb | Pending. Good potential digital insurance / digital banking-style reference, but do not use until information is confirmed. |
| Manulife | More information is pending from Sales. Hold detailed Manulife content until updated case materials are confirmed. |
| L'Oreal Taiwan | Partnership story is approved, but internal figures such as NTD 2.35M prize distribution and 816 fulfillments are CONFIRM. |
| Unhighlighted / older cases | Treat as backup examples. Use for scenario naming only unless details are requested and approval is checked. |

## Related Reference Pointers

Use these files when a case needs product, claim, or partner governance.

| Need | Read this file |
|---|---|
| Claim scope and whether a number is company, product, campaign, or client level | `claim_scope_hierarchy.md` |
| General proof point usage | `proof_points.md` |
| Smart E-Voucher journey, merchant choice, redemption tracking | `../Tier 2 - Product Context/smart_e_voucher.md` |
| On-us Form, Voucher Pack, Lucky Draw, event mechanics | `../Tier 2 - Product Context/vas.md` |
| Card-linked offers, Visa Offer Platform, non-cashback benefits | `../Tier 2 - Product Context/vop.md` |
| Visa-specific wording and approval boundaries | `visa_governance.md` |
| General partner / second-party naming rules | `second_party_approval_rules.md` |
| Green Voucher, ESG Voucher, Wellness Voucher | `../Tier 2 - Product Context/green_esg_solution.md` |
| Campaign insight, behavioral signals, retargeting | `../Tier 2 - Product Context/on_us_intelligence.md` |
| Approved product names and audience terms | `approved_terminology.md` |

## Case Retrieval Workflow

Use this workflow before placing any case study into a master content brief.

1. Identify the request:
   - Vertical: banking, insurance, FMCG / corporate HR, property / event, research, loyalty tech, Green / ESG / wellness
   - Scenario: loyalty program, lead acquisition, VOP, cross-border, digital banking, employee benefit, event, survey, API automation, Green / ESG / wellness
   - Region: Hong Kong, Taiwan, cross-border, multi-market
   - Product involved: Smart E-Voucher, VAS, VOP, On-us Intelligence, Green & ESG Solution

2. Select the best-fit case:
   - Prefer highlighted / priority cases when available.
   - Use unhighlighted or older cases as backup scenario examples only.
   - Do not use PENDING / TBC cases for client-facing content.

3. Choose the usage mode:

| Usage mode | When to use | Output style |
|---|---|---|
| Named case with approved metric | Client name and metric are both APPROVED | Use client name + approved number |
| Named case without metric | Case framing is useful but metrics are CONFIRM / MIXED | Use client name, product logic, and scenario only |
| Anonymized metric case | Metric is useful but client + metric pairing is not approved | Remove client name and describe vertical / scenario |
| Scenario-only backup | Case is old, unhighlighted, sparse, or only useful as reference | Use as internal logic, not as a public proof point |
| Hold / do not use | PENDING, TBC, excluded, masked, or sensitive case | Do not use unless human confirms |

4. Check privacy and partner risk:
   - If partner / platform is named, read `second_party_approval_rules.md`.
   - If Visa / VOP is involved, read `visa_governance.md` and `vop.md`.
   - If the case includes internal mechanics, customer-level details, or employee-level details, keep them out of external copy.

5. Add only the useful supporting detail:
   - The AI does not need to mention a case in every output.
   - When used, the case should support the content point in the middle of the brief, not become the whole content.
   - If the content can be stronger with a scenario example but not a client name, use anonymized scenario wording.

## Reusable Case Structure

Each detailed case should be interpreted with this structure:

```text
Case:
Vertical:
Region:
Scenario:
Product / solution involved:
Approval status:
Overview:
Execution process:
Redemption / fulfillment mechanism:
Impact:
Approved usage mode:
Privacy usage note:
Safe sentence:
Avoid:
Reference files to check:
```

If any field is missing from a case, do not fill it by reasoning. Mark it as an open question for human review.

## Vertical Routing Index

Use this table if the prompt is industry-specific.

| Vertical | Best-fit cases | Scenario logic |
|---|---|---|
| Banking / card issuers | DBS VOP, DBS Lucky Draw, Hang Seng, CITIC Bank, Dah Sing, CCBA, Taiwan Visa bank cases, KGI Bank, Bank SinoPac | Cardholder engagement, enrollment, card-linked rewards, digital banking app engagement, non-cashback benefits |
| Insurance | BOC Life, Sun Life, Manulife, HSBC Life Well+, Zurich, Blue, AIA, Chubb | Policyholder loyalty, lead acquisition, wellness engagement, in-app reward automation |
| FMCG / corporate HR | L'Oreal Taiwan | Employee engagement, reward allocation, staff event fulfillment |
| Property / event / community | Swire Properties, masked HK community organization, Quality HealthCare | Event commerce, voucher packs, merchant onboarding, community participation |
| Research / survey | Ipsos HK, NTU, Ipsos Taiwan, ShareParty | Respondent incentives, research participation, cross-market survey reward automation |
| Loyalty tech / platform partners | ShareParty, Cybersoft | API reward automation, points redemption, cross-border reward fulfillment |
| Green / ESG / wellness | Green & ESG Solution references; Swire only for approved event sustainability metrics; BOC Life only for approved wellness reward fulfillment; Manulife pending | Wellness rewards, sustainability-linked event rewards, purpose-led engagement |

## Scenario Routing Index

Use this table if the prompt is use-case-specific.

| Scenario | Best-fit cases | Product references |
|---|---|---|
| Loyalty programs | BOC Life, Sun Life, Manulife, KGI Bank, Shin Kong Life | Smart E-Voucher, On-us Intelligence |
| Lead acquisition | Sun Life, Manulife, AIA | VAS, Smart E-Voucher |
| Cardholder rewards / VOP | DBS VOP, Visa x Mega Bank, Visa x COMMEET, Visa x FEIB, Visa Taiwan Roadshow | VOP, Visa Governance, Smart E-Voucher |
| Cross-border / overseas spending | DBS VOP, ShareParty, Visa x FEIB | VOP, Smart E-Voucher, Second-party rules |
| Digital banking / app engagement | CITIC Bank, KGI Bank, Blue, Chubb pending | Smart E-Voucher, On-us Intelligence |
| Employee benefit / staff engagement | L'Oreal Taiwan, Zurich employee campaigns | VAS, Smart E-Voucher |
| Event engagement / MICE | Swire Properties, Hang Seng Petshow, Quality HealthCare, Visa Taiwan Roadshow | VAS, Smart E-Voucher |
| Survey / research incentives | Ipsos HK, Ipsos Taiwan, NTU, ShareParty | VAS, Smart E-Voucher |
| API reward automation | ShareParty, Blue, Cybersoft | Smart E-Voucher, API context |
| Green / ESG / wellness | Green & ESG Solution references; BOC Life only for approved wellness reward fulfillment; Manulife only after confirmation | Green & ESG Solution, Smart E-Voucher |

## Case Catalog

This catalog helps the AI find the correct case. Detailed reusable cases are written below the catalog.

| Code | Case | Region | Vertical | Scenario | Status | Use rule |
|---|---|---|---|---|---|---|
| A1 / C2 | DBS - Visa x DBS Eminent Card Overseas Spending Campaign (VOP) | HK / Cross-border | Banking / card scheme | Card-linked overseas dining reward | MIXED | Use as DBS named case without metrics, or anonymized metric case. Also route under cross-border. |
| A2 | DBS - Appointment Lucky Draw Program | HK | Banking | Gamified RM touchpoints | CONFIRM | Internal / backup example. |
| A3 | Hang Seng - Petshow | HK | Banking / MICE | Event voucher and card acquisition | CONFIRM | Backup example. |
| A4 | Hang Seng x Mastercard | HK | Banking / card scheme | Dynamic incentive values | CONFIRM | Partner approval needed. |
| A5 | CITIC Bank (CNCBI) | HK | Banking | Digital banking app engagement | CONFIRM | Backup digital banking example. |
| A6 | Dah Sing Bank | HK | Banking | Festive dining incentive | CONFIRM | Backup banking campaign example. |
| A7 | CCBA | HK | Banking | WhatsApp promotion | CONFIRM | Backup messaging-channel example. |
| A8 | BOC Life - Live Young Rewards Program | HK | Insurance | Loyalty and wellness reward fulfillment | APPROVED | Strong approved insurance case; client + approved metrics can be used. |
| A9 | Sun Life | HK | Insurance | CRM rewards and lead acquisition | MIXED | Internal metrics need confirmation; can use anonymized lead acquisition logic. |
| A10 | Manulife - MOVE | HK | Insurance | Wellness loyalty and acquisition | CONFIRM / TBC | Hold until updated materials are shared. |
| A11 | HSBC Life Well+ | HK | Insurance | Anniversary lucky draw | CONFIRM | Backup insurance engagement example. |
| A12 | Zurich | HK | Insurance | Employee and new customer incentives | CONFIRM | Backup insurance / employee incentive example. |
| A13 | Blue | HK | Digital insurance | In-app API reward automation | CONFIRM | Backup API / app example. |
| A14 | AIA | HK | Insurance | Activation and verification | CONFIRM | Sparse detail; do not expand. |
| A15 | Chubb | HK | Digital insurance | TBC | PENDING / TBC | Do not use yet. |
| A16 | BCT | HK | Pensions / MPF | Survey incentive via Event Form | CONFIRM | Backup survey example. |
| A17 | Swire Properties - White Christmas Street Fair | HK | Property / community event | Event commerce, ESG, merchant onboarding | MIXED | Approved website metrics can be used; internal aggregates need confirmation. Always multi-year. |
| A18 | Masked HK community organization | HK | Community / non-profit | Volunteer recognition | CONFIRM | Never name the client. Mask only. |
| A19 | Quality HealthCare | HK | Healthcare | Lucky Draw / Voucher Pack fulfillment | CONFIRM | Backup healthcare event fulfillment example. |
| A20 | Ipsos HK | HK | Research | Offline survey Event Form | CONFIRM | Backup research incentive example. |
| B1 | Visa x Mega Bank | Taiwan | Card scheme / corporate card | Corporate card reward redemption | CONFIRM | Visa approval needed. |
| B2 | Visa x COMMEET | Taiwan | Card scheme / corporate card | Year-end corporate card rewards | CONFIRM | Visa approval needed. |
| B3 | Visa x FEIB Bankee Boss | Taiwan | Card scheme / B2B trade | Cross-border trade offers (GTPP) | CONFIRM | Visa approval needed; cross-border trade angle. |
| B4 | Visa Taiwan Roadshow | Taiwan | Card scheme / SME | On-site Event Form acquisition | CONFIRM | Visa approval needed. |
| B5 | KGI Bank | Taiwan | Banking | App engagement and dormant revival | CONFIRM | Backup banking app example. |
| B6 | Bank SinoPac | Taiwan | Banking | VIP client appreciation | CONFIRM | Backup VIP banking example. |
| B7 | Shin Kong Life | Taiwan | Insurance | Policyholder and sales incentives | CONFIRM | Backup Taiwan insurance example. |
| B8 | L'Oreal Taiwan | Taiwan | FMCG / beauty | Staff engagement / Lucky Draw | MIXED | Partnership story approved; figures need confirmation. |
| B9 | Speak | Taiwan | EdTech | Habit streak reward | CONFIRM | Backup habit challenge example. |
| B10 | Cybersoft | Taiwan | Loyalty tech | API points redemption | CONFIRM | Backup API points example. |
| B11 | EK2A | Taiwan | Loyalty tech | API points redemption | EXCLUDED | Remove. Use ShareParty instead. |
| B12 | NTU | Taiwan | Academic research | Survey Pass Code incentive | CONFIRM | Backup academic research example. |
| B13 | Ipsos Taiwan | Taiwan | Research | Survey respondent incentive | CONFIRM | Backup survey incentive example. |
| C1 | ShareParty Insight | Multi-market | MarTech / research / rewards | Cross-border API reward automation | APPROVED | Strong approved cross-border case; preferred over EK2A. |

## Part C: Cross-Border / Multi-Market Client Campaigns

Use this section when the content request is about cross-border rewards, overseas spending, multi-market campaign execution, regional reward operations, or cross-market API automation.

This section should not only include clients based outside Hong Kong. A Hong Kong-origin client case can also be indexed here if the campaign mechanic is cross-border.

| Code | Case | Cross-border logic | Status | AI usage |
|---|---|---|---|---|
| C1 | ShareParty Insight - Cross-Border Reward Automation | Multi-market reward operations across Taiwan, Indonesia, Philippines, Singapore, Thailand, and Malaysia | APPROVED | Preferred approved case for API-based cross-border reward automation. |
| C2 | DBS - Visa x DBS Eminent Card Overseas Spending Campaign (VOP) | Overseas dining spend, non-HKD transaction verification, and cross-border cardholder reward activation | MIXED | Use as cross-border card-linked overseas spending case. Use DBS name without CONFIRM metrics unless re-approved. |

### Section C Handling Notes

- C1 is the cleaner approved cross-border API automation case.
- C2 is the stronger banking / card-linked cross-border spending case.
- C2 refers to the same campaign as A1, but it is indexed here because the campaign mechanic is cross-border.
- Do not duplicate C2 facts differently across A1 and C2. A1 is the Hong Kong banking view; C2 is the cross-border use case view.
- For C2, read `visa_governance.md` and `../Tier 2 - Product Context/vop.md` before generating content.

## C2. DBS - Visa x DBS Eminent Card Overseas Spending Campaign (VOP)

Region: Hong Kong / Cross-border

Business Vertical: BFSI - Banking / Card Scheme partnership

Use Case: Card-linked offers using Visa Offer Platform; overseas and cross-border spending activation; non-cashback cardholder benefits

Year of Campaign: December 2024 launch, running into 2025 Q1

Products Used: Smart E-Voucher with Visa Offer Platform (VOP)

Approval Status: MIXED - campaign existence and framing are APPROVED through published On-us materials; campaign metrics from internal deck are CONFIRM

Source: DBS_VOP_CaseStudy; master deck for 2025 Q1 campaign mechanics; On-us patent announcement news page dated 2025-04-03

### What

Visa and DBS adopted On-us' Smart E-Voucher solution for the DBS Eminent Card overseas dining spending campaign, rewarding cardholders with instant dining e-vouchers based on real-time verification of cross-border transactions.

Cardholders registered once via an On-us online form on the official DBS website, spent overseas as normal, and received rewards automatically, with no receipt upload or manual claim.

### How

- Step 1 - Cardholder VOP registration: one-time enrollment via the On-us online form on the DBS website.
- Step 2 - Real-time transaction verification and reward qualification via VOP: BIN code, MCC code for dining, transaction currency as non-HKD, transaction amount as single net spend HK$800+, and reward acquisition limits checked against pre-set criteria.
- Step 3 - Automatic verification reduces manual checking, lowers operating cost, and allows incentive criteria to be flexibly configured according to promotion targets.
- Step 4 - Instant reward fulfillment: HK$50 dining e-voucher delivered immediately upon qualification, redeemable via dynamic QR code that refreshes every 120 seconds.

### Impact

| Metric | Detail / Context | Approval Status |
|---|---|---|
| 3,000+ enrollments | Cardholder VOP enrollments within 2 weeks of launch | CONFIRM |
| US$110K | Overseas dining spending driven by the campaign | CONFIRM |
| Real-time qualification | Automated multi-criteria verification per transaction | APPROVED mechanism / framing |

### Positioning Note

This is a flagship proof point for On-us' patented card-linked incentive infrastructure and last-mile behavioral signal capture.

This case should be indexed under both:

- Banking / cardholder reward cases
- Cross-border / overseas spending cases

For external content, use DBS as a named case without CONFIRM metrics unless the metric has been re-approved. If using enrollment or spending figures, flag for confirmation with the DBS / Visa account owner.

### Related References

When using this case, also read:

```text
visa_governance.md
../Tier 2 - Product Context/vop.md
claim_scope_hierarchy.md
second_party_approval_rules.md
```

Privacy usage note: For external content, do not combine the DBS name with CONFIRM enrollment or spending metrics unless re-approved. Use DBS as a named case without metrics, or use anonymized metric wording.

## Detailed Reusable Case: BOC Life Live Young Rewards Program

### Basic Information

| Field | Detail |
|---|---|
| Code | A8 |
| Region | Hong Kong |
| Vertical | BFSI - Insurance |
| Scenario | Loyalty program reward fulfillment, wellness engagement, merchant enablement |
| Year / period | Since 2022, ongoing partnership |
| Product | Smart E-Voucher, digitalized product vouchers, merchant enablement templates |
| Approval status | APPROVED |

### Overview

BOC Life runs the Live Young Rewards Program, a digital ecosystem integrating lifestyle, wellness, and reward incentives for its insured community. Since 2022, On-us has powered the reward layer across the Live Young Rewards App and related wellness initiatives.

### Execution Process

1. On-us supports diversified reward categories, including F&B, groceries, wellness, and designated health services.
2. Voucher procurement and distribution are consolidated on the On-us platform.
3. On-us provides merchant enablement templates for merchant partners that do not have their own e-redemption systems.
4. Agent-to-customer incentive distribution can use pre-generated passwords to track and verify agent identity.

### Impact

| Metric | Detail | Approval status |
|---|---|---|
| 140,000+ users | Reached through targeted in-app campaigns | APPROVED |
| 250,000+ incentives | Delivered via the On-us platform | APPROVED |
| 85%+ use rate | Use rate of incentives delivered | APPROVED |

### Safe Reference Sentence

```text
In BOC Life's Live Young Rewards Program, On-us helped deliver 250,000+ incentives and reach 140,000+ users through targeted in-app campaigns since 2022.
```

Privacy usage note: This case has approved public metrics, but do not add policyholder-level data, agent-level data, internal app data, or unapproved performance claims beyond the approved metrics listed above.


Positioning boundary: Use BOC Life as an approved insurance loyalty and wellness reward fulfillment case. Do not reposition it as proof of lead conversion, policy activation, renewal improvement, Green Voucher impact, ESG Voucher impact, or LTV uplift unless a separate approved source confirms that exact use.

## Detailed Reusable Case: Swire Properties White Christmas Street Fair

### Basic Information

| Field | Detail |
|---|---|
| Code | A17 |
| Region | Hong Kong |
| Vertical | Property / real estate / community event |
| Scenario | MICE and event commerce, merchant onboarding, paperless voucher redemption, ESG event enablement |
| Year / period | Ongoing partnership since 2023; four consecutive editions through 2026 |
| Product | Smart E-Voucher, VAS Event Forms, Voucher Packs, merchant WebApp, live event dashboard |
| Approval status | MIXED |

### Overview

Swire Properties replaced paper vouchers with On-us Smart E-Vouchers across its White Christmas Street Fair, turning the event into a digital, lower-waste F&B and community engagement experience.

### Execution Process

1. Walk-in visitors purchased voucher packs through On-us Event Forms and received vouchers instantly by SMS.
2. Pre-registered VIP guests and staff received voucher packs with official email invitations.
3. Voucher Packs combined multiple F&B vouchers into a single URL.
4. Temporary merchants were onboarded through the On-us merchant WebApp without POS integration.
5. Live performance dashboards supported redemption tracking, transaction reporting, merchant settlement, and future event planning.

### Approved Impact

| Metric | Detail | Approval status |
|---|---|---|
| 82,000+ visitors | 5-day event period, 2024 edition, plus 3,000+ VIPs | APPROVED |
| 58,000+ vouchers | Issued across 2023 and 2024 editions | APPROVED |
| 0.27 tonnes CO2 | Cut per year by replacing paper vouchers, equivalent to 12 trees per year | APPROVED |
| 80%+ merchants | Shared positive feedback on the On-us solution | APPROVED |
| 2-week settlement | Usage summary and post-event settlement completed within 2 weeks | APPROVED |

### Internal Metrics Requiring Confirmation

| Metric | Detail | Approval status |
|---|---|---|
| 90,000+ vouchers | Cumulative 2023-2025 | CONFIRM |
| HKD 4.5M | Cumulative transaction amount, 2023-2025 | CONFIRM |
| -1,200 kg CO2e | Estimated emissions avoided from replaced paper vouchers, 2023-2025 | CONFIRM |
| 29 merchants | Onboarded cumulatively, 2023-2025 | CONFIRM |
| 78% redemption rate | 2024 edition | CONFIRM |

### Framing Rule

Always frame Swire Properties as a long-term ongoing partnership, not a single event. If using year-specific results, state the year or period clearly.

Privacy usage note: Use only approved public event metrics externally. Keep internal cumulative figures, merchant-level details, settlement details, and CONFIRM CO2e estimates for internal drafts unless re-approved.


Property / mall boundary: Use Swire Properties as an event / community engagement and paperless voucher case. Do not use it as proof of mall loyalty, tenant sales uplift, shopper loyalty, or property-wide member conversion unless a separate approved source confirms that exact claim.

## Detailed Reusable Case: ShareParty Insight Cross-Border Reward Automation

### Basic Information

| Field | Detail |
|---|---|
| Code | C1 |
| Region | Cross-border / multi-market: Taiwan, Indonesia, Philippines, Singapore, Thailand, Malaysia |
| Vertical | MarTech - research and rewards platform |
| Scenario | Cross-border reward fulfillment, API automation, panel incentive operations |
| Year / period | Ongoing partnership; 16 campaigns to date |
| Product | Smart E-Voucher, API-based issuance, real-time tracking, customizable voucher presentation |
| Approval status | APPROVED |

### Overview

ShareParty Insight, a research and rewards platform, partnered with On-us to automate and scale cross-border reward operations across six Asian markets.

### Execution Process

1. Smart E-Vouchers are issued automatically through API within ShareParty's existing workflows.
2. The process reduces manual validation, issuance, balance replenishment, and reconciliation.
3. Real-time tracking provides visibility into engagement, redemption behavior, and campaign performance.
4. Campaign-specific voucher banners and titles support brand visibility and guide users to their next in-app action after redemption.

### Approved Impact

| Metric | Detail | Approval status |
|---|---|---|
| 82,000+ vouchers | Smart E-Vouchers distributed across six Asian markets | APPROVED |
| 16 campaigns | Targeted campaigns launched since partnering | APPROVED |
| 6 markets | Taiwan, Indonesia, Philippines, Singapore, Thailand, Malaysia | APPROVED |

### Usage Rule

Use ShareParty as the preferred approved cross-border API automation case. Do not use EK2A as a separate reference.

Privacy usage note: This case can be used as an approved cross-border example, but do not disclose API implementation details, user-level reward data, client-side workflow details, or market-specific internal performance beyond the approved metrics.


Research positioning boundary: For Research & Insights content, use ShareParty as the approved cross-border API automation / research incentive case. It should not be treated as a generic MarTech example when the task is specifically about research participation, survey incentives, respondent reward fulfillment, or multi-market fieldwork.

## Detailed Reusable Case: L'Oreal Taiwan Spring Celebration

### Basic Information

| Field | Detail |
|---|---|
| Code | B8 |
| Region | Taiwan |
| Vertical | FMCG / beauty and consumer goods |
| Scenario | Staff engagement, employee rewards, corporate event activation, Lucky Draw |
| Year / period | 2026 |
| Product | Rewards and recognition infrastructure, Lucky Draw mechanics |
| Approval status | MIXED |

### Overview

On-us powered L'Oreal Taiwan's 2026 Spring Celebration, a staff engagement event designed to motivate and reward employees through a digitally driven reward experience.

### Approval Split

| Item | Approval status |
|---|---|
| Partnership story and staff engagement framing | APPROVED |
| NTD 2.35M prize value distributed | CONFIRM |
| 816 fulfillments | CONFIRM |

### Usage Rule

For external content, use the L'Oreal Taiwan name only for the approved partnership story unless the internal figures are confirmed for the specific asset.

Safe named version:

```text
On-us supported L'Oreal Taiwan's staff engagement event with a digital reward and recognition experience.
```

Safe anonymized metric version:

```text
In a large-scale corporate staff engagement event, On-us supported NTD 2.35M in prize distribution and 816 fulfillments.
```

Privacy usage note: For external content, use the approved partnership story only. Do not pair L'Oreal Taiwan with CONFIRM prize value, fulfillment count, employee-level details, winner details, or internal event logistics unless re-approved.

## Hold / Pending Cases

### Manulife

Status: CONFIRM / TBC.

Manulife is a potentially useful wellness loyalty and acquisition case, but the internal draft contains placeholders and pending updates. Do not generate detailed Manulife content until Sales or Mavis provides updated materials.

Privacy usage note: Do not use Manulife client name, metrics, or detailed campaign mechanics externally until updated materials and approval status are confirmed.

### Chubb

Status: PENDING / TBC.

Chubb may become a useful digital insurance case, but the current knowledge base does not have enough confirmed information. Do not use Chubb in generated content yet.

Privacy usage note: Do not use Chubb as a named case externally. Treat it as pending internal context only until Sales confirms usable information.

### Masked HK Community Organization

Status: CONFIRM.

This case is a volunteer recognition program. The original client name must never be shown. Use only masked wording such as:

```text
a Hong Kong community organization
```

or

```text
a community volunteer recognition program in Hong Kong
```

Privacy usage note: Never reveal the original client name or identifying details. Use only masked wording and avoid location, event, or partner details that could make the organization identifiable.

## Approved Metric Library

Use approved metrics with client names only when the case status supports it.

| Case | Approved metric | Period / context |
|---|---|---|
| BOC Life | 140,000+ users reached | Since 2022, targeted in-app campaigns |
| BOC Life | 250,000+ incentives delivered | Since 2022, via On-us platform |
| BOC Life | 85%+ use rate | Incentives delivered |
| Swire Properties | 82,000+ visitors | 2024 5-day event period plus 3,000+ VIPs |
| Swire Properties | 58,000+ vouchers issued | 2023 and 2024 editions |
| Swire Properties | 0.27 tonnes CO2 cut per year | Replacing paper vouchers |
| Swire Properties | 80%+ merchant positive feedback | Approved website case study |
| ShareParty Insight | 82,000+ vouchers distributed | Across six Asian markets |
| ShareParty Insight | 16 campaigns | Since partnering |
| ShareParty Insight | 6 markets | Taiwan, Indonesia, Philippines, Singapore, Thailand, Malaysia |

## Internal / Confirm Metric Library

These metrics can help internal planning or anonymized drafts, but require confirmation before external use with client names.

| Scenario | Metric | Status |
|---|---|---|
| DBS VOP banking reward enrollment | 3,000+ enrollments within 2 weeks | CONFIRM |
| DBS VOP overseas spending | US$110K overseas dining spending | CONFIRM |
| DBS Lucky Draw | HK$1.2M+ voucher value distributed | CONFIRM |
| DBS Lucky Draw | 11,694 appointments incentivized | CONFIRM |
| Sun Life | 81 campaigns since 2020 | CONFIRM |
| Sun Life | 390,000 vouchers distributed since 2020 | CONFIRM |
| Manulife | 490K+ reached | CONFIRM / TBC |
| Manulife | 46% engagement | CONFIRM / TBC |
| Manulife | 74% open / redeem | CONFIRM / TBC |
| Manulife | 30-40% cost savings | CONFIRM / TBC |
| L'Oreal Taiwan | NTD 2.35M prize value distributed | CONFIRM |
| L'Oreal Taiwan | 816 fulfillments | CONFIRM |
| Swire Properties | 90,000+ vouchers, HKD 4.5M transaction amount, -1,200 kg CO2e, 29 merchants, 78% redemption rate | CONFIRM |

## AI Output Trace Requirement

When using case studies, the AI should include an internal reference trace for human review:

```text
Case used:
Region:
Vertical:
Scenario:
Approval status:
Client name used: yes / no
Metric used: yes / no
If metric used, approved or confirm:
Human confirmation needed: yes / no
Related reference files:
```

This trace helps reviewers quickly see whether the case was used safely.
