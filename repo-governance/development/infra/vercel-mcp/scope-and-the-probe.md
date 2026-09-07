---
description: How to decide mechanically whether a plan is in scope for this convention, and how to probe whether Vercel MCP is connected and authenticated.
when_to_use: Use when checking whether a plan's surface makes it in scope, or when running the probe for Vercel MCP connection state.
---

# Scope and the Probe

## Which Projects Are In Scope

Decide mechanically, never from a remembered list — the set drifts, and it is empty in some repos of
this ecosystem. A plan is in scope if **any** of the following holds:

1. A path the plan changes is covered by a `vercel.json`.
2. The plan names a deploy branch (`prod-*`, `stag-*`) that a Vercel project builds from.
3. A deployment agent exists for an app the plan changes.

Enumerate condition 1 directly:

```bash
git ls-files | grep 'vercel\.json$'
```

Empty output means this repository currently has no Vercel-deployed surface, and every plan in it is
out of scope until one is added. That is a legitimate state, not a gap to paper over.

## The Probe

The probe answers one question: **is a Vercel MCP server connected and authenticated right now?**

Three outcomes, each with a different consequence:

| Outcome                         | Consequence                                                                                                                                                            |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Connected and authenticated** | Proceed. Deployment-observation steps are `[AI]`.                                                                                                                      |
| **Present but unauthenticated** | A human authenticates out of band. Until then, treat as absent — an unauthenticated server exposes only its authentication tools.                                      |
| **Absent**                      | Degraded mode (see [Degraded Mode](./identifier-hygiene-degraded-mode-and-when-to-check.md#degraded-mode)). The plan still ships; its verification steps change shape. |

Confirm by listing the configured MCP servers and checking the Vercel entry's state. A server that
reports connected but whose only available tools are authentication tools is **unauthenticated**, not
available — check the tool surface, not just the connection state.
