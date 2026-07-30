# Blog Style Guide

Last updated: July 2026
Status: Draft for review
Use stage: Repurposing only

## Purpose

Use this file to turn an approved or testing master content brief into a Blog-ready SEO/AEO retrieval asset.

The Blog output should be useful enough for a human marketer to review and paste into a blog CMS after final human approval. It should not be an outline, planning note, testing log, or markdown-heavy internal brief.

The Blog is designed to answer the questions that target buyers search for. It is not an academic essay, research paper, or internal thought-leadership memo.

## SEO / AEO Role

The Blog should:

- Answer the primary search intent directly within the first 60-100 words.
- Use clear, query-led headings that match how a buyer may search, such as "What are card-linked incentives?" or "How do Smart E-Vouchers support consumer engagement?"
- Give each section one clear job: define, explain a mechanism, compare approaches, show a use case, provide supported proof, or answer a question.
- Include a concise FAQ section with 2-4 questions when it improves answer-engine retrieval.
- Use approved statistics, dated research, and source attribution when external evidence is available.
- Explain On-us products in plain business language and connect them to the target audience's objective.
- Remain useful when a search engine or answer engine extracts one paragraph without the rest of the article.

## Output Rule For Repurpose Agent

When Blog is requested, write the Blog content under:

```text
### Blog Clean Copy
```

The content inside `Blog Clean Copy` must be clean publish-ready text:

- Do not include markdown heading symbols such as `#`, `##`, or `###`.
- Do not include "Blog Draft / Notes", "Status", "Testing only", "Needs approval", or internal process comments inside the clean copy.
- Do not write only an outline.
- Do not write only structural notes.
- If the source master content is not approved, keep warnings outside the clean copy under `Channel Review Notes`.
- The frontend will extract only this clean copy into an editable field.

## Recommended Blog Format

Use this plain-text format:

```text
Title
Month DD, YYYY
X min read

Short opening paragraph that explains the buyer problem and why the topic matters now.

Direct answer paragraph that defines the topic or answers the primary search query.

Main Section Heading
Paragraph-led explanation.

Second Section Heading
Paragraph-led explanation.

What [Topic / Product / Mechanism] Can Support
- Bullet point with business value
- Bullet point with mechanism
- Bullet point with proof or safe example

How On-us Approaches It
Paragraph-led explanation connecting the business problem to On-us product logic.

Use Case / Example
Safe case example or anonymized scenario.

Frequently Asked Questions
Question followed by a concise, self-contained answer.

CTA sentence.
```

## Length Guidance

Follow the length and depth of On-us' existing blog style.

- Standard blog: around 400-600 words.
- Short explainer: around 300-450 words.
- Complex thought leadership or case-heavy blog: no more than 750 words.
- Reading-time label should usually be 3-5 mins.

Preserve the master content's essential substance, but remove repeated context, repeated product explanation, internal governance detail, secondary examples, and any section that does not help the primary search query. SEO/AEO usefulness comes from a direct answer and extractable sections, not from maximum length.

## Content Requirements

Include:

- Clear title
- Date placeholder or generated date line
- Reading time line
- Clear definition or category explanation
- Specific business problem
- On-us point of view
- Product / mechanism explanation
- Proof point or safe case example if supported
- CTA

Use headings that read like article headings, for example:

- How Smart E-Vouchers Become a Consumer Behaviour Data Engine
- What Behavioural Data Can E-Vouchers Capture?
- The Role of Personalisation in Consumer Engagement
- The Data-Driven Optimisation Loop
- How Card-Linked Qualification Changes Reward Campaign Design

## Writing Rules

Do:

- Write in paragraph-led article style.
- Make the first paragraph concrete, useful, and responsive to the primary search intent.
- Prefer direct statements over commentary about what the article will argue or explore.
- Use descriptive headings that can stand alone in search and answer-engine results.
- Keep definitions and FAQ answers concise enough to be quoted without losing their meaning.
- Use bullets only for lists, data types, steps, or comparison points.
- Use On-us product names exactly as approved.
- Keep claims within the master content and reviewer boundaries.
- Use British English only when requested by the source request or language rule.

Avoid:

- Outline-only output.
- Internal labels such as "testing only" inside the clean copy.
- Markdown tables unless explicitly useful.
- Unsupported ROI or performance claims.
- Client names, partner names, or metrics unless both the master content and reviewer mark them safe.
- Turning approval questions into confirmed facts.
- Academic or meta-writing openings such as "This piece argues that", "This article argues that", "This essay explores", "The central thesis is", or "It can be argued that".
- Generic academic or AI filler such as "In today's rapidly evolving landscape", "paradigm shift", "discourse", or "conceptual framework" unless a cited source genuinely requires the term.
- Writing about the article itself instead of answering the buyer's question.

Prefer this:

```text
Incentives are increasingly being evaluated as measurable engagement infrastructure, not only as a marketing cost.
```

Avoid this:

```text
This piece argues that incentives are no longer just a marketing cost line.
```
