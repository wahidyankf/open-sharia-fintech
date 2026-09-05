---
title: "API Verification"
description: "How to manually verify an API endpoint with curl."
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use when preparing to manually verify an API change."
---

# API Verification

Use `curl` via Bash to verify API endpoints respond correctly.

## API Verification Checklist

After implementing an API change, verify:

1. **Health check**: Confirm the server is running and responding.
2. **Happy path**: Send a valid request and confirm the expected response shape, status code, and data.
3. **Error cases**: Send invalid requests and confirm proper error responses (4xx status codes, error messages).
4. **Edge cases**: Test boundary conditions (empty payloads, missing fields, maximum lengths).

## Example: API Endpoint Verification

```bash
# Health check
curl -s http://localhost:8202/health | jq .

# Happy path -- create a resource
curl -s -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 9.99}' | jq .

# Verify the response status code
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 9.99}'

# Error case -- missing required field
curl -s -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"price": 9.99}' | jq .

# Error case -- invalid data type
curl -s -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "price": "not-a-number"}' | jq .
```

Record the command, response body, and HTTP status code inline in `delivery.md` under the
implementation notes for the step. If the response is long (> 20 lines), save it to
`evidence/phase-N-<endpoint-slug>.txt` and reference it by path.

## Locale-Aware API Verification

For APIs that serve locale-specific responses (e.g., localized error messages, locale-dependent
formatting), verify each supported locale explicitly:

```bash
# Verify locale-specific response (Accept-Language header or query param)
curl -s -H "Accept-Language: en" http://localhost:8202/api/products | jq .name
curl -s -H "Accept-Language: id" http://localhost:8202/api/products | jq .name
```
