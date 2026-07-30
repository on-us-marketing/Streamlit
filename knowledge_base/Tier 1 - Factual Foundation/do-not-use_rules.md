# Do-Not-Use Rules

Last updated: July 2026
Status: Draft for review
Use stage: Master Content Brief and final review

## Purpose

This file prevents the AI from generating risky claims, inaccurate technical descriptions, outdated wording, and generic AI writing patterns.

## Related Reference Pointers

If the AI wants to use a claim that may be risky, check the relevant source file instead of rewriting it from assumption.

| Risk area | Check this file | Why |
|---|---|---|
| Product naming or outdated wording | `Tier 1 - Factual Foundation/approved_terminology.md` | To use current approved terms |
| Partner names, logos, endorsements, data access | `Tier 1 - Factual Foundation/second_party_approval_rules.md` | To avoid unsafe second-party claims |
| AI, agentic AI, automation, future-facing capability status | `Tier 2 - Product Context/on_us_intelligence.md` | To avoid presenting future-facing AI features as live |
| Campaign numbers or proof points | `Tier 1 - Factual Foundation/proof_points.md`; `Tier 1 - Factual Foundation/case_studies.md` | To avoid unsupported performance claims |
| Smart E-Voucher mechanics or technical detail | `Tier 2 - Product Context/smart_e_voucher.md` | To avoid inaccurate product descriptions |

## Terms to Avoid or Use Carefully

Do not use:

- Agentic Growth Engine
- ON-US
- On-Us
- Onus
- on-us as company name

Use instead:

- Incentive Intelligence
- On-us

## Banned Framings

Do not frame On-us as:

- Benefiting from client data instead of empowering the client
- Selling raw customer data
- A surveillance-based marketing tool
- A generic AI vendor
- A cashback-only or coupon-only platform
- A replacement for the client's CRM

Correct framing:

```text
On-us helps marketers turn reward interactions into campaign-level insights and better incentive decisions.
```

## Partner and Competitor Restrictions

Do not:

- Disparage named foundation model competitors
- Suggest Microsoft, Visa, Google, or any partner endorses all On-us products unless explicitly approved
- Claim exclusivity unless exact wording has been cleared

## Consumer-Copy Risk Words

Avoid technical or surveillance-adjacent wording in consumer-facing content.

| Avoid | Better alternative |
|---|---|
| geo-fenced | offers near you |
| tracking users | understanding campaign engagement |
| monitoring customer behavior | analyzing reward interaction signals |
| raw data monetization | campaign-level insights |

## Technical Accuracy Trap

Correct security mechanism:

```text
Dynamic QR codes refresh every 120 seconds and are paired with unique voucher IDs.
```

Do not write:

```text
encrypted algorithmically generated codes
```

Reason:

This was a prior published error and should not be regenerated.

## AI Writing Patterns to Strip

Avoid:

- Em dashes
- Fragmented triplets
- Staccato punchlines
- Broken sentences
- Redundant restatement
- Analogy as section opener
- Overstatement
- Too many buzzwords in one paragraph
- Long generic opening paragraphs

## Repurpose Governance Inheritance

The Blog or LinkedIn layer must not weaken, hide, or reverse a Master Content restriction.

Treat these labels as instructions, not source copy:

- requires approval
- confirm / confirm-only
- pending / TBC
- not approved
- internal only
- never use
- avoid
- unsupported
- open question

Any claim carrying one of these labels must stay out of public-facing clean copy. This applies even when the claim appears elsewhere in the Master Content or was supplied in the human prompt. Repurposing must not turn a restricted claim into a headline, hook, CTA, comparison, caption, or hashtag.

Do not introduce a new:

- Statistic or performance number
- Client or partner name
- Product capability
- Comparative performance statement
- Market share or leadership statement
- Campaign result

## Channel-Level Hard Bans

Do not use:

- Academic self-reference such as "This piece argues", "This article offers", "This article explores", "The goal of this comparison", or "The central thesis"
- `#Onus`
- `hashtag#` artifacts
- `{.mark}` or other export markup
- A literal `Title` placeholder
- "First in HK" or "first in Hong Kong" unless the exact claim is approved
- "AI leader"
- "Agentic Growth Engine"
- "Outperforms" or "outperforming" in a comparative headline or claim unless an approved comparison supports it

Do not use fragmented triplets or staccato punchlines such as:

```text
Infrequent. Hard to personalize. Even harder to measure.
```

Use a complete sentence instead:

```text
Infrequent campaigns are harder to personalize and measure over time.
```

## On-us Intelligence Tense

Check every On-us Intelligence sentence against `Tier 2 - Product Context/on_us_intelligence.md`.

- Current capability may use present tense only when the product file supports it.
- Roadmap capability must use explicit future-facing language such as "is building", "is designed to support", or "will support".
- Do not describe autonomous optimization, predictive recommendation, respondent scoring, or similar roadmap concepts as live capability unless the KB status has been updated and approved.

## English Standard

Use American English by default. British spelling is allowed only when the human input explicitly requests it or an approved co-branded asset requires it.

Do not use British spelling by default, including:

- behaviour
- optimise
- programme
- centre
- personalise
- recognised
- honour

## Generic Vocabulary Guidance

Some common marketing words are acceptable in On-us content, but they should not be used as empty filler. If the AI uses these terms, it should attach them to a concrete product feature, workflow, proof point, or case example.

These are **not banned**, but should be used with support:

- innovative solution
- seamless experience
- cutting-edge technology
- revolutionize
- game-changing
- one-stop solution

Weak:

```text
On-us provides an innovative and seamless one-stop solution.
```

Better:

```text
On-us provides a Smart E-Voucher workflow covering issuance, merchant selection, redemption, settlement support, and campaign performance visibility.
```

Avoid terms that are both generic and unsupported:

- best-in-class
- unmatched
- world-leading, unless approved
- unlock the future
- leverage synergies
- next-gen, unless the next-generation capability is explained
