---
title: "Vercel MCP Capability Convention"
description: The Vercel MCP server is an assumed capability for plans touching a Vercel-deployed surface, probed at planning time and again at execution Phase 0
category: explanation
subcategory: development
tags:
  - vercel
  - mcp
  - deployment
  - planning
  - verification
created: 2026-08-01
---

# Vercel MCP Capability Convention

An MCP server for Vercel is **assumed available** to any plan whose surface includes a
Vercel-deployed project. Deployment state, runtime invocation counts, build logs, and deploy
provenance are therefore agent-readable, and steps that read them are tagged `[AI]` rather than
`[HUMAN]`.

The assumption is load-bearing, so it is **probed, never presumed** — once while planning, and again
at execution Phase 0 before any step depends on it.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: a
  plan that tags a deployment-verification step `[AI]` is asserting a capability. The assertion is
  written down and checked, not assumed from the fact that a previous plan managed it.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: the
  probe is cheap and runs before the work is shaped around its answer, rather than after an executor
  discovers mid-phase that a step it planned cannot be performed.

## Conventions Implemented/Respected

- **[Vercel Deployment Convention](./vercel-deployment.md)**: defines which projects deploy through
  Vercel and how their builds are configured. This convention governs what an agent may **observe**
  about those deployments; that one governs how they are **built**.
- **[Manual Behavioral Verification](../quality/manual-behavioral-verification.md)**: the same
  shape — a capability an agent uses to verify real running behavior instead of asserting from
  source.
- **[Plans Organization Convention](../../conventions/structure/plans.md)**: supplies the
  `[AI]` / `[HUMAN]` executor tags this convention shifts between.

## The Core Rule

**If a plan touches a Vercel-deployed surface, it MUST resolve Vercel MCP availability at both
gates, and record the answer.**

| Gate                                                   | Who         | What it decides                                                              |
| ------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------- |
| **Planning** — before authoring the delivery checklist | plan author | whether deployment-verification steps are written `[AI]` or `[HUMAN]`        |
| **Execution** — Phase 0, before Phase 1 starts         | executor    | whether the checklist's `[AI]` assumption still holds, or must be downgraded |

A plan that touches no Vercel-deployed surface is **out of scope** — it neither probes nor records
anything. Do not add a vacuous check to plans that cannot use the answer.

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

| Outcome                         | Consequence                                                                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Connected and authenticated** | Proceed. Deployment-observation steps are `[AI]`.                                                                                 |
| **Present but unauthenticated** | A human authenticates out of band. Until then, treat as absent — an unauthenticated server exposes only its authentication tools. |
| **Absent**                      | Degraded mode (below). The plan still ships; its verification steps change shape.                                                 |

Confirm by listing the configured MCP servers and checking the Vercel entry's state. A server that
reports connected but whose only available tools are authentication tools is **unauthenticated**, not
available — check the tool surface, not just the connection state.

## Capability Boundary

This boundary is the point of the convention. A plan that assumes more than this will write `[AI]`
steps no agent can execute.

**Available** — read and deploy:

- Project and team enumeration; deployment listing, state, and git provenance.
- Runtime logs, including counts grouped by source, route, status code, and deployment — the basis
  for per-project and per-route invocation measurement.
- Build logs and runtime errors.
- Triggering a deployment.
- Deployment-protection settings.

**Not available** — every one of these stays `[HUMAN]`:

- Billing, usage figures, line items, invoices, and any currency value.
- Spend Management.
- Observability settings, including enabling or disabling paid tiers.
- Firewall and WAF managed rulesets.
- The compute-model setting (an agent cannot even read whether it is enabled).
- Domain and DNS configuration, including redirect behavior.

**The consequence for cost, security, and platform-settings plans**: their dashboard steps do not
become `[AI]` merely because a Vercel MCP is connected. Group every such step into Phase 0 so the
human actions happen in a single sitting, and keep the rest of the plan `[AI]`.

## Operational Limits

Verified against a live project, 2026-08-01. Plans that write acceptance commands must respect these
or the commands fail at execution:

- **Query window**: a 72-hour lookback returns; a 7-day lookback times out. Treat 72h as the widest
  usable window, and never write an acceptance criterion that depends on a longer one.
- **Truncation is silent-ish**: grouped queries return the top _N_ with only a footer saying so.
  Always pass an explicit result limit, or rows vanish without an error.
