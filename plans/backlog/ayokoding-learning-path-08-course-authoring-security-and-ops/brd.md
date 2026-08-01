# Business Requirements — Learning Path Course Authoring: Security, Ops & Delivery (Band 7)

## Business Goal

Fill the shared course library with the **eleven course bodies** Band 7 owns, so that the three
`careers/software-engineer`-role paths (`interview-ready`, `immediately-effective`,
`fundamentally-strong`) can each grow their manifest to include a complete security-and-operations
tier, and so that Band 8's five security/ops-dependent capstones
(`capstone-secure-service`, `capstone-build-your-own-pentest-engine`, `capstone-real-world-delivery`,
`capstone-concurrency-and-systems`, `capstone-lead-at-altitude`) have their prerequisite bodies to
assemble. `capstone-data-pipeline` is **not** in this list — Band 8's own per-capstone dependency
audit found its prerequisites are entirely SQL/data-engineering/AI-powered-apps, no Band-7 topic. A path manifest is an ordered
list of course IDs; an ID with no resolving body is an integrity failure, not a path. **This plan is
the one that gives the security/ops/quality/delivery tier of the curriculum something to compose.**

Concretely it authors:

- **`it-and-application-security`** — CIA, STRIDE, OWASP, crypto, identity (Annotated-concept).
- **`offensive-security`** — recon, scanning, exploitation, lab-local only (By Example).
- **`defensive-security`** — hands-on generalist blue-team: Sigma-on-ELK/OpenSearch, the IR lifecycle,
  hardening (By Example, **re-labelled hands-on, not concept-level** — DL-9/DD-12).
- **`detection-engineering-and-siem-operations`** — the Wazuh-specific deep tier: decoders,
  correlation-rule authoring, false-positive tuning, dashboards (By Example, **net-new** — the only one
  of these eleven with no legacy or FS-SE-transferred home).
- **`vulnerability-management-and-assessment`** — scanning, triage, remediation at scale, SBOM (By
  Example).
- **`it-governance-grc`** — governance, risk, compliance, audit (Annotated-concept).
- **`bare-metal-virtualization`** — Proxmox and hypervisors, the full-depth sibling of
  `self-hosting-essentials` (By Example).
- **`self-managed-kubernetes-and-gitops`** — self-owned production Kubernetes plus GitOps (By
  Example).
- **`platform-engineering-and-devex`** — internal platforms, golden paths (Annotated-concept).
- **`site-reliability-engineering`** — SLOs, observability, incident response (Annotated-concept).
- **`analytics-and-experimentation`** — metrics and A/B testing (By Example).

The business change here is **content**, not architecture: no schema, no route, no component, no
redirect, and — by binding invariant, inherited from plan 04 — **no manifest**.

## Why this band was carved out of plan 04 rather than authored in place

