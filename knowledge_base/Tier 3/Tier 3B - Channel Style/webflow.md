# Webflow CMS Style Guide

Last updated: July 2026
Status: Draft for review
Use stage: Repurposing

## Purpose

Use this file when preparing content for Webflow CMS staging.

## Key Requirements

Webflow content should be structured, clean, and easy to review before publishing.

## Suggested Fields

```text
Title:
Slug:
Meta title:
Meta description:
Market:
Language:
Category:
Hero summary:
Body HTML:
FAQ:
CTA:
Source links:
Review status:
```

## Body Structure

Use clear section hierarchy:

```html
<h2>Section title</h2>
<p>Paragraph content.</p>
<ul>
  <li>Bullet point</li>
</ul>
```

## SEO / GEO Notes

Include:

- Definition paragraph
- FAQ
- Comparison or use case section
- Clear On-us product relevance
- Meta title and meta description

## Webflow EN Base Locale Notes

From the original EN context, the EN base locale should stay APAC/global-facing. Avoid making EN Webflow content overly Taiwan-specific unless the page is explicitly a Taiwan page.

Suggested global page framing:

```text
On-us Smart E-Voucher Platform | Multi-Merchant Digital Rewards
```

Use meta descriptions that mention Smart E-Vouchers, digital rewards, multiple merchants, and enterprise customer engagement. Avoid unsupported partner or client result claims in metadata.

## Writing Rules

Do:

- Keep headings specific
- Avoid duplicate sections
- Make the first paragraph explain the topic clearly
- Include source links if external data is referenced
- Mark any unconfirmed claim before staging

Avoid:

- Unsupported client statistics
- Partner claims without approval
- Overly long paragraphs
- Broken HTML
- Mixing language rules in the wrong market version
