# On-us Content Agent

This project is the Phase 1 POC for the On-us Master Content Generator.

It follows the proposed system framework:

```text
Input Layer
-> Context & Retrieval Layer
-> GEO / SEO Gap Finder
-> Optional Tavily Web Research + Human Source Approval
-> CrewAI Agent Workflow
-> Output Layer
-> Feedback Layer
```

The project has two execution modes:

```text
controller = default usable workflow controller with real API calls, quality gate, revision loop, human approval gate, and repurpose output
compact    = alias for controller, kept for older commands
crewai     = optional CrewAI Agent / Task orchestration using the full subagent structure
```

Use `controller` for real content generation and token logging. Use `crewai` only when testing the CrewAI package orchestration itself.

Related documentation:

```text
SYSTEM_FRAMEWORK.md      = overall system layer diagram
AGENT_CREWAI_GUIDE.md   = detailed agent and CrewAI workflow guide
```

## System Structure

```text
Gap Finder Agent
-> Content Request / Topic Input
-> Core Engine / Workflow Controller
-> Planning Agent
-> Brand Knowledge Base routing
-> Research Agent
-> Structure Agent
-> Writer Agent
-> Visual Recommendation Agent
-> Evaluation & Safeguarding Agent
-> Pass Quality Check?
   -> No: revise and re-check
   -> Yes: Human Review Packet
-> Approved?
   -> No: stop before repurpose
   -> Yes: Repurpose Agent
          -> Content Rewriter
          -> Content Translator
          -> Formatting Agent
          -> Excel Content Hub / staging-ready output
-> Performance Feedback
-> Optimization Agent for next-round generator improvement
```

## Project Files

```text
on_us_content_agent/
|
+-- .env.example
+-- pyproject.toml
+-- README.md
+-- SYSTEM_FRAMEWORK.md
+-- sample_request.json
|
+-- knowledge_base/
|   +-- Put the organized KB markdown files here
|
+-- outputs/
|   +-- generated_content.csv
|   +-- runs/
|
+-- src/
    +-- on_us_content_agent/
        +-- main.py
        +-- crew.py
        +-- crewai_llm.py
        +-- llm_client.py
        +-- tools/
        |   +-- retrieval_tool.py
        |   +-- research_tool.py
        |   +-- excel_tool.py
        |   +-- webflow_tool.py
        +-- config/
            +-- agents.yaml
            +-- tasks.yaml
```

## Knowledge Source

By default, the agent reads the knowledge base from:

```text
on_us_content_agent/knowledge_base
```

Put the organized KB markdown files in this folder. If the KB is stored elsewhere, set `ON_US_KB_PATH` in `.env` or pass `--kb` in the command.

## Install

Create a local virtual environment and install dependencies:

```bash
python3 -m venv on_us_content_agent/.venv
on_us_content_agent/.venv/bin/python -m pip install -e on_us_content_agent
```

Install the optional CrewAI experiment only when testing `--engine crewai`:

```bash
on_us_content_agent/.venv/bin/python -m pip install -e 'on_us_content_agent[crewai]'
```

## Human Input

Use `sample_request.json` as the human intake form.

Recommended human-provided fields:

```text
content_category
target_audience
content_objective
channel
supporting_notes
claims_to_include
claims_to_avoid
similar_reference
future_repurpose_channels
```

The agent can infer:

```text
strategic pillar
writing angle
enterprise objective
relevant product / solution
relevant case study
required structure
relevant KB files
assumptions
open questions
```

## GEO / SEO Gap Finder

The Streamlit app supports three content entry paths:

```text
1. Direct input -> editable category / optional audiences / objective / notes
2. Google Ads and/or GA4 -> concentrated opportunities -> select and edit a brief
3. GeoVector CSV or manual gap -> optionally enrich with Ads / GA4 -> select and edit a brief
-> content generation
```

Target Audience is optional and supports multiple selections. Leaving it blank keeps broad SEO, promotional, event, and company-level content from being forced into a banking or other vertical.

