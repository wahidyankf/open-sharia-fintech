# Rule 21: Vercel MCP Capability Declaration (Step 5o — CONDITIONAL)

Enforces the
[Vercel MCP Capability Convention](../../../../repo-governance/development/infra/vercel-mcp.md). A
plan touching a Vercel-deployed surface asserts a tool capability when it tags deployment observation
`[AI]`. This checks the assertion was deliberate and stays inside the real boundary — the
capability-shaped sibling of rule 14's executor-tag validation.

**What to validate**:

1. **Trigger detection** — mechanically determine whether the plan touches a Vercel-deployed surface:
   a changed path covered by a `vercel.json` (`git ls-files | grep 'vercel\.json$'`), a named
   `prod-*`/`stag-*` deploy branch, or a deployment agent for an in-scope app. A repository with no
   `vercel.json` at all makes every plan exempt — record the exemption, don't flag.
2. **Availability declared** — a triggered plan's chosen technical form states whether a Vercel MCP
   server is available and what follows. For a directory form, the section lives in its README or a
   companion that README maps. Absent: **MEDIUM**.
3. **No step assumes a capability outside the boundary** — any `[AI]`-tagged step requiring billing/
   usage figures, an invoice, Spend Management, Observability settings, firewall/WAF rulesets, the
   compute-model setting, or domain/DNS configuration: **HIGH** — no tool provides these; the step
   must be `[HUMAN]`. This is the single most common failure of this rule.
4. **Human platform steps consolidated** — a triggered plan should gather `[HUMAN]` dashboard steps
   into Phase 0 rather than scattering across later phases. Scattered without a stated reason:
   **MEDIUM**.
5. **Acceptance commands respect operational limits** — a criterion depending on a query window wider
   than 72 hours, or a grouped query with no explicit result limit, will fail or silently truncate:
   **MEDIUM**. A criterion treating log-event counts as cost evidence: **HIGH** — log events are not
   billed units.
6. **Identifier hygiene** — opaque `team_*`/`prj_*`/`dpl_*` identifiers committed in plan docs or
   evidence: **MEDIUM** (slugs are accepted by the same tools, already public in deployment hostnames,
   safe in a public repo's permanent history).
7. **Phase 0 probe step present** — a triggered plan's Phase 0 includes the availability probe.
   Missing: **MEDIUM**.

**Finding severity**: `[AI]` step requiring billing/settings/firewall/domain config: **HIGH** per
occurrence. Acceptance criterion treating log-event counts as cost evidence: **HIGH**. Missing
availability declaration: **MEDIUM**. Missing Phase 0 probe: **MEDIUM**. Query window over 72h, or
grouped query with no limit: **MEDIUM**. Opaque Vercel IDs committed: **MEDIUM**. Scattered `[HUMAN]`
platform steps with no stated reason: **MEDIUM**. Plan touching no Vercel-deployed surface: not
flagged (exempt).
