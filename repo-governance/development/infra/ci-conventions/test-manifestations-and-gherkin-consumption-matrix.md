---
title: "Project-Role Testing and Gherkin Matrix"
description: "Applicable Gherkin adapters by project role and real boundary"
category: explanation
subcategory: development
tags: [ci-cd, testing, gherkin]
created: 2026-03-31
when_to_use: "Use when deciding which adapters and targets a project owns."
---

# Project-Role Testing and Gherkin Matrix

| Project role          | Unit                                  | Integration                                    | E2E                                                               |
| --------------------- | ------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| Application           | Required against the canonical corpus | Required only for an owned real local boundary | Implemented by a dedicated project for an exposed public boundary |
| Library               | Required                              | Required only for an owned real local boundary | Never library-owned; prove through a consuming application        |
| Executable tool       | Required                              | Required for owned local resources             | Required for a public process boundary                            |
| Dedicated E2E project | Owner's responsibility                | Owner's responsibility                         | Required against the owner's corpus                               |

All applicable adapters consume the same recursively discovered `behaviours/` corpus. Unit has no
exemption. A higher-layer scenario requires implementation or a valid boundary-mismatch exemption;
both Integration and E2E exemptions may annotate one scenario and are reviewed independently.
Inapplicable layers are documented and omitted rather than represented by no-op targets.