- **Log events are not billed units.** Counts prove volume and attribution. They never prove cost.
  A plan whose objective is a monetary figure cannot be graded from them.
- **Web Analytics is a separate product** and is not enabled by default. Do not plan around it; a
  query against a project without it fails outright.

## Identifier Hygiene

Address projects and teams by **slug, never by opaque ID**, in every committed artifact — plan
documents, evidence files, commit messages, and specs.

Vercel IDs are identifiers rather than credentials, and grant nothing without a bearer token. They
are still kept out of committed files: they are stable and not practically rotatable, the platform's
own tooling keeps them out of version control, and this ecosystem contains public repositories whose
history is permanent. Slugs are already public — they appear in every deployment hostname — and the
MCP tools accept a slug wherever they accept an ID, so nothing is lost.

Related: **[Secrets and Env Standards](../../conventions/security/secrets-and-env-standards.md)**.

## Degraded Mode

When the probe says absent, the plan does not stall. Each observation falls back:

| Wanted                          | Fallback                                                                |
| ------------------------------- | ----------------------------------------------------------------------- |
| Deployment state and provenance | The deploy branch's git log, plus the CI run that pushed it             |
| Cache and header behavior       | An HTTP request against the live URL, recording response headers        |
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

## Examples

### PASS: a plan that measures its own effect

A plan converting server-rendered pages to static declares in `tech-docs.md` that a Vercel MCP is
available, and its delivery checklist carries an `[AI]` post-deploy step: re-query runtime log counts
grouped by source and route 24 hours after deploying, and require the function-source count to fall
by at least 90% against a baseline captured at Phase 0. The criterion is falsifiable in both
directions and needs no human.

### PASS: a repository with no Vercel surface

`git ls-files | grep 'vercel\.json$'` returns nothing. The plan states that the repository has no
Vercel-deployed surface and skips both gates. Nothing further is required.

### FAIL: assuming the boundary is wider than it is

A cost-reduction plan tags "read the completed cycle's invoice total" as `[AI]` because a Vercel MCP
is connected. No billing tool exists; the step cannot execute, and it is discovered only when the
executor reaches it. The step belonged in Phase 0 as `[HUMAN]`.

### FAIL: an unrecorded probe

A plan's author probes, finds the server available, and writes `[AI]` deployment steps without
recording the dependency anywhere. A later executor in a session without the server sees `[AI]` tags,
cannot perform them, and has no statement to check against.

## Validation

- `plan-checker` verifies that a plan touching a Vercel-deployed surface states its Vercel MCP
  dependency and that no step assumes a capability outside the boundary above.
- `plan-execution-checker` verifies that Phase 0 recorded the probe outcome.
- `repo-setup-manager` performs the Phase 0 probe and records it.

## References

**Related Development Standards:**

- [Vercel Deployment Convention](./vercel-deployment.md) - How Vercel builds are configured
- [Manual Behavioral Verification](../quality/manual-behavioral-verification.md) - Verifying real
  running behavior rather than asserting from source
- [CI Post-Push Verification](../workflow/ci-post-push-verification.md) - The CI-side counterpart

**Related Workflows:**

- [Plan Planning](../../workflows/plan/plan-planning.md) - Where the planning-time gate binds
- [Plan Execution](../../workflows/plan/plan-execution.md) - Where the Phase 0 gate binds

**Agents:**

- `plan-maker` - Probes while authoring and records the result
- `repo-setup-manager` - Probes at Phase 0
- `plan-checker`, `plan-execution-checker` - Validate that both happened

## Platform Binding Examples

The content under this heading is intentionally vendor-specific and is skipped by the vendor-audit
scanner.

Listing configured MCP servers and their connection state:

```binding-example
claude mcp list
```

A connected, authenticated Vercel entry appears as a URL-backed HTTP server with a healthy state; an
unauthenticated one is reported as needing authentication. Authentication is interactive and belongs
to a human: `/mcp`, then select the Vercel server.

Representative tool names on the current server: `list_projects`, `list_deployments`,
`get_deployment`, `get_deployment_build_logs`, `get_runtime_logs`, `get_runtime_errors`,
`deploy_to_vercel`, `search_vercel_documentation`. The absence of any billing, firewall, or
domain-configuration tool is what the Capability Boundary section above describes.
