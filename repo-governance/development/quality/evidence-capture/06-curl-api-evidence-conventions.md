---
title: "curl / API Evidence Conventions"
description: "How to capture and format curl/API evidence during plan execution."
category: explanation
subcategory: development
tags:
  - evidence
  - testing
  - screenshots
  - plans
  - verification
  - locale
  - manual-testing
created: 2026-06-20
when_to_use: "Use when capturing curl or API-response evidence for a plan."
---

# curl / API Evidence Conventions

For every API endpoint verified:

1. Record the actual command run (so it is reproducible).
2. Record the full response (or the first 20 lines if very long, with "…truncated" noted).
3. Note the HTTP status code.
4. If the response is > 20 lines, save the full response to `evidence/phase-{N}-{endpoint}.txt`.

**Minimum coverage per endpoint**: happy path (valid input → expected 2xx) + at least one error
path (invalid input → expected 4xx with error body).

Example inline record:

````markdown
> **Evidence** (2026-06-20): API verification for `/api/tools`
>
> ```bash
> curl -s http://localhost:8202/api/tools | jq .
> ```
>
> ```json
> { "tools": [{ "id": "cost-of-living-calculator", "name": "Cost of Living Calculator" }] }
> ```
>
> HTTP 200. Error path: `curl -s -w "\n%{http_code}" http://localhost:8202/api/tools/nonexistent` → 404.
````
