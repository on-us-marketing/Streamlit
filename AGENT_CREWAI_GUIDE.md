# Agent and CrewAI Workflow Guide

Last updated: July 2026
Status: POC documentation for review

## 1. Purpose

This document explains the agent design and CrewAI workflow for the On-us Master Content Generator.

It focuses only on:

- What each agent does
- How the CrewAI workflow is structured
- What each task receives and produces
- Which project files control agent behavior
- How the POC can generate content now

For the overall system layer diagram, see:

```text
SYSTEM_FRAMEWORK.md
```

## 2. CrewAI Concepts Used In This POC

### Agent

An agent is a role-based LLM worker.

In this project, each agent has:

- Role
- Goal
- Backstory
- Responsibilities
- Inputs
- Expected output
- Guardrails

The editable agent definitions are stored in:

```text
src/on_us_content_agent/config/agents.yaml
```

### Task

A task is a specific work step assigned to an agent.

In this project, each task defines:

- Stage
- Agent responsible
- Dependency on previous tasks
- Purpose
- Expected output

The editable task definitions are stored in:

```text
src/on_us_content_agent/config/tasks.yaml
```

### Crew

A crew is the workflow that runs agents and tasks together.

In this POC, the CrewAI workflow is sequential:

```text
Gap Finder
-> Planning
-> Research
-> Structure
-> Writer
-> Visual Recommendation
-> Optimization
-> Evaluation & Safeguarding
-> Content Rewriter
-> Content Translator
-> Formatting
```

The workflow is implemented in:

```text
src/on_us_content_agent/crew.py
```

### Tools

Tools are helper functions outside the LLM.

Current tools:

```text
tools/retrieval_tool.py
tools/excel_tool.py
tools/webflow_tool.py
```

Current status:

- `retrieval_tool.py` is active. It selects relevant KB files based on the request.
- `excel_tool.py` is a placeholder for future Excel / SharePoint Content Hub output.
- `webflow_tool.py` is a placeholder for future Webflow staging output.

## 3. Current Execution Modes

The project supports two modes.

### Controller Mode

Command:

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py
```

Controller mode is the default usable engine.

It uses the Claude Messages API wrapper directly and follows the architecture in the diagram:

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
   -> Yes: Repurpose Agent -> Content Rewriter / Translator / Formatting
-> Excel Content Hub / staging-ready output
```

Why controller mode is the recommended path:

- It is stable with the current Claude-compatible API endpoint.
- It can generate real content now.
- It logs token usage and time clearly.
- It supports a quality gate and automatic revision loop.
- It supports a human approval gate before repurposing.
- It can create `generated_content.csv` after approval.

Controller mode still follows the same agent logic, but combines some roles into fewer API calls for reliability:

| Controller stage | Agent roles included |
|---|---|
| Planning | Gap Finder, Planning, Research, Structure |
| Drafting | Writer |
| Visual | Visual Recommendation |
| Quality gate | Evaluation & Safeguarding |
| Revision loop | Writer, Evaluation & Safeguarding |
| Repurpose, after `--approved` | Content Rewriter, Content Translator, Formatting |

