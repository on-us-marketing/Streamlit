# Claim Scope Hierarchy

Last updated: July 2026
Status: Draft for review
Use stage: Master Content Brief

## Purpose

This file tells the AI how to control the scope of claims, numbers, proof points, and case evidence.

The main rule is:

```text
A proof point can only be used at the scope it was approved for.
Do not push a broad claim down into a specific campaign, client, product, or market unless the source clearly supports that exact scope.
```

For example, `50M+ consumer reach` is an approved company-scale proof point. It can support On-us' company scale, but it should not be used to imply that one campaign reached 50M+ consumers.

## Scope Hierarchy

Use this hierarchy before placing any claim in a brief or draft:

```text
Company
  ↓
Platform
  ↓
Product / Solution
  ↓
Campaign / Use Case
  ↓
Client / Partner
```

Claims can move **up** the hierarchy more safely than they can move **down**.

Example:

- A campaign result can support a broader product narrative if anonymized and carefully framed.
- A company-scale number cannot automatically become a product result, campaign result, or client result.

## Claim Levels

| Level | What it means | Example claim type | Safe use | Unsafe use |
|---|---|---|---|---|
| Company | Facts about On-us as a company | Founded background, markets served, company positioning, awards, broad client categories | Company profile, partner intro, high-level credibility | Do not use as proof that a specific product or campaign performed well |
| Platform | Overall On-us platform or ecosystem capability | 50M+ consumer reach, 3,000+ merchants, 400,000+ store touchpoints, 75% average voucher open rate | Platform overview, broad capability content | Do not attach to one client, one market, or one campaign |
| Product / Solution | Capability of a specific On-us product or solution | Smart E-Voucher features, VOP non-cashback benefits, On-us Express HK self-serve scope, ESG Voucher 12.2g CO2/Voucher | Product education, solution explanation | Do not imply every product has the same capability |
| Campaign / Use Case | Result or setup of a campaign type or scenario | Anonymized banking enrollment, insurance lead acquisition, employee event fulfillment | Scenario-based case support | Do not attach to a named client unless approved |
| Client / Partner | A named client, partner, or second-party reference | DBS, BOC Life, Sun Life, L'Oreal Taiwan, Visa, Microsoft, Google Wallet | Named credibility only when approved | Do not attach real metrics, endorsement, exclusivity, or data access unless explicitly approved |

## Default Direction Rule

When the AI is unsure about scope, use the broader and safer level.

```text
If the source says company scale, write company scale.
If the source says platform average, write platform average.
If the source says anonymized campaign result, write anonymized campaign result.
If the source says named client only, write named client only without numbers.
```

If the prompt asks for a more specific claim than the source supports, write:

```text
Needs confirmation: the loaded files do not confirm this proof point at campaign / client / market level.
```

## Proof Point Placement Rules

### Company-Level Claims

Use for:

- Company profile
- Partner introduction
- Investor / ecosystem credibility
- General On-us overview

Examples:

```text
On-us is a Hong Kong-founded Smart E-Voucher platform with regional market presence across Hong Kong, Taiwan, Singapore, Malaysia, and Thailand.
```

```text
On-us reaches 50M+ consumers across its broader ecosystem.
```

Do not write:

```text
This campaign reached 50M+ consumers.
```

unless the campaign source explicitly says so.

### Platform-Level Claims

Use for broad On-us platform capability:

- 50M+ consumer reach
- 3,000+ merchants
- 400,000+ physical store touchpoints
- 75% average voucher open rate
- 65% average campaign cost saving
- 70%+ conversion rate
- 2.5 minutes average voucher interaction time

Safe framing:

```text
At a platform level, On-us has supported reward engagement through a merchant ecosystem of 3,000+ merchants and 400,000+ physical store touchpoints.
```

Avoid:

```text
This ESG Voucher campaign achieved a 75% open rate.
```

unless that exact campaign metric is approved.

### Product / Solution-Level Claims

Use only for the relevant product or solution.

Examples:

- `ESG Voucher` can use `ISO 14067:2018 Certified — Savings: 12.2g CO2/Voucher`.
- `On-us Express` should be described as a Hong Kong-focused self-serve e-voucher platform for SMEs.
- `VOP` should use the approved wording: `On-us powers the Visa Offer Platform to deliver card-linked non-cashback benefits.`

Do not transfer product-level claims across products.

Avoid:

```text
Every Smart E-Voucher saves 12.2g CO2.
```

Correct:

```text
For ESG Voucher, the approved carbon-saving proof point is ISO 14067:2018 Certified with 12.2g CO2 savings per voucher.
```

### Campaign / Use Case-Level Claims

Use campaign metrics only when they are anonymized or explicitly approved.

Safe:

```text
In an anonymized banking reward enrollment campaign, On-us supported 3,000+ enrollments within 2 weeks.
```

Unsafe:

```text
DBS achieved 3,000+ enrollments in 2 weeks.
```

unless this exact wording is approved for the current use.

### Client / Partner-Level Claims

Use named clients or partners carefully.

Named client mode:

```text
DBS Oversea Reward Program can be referenced as a banking reward example.
```

Anonymized metric mode:

```text
In a banking reward enrollment campaign, On-us supported 3,000+ enrollments within 2 weeks.
```

Do not combine the two modes unless the exact client + metric claim has been approved.

For second-party partners such as Visa, Microsoft, or Google Wallet, always check `second_party_approval_rules.md`.

## Claim Downgrade Rule

If a specific claim is not safely supported, downgrade it to a broader level.

| User asks for | If not supported | Safer output |
|---|---|---|
| Client result | Use anonymized scenario result | "In an anonymized banking campaign..." |
| Campaign result | Use platform-level capability | "At platform level..." |
| Product result | Use product capability only | "The product supports..." |
| Market result | Use regional / company context | "On-us has regional presence..." |
| Guaranteed impact | Use enabling language | "can support", "helps marketers", "is designed to" |

## Words That Signal Overclaiming

Be careful if a draft includes:

- achieved
- guaranteed
- proven to
- increased by
- generated
- reached
- delivered
- exclusive
- endorsed by
- powered by partner data
- best / leading / No. 1

These words are not always banned, but they require the correct claim scope and supporting source.

## Required QA Questions

Before final output, the AI should check:

1. Is this claim company-level, platform-level, product-level, campaign-level, or client-level?
2. Is the source approved for this exact level?
3. Am I moving a broad number into a specific product, campaign, market, or client?
4. Am I combining a named client with a real metric?
5. Am I implying partner endorsement, exclusivity, or data access?
6. If the support is missing, did I write `Needs confirmation` instead of guessing?

## Related Files

Read these files depending on the claim:

| Need | Read |
|---|---|
| Approved numbers and broad proof points | `proof_points.md` |
| Case metrics and named client rules | `case_studies.md` |
| Partner / second-party claim rules | `second_party_approval_rules.md` |
| Product-specific claim boundaries | Relevant Tier 2 product file |
| Company description / market presence | `company_overview.md` |

