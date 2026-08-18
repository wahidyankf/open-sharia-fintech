---
title: "Mandatory Test Levels Matrix"
description: "Mandatory levels per project type."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-03-13
when_to_use: "Use to check required test levels for a project type."
---

# Mandatory Test Levels Matrix

The table below states which test levels are mandatory per app type:

| App Type                         | test:unit | test:integration                 | test:e2e               |
| -------------------------------- | --------- | -------------------------------- | ---------------------- |
| API backends                     | Mandatory | Mandatory (real PostgreSQL)      | Mandatory (Playwright) |
| CLI apps                         | Mandatory | Mandatory (real filesystem)      | N/A                    |
| Product app-web (app-tier)       | Mandatory | Mandatory (MSW / mocked backend) | Mandatory (Playwright) |
| Content platforms & marketing FE | Mandatory | N/A (no-op `echo`)               | Mandatory (Playwright) |
| Libraries                        | Mandatory | Optional                         | N/A                    |
| E2E runners                      | N/A       | N/A                              | Mandatory              |

**The integration tier is for app-tier products that cross a real integration boundary** — API
backends (real PostgreSQL), CLI apps (real filesystem), and **product app-web clients** (`*-app-web`,
e.g. `organiclever-app-web`, `ose-app-web`) that integrate with a real backend API (mocked in-process
via MSW). **Content platforms and marketing front-ends** (`*-www`, e.g. `ayokoding-www`, `ose-www`,
`organiclever-www`, `wahidyankf-www`) have **no integration tier**: their `test:integration` target is a
no-op `echo`, and their full Gherkin contract is consumed at the **unit** tier (all external
dependencies mocked) plus the **e2e** tier. A site that renders content and calls a typed tRPC layer
does not integrate a separate backend service, so a middle tier would only duplicate unit coverage.
