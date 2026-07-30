# Frontend Review UI Notes

This package is the updated Streamlit version of the On-us Master Content Generator.

## What changed

- Backend code is synced from `/Users/xyyyyy/Downloads/content_generator-main/src/on_us_content_agent`.
- Knowledge base is synced from `/Users/xyyyyy/Downloads/content_generator-main/knowledge_base`.
- The frontend now shows the generated master content revision directly in a review-friendly view.

## Main review screen

After generation, open the `Master Review` tab.

It shows:

- `Narrative`: the revisioned master content split into collapsible sections.
- `Claim Boundaries`: safe claims, approval-needed claims, and avoid items highlighted in different colors.
- `Review & Trace`: open questions as checkboxes, reviewer output, and reference trace for human checking.

The app chooses the best available master file in this order:

1. `final_master_content.md`
2. latest `*_master_content_revision_round_*.md`
3. `draft_needs_revision.md`
4. `02_master_content_draft_v1.md`

This means mentor can still review the latest revision even if the quality gate fails and the content is not yet approved for final repurpose.

## API note

The API key is entered in the Streamlit sidebar for the current session only. It is not written into the repo or saved in the app files.
