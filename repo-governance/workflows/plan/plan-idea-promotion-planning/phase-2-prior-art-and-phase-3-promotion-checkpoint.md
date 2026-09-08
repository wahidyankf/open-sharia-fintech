---
description: Delegating a fanned-out web-researcher prior-art survey, then presenting findings inline and getting explicit user approval to promote.
when_to_use: Use when running the deferred deep research pass, or confirming go/no-go before authoring the backlog plan.
---

# Phase 2 — Deep Prior-Art Study, and Phase 3 — Promotion Checkpoint

## 2. Deep Prior-Art Study (Parallel, delegated)

Run the deep prior-art survey the capture phase deferred (per the
[Prior art discipline](../../../conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#ideas-folder-two-pagers): "the deep
`web-researcher` prior-art study is deferred to promotion"). The two-pager's own _Prior art_ section
is the lightweight starting point; now the full plan can afford real research.

Delegate to `web-researcher` — the [default primitive for public-web information gathering](../../../conventions/writing/web-research-delegation.md).
Fan out **by research angle**, not one agent per link, under the **N+1 model** — `1 main thread + N
background agents = N+1 total`, default **N=3** — per the
[Subagent Orchestration Convention](../../../development/agents/subagent-orchestration.md). Angles are
independent DAG nodes (none reads another's output), so the number of angles is the fan-out and N
only caps it. Typical angles:

- **Precedents & patterns** — who has solved this before (named tools, libraries, prior in-repo plans)
  and how; where each falls short for this context.
- **Standards & specifications** — any formal standard, RFC, or convention the idea should conform to
  or deliberately diverge from.
- **Existing solutions & alternatives** — buy-vs-build options, their trade-offs, and licensing.

Each finding must carry a **verified** source (fetched, dated) or be cited name-only when no stable
URL exists — never a fabricated link, inheriting the repo's anti-fabrication rule.

Write the survey progressively to
`local-tmp/plan-idea-promotion-planning/plan-idea-promotion-planning__<uuid>__<YYYY-MM-DD--HH-MM>__report.md`
(the `prior-art-report` output) per the [Temporary Files convention](../../../development/infra/temporary-files.md).

**Agent**: `web-researcher` (one invocation per angle).

**Output**: `prior-art-report` written — the design input Phase 4 folds into the plan.

## 3. Promotion Checkpoint (Sequential, Hard Gate)

Present, inline: the ripeness confirmation, a digest of the `prior-art-report`, and the two-pager's
own open questions. Then use `AskUserQuestion` (options-first, per the
[Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md)) to:

1. Confirm the `plan-identifier` (default `<slug>`).
2. Confirm the plan's technical shape: one `tech-docs.md` or a mapped `tech-docs/` directory,
   selected by reader jobs and cohesion. The mature core itself is fixed.
3. Confirm the `push-target`.
4. **Explicitly approve** promoting this brief to a backlog plan now.

The deep design grilling — resolving the open questions into concrete plan requirements — is **not**
run here; it is left to `plan-planning`'s own grill in Phase 4, seeded by the handoff, so the user is
grilled once, not twice.

**Do NOT proceed to Phase 4** until the user approves. The user may defer (keep it as a two-pager) or
trim scope here.

**Output**: Confirmed identifier, structure, push target, and an explicit go.
