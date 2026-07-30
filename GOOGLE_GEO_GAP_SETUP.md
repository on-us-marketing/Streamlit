# GEO / SEO Gap Workflow Setup

## What Each Source Does

```text
GeoVector = Which buyer prompts rarely mention On-us?
Google Ads = Is there measurable search or commercial demand around the prompt?
GA4 = Does On-us already have a related page, and is it attracting engaged organic traffic?
Internal KB = What can On-us safely and accurately say?
Tavily = Optional current external evidence after a gap has been selected.
```

For GeoVector-led opportunities, the app combines the first three signals into a prioritisation score:

```text
60% GEO visibility gap
25% Google Ads demand
15% GA4 site-coverage gap
```

This score is for content planning. It is not a traffic or revenue forecast.

Google Ads and GA4 can also be used without GeoVector:

```text
Google Ads only = group concentrated search demand and identify likely missing SEO/AEO assets.
GA4 only = identify weak existing landing pages that may need a clearer intent, expansion, or refresh.
Google Ads + GA4 = compare demand with current page coverage and choose create vs refresh.
```

## Recommended Rollout

### Phase 1: Start With Exports

1. Export prompt-level results from GeoVector as CSV or JSON.
2. Export either Google Ads Search Terms or Keyword Planner results as CSV.
3. Export GA4 Organic Search landing pages as CSV.
4. Upload any available source in `Find Content Gaps`. All three are not required.
5. Review Ads / GA4 opportunities or GeoVector / manual gaps and choose one for the Content Generator.
6. Edit the generated category, optional audience selections, objective, and supporting notes.
7. Leave Web Research off when internal KB evidence is enough, or turn it on for current market evidence.
8. Generate Master Content, review it, then use the requested repurpose outputs.

This phase works without Google developer credentials and is the quickest way to validate whether the ranking is useful.

### Phase 2: Connect GA4 Data API

1. Create or choose a Google Cloud project.
2. Enable `Google Analytics Data API`.
3. Create a service account and download its JSON key.
4. In GA4, open `Admin -> Property access management` and add the service-account email with Viewer access.
5. Copy the numeric GA4 Property ID.
6. Add `GA4_PROPERTY_ID` and `GOOGLE_SERVICE_ACCOUNT_JSON` to Streamlit Secrets.
7. In the app, open `Find Content Gaps -> Data Sources` and click `Sync GA4 Organic Landing Pages`.

The app requests read-only Organic Search landing-page metrics for the previous 180 days.

Official documentation:

- https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries
- https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport

### Phase 3: Connect Google Ads API

1. Use a Google Ads manager account or the account approved by the company.
2. Apply for a Google Ads API developer token under `Tools & Settings -> API Center`.
3. In Google Cloud, create an OAuth 2.0 client.
4. Authorise a company Google user with the `https://www.googleapis.com/auth/adwords` scope and obtain a refresh token.
5. Add these values to Streamlit Secrets:

```toml
GOOGLE_OAUTH_CLIENT_ID = "..."
GOOGLE_OAUTH_CLIENT_SECRET = "..."
GOOGLE_OAUTH_REFRESH_TOKEN = "..."
GOOGLE_ADS_DEVELOPER_TOKEN = "..."
GOOGLE_ADS_CUSTOMER_ID = "..."
GOOGLE_ADS_LOGIN_CUSTOMER_ID = "..." # only when using a manager account
GOOGLE_ADS_API_VERSION = "v23"
```

6. Click `Sync Google Ads Search Terms` in the app.

The live connector reads only search-term performance. It does not create or change campaigns. Keyword Planner exports can still be uploaded to add average monthly search volume and competition signals.

Official documentation:

- https://developers.google.com/google-ads/api/docs/get-started/dev-token
- https://developers.google.com/google-ads/api/docs/oauth/overview
- https://developers.google.com/google-ads/api/docs/reporting/search-terms

## GeoVector Integration

The first version uses GeoVector CSV/JSON imports because normal API access may require a separate enterprise agreement. Ask the GeoVector account owner whether API access or scheduled exports are included in the company plan.

Useful import columns include:

```text
Prompt
Mention Rate
Mentions
Responses
Competitors
Engine
Market
Language
Journey Stage
```

The importer accepts alternative column names such as `Query`, `Visibility Rate`, and `Platform`.

## Gap Decision Rules

```text
Low mention + paid-search demand + no related GA4 page
-> Create a new SEO/AEO pillar or explainer.

Low mention + paid-search demand + weak related GA4 page
-> Refresh and expand the existing page.

Low mention + healthy related GA4 page
-> Strengthen definitions, comparison coverage, evidence, FAQ answers, and citation-ready passages.

Low mention + no Google Ads demand
-> Treat as a GEO experiment or thought-leadership opportunity, not automatically a priority SEO asset.
```

## Streamlit Secret Handling

Put credentials in Streamlit Cloud under `Manage app -> Settings -> Secrets`. Never commit `.streamlit/secrets.toml`, downloaded service-account JSON files, refresh tokens, developer tokens, or API keys to GitHub.

Use `.streamlit/secrets.toml.example` only as a field-name reference.

## Lean Generation Output

Fast Generation now makes three LLM calls:

```text
Master Drafter
-> Reviewer / Finalizer
-> Repurpose
```

Normal runs keep the useful files:

```text
final_master_content.md OR draft_needs_revision.md
content_review.md
repurpose_content.md
request.json
workflow_state.json
run_log.csv
generated_content.csv
```

Prompt files, planning drafts, visual notes, intermediate revisions, and selected-KB Markdown are omitted in normal Fast Generation. Use `--debug-artifacts` only when diagnosing the workflow.