Compact is kept as an older alias:

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py --engine compact
```

### CrewAI Mode

Command:

```bash
on_us_content_agent/.venv/bin/python on_us_content_agent/src/on_us_content_agent/main.py --engine crewai
```

CrewAI mode runs the full multi-agent structure.

Current status:

- CrewAI is installed.
- Agent and task configs are prepared.
- The workflow is implemented in `crew.py`.
- It is kept as the architecture-aligned orchestration mode.
- In this local Python environment, CrewAI import can be slow because of its dependency chain.
- For reliable content generation, use controller mode first.

Recommended explanation:

```text
The POC is really usable through the workflow controller now. CrewAI is installed and the full-agent workflow is prepared, but controller mode is the reliable path for actual generation and token logging.
```

## 4. Agent Workflow Overview

```text
Gap Finder Agent
|
v
Content Request / Topic Input
|
v
Core Engine / Workflow Controller
|
v
Planning Agent
|
v
Brand Knowledge Base routing
|
v
Research Agent
|
v
Structure Agent
|
v
Writer Agent
|
+-------> Visual Recommendation Agent
|
v
Evaluation & Safeguarding Agent
|
v
Pass Quality Check?
|-- No -> revise through Research / Structure / Writer and re-check
|
v
Human Review
|
v
Approved?
|-- No -> stop before repurpose
|
v
Repurpose Agent
|
+-- Content Rewriter
+-- Content Translator
+-- Formatting Agent
|
v
Excel Content Hub / Staging
|
v
Performance Feedback -> Optimization Agent for next-round improvement
```

## 5. Agent Details

### 5.1 Gap Finder Agent

Group:

```text
Discovery and Planning
```

Purpose:

Check whether the human request is complete enough before planning starts.

Main checks:

- Missing topic
- Missing market
- Missing content type
- Missing target audience
- Missing channel
- Missing supporting notes
- Unclear CTA
- Unsupported claim
- Sensitive client, partner, or metric usage
- SEO/GEO/AEO opportunity

Input:

- Human intake request
- Keyword bank, if available
- Existing content records, if available
- Approved terminology
- Loading logic

Output:

- Missing input report
- Topic gap list
- SEO/GEO/AEO opportunity notes
- Claims needing verification
- Proceed / pause recommendation

Guardrail:

```text
This agent does not draft content.
```

### 5.2 Planning Agent

Group:

```text
Discovery and Planning
```

Purpose:

Turn the human input into a clear content route.

Main decisions:

- Content cluster
- Strategic pillar
- Target audience / vertical
- Market
- Enterprise objective
- Writing angle
- CTA direction
- Product route
- Case study route
- KB files to read

Input:

- Human intake request
- Gap Finder output
- `enterprise_objectives_by_vertical.md`
- `content_cluster_mapping.md`
- `master_content_drafting_guidelines.md`

Output:

- Planning brief
- Relevant product / solution route
- Relevant case study route
- Required KB files
- Assumptions
- Open questions

Guardrail:

```text
This agent should route the work, not write the final content.
```

### 5.3 Research Agent

Group:

```text
Master Content Generator
```

Purpose:

Retrieve and summarize supporting facts before the Writer Agent drafts.

Main work:

- Check selected Tier 1 and Tier 2 KB files
- Check product context
- Check proof points
- Check case study support
- Check partner governance if needed
- Add source trace
- Flag missing evidence

Input:

- Planning Agent output
- Brand knowledge base
- Product context files
- Case studies
- Keyword bank
- Translation dictionary
- Source links

Output:

- Source trace by purpose
- Product context summary
- Proof / case support
- Missing evidence risks
- Claims that should stay as open questions

Guardrail:

```text
This agent should not create unsupported claims from reasoning.
```

### 5.4 Structure Agent

Group:

```text
Master Content Generator
```

Purpose:

Build the master content outline before drafting.

Main work:

- Select the right structure based on content cluster
- Define message flow
- Decide proof placement
- Decide CTA placement
- Decide section depth

Input:

- Planning Agent output
- Research Agent output
- Content cluster mapping
- Master content drafting guidelines

Output:

- Section-by-section outline
- Message flow
- Proof placement
- Repurpose notes to preserve

Guardrail:

```text
This agent should not remove claim-boundary sections.
```

### 5.5 Writer Agent

Group:

```text
Master Content Generator
```

Purpose:

Generate the full master content draft.

Main work:

- Write from target audience and enterprise objective
- Explain business context
- Explain On-us point of view
- Explain product / solution logic
- Include proof or case support
- Include claim boundaries
- Include reference trace
- Include open questions

Input:

- Human input
- Planning Agent output
- Research Agent output
- Structure Agent output
- Selected KB files

Output:

- Complete master content draft

Guardrail:

```text
This agent writes source content, not final LinkedIn or blog copy.
```

### 5.6 Visual Recommendation Agent

Group:

```text
Master Content Generator
```

Purpose:

Suggest visual directions to support the content.

Main work:

- Decide whether visual should be product-led, case-led, workflow-led, chart-led, or quote-led
- Suggest safe on-visual text
- Identify approval risks for logos, client names, or metrics

Input:

- Structure Agent output
- Writer Agent draft
- Brand guideline
- Case study and proof point rules

Output:

- Visual direction
- Suggested layout
- Safe on-visual text
- Assets needed
- Approval risks

Guardrail:

```text
This agent does not create final design assets.
```

### 5.7 Optimization Agent

Group:

```text
Review and Optimization
```

Purpose:

Improve clarity, answerability, and SEO/AEO/GEO fit without adding unsupported claims.

Main work:

- Improve headings
- Improve section flow
- Improve keyword alignment
- Remove repetition
- Preserve claim boundaries

Input:

- Writer Agent draft
- Keyword bank
- Brand voice and style guide
- Structure Agent output

Output:

- Optimized master content or edit notes
- SEO/AEO/GEO notes
- Remaining open questions

Guardrail:

```text
This agent cannot add new facts just to improve SEO.
```

### 5.8 Evaluation & Safeguarding Agent

Group:

```text
Review and Optimization
```

Purpose:

Act as a strict reviewer before human review.

Main checks:

- Brand voice
- Approved terminology
- Claim scope hierarchy
- Product accuracy
- Partner / second-party governance
- Case privacy
- Client name and metric pairing
- Localization risk
- Format readiness

Input:

- Optimized draft
- Approved terminology
- Claim scope hierarchy
- Proof points
- Do-not-use rules
- Second-party approval rules
- Translation dictionary

Output:

- Pass / Fail
- Key issues
- Required fixes
- Claim scope risks
- Product accuracy risks
- Partner risks
- Case privacy risks
- Human review questions

Guardrail:

```text
This agent should challenge the draft, not simply polish it.
```

### 5.9 Content Rewriter Agent

Group:

```text
Repurpose Agents
```

Purpose:

Adapt reviewed master content into channel-specific drafts or notes.

Channels:

- LinkedIn
- Newsletter
- Blog excerpt
- News summary
- Sales email

Input:

- Reviewed master content
- Evaluation & Safeguarding output
- Channel style guide

Output:

- Channel-specific draft or adaptation notes
- Claim cautions carried forward

Guardrail:

```text
This agent should not ignore reviewer warnings.
```

### 5.10 Content Translator Agent

Group:

```text
Repurpose Agents
```

Purpose:

Localize content for selected markets and languages.

Main work:

- Use approved terms
- Preserve product names
- Follow ZH-HK / ZH-TW / EN rules
- Flag missing approved translations

Input:

- Reviewed master content
- Translation dictionary
- Language rules

Output:

- Localized content or localization notes
- Terminology notes
- Missing translation questions

Guardrail:

```text
This agent should not translate product names unless approved.
```

### 5.11 Formatting Agent

Group:

```text
Repurpose Agents
```

Purpose:

Prepare content for publishing or content hub formats.

Formats:

- Excel / SharePoint Content Hub
- Webflow
- LinkedIn draft format
- Newsletter draft format

Input:

- Rewritten content
- Localized content
- Review report
- Publishing requirements

Output:

- Metadata fields
- Publishing format
- Missing field questions
- Approval warnings

Guardrail:

```text
This agent prepares content for publishing but does not publish automatically.
```

## 6. CrewAI Task Sequence

The full CrewAI mode maps each task to one agent:

| Step | Task | Agent | Output file |
|---|---|---|---|
| 1 | `gap_check` | Gap Finder Agent | `01_gap_finder_output.md` |
| 2 | `plan_content` | Planning Agent | `02_planning_agent_output.md` |
| 3 | `retrieve_context` | Research Agent | `03_research_agent_output.md` |
| 4 | `build_structure` | Structure Agent | `04_structure_agent_output.md` |
| 5 | `draft_master_content` | Writer Agent | `05_writer_agent_output.md` |
| 6 | `recommend_visuals` | Visual Recommendation Agent | `06_visual_recommendation_output.md` |
| 7 | `optimize_content` | Optimization Agent | `07_optimization_agent_output.md` |
| 8 | `review_and_safeguard` | Evaluation & Safeguarding Agent | `08_evaluation_safeguarding_output.md` |
| 9 | `rewrite_for_channel` | Content Rewriter Agent | `09_content_rewriter_output.md` |
| 10 | `localize_content` | Content Translator Agent | `10_content_translator_output.md` |
| 11 | `format_for_publishing` | Formatting Agent | `11_formatting_agent_output.md` |

## 7. Human Input vs LLM Inference

Recommended human input:

```text
Content Category / Cluster
Target Audience / Vertical
Content Objective
Channel
Supporting Notes
Claims to Include
Claims to Avoid
Similar Reference, if any
Future Repurpose Channels
```

LLM can infer:

```text
Strategic pillar
Enterprise objective
Writing angle
Relevant product / solution
Relevant case study
Required structure
Relevant KB files
Open questions
```

Reason:

The human should define business intent. The LLM should decide routing, structure, and evidence selection based on the KB.

## 8. Why The Reviewer Is Separate

The system should not rely on the Writer Agent to approve its own content.

The Writer Agent focuses on:

- Completeness
- Business logic
- Product explanation
- Master content structure

The Evaluation & Safeguarding Agent focuses on:

- Product accuracy
- Claim scope
- Partner governance
- Case privacy
- Proof point usage
- Localization risk

This separation helps reduce "garbage in, garbage out" and makes the output safer for human review.

## 9. Current File Control Map

| File | Purpose |
|---|---|
| `main.py` | CLI entry point |
| `crew.py` | Main workflow implementation |
| `llm_client.py` | Direct Claude Messages API wrapper for controller mode |
| `crewai_llm.py` | CrewAI LLM adapter for Claude Messages-style endpoints |
| `config/agents.yaml` | Agent role and behavior definitions |
| `config/tasks.yaml` | Task sequence and expected outputs |
| `tools/retrieval_tool.py` | KB file selection and loading |
| `tools/excel_tool.py` | Future Excel / SharePoint writer |
| `tools/webflow_tool.py` | Future Webflow helper |

## 10. Recommended Mentor Explanation

```text
The current POC has two layers of implementation.

First, the agent architecture is designed as a CrewAI multi-agent workflow with separate agents for planning, research, writing, review, repurposing, localization, and formatting.

Second, the usable controller engine runs the same logic with real API calls, quality-gate review, revision loop, human approval gate, and repurpose output. This lets us generate real content and record tokens now, while the full CrewAI orchestration remains available for further testing.
```
