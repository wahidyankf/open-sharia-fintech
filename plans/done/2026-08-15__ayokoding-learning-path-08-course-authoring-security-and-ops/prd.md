# Product Requirements — Learning Path Course Authoring: Security, Ops & Delivery (Band 7)

## Product Overview

This plan authors **Band 7 — Security, ops, quality & delivery** of the shared course library's Band
7: eleven page bundles under `apps/ayokoding-www/content/en/learn/courses/`, each a standalone,
path-neutral building block with a stable course ID, a canonical URL, a declared prerequisite list, a
learning track, and a drilling track.

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
neither the path manifests (`ayokoding-learning-path-12-careers-se-manifests`'s scope) nor plan 04's other eight
bands. Three **`careers/`** paths reference this band's bodies once
`ayokoding-learning-path-12-careers-se-manifests` grows their manifests to include them:

- **`careers/interview-ready/software-engineer`** — the interview/job-prep-first arc.
- **`careers/immediately-effective/software-engineer`** — the immediately-effective, build-a-real-app
  first arc.
- **`careers/fundamentally-strong/software-engineer`** — the university-style, fundamentals-first arc.

The fourth path, `careers/immediately-effective/ai-engineer`, does **not** reference this band — its
manifest grows only from Bands 5 and 8 (the AI/harness cluster and its capstones), per plan 04's own
`GROW_MANIFESTS` routing.

The library body is **content**, exempt from `specs:coverage`; the navigation feature that renders it
is app code owned by `ayokoding-learning-path-03-navigation-ui`. The acceptance criteria below are
therefore **content-level** criteria, verified by the ayokoding content checkers and by
grep-checkable assertions on the authored bodies, not by application tests.

## Personas

Reproduced from plan 04, since every course this band authors is reached by readers of all three
`careers/software-engineer` paths — no persona is scoped to a single path for this band's bodies.

- **Experienced engineer re-entering the job market (north-star for
  `careers/interview-ready/software-engineer`)** — needs breadth refreshed fast, including this band's
  security/ops/quality/delivery topics, without walking a from-scratch curriculum.
- **A builder who wants to be effective fast (north-star for
  `careers/immediately-effective/software-engineer`)** — ships a real app early, then deepens into this
  band's material as part of "deepen into CS fundamentals, DS&A, algorithms, and systems."
- **A university-style, fundamentals-first learner (north-star for
  `careers/fundamentally-strong/software-engineer`)** — wants the rigorous bottom-up route, including
  this band's security and operations depth, after CS foundations.
- **A reader who lands on a shared course by deep-link / share** — arrives at, say,
  `detection-engineering-and-siem-operations` without a path context and must get a coherent standalone
  view (with its `defensive-security` prerequisite surfaced) plus an obvious way to enter a path.
- **Maintainer (content strategist / content author / reviewer)** — owns this band's scope boundaries
  and authors the eleven bodies via the ayokoding maker agents.

## User Stories

Scoped to this plan's surface — the eleven course bodies themselves.

- As a **reader following any of the three `careers/software-engineer` paths**, I want a complete
  security-and-operations tier (application security, offensive and defensive security technique,
  SIEM operations, vulnerability management, IT governance, virtualization, self-managed Kubernetes,
  platform engineering, SRE, and product analytics), so that the path does not silently skip this
  discipline.
- As a **security-track reader**, I want hands-on detection engineering to stay distinct from
  generalist defensive security, so that I can tell which course teaches breadth and which teaches the
  deep SIEM-ops tier.
- As a **reader of `offensive-security`**, I want the course to explicitly state its lab-local,
  authorized-scope-only rules of engagement, so that I never mistake worked examples for guidance on
  unauthorized real-world exploitation.
- As a **reader comparing `bare-metal-virtualization` with `self-hosting-essentials`**, I want each
  course to state the altitude boundary between them, so that I know when to graduate from a light
  on-ramp to full-depth virtualization.
- As a **reader comparing `analytics-and-experimentation` with `statistics-for-evaluation`**, I want
  each course to state its scope boundary, so that classical product A/B testing and AI-evals
  statistics never read as one topic taught twice.
- As a **Band 8 capstone reader** (`capstone-secure-service`, `capstone-build-your-own-pentest-engine`,
  `capstone-real-world-delivery`, `capstone-concurrency-and-systems`, `capstone-lead-at-altitude`), I
  want this band's bodies authored and stable before the capstone assembles them, so that "done" is a
  thing I can run.
- As the **maintainer**, I want every body authored **from** its settled spec file, so that concept
  coverage and prerequisite edges are transcribed rather than re-invented.
- As the **downstream manifest author**, I want one complete, explicit band-completion signal naming
  every manifest to grow, so that I never have to guess which paths this band affects.

## Acceptance Criteria (Gherkin)

This plan owns **one** scenario routed verbatim from plan 04 (the only one of its ten routed scenarios
that names a Band-7 course), plus **four** new scenarios scoped to this band's own reconciliation
rulings and boundary statements, plus **one** scoped build-green scenario mirroring plan 04's own
pattern for its own authored surface.

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And` / `But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule).

