# Rules 19-21: Delivery Mode, Learning-Bearing Syllabus, Vercel MCP Capability

## 19. Delivery Mode Validation (Step 5m — MANDATORY)

Enforces
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode):
every plan resolves to exactly one of four modes (`worktree-to-pr` default,
`worktree-to-origin-main`, `main-to-origin-main`, `main-to-pr`) before execution. Sibling to Step 5d
(Worktree Specification) — a worktree is a work location; delivery mode additionally fixes the
integration target and merge authority.

**What to validate**:

1. **Value validity when declared** — a `## Delivery Mode: <value>` declaration must be exactly one
   of the four valid modes; an invalid non-empty value (typo, retired name, free text) is never
   silently coerced to the default — flag it directly.
2. **Absence is not itself a violation** — an unmarked plan resolves to the tier-3 default
   (`worktree-to-pr`); don't flag omission. `plan-maker` always authors the section explicitly (see
   `.claude/agents/plan-maker.md` Step 7) — flag a freshly-authored plan missing it entirely at
   **LOW** (best-practice gap, not correctness defect).
3. **Every PR carries the behavior classifier** — when the resolved mode produces a PR, `delivery.md`
   records the canonical classifier: eligible executable work runs sequential CI-green-gated
   specialist cycles to the earliest clean code M/H/C result within seven; ineligible work requires
   the named `pr-quality-gate.yml` workflow, per the
   [PR Review Quality Gate workflow](../../../../repo-governance/workflows/pr/pr-review-quality-gate.md),
   positioned before the PR-merge step. A `*-to-pr` plan jumping straight from PR creation to merge
   with no review-cycle steps is missing required steps.
4. **Merge tagging matches mode** — for `*-to-pr` modes, the final PR-merge step defaults to `[AI]`; a
   `[HUMAN]` tag IS the plan's opt-in into human merge judgment, per
   [Delivery Mode](../../../../repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode)
   — the tag itself is the complete declaration, with no separate opt-in field to look for. A
   `[HUMAN]`-tagged merge step under `*-to-pr` is NEVER a defect and MUST NOT be flagged or retagged;
   the only defect is an invalid tag value. For `*-to-origin-main` modes, the final push MUST be
   `[AI]` (never gated behind an unrequested `[HUMAN]` approval — see the PR Step Authorization Check
   in `reference/02-delivery-checklist-and-pr-authorization.md`; its "unsolicited PR step" framing
   applies only to `*-to-origin-main`-mode plans, since a PR step is expected under `*-to-pr` modes).
5. **"Done" is not "merged"** — a `*-to-pr` plan's completion/Gate criteria must not require the PR to
   actually be merged; a green, fully-reviewed PR awaiting merge is a valid done state. Flag
   conflation.
6. **Archival-in-PR present** — for `*-to-pr` modes (plan folder tracked in-repo), the checklist
   includes an archival step (`git mv` to `plans/done/`, README/index updates) committed **inside the
   delivering PR**, not deferred to a follow-up commit/PR. Missing or deferred archival: flag it. N/A
   for repos where the plan folder isn't tracked (see the
   [PR Review Quality Gate workflow](../../../../repo-governance/workflows/pr/pr-review-quality-gate.md)'s
   three-repo nuance).
7. **Phase 0 carries no PR/push/review/merge step** — run the Phase 0 detection command from
   `reference/02-delivery-checklist-and-pr-authorization.md` and confirm it returns `0`, under every
   mode including direct-push ones. An unscoped Per-Phase Integration Protocol block is the same
   defect stated once instead of per-phase — flag it too.
8. **PR steps appear only in declared delivery boundaries** — run the two detection commands from
   `reference/02-delivery-checklist-and-pr-authorization.md` and confirm integration-step phases are a
   subset of `### Delivery Boundaries`; confirm every change-producing phase appears in exactly one
   table row and the last change-producing phase is a boundary.
