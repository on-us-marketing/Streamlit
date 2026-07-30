# Internal UI MVP

Last updated: July 2026
Status: Working MVP

## Purpose

This MVP gives the On-us Marketing team a simple frontend for the Master Content Generator.

It turns human input into:

- Master content
- Reviewer / claim-checker result
- Repurpose output
- Selected KB file trace
- Run log and saved generation records

## User Flow

```text
Marketing user opens frontend
-> selects provider preset and API format
-> enters API URL and API key
-> enters content request
-> selects repurpose channels and languages
-> generates master content
-> reviewer runs automatically
-> repurpose output is generated
-> all files are saved under outputs/runs/{timestamp}/
```

## Human Inputs

The frontend asks the user for:

- API URL
- API format: anthropic / openai
- API key
- Model name
- Reviewer model, optional
- Content Category
- Target Audience
- Content Objective
- Supporting Notes
- Claims to Include
- Claims to Avoid
- Similar Reference URL / notes
- Repurpose channels: Blog, LinkedIn, Newsletter, Webflow
- Languages: EN, ZH-HK, ZH-TW

## LLM-Inferred Fields

The system asks the LLM to infer:

- Writing angle
- Relevant product / solution
- Relevant case study
- Required structure
- Selected KB files
- Repurpose structure
- Open questions

## Frontend Result Tabs

The Streamlit UI shows:

- Master Content
- Reviewer Result
- Repurpose
- Selected KB
- Planning
- Visual
- Run Log
- Files

## Saved Output Files

Each run creates a timestamped folder:

```text
outputs/runs/{timestamp}/
```

Typical files:

```text
request.json
01_planning_agent_output.md
selected_kb_files.md
02_master_content_draft_v1.md
03_visual_recommendation_output.md
04_evaluation_safeguarding_output.md
final_master_content.md
human_review_packet.md
90_repurpose_agent_output.md
workflow_state.json
run_log.csv
generated_content.csv
```

## API Key Safety

The API key is entered in the frontend session only.

It is not saved into:

- `request.json`
- `run_log.csv`
- `human_review_packet.md`
- generated content files

The frontend supports provider presets for:

- Claude / devaicode, using Anthropic-compatible messages format
- NVIDIA models, using OpenAI-compatible chat completions format
- Custom endpoint and model input

## How To Run

```bash
cd <project-folder>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -e .
.venv/bin/streamlit run app.py
```

## Current Limitation

This is still an MVP. The repurpose output is generated immediately after review, but it should still be treated as an internal draft until a human approves it for publishing.
