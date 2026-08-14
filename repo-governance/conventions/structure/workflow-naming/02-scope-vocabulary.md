---
title: "Scope Vocabulary"
description: The full list of valid workflow scope tokens, each matching a parent directory under repo-governance/workflows/, and the rule for adding new scopes
when_to_use: Read this when picking or validating the scope token (first segment) of a workflow filename.
category: explanation
subcategory: conventions
tags:
  - workflows
  - naming
  - conventions
created: 2026-04-17
---

# Scope Vocabulary

Workflow scope MUST match its parent directory under `repo-governance/workflows/`. Current scopes:

- **`api`** — Workflows that operate against a live running HTTP API (REST or GraphQL): contract-conformance, auth/authz, pagination, idempotency, and edge-case exploratory testing of a deployed service. Aligned with agent scope `api` (`api-exploratory-tester`).
- **`ayokoding-web`** — Workflows scoped to the AyoKoding Web application (content quality gates).
- **`ci`** — Workflows that diagnose, validate, or repair continuous-integration pipelines.
- **`docs`** — Workflows scoped to the `docs/` tree (Diátaxis content, link integrity, software-engineering separation).
- **`infra`** — Workflows that provision development environments or infrastructure resources.
- **`plan`** — Workflows in the plan lifecycle (authoring quality gate, plan execution).
- **`pr`** — Workflows for the pull-request review lifecycle (maker→fixer review cycles gating the merge for `*-to-pr` delivery modes).
- **`repo`** — Repository-wide governance workflows (conventions, workflows, cross-reference integrity). Aligned with agent scope `repo` (both use `repo`, not `repository`).
- **`content`** — Workflows scoped to content processing and transformation. Acts as a directory grouping for a family of content workflows. Workflows within `content/` use a more specific scope prefix in their filename (e.g., `pdf-to-md`) to communicate the exact sub-scope, since the directory name groups related content workflows rather than naming a single scope.
- **`pdf-to-md`** — Workflows for converting PDF documents to verbatim Markdown and validating conversion fidelity (text completeness, tables, figures, OCR quality). Hosted under the `content/` directory.
- **`specs`** — Workflows scoped to the `specs/` tree (Gherkin features, OpenAPI contracts, C4 diagrams).
- **`ui`** — Workflows scoped to UI component quality (tokens, accessibility, responsive design).
- **`web`** — Workflows that operate against the public web or a live running website: spec-aware exploratory testing, spec-blind heuristic-usability evaluation, and design-aware design-fidelity evaluation of a running site, optionally combined into a fix-planning deliverable. Aligned with agent scope `web` (`web-researcher`, `web-exploratory-tester`, `web-usability-tester`, `web-design-tester`).

New scope tokens MUST be added to this vocabulary first before any workflow is named against them.