9. **Per-repository delivery mode restriction** (enforces
   [Per-Repository Delivery Mode Restrictions](../../../../repo-governance/conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule))
   — determine the repository (`git remote get-url origin` or `repo-config.yml`); check the resolved
   mode against it:
   - **`ose-public`, `ose-primer`**: `worktree-to-origin-main` or `main-to-origin-main` resolved:
     **HIGH** — `main` is branch-protected against direct pushes, including for admins, so these
     modes have no executable path.
   - **`ose-private`**: same modes resolved: **HIGH**, unless the plan is genuinely
     infrastructure-as-code (BRD/PRD or folder scope it to Terraform, Ansible, or equivalent
     state-changing infra work needing the primary checkout's real credentials/state) — read the
     plan's stated scope, don't rely on a bare self-declared label.

**Finding severity**: invalid non-empty value: **HIGH**. `*-to-pr` mode missing PR-Review
Maker→Fixer Cycle steps before merge: **HIGH**. Merge step tagged with anything other than `[AI]`,
`[HUMAN]`, `[AI+HUMAN]`: **HIGH** (a `[HUMAN]` merge step is always valid, never itself a finding).
Completion criteria conflating "done"/"merged" on `*-to-pr`: **MEDIUM**. Missing or post-merge-deferred
archival-in-PR on an applicable `*-to-pr` plan: **HIGH**. Freshly-authored plan missing the Delivery
Mode declaration entirely: **LOW**. Any PR/push/review/merge/CI-verification step inside Phase 0 (any
mode): **HIGH**. Per-Phase Integration Protocol block not scoped to Phase 1 onward: **HIGH**.
PR-creation/review-cycle/merge/CI-verification step in a non-boundary phase: **HIGH**.
Change-producing phase absent from `### Delivery Boundaries`: **HIGH**. Non-boundary final
change-producing phase: **HIGH**. Missing `### Delivery Boundaries` table on a non-trivial plan:
**MEDIUM**. Single end-of-plan boundary on a plan declaring independent parallel nodes: **MEDIUM**.
Resolved `worktree-to-origin-main`/`main-to-origin-main` in `ose-public`/`ose-primer`: **HIGH**. Same
in `ose-private` on a non-infra plan: **HIGH**.

## 20. Learning-Bearing Syllabus Completeness (Step 5n — CONDITIONAL)

Enforces the
[Learning-Plan `syllabus/` Folder Convention](../../../../repo-governance/conventions/structure/learning-plan-syllabus.md)
— the learning-side sibling of the UI-design-funnel Step 5k. A plan is learning-bearing when its
delivery checklist authors or restructures course, tutorial, or curriculum content; merely citing,
linking to, or lightly correcting an existing corpus does not trigger it.

**What to validate**:

1. **Scope detection** — determine learning-bearing status from Scope, file-impact, and delivery
   steps; if not learning-bearing, skip (confirm the exemption is recorded explicitly).
2. **Required folder layout** — `syllabus/README.md`, `syllabus/courses/` (with its own `README.md`
   for a new corpus), `syllabus/paths/` (with its own `README.md` for a new corpus). Missing
   `syllabus/README.md`: **HIGH**. Missing a required subfolder README for a new corpus: **HIGH**
   (grandfathered pre-existing corpus lacking it is exempt — see the convention's Grandfathered Format
   Cohort section).
3. **Template-derived per-course shape** — every new course file carries the REQUIRED skeleton
   (`**Course ID**`, `## Why this exists`, `## Prerequisites`, `## Accuracy notes`, `**Scope note**`,
   `## Concepts`, `## In which paths`), with the capstone carve-out honored. Missing a REQUIRED
   section: **HIGH**.
4. **`## Corpus Disposition` declaration (owning plan only)** — the owning (custodian) plan's
   `tech-docs.md` carries a `## Corpus Disposition` section with exactly one of `archive-with-plan` or
   `promote-to:<path>`. A pure consumer plan never carries this section. Missing, or invalid value on
   an owning plan: **HIGH**.
5. **Custodian line and consumer echo** — the corpus's `syllabus/README.md` carries a
   `**Custodian**: <plan-id>` line, echoed in every consumer plan's `tech-docs.md` under its own
   `## Corpus Custody` heading as `custodied-by:<plan-id>` (distinct from item 4). Missing either:
   **HIGH**.
6. **Delivery steps produce the artefacts** — `delivery.md` carries explicit steps scaffolding the
   layout, authoring the course files, and declaring disposition/custodian — not merely assuming they
   appear. Declared artefact with no corresponding step: **HIGH**.
7. **Exemption** — plans that only read/link/lightly correct an existing corpus are EXEMPT. Verify
   legitimacy; illegitimate exemption on a genuinely learning-bearing plan: **HIGH**.

**Finding severity**: missing `syllabus/README.md`/`courses/`/`paths/` (or a new corpus's subfolder
README): **HIGH**. New course file missing a REQUIRED section: **HIGH**. Missing/invalid `## Corpus
Disposition`: **HIGH**. Missing Custodian line or `## Corpus Custody` echo: **HIGH**. Declared
artefact with no delivery step: **HIGH**. Illegitimate "not learning-bearing" exemption: **HIGH**.
Non-learning-bearing plan: not flagged (record the exemption explicitly).

## 21. Vercel MCP Capability Declaration (Step 5o — CONDITIONAL)

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
2. **Availability declared** — a triggered plan's `tech-docs.md` states whether a Vercel MCP server is
   available and what follows. Absent: **MEDIUM** (an executor can't tell an assumed capability from
   an overlooked one).
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
