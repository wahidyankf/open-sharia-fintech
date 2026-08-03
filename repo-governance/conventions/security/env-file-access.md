---
title: "Environment File Access Convention"
description: AI agents must not directly read, write, edit, or commit any .env* file except .env.example. Full policy in secrets-and-env-standards.md.
category: explanation
subcategory: conventions
tags:
  - security
  - env-files
  - agents
  - guard-env-file-access
created: 2026-05-24
---

# Environment File Access Convention

> **Stub.** The full `guard-env-file-access` policy lives in
> [`secrets-and-env-standards.md` § 9](./secrets-and-env-standards.md#9-guard-env-file-access-policy).

**Summary**: AI agents must not directly read, write, edit, or commit any `.env*` file except
`.env.example`. Policy identifier: `guard-env-file-access`. Exceptions: project scripts under
`apps/`, `libs/`, and `scripts/`.

**Content-fixture exclusion**: a non-dotfile `<word>.env` (e.g. `kata.env`, `app.env`) under an
app's published content tree — `apps/<app>/content/**` — is curriculum material and is exempt.
Dotfile `.env*` names stay denied even under `content/`, and a `<word>.env` outside a content tree
stays denied. Each repo maintains its own list of excluded content trees; see
[§9 Content-fixture exclusion](./secrets-and-env-standards.md#content-fixture-exclusion).

See: [`secrets-and-env-standards.md`](./secrets-and-env-standards.md)
