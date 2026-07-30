# On-us Master Content Generator System Framework

Last updated: July 2026
Status: POC architecture reference

## 1. System Purpose

The On-us Master Content Generator turns a human content request into a structured master content draft.

The master content is not the final LinkedIn post, blog post, newsletter, or press release. It is the factual source draft that downstream repurpose agents can adapt safely.

## 2. Layer Diagram

```text
On-us Master Content Generator
|
+-- 1. Input Layer
|   |
|   +-- Human provides:
|       +-- Topic
|       +-- Market
|       +-- Content type / cluster
|       +-- Target audience / vertical
|       +-- Channel / future repurpose channel
|       +-- Supporting notes
|       +-- Claims to include / avoid
|
+-- 2. Context & Retrieval Layer
|   |
|   +-- Brand Knowledge Base
|   +-- Brand Voice & Style Guide
|   +-- Product Information
|   +-- Past Blogs / LinkedIn / Case Studies
|   +-- Keyword Bank
|   +-- Translation Dictionary
|   +-- Competitor References
|   +-- Source Links
|
+-- 3. CrewAI Agent Workflow
|   |
|   +-- Discovery and Planning
|   |   +-- Gap Finder Agent
|   |   +-- Planning Agent
|   |
|   +-- Master Content Generator
|   |   +-- Research Agent
|   |   +-- Structure Agent
|   |   +-- Writer Agent
|   |   +-- Visual Recommendation Agent
|   |
|   +-- Review and Optimization
|   |   +-- Optimization Agent
|   |   +-- Evaluation & Safeguarding Agent
|   |
|   +-- Repurpose Agents
|       +-- Content Rewriter Agent
|       +-- Content Translator Agent
|       +-- Formatting Agent
|
+-- 4. Output Layer
|   |
|   +-- Master Content Draft
|   +-- Review Report
|   +-- LinkedIn Draft / Notes
|   +-- Newsletter Draft / Notes
|   +-- Excel / SharePoint Content Hub Format
|   +-- Webflow / Publishing Format
|
+-- 5. Feedback Layer
    |
    +-- Human approval / rejection
    +-- Revision notes
    +-- Performance data
    +-- Future topic planning reference
```

## 3. Agent Groups

### Discovery and Planning

Purpose:

- Diagnose missing input.
- Decide the content route before drafting.
- Prevent unclear topic, audience, objective, or claim input from becoming weak output.

Agents:

```text
Gap Finder Agent
Planning Agent
```

Key outputs:

- Missing input report
- Content cluster
- Target audience / vertical
- Enterprise objective
- Writing angle
- CTA direction
- Product and case study route
- KB files to retrieve

### Master Content Generator

Purpose:

- Build the actual source content using the right KB files.
- Keep the content factual, structured, and business-outcome-led.

Agents:

```text
Research Agent
Structure Agent
Writer Agent
Visual Recommendation Agent
```

Key outputs:

- Source trace
- Outline and message flow
- Master content draft
- Visual recommendation notes

### Review and Optimization

Purpose:

- Improve clarity and SEO/AEO/GEO fit.
- Check claims, product accuracy, partner governance, case privacy, localization, and format before human review.

Agents:

```text
Optimization Agent
Evaluation & Safeguarding Agent
```

Key outputs:

- Optimized draft
- Review report
- Required fixes
- Human review questions

### Repurpose Agents

Purpose:

- Adapt the reviewed master content into channel-specific draft formats.
- Preserve claim warnings and approval boundaries.

Agents:

```text
Content Rewriter Agent
Content Translator Agent
Formatting Agent
```

Key outputs:

- LinkedIn / newsletter / blog adaptation notes
- Localization notes
- Excel / SharePoint / Webflow formatting notes

## 4. Project File Mapping

```text
on_us_content_agent/
|
+-- .env.example
|   +-- Environment variable template. API keys should stay in local .env or terminal env.
|
+-- pyproject.toml
|   +-- Python dependencies and project metadata.
|
+-- README.md
|   +-- Developer-facing project guide.
|
+-- SYSTEM_FRAMEWORK.md
|   +-- Mentor-facing architecture and layer explanation.
|
+-- sample_request.json
|   +-- Example human input form.
|
+-- knowledge_base/
|   +-- Organized KB markdown files.
|
+-- outputs/
|   +-- generated_content.csv and local run outputs.
|
+-- src/on_us_content_agent/
    |
    +-- main.py
    |   +-- CLI entry point.
    |
    +-- crew.py
    |   +-- Workflow controller and optional CrewAI orchestration.
    |
    +-- llm_client.py
    |   +-- Direct Claude Messages API wrapper used by stable controller mode.
    |
    +-- crewai_llm.py
    |   +-- CrewAI LLM adapter for Claude Messages-style endpoints.
    |
    +-- tools/retrieval_tool.py
    |   +-- KB routing and file loading logic.
    |
    +-- tools/excel_tool.py
    |   +-- Future Excel / SharePoint content hub writer.
    |
    +-- tools/webflow_tool.py
    |   +-- Future Webflow staging helper.
    |
    +-- config/agents.yaml
    |   +-- Editable agent role, responsibility, input, output, and guardrail definitions.
    |
    +-- config/tasks.yaml
        +-- Editable task sequence and expected output definitions.
```

## 5. Current POC Logic

The current system supports two modes:

```text
controller mode:
Gap Finder -> Topic Input -> Core Engine -> Planning -> KB routing -> Research -> Structure -> Writer -> Visual Recommendation -> Evaluation & Safeguarding -> Quality Gate -> Human Review -> Approved Repurpose

crewai mode:
Full CrewAI Agent / Task orchestration for the same agent structure
```

Controller mode is the recommended usable mode because it already works with the Claude Messages API endpoint, produces token logs, supports quality-gate revision, and stops before repurpose unless human approval is provided.

CrewAI mode is kept as the architecture-aligned orchestration mode. It is installed, but its local import chain can be slower than the controller path.

## 6. Why This Structure Matters

This structure separates:

- Planning from writing
- Retrieval from reasoning
- Drafting from reviewing
- Master content from channel-specific repurposing
- Human-provided intent from LLM-inferred route

This helps reduce:

- Wrong product routing
- Unsupported claims
- Overuse of proof points
- Partner governance risks
- Case study privacy issues
- Channel copy being written too early