GeoVector CSV/JSON, Google Ads CSV, and GA4 CSV work without developer credentials. Live read-only GA4 and Google Ads connections are also supported through Streamlit Secrets. See `GOOGLE_GEO_GAP_SETUP.md` for the exact setup and decision rules.

## Web Research And Source Approval

Tavily research is optional for each content request:

```text
Human input
-> Generate directly from the internal KB
OR
-> 1-2 Tavily basic searches
-> source-policy and publication-date filtering
-> human may select approved sources or continue without one
-> approved web research + internal KB go to the Master Content Drafter
-> Reviewer checks attribution and On-us claim boundaries
```

The default limit is two basic searches and five candidate sources. Reddit, common forum and personal-blog platforms, forum-style URLs, and pages without a detectable publication or update date are excluded.

External research may support market trends, external statistics, research reports, competitor context, current news, and SEO/GEO analysis. On-us product facts, customer cases, partner relationships, capabilities, and proof points must still come from the internal KB.

Configure the company Tavily key in Streamlit Cloud under `Manage app -> Settings -> Secrets`:

```toml
TAVILY_API_KEY = "tvly-your-company-key"
LLM_API_KEY = "your-company-llm-key"
LLM_PROVIDER = "anthropic"
LLM_API_URL = "https://devaicode.dev/v1/messages"
LLM_MODEL = "claude-sonnet-5"
```

For local use, create `.streamlit/secrets.toml` with the same settings. This file is ignored by Git. The app automatically uses the company Tavily and LLM APIs; users may enter temporary override keys in the sidebar, and override keys are not written into run files.

The app enables Fast Generation by default:

```text
Master Drafter
-> independent Reviewer + Finalizer
-> requested Repurpose output
```

Fast Generation uses three LLM calls in the normal case. KB routing is deterministic, and the Planning and Visual Recommendation stages do not call the LLM or create empty process outputs. Turn Fast Generation off only when testing the full experimental workflow.

Lean artifacts are enabled in the frontend. Normal fast runs retain the final Master Content, Content Review, Repurpose Content, request, workflow state, token log, and CSV index. Prompts and intermediate Markdown files are only retained when the CLI is run with `--debug-artifacts`.

## Run Dry Run

Dry run checks file routing without calling the API.

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py --dry-run
```

## Run Content Generation

Set the API key in your terminal environment.

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py
```

This runs the default usable controller flow and stops at the human review gate.

After human approval, run with `--approved` to generate repurposed output and `generated_content.csv`:

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py --approved
```

Optional separate reviewer model:

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py --review-model claude-opus-4-8
```

Optional CrewAI package orchestration mode:

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py --engine crewai
```

Note: CrewAI is installed, but in this local Python environment the CrewAI import chain can be slow. The reliable production-style POC path is `--engine controller`.

## Output

Each run creates a timestamped folder under:

```text
on_us_content_agent/outputs/runs/
```

Normal Fast Generation output files:

```text
request.json
final_master_content.md OR draft_needs_revision.md
content_review.md
repurpose_content.md
workflow_state.json
run_log.csv
generated_content.csv
```

When optional web research is used, the source log and approved research brief are also retained. To keep prompts, planning output, selected-KB notes, intermediate drafts, visual recommendations, and revision files for troubleshooting, run the CLI with:

```bash
--fast-mode --debug-artifacts
```

`run_log.csv` records stage, agent, model, token usage, and API time where available.

## Config Files

Agent behavior is editable here:

```text
src/on_us_content_agent/config/agents.yaml
```

Task behavior is editable here:

```text
src/on_us_content_agent/config/tasks.yaml
```

The YAML files are intentionally detailed so the team can adjust responsibilities, guardrails, and expected outputs without rewriting the whole workflow.

## Next Upgrade

Recommended next improvements:

1. Connect Excel / SharePoint content hub output.
2. Add memory for approved / rejected content.
3. Add performance feedback for future topic planning.
4. Add Webflow staging mapping.
5. Add a simple UI for human input fields.