### Security reconciliation (routed from plan 04)

```gherkin
Scenario: Hands-on detection engineering stays distinct from generalist defensive security
  Given the detection-engineering-and-siem-operations course is authored
  When a reader compares it with the hands-on defensive-security course
  Then it has the reader author working Wazuh decoders, correlation rules, and a dashboard with false-positive tuning
  And defensive-security keeps the generalist Sigma/ELK breadth, IR, and hardening as its distinct scope
```

### Rules of engagement (new)

```gherkin
Scenario: The offensive-security course states its lab-local rules of engagement
  Given the offensive-security course is authored
  When a reader reads its overview
  Then it explicitly states the material is lab-local and authorized-scope-only
  And no lesson presents exploitation technique as guidance for unauthorized real-world targets
```

### Two-altitude boundaries (new)

```gherkin
Scenario: Bare-metal virtualization stays the full-depth sibling of light self-hosting
  Given the bare-metal-virtualization course is authored
  When a reader compares it with self-hosting-essentials
  Then bare-metal-virtualization names self-hosting-essentials as its lighter-altitude sibling
  And it covers Proxmox and hypervisor depth self-hosting-essentials deliberately excludes
```

```gherkin
Scenario: Analytics and experimentation stays distinct from statistics for evals
  Given the analytics-and-experimentation course is authored
  When a reader compares it with statistics-for-evaluation
  Then analytics-and-experimentation names statistics-for-evaluation as its scope-boundary sibling
  And it covers classical product metrics and A/B testing, not evals-specific judge concordance
```

### Scoped build-green (this plan's own surface)

```gherkin
Scenario: The authored Band-7 course bodies build and validate green
  Given every course body this plan authors has landed under the courses bucket
  When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
  Then the build succeeds over the eleven authored bodies
  And link, heading-hierarchy, and markdownlint validation report no errors across them
```

## Scenario-to-delivery binding

| Scenario                                                                         | Binds to                                                              | Status            |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ----------------- |
| Hands-on detection engineering stays distinct from generalist defensive security | Phase 1 (Cohort A) · `detection-engineering-and-siem-operations` step | routed (verbatim) |
| The offensive-security course states its lab-local rules of engagement           | Phase 1 (Cohort A) · `offensive-security` step                        | new (this plan)   |
| Bare-metal virtualization stays the full-depth sibling of light self-hosting     | Phase 2 (Cohort B) · `bare-metal-virtualization` step                 | new (this plan)   |
| Analytics and experimentation stays distinct from statistics for evals           | Phase 2 (Cohort B) · `analytics-and-experimentation` step             | new (this plan)   |
| The authored Band-7 course bodies build and validate green                       | Phase 3 · Section & Authored-Tree Verification                        | new (scoped)      |

## Course specifications (this band's eleven bodies)

Full per-course concept / example / prerequisite detail lives in the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)
(one file per course ID) and in
[tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) — the notes below fix each
course's purpose and register; they are not a substitute for the spec.

**Register.** All eleven courses use the normal **first-learn By-Example / Annotated-concept
register** (none is a refresh-register interview course; none is primer scope).

**Volume-target bands** (inherited from plan 04; floor not cap):

| Course shape                    | Concept floor (`co-NN`) | Worked-example band (`ex-NN`) |
| ------------------------------- | ----------------------- | ----------------------------- |
| By Example                      | ≥ 10                    | 75–85 code examples           |
| Annotated-concept, code-bearing | ≥ 10                    | 45–60 worked examples         |
| Annotated-concept, no-code      | ≥ 8                     | 30–60 worked scenarios        |

- **`it-and-application-security`** (Annotated-concept · Python) — CIA triad, STRIDE threat modeling,
  OWASP Top-10-class vulnerability classes, applied cryptography, identity/authN/authZ.
- **`offensive-security`** (By Example · Python + shell) — reconnaissance, scanning, exploitation
  technique, **lab-local and authorized-scope-only** throughout.
- **`defensive-security`** (By Example · Python + shell — **hands-on, DL-9/DD-12 label fix**) —
  Sigma-on-ELK/OpenSearch detection authoring, the incident-response lifecycle, hardening, as
  generalist blue-team breadth.
- **`detection-engineering-and-siem-operations`** (By Example · XML/rules + config + Python; declares
  `defensive-security` a prerequisite) — Wazuh-specific deep tier: decoder authoring, correlation-rule
  authoring, log parsing/normalization, false-positive tuning, dashboard construction, alert triage.
