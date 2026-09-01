---
title: "Standard 6 and 7 — BDD/Contracts Adoption, and Cross-Link Integrity"
description: Adoption expectations for BDD and API contracts by surface profile and per-app rollout status, plus the two-way navigation requirement between app READMEs and specs trees.
when_to_use: Use when checking whether an app should have adopted BDD/API contracts yet, or verifying README-to-specs cross-links are intact.
category: explanation
subcategory: conventions
status: "Pilot — initial issue"
tags:
  - conventions
  - readme
  - specs
  - spec-tree-shape
  - pm-readability
  - c4
created: 2026-05-09
---

# Standard 6 and 7 — BDD/Contracts Adoption, and Cross-Link Integrity

## Standard 6 — BDD/Contracts Adoption (FR-10)

This standard defines adoption expectations per app type and rollout timeline. "SHOULD" means the convention recommends adoption; not adopting is a MEDIUM finding that requires explicit justification. "REQUIRED" means the convention mandates adoption; not adopting is a HIGH finding.

### Adoption matrix by surface profile

| Surface profile | BDD (Gherkin specs) | API Contracts (OpenAPI) |
| --------------- | ------------------- | ----------------------- |
| Full-stack app  | REQUIRED            | REQUIRED                |
| Web-only app    | REQUIRED            | NOT APPLICABLE          |
| CLI app         | REQUIRED            | NOT APPLICABLE          |
| Multi-CLI       | REQUIRED            | NOT APPLICABLE          |

### Rollout adoption mapping

| App            | BDD              | Contracts       |
| -------------- | ---------------- | --------------- |
| `organiclever` | Adopted (pilot)  | Adopted (pilot) |
| `ose`          | SHOULD — backlog | SHOULD          |
| `ayokoding`    | Adopted          | NOT APPLICABLE  |
| `wahidyankf`   | SHOULD — backlog | NOT APPLICABLE  |
| `rhino`        | Adopted          | NOT APPLICABLE  |

### Validation hooks

- **HIGH**: Full-stack or web-only app missing BDD Gherkin specs entirely after one full rollout cycle
- **MEDIUM**: Full-stack app missing API contracts when it exposes a REST API

## Standard 7 — Cross-Link Integrity

App READMEs and their corresponding specs trees maintain two-way navigation:

- The app README `## Behavior and Architecture` section carries a direct link to `specs/apps/<app-family>/README.md`.
- The spec tree `specs/apps/<app-family>/README.md` carries a link back to each app README it covers.
- When a spec file moves (e.g., during flat-root migration), ALL inbound links to that file update in the same commit.

Cross-link violations are CRITICAL findings if a link points to a non-existent file, HIGH findings if a required cross-link is missing.