Plan 04 **originally** authored 90 course bodies across nine bands plus a six-course AI-engineering
phase, inside one delivery checklist. That scope was large enough that delivering it as one
continuously-running plan risked a long-lived, hard-to-audit in-progress state, so plan 04 was split:
its terminal scope is now Band 1 + Band 2 + Phase 1 (21 bodies), and the other bands are carved into
seven sibling plans, `05`-`11` (see plan 04's own
[Successor plans table](../../in-progress/ayokoding-learning-path-04-course-authoring/README.md#successor-plans)).
Band 7 is a coherent, self-contained unit — eleven course bodies whose only shared dependency on the
rest of the split family is a handful of already-existing prerequisite course IDs: `containers-and-orchestration`
and `cicd-and-release-engineering`, authored natively in plan 04's own current Band 2;
`security-essentials`, `networking-essentials`, and `sql-essentials`, re-homed by
`ayokoding-learning-path-01-url-restructure`; and `system-design`, authored by
`ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`. Carving it into its own plan
lets it be delivered, reviewed, and archived on its own schedule, independently of whichever other
plans in the split family are still open — while plan 04's own hard `blockedBy` on this plan's
completion ensures Band 7 is authored exactly once.

## Why the bodies must be authored, not generated ad hoc

The naive alternative is to let this pass make its own judgment calls about scope, concept coverage,
worked-example volume, and prerequisite edges. That fails in the same specific, expensive way plan 04
already identified for its own 90 bodies [Judgment call]:

- **Concept coverage drifts.** Each of these eleven courses already has a settled spec file with an
  enumerated `co-NN` concept list and an `ex-NN` worked-example inventory. Authoring "from a fresh
  judgment call" silently drops concepts nobody notices are missing until a reader hits the gap.
- **Prerequisite edges get invented.** A body that declares a prerequisite the spec never named adds an
  edge to the library's DAG. The DAG stops being topologically consistent — and that failure does
  **not** surface here. It surfaces much later, in `ayokoding-learning-path-12-careers-se-manifests`, as a
  manifest-integrity failure with no traceable link back to the authoring decision that caused it.
- **The band's own reconciliation ruling collapses.** `defensive-security` and
  `detection-engineering-and-siem-operations` were reconciled by plan 04's DL-9/DD-12 specifically to
  prevent one course silently re-teaching the other's material. Authoring `defensive-security`'s
  hands-on scope or `detection-engineering-and-siem-operations`'s deep-Wazuh scope from a fresh
  judgment call — rather than the locked reconciliation — reopens exactly the overlap the ruling closed.

Authoring **from** the settled `syllabus/courses/<course-id>.md` spec removes all three failure modes
at their root, exactly as it did for plan 04.

## Business Impact

**Pain points addressed**:

- Without this plan, none of the three `careers/software-engineer` paths has a security-and-operations
  tier — a reader following any of the three paths has no course teaching CIA/STRIDE/OWASP fundamentals,
  offensive or defensive security technique, deep SIEM operations, vulnerability management, IT
  governance, bare-metal virtualization, self-managed Kubernetes/GitOps, platform engineering, SRE
  practice, or classical product analytics.
- Band 8's `capstone-secure-service` (which assembles `it-and-application-security`,
  `offensive-security`, and `defensive-security` among its prerequisites), `capstone-build-your-own-pentest-engine`
  (which assembles `offensive-security` and `detection-engineering-and-siem-operations`),
  `capstone-real-world-delivery` and `capstone-concurrency-and-systems` (both of which assemble
  `defensive-security`/`site-reliability-engineering`), and `capstone-lead-at-altitude` (which assembles
  `site-reliability-engineering`) have **no** prerequisite bodies to build from until this band lands —
  a real blocking dependency, not a convenience ordering.
- The catalog's original mislabeling of `defensive-security` as "concept-level" material, when it is
  actually hands-on By-Example, would ship uncorrected without this plan re-authoring the body per the
  DL-9/DD-12 reconciliation.
- Landing eleven new always-served content pages onto a site whose function-duration billing is already
  overrun (see `vercel-function-cost-reduction`) would make an existing cost problem worse rather than
  better — hence that plan's hard `blockedBy` status here.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- **One authoring investment, three converging paths.** Each of the eleven bodies is authored once,
  path-neutral, at one canonical URL. All three `careers/software-engineer` manifests reference the
  same bodies once `ayokoding-learning-path-12-careers-se-manifests` grows them in.
- **A curriculum that can be audited.** Because every body traces to a settled spec, "is this course
  complete?" is answerable by comparing the body against its `co-NN`/`ex-NN` enumeration, rather than by
  a reviewer's impression.
- **The distinctness contract is applied by construction.** `defensive-security` and
  `detection-engineering-and-siem-operations` are authored together, in the same delivery cohort, so
  the scope-boundary lines each body must state are written against the other body's actual, current
  text — not retrofitted after the fact.
- **A bounded delivery unit.** Eleven bodies fit one reviewable terminal PR, rather than waiting on
  the rest of the split family's other plans (`05`-`07`, `09`-`11`).

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns the `defensive-security` / `detection-engineering-and-siem-operations`
  scope boundary and the two-altitude boundaries this band restates
  (`bare-metal-virtualization` ↔ `self-hosting-essentials`;
  `analytics-and-experimentation` ↔ `statistics-for-evaluation`).
- **Content author** (via the `apps-ayokoding-www-*-maker` agents) — writes the eleven bodies.
- **Content reviewer** (via the `apps-ayokoding-www-*-checker` plus facts and link checkers) —
  validates every body before its PR merges.

Consuming agents [Repo-grounded]: `apps-ayokoding-www-by-example-maker`,
`apps-ayokoding-www-annotated-concept-maker`, and their matching checkers, plus
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`, and `web-researcher` for the
accuracy pre-verification pass.

**Roles explicitly NOT worn by this plan**: frontend engineer (owned by
`ayokoding-learning-path-03-navigation-ui`), data/schema author (owned by
`ayokoding-learning-path-02-schema-and-prerequisite-dag`), path composer (owned by
`ayokoding-learning-path-12-careers-se-manifests`), IA/URL owner (owned by
`ayokoding-learning-path-01-url-restructure`), any other band of the course-authoring split family
(owned by the respective successor plan `05`-`11`; plan 04 itself now owns only Band 1 + Band 2 +
Phase 1).

## Business-Level Success Metrics

Each metric below is an **observable check**, not a projected number.

- **Eleven authored bodies exist** (observable): every slug listed in
  `evidence/authored-body-slugs.txt` resolves to a directory under `<COURSES>`. Falsifiable in both
  directions — before Phase 1 all eleven are absent; after Phase 2 none is.
- **Every body traces to its spec** (observable): each authored course's scope, concept coverage, and
  declared prerequisites match the `co-NN` / `ex-NN` / prerequisite-chain enumeration in its
  `syllabus/courses/<course-id>.md` spec. Verified per-course by its checker pass.
- **Every body declares `prerequisites`** (observable): each `_index.md` carries a
  `prerequisites: [course-id, ...]` list in the contracted shape.
- **Every body passes its content checkers** (observable): zero CRITICAL / HIGH / MEDIUM findings from
  the matching learning checker, `apps-ayokoding-www-facts-checker`, and `apps-ayokoding-www-link-checker`.
- **The DL-9/DD-12 distinctness contract holds** (observable): `defensive-security` states its hands-on,
  generalist Sigma/ELK-and-IR-and-hardening scope; `detection-engineering-and-siem-operations` declares
  `defensive-security` a prerequisite and states its deep-Wazuh scope; no lesson title is duplicated
  across the two courses' syllabi.
- **Both two-altitude boundaries are stated** (observable): `bare-metal-virtualization` names
  `self-hosting-essentials`; `analytics-and-experimentation` names `statistics-for-evaluation`.
- **`offensive-security` states its rules of engagement** (observable): its `overview.md` names both
  "authorized" and "lab" scope language.
- **No manifest file changed in this plan's commits** (observable): the plan's own diff across all
  merged PRs touches zero paths under `<MANIFESTS>`.
- **The band emitted one complete signal** (observable): the single five-field band-completion signal
  names all three `software-engineer` manifests by full path and carries a resolvable merge commit SHA.
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; markdownlint, link
  validation, and heading-hierarchy validation pass across the authored tree.

## Business-Scope Non-Goals

- **Editing any manifest file.** Binding invariant — owned by `ayokoding-learning-path-12-careers-se-manifests`.
- **Building any part of the navigation UI.** Owned by `ayokoding-learning-path-03-navigation-ui`.
- **Authoring any other band of the split family, or plan 04's own remaining scope (Band 1, Band 2,
  Phase 1 AI-engineering).** Those are owned by the respective successor plans (`05`-`07`, `09`-`11`)
  or by plan 04 itself; this plan owns Band 7 only.
- **Re-homing any shipped topic or existing capstone.** None of this band's eleven bodies is a re-home —
  ten are FS-SE-transferred topics authored native, one
  (`detection-engineering-and-siem-operations`) is net-new.
- **Defining the `prerequisites` frontmatter contract.** This plan **consumes** the contract;
  `ayokoding-learning-path-02-schema-and-prerequisite-dag` owns its canonical shape.
- **Adding an Indonesian mirror of the course content.** Deferred, recorded as a decision rather than an
  omission. Every course body in this plan is `en`-only.
- **Rewriting the pedagogy or depth of any of the ten transferred topics.** They are authored native from
  their settled specs; they are not re-conceived.
- **Enumerating speculative course variants.** A distinct-pedagogy variant is authored on demand only,
  never pre-enumerated (DD-8, plan 04's decision, inherited).
- **Fixing `apps/ayokoding-www`'s Vercel function-cost problem itself.** That is
  `vercel-function-cost-reduction`'s own scope; this plan only waits on its completion as a hard
  precondition.

## Business Risks and Mitigations

| Risk                                                                                                                                                                                                         | Mitigation                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A body is authored from a fresh judgment call instead of its settled spec, so concept coverage drifts.                                                                                                       | Every authoring step names the exact cross-plan `syllabus/courses/<course-id>.md` path and makes "authored from that spec" an explicit acceptance criterion; the checker pass compares the body against the spec's `co-NN`/`ex-NN` enumeration.                   |
| Band 7 is authored twice — once here, once if plan 04's own trim did not land cleanly.                                                                                                                       | Phase 0 checks that none of the eleven Band-7 slugs already exists under `<COURSES>` before authoring begins, exactly mirroring plan 04's own 29-new-slug collision check.                                                                                        |
| A step in this plan mutates a manifest, making the split unschedulable.                                                                                                                                      | The manifest ownership invariant is stated in `README.md`, `tech-docs.md`, and `delivery.md`; the handoff is a five-field band-completion signal; a phase gate asserts the plan's diff touches zero paths under `<MANIFESTS>`.                                    |
| `defensive-security` and `detection-engineering-and-siem-operations` overlap, reopening the reconciliation plan 04 already closed.                                                                           | Both are authored in the same prerequisite-oriented phase on the persistent final-delivery branch; the prerequisite declaration and the duplicate-lesson-title check are explicit per-course acceptance criteria, not a downstream discovery.                     |
| Landing eleven more always-dynamic content pages compounds the ayokoding-www function-duration cost overrun `vercel-function-cost-reduction` is fixing.                                                      | `vercel-function-cost-reduction` is a hard `blockedBy` precondition, checked concretely in Phase 0 against that plan's actual Phase 1 (`app/layout.tsx` deletion) and Phase 3 (`middleware.ts` deletion) changes — not merely assumed merged.                     |
| Invented prerequisite edges break the DAG, surfacing far downstream with no traceable cause.                                                                                                                 | Each body's `prerequisites` are transcribed from its spec's declared chain, never re-derived.                                                                                                                                                                     |
| Volatile security-tooling / SIEM-platform facts (Wazuh, Sigma, ELK/OpenSearch specifics) are written into the stable spine and age the curriculum badly.                                                     | Volatile facts sit only in dated accuracy-note sidebars, enforced per-course by the accuracy pre-verify step and re-checked by `apps-ayokoding-www-facts-checker`.                                                                                                |
| `offensive-security`'s worked examples are read as endorsement of unauthorized real-world exploitation.                                                                                                      | The body must restate its lab-local, authorized-scope-only rules of engagement, checked by a grep-checkable acceptance clause per course.                                                                                                                         |
| A course body reproduces copyrighted material — SIEM vendor documentation prose, a lifted dashboard screenshot, or a well-known security-course's module structure (programme `A8`, inherited from plan 04). | The same six-hazard licensing posture plan 04 states in its `tech-docs.md` §Licensing posture applies verbatim; step-5 content checkers are the enforcement point.                                                                                                |
| A band lands but the manifest plan never grows its manifests, leaving the three `software-engineer` paths permanently missing this tier.                                                                     | The single band-completion signal names every affected manifest by full path plus the merge commit SHA; an incomplete signal is rejected by the receiving plan rather than guessed at.                                                                            |
| The cross-plan link to `ayokoding-learning-path-04-course-authoring` breaks once that plan archives mid-way through this plan's own execution.                                                               | Phase 0 resolves the actual archived path dynamically (mirroring plan 04's own schema-plan repoint pattern) rather than hardcoding a guessed completion date; a pre-archival link-validation gate in this plan's own Phase 3 catches a broken or stale reference. |