- **`vulnerability-management-and-assessment`** (By Example · Python) — scanning programs, triage
  workflows, remediation at scale, SBOM practice.
- **`it-governance-grc`** (Annotated-concept · no code) — governance frameworks, risk management,
  compliance regimes, audit practice.
- **`bare-metal-virtualization`** (By Example · HCL/YAML/shell) — Proxmox and hypervisor management,
  the full-depth sibling of the light `self-hosting-essentials` on-ramp (owned by plan 04's Band 2,
  DD-14 two-altitude split).
- **`self-managed-kubernetes-and-gitops`** (By Example · YAML/CLI) — self-owned production Kubernetes
  operation plus GitOps delivery.
- **`platform-engineering-and-devex`** (Annotated-concept · no code) — internal developer platforms,
  golden paths.
- **`site-reliability-engineering`** (Annotated-concept · Python) — SLOs, observability, incident
  response practice.
- **`analytics-and-experimentation`** (By Example · Python) — metrics design and classical product A/B
  testing, distinct from `statistics-for-evaluation`'s evals-only statistics scope (plan 04's DD-26).

## Product Scope

**In-scope**:

- Authoring **eleven course page bundles** under
  `apps/ayokoding-www/content/en/learn/courses/<course-id>/`, each with `_index.md` (declaring
  `prerequisites`), `overview.md`, a `learning/` track, and a `drilling/` track in the fixed
  five-section order.
- Declaring each body's `prerequisites` in the contracted frontmatter shape, transcribed from its
  settled spec.
- Stating the DL-9/DD-12 distinctness boundary (`defensive-security` ↔
  `detection-engineering-and-siem-operations`) and both two-altitude boundaries
  (`bare-metal-virtualization` ↔ `self-hosting-essentials`;
  `analytics-and-experimentation` ↔ `statistics-for-evaluation`).
- Stating `offensive-security`'s lab-local, authorized-scope-only rules of engagement.
- Adding this plan's authored courses to the tracked
  [Course Library Catalog](./tech-docs.md#course-library-catalog) as real rows.
- Updating `<COURSES>_index.md` to list every authored course.
- Emitting one complete **band-completion signal**.
- Manual behavioural verification of a sample of authored course pages via Playwright MCP, with
  committed screenshot evidence in `evidence/`.

**Out of scope**:

- **Any manifest file** under `<MANIFESTS>` — creating, appending to, reordering, or re-verifying.
  Owned by `ayokoding-learning-path-12-careers-se-manifests`. Binding invariant.
- **Any other band of the split family, or plan 04's own remaining scope (Band 1, Band 2, Phase 1
  AI-engineering).**
- **Any path landing anchor** under `<PATHS>` and the paths hub.
- **Any `course-paths` feature code** (`core/` or `shell/`).
- **Any redirect module or rule.**
- **The `prerequisites` frontmatter contract's definition.**
- **The `syllabus/` folder** — read-only from this plan; never copied.
- **Any Indonesian (`id`) course content** — explicitly deferred.
- **The UI design funnel** — this plan is not UI-bearing.
- **The rule-15 three-tester retest** — exemption recorded with reasons in
  [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded).
- **Fixing `apps/ayokoding-www`'s Vercel function-cost problem.** Consumed as a repository-baseline check, not
  authored here.

## Product-Level Risks

- **A body authored from judgment rather than its spec.** Concept coverage silently drops and
  prerequisite edges get invented. Mitigated by naming the exact cross-plan spec path in every
  authoring step and making "authored from that spec" an explicit acceptance criterion.
- **The `defensive-security` / `detection-engineering-and-siem-operations` reconciliation reopens.**
  Mitigated by authoring both in the same delivery cohort with an explicit duplicate-lesson-title
  check.
- **Volatile SIEM-platform / security-tooling facts written into the stable spine.** Mitigated by the
  accuracy pre-verify step and re-checked by `apps-ayokoding-www-facts-checker`.
- **`offensive-security` read as real-world exploitation guidance.** Mitigated by a grep-checkable
  rules-of-engagement acceptance clause.
- **A cross-plan reference to plan 04 breaks once it archives mid-execution.** Mitigated by dynamically
  resolving the archived path at Phase 0 rather than hardcoding a guessed date, plus a pre-archival
  link-validation gate.
- **A manifest-mutating step reintroduced into this plan.** Mitigated by the invariant being stated in
  three documents plus a phase-gate check that the plan's diff touches zero `<MANIFESTS>` paths.
- **A vague band-completion signal.** Mitigated by the five-field signal contract, with an explicit
  rejection rule for incomplete signals.
