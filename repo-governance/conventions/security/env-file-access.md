---
title: "Environment File Access Convention"
description: AI agents must not directly read, write, or edit exactly .env.prod or .env.stag; every other real .env* file is agent-readable. Full policy in secrets-and-env-standards.md.
when_to_use: Use when an AI agent needs to know whether it may directly open a specific .env* file.
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
> [`secrets-and-env-standards.md` § 9](./secrets-and-env-standards/guard-env-file-access-policy.md).

**Summary**: AI agents must not directly read, write, or edit **`.env.prod`** or **`.env.stag`** —
the two restricted-secrets tiers. Every other real `.env*` file (`.env`, `.env.local`, `.env.test`,
etc.) is agent-readable; `.env.example` remains the always-committable template. Commit policy stays
deny-all for every real `.env*` file regardless. Policy identifier: `guard-env-file-access`.
Exceptions: project scripts under `apps/`, `libs/`, and `scripts/`.

**Content-fixture exclusion**: a non-dotfile `<word>.env` (e.g. `kata.env`, `app.env`) under an
app's published content tree — `apps/<app>/content/**` — is curriculum material and is exempt.
Dotfile `.env*` names stay denied even under `content/`, and a `<word>.env` outside a content tree
stays denied. Each repo maintains its own list of excluded content trees; see
[§9 Content-fixture exclusion](./secrets-and-env-standards/content-fixture-exclusion.md).

See: [`secrets-and-env-standards.md`](./secrets-and-env-standards.md)
