---
title: "Identifier Hygiene, Degraded Mode, and When to Check"
description: Slug-over-ID addressing for Vercel projects and teams, the fallbacks a plan uses when Vercel MCP is absent, and the four moments to re-run the probe.
category: explanation
subcategory: development
tags:
  - vercel
  - mcp
  - verification
created: 2026-08-01
when_to_use: Use when naming a project or team in a committed artifact, planning around an absent Vercel MCP server, or deciding when to re-probe.
---

# Identifier Hygiene, Degraded Mode, and When to Check

## Identifier Hygiene

Address projects and teams by **slug, never by opaque ID**, in every committed artifact — plan
documents, evidence files, commit messages, and specs.

Vercel IDs are identifiers rather than credentials, and grant nothing without a bearer token. They
are still kept out of committed files: they are stable and not practically rotatable, the platform's
own tooling keeps them out of version control, and this ecosystem contains public repositories whose
history is permanent. Slugs are already public — they appear in every deployment hostname — and the
MCP tools accept a slug wherever they accept an ID, so nothing is lost.

Related: **[Secrets and Env Standards](../../../conventions/security/secrets-and-env-standards.md)**.

## Degraded Mode

When the probe says absent, the plan does not stall. Each observation falls back:

| Wanted                          | Fallback                                                                |
| ------------------------------- | ----------------------------------------------------------------------- |
| Deployment state and provenance | The deploy branch's git log, plus the CI run that pushed it             |
| Cache and header behaviour      | An HTTP request against the live URL, recording response headers        |
| Per-route invocation volume     | **No fallback.** Mark the step `[HUMAN]` (dashboard) or drop the claim. |
| Build failure diagnosis         | The CI job log                                                          |

State the degradation in the plan rather than silently weakening an acceptance criterion. A criterion
that quietly becomes unfalsifiable is worse than one openly marked unavailable.

## When to Check

1. **Authoring any plan touching a Vercel-deployed surface** — before the delivery checklist is
   written, since the answer decides executor tags.
2. **Phase 0 of executing such a plan** — before Phase 1, since the checklist already depends on it.
3. **Resuming a plan after a pause** — connection state is session-scoped and does not survive.
4. **When a deployment-observation step fails at execution** — re-probe before assuming the
   deployment itself is broken.
