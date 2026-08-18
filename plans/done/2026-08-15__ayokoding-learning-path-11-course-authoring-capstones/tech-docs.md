# Technical Docs — Learning Path Course Authoring: Capstones (Band 8)

## Corpus Custody

`custodied-by:ayokoding-learning-path-02-schema-and-prerequisite-dag` — this plan **reads** the
shared course corpus custodied by plan 02 but never edits, copies, or forks any file under it. Any
needed change to that corpus is routed to plan 02's own `delivery.md` as a change request, per the
[Learning-Plan Syllabus Convention §Custody Rule](../../../repo-governance/conventions/structure/learning-plan-syllabus/custody-rule.md#custody-rule).

## Overview

This plan produces **content artefacts only**: 8 page bundles under
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`. It writes no TypeScript, no JSON manifest data
file, no route, no component, and no redirect rule. Its "architecture" is therefore an **authoring
architecture**, inherited from plan 04 and every sibling split plan unchanged: where each body's
authoritative spec lives, what shape the produced bundle takes, and how a landed band is handed to the
manifest-growth plans. What is genuinely different about this band is the **dependency surface**: a
capstone assembles two or more prior bands' content, so it cannot be authored until every band it
assembles has landed. This document's centerpiece is therefore the confirmed per-capstone dependency
map below, verified directly against each course's own syllabus spec rather than assumed from its
catalog section heading.

## Programme decisions (folded, condensed)

Reproduced from plan 04's own folded programme-decisions section so this plan is self-contained. Only
the ids genuinely load-bearing for capstone authoring are restated here:

| Id  | Decision                                                                                                                                                                                                                                                                   |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R9  | Every plan declares its UI-gate and API-gate posture explicitly; a plan bearing neither surface is not thereby exempt and must state why. See [§UI-gate and API-gate posture](#ui-gate-and-api-gate-posture-r9) below.                                                     |
| A8  | Strict clean-room licensing, programme-wide: nothing copyrighted is reproduced; every concept is restated in original words with a citation. Binds this band's security capstones with particular force — see [§Licensing posture](#licensing-posture-programme-a8) below. |
| A9  | Both corpora expand past 20 courses as the domain requires; every derived count follows.                                                                                                                                                                                   |
| A12 | Every syllabus is independently authored, then externally confirmed; a published curriculum may corroborate coverage but must never supply the structure being written.                                                                                                    |

## The manifest ownership invariant (binding)

> **This plan never edits a manifest file.** Every file under
> `apps/ayokoding-www/src/features/course-paths/manifests/` is owned by
> `ayokoding-learning-path-12-careers-se-manifests` (three software-engineer-role manifests) and
> `ayokoding-learning-path-13-careers-ai-manifest` (the `ai-engineer` manifest). A step here that
> creates, appends to, reorders, or re-verifies a `.json` manifest is a **boundary violation**, not a
> convenience — the identical invariant plan 04 established and every sibling split plan carries
> unchanged.

### What the invariant permits and forbids, concretely

| Action                                                              | Permitted here?                                                  |
| ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Create `<COURSES><course-id>/` and author its bundle (8 capstones)  | **Yes**                                                          |
| Declare `prerequisites` in a course's own `_index.md`               | **Yes**                                                          |
| Add a course's row to the Course Library Catalog in this file       | **Yes**                                                          |
| List a course in `<COURSES>_index.md`                               | **Yes**                                                          |
| Record the one band-completion signal in this plan's `delivery.md`  | **Yes**                                                          |
| Read a `.json` manifest to check what a path expects                | **Yes** (read-only)                                              |
| Append a course ID to any `<MANIFESTS>**/*.json`                    | **No**                                                           |
| Re-order any `courseOrder`                                          | **No**                                                           |
| Re-run manifest integrity / prerequisite-consistency as a gate here | **No** — the manifest-growth plans re-verify their own artefacts |
| Edit any other course-authoring successor plan's folder             | **No** — flag discrepancies, never patch another plan's files    |

## Confirmed per-capstone dependency map

**Method.** Every edge below was verified by directly reading the capstone's own catalog row in
plan 04's Course Library Catalog **and** its full syllabus-spec text (its own dedicated spec file, or
its embedded inter-topic capstone section inside a donor course file) — never inferred from a catalog
section heading alone. A prerequisite course's **origin letter** (`E`/`Ecap` = existing, already
re-homed by plan 01; `T(n)` = transferred-native, authored by whichever band's successor plan owns it;
`N` = net-new, same rule) determines which plan actually delivers it — this matters because several
courses that appear inside a Band-5-themed catalog section (e.g. `software-engineering-practices`,
`agentic-coding`) are actually origin `E`, meaning plan 01 already delivered them, not plan 06.

| Capstone                                 | Confirmed prerequisites (owning plan)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `capstone-build-your-own-coding-agent`   | `the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`, `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`, `browser-automation-with-cdp` — all origin `N`, **plan 06** (Band 5) · `async-python-and-fastapi-services` — origin `N`, **plan 04** (Band 2) · `software-engineering-practices` — origin `E(30)`, **plan 01** (already re-homed)                                                                                                                                                                                                                                                                                                                                                                            | `syllabus/courses/capstone-build-your-own-coding-agent.md` §Prerequisites, read in full                                                                                                                                                                                                                                                                                                                                                                                                |
| `capstone-build-your-own-pentest-engine` | `agentic-ai` — origin `T(57)`, **plan 06** (Band 5) · the full harness cluster (same 5 courses above) — **plan 06** · `browser-automation-with-cdp` — **plan 06** · `security-essentials` — origin `E(17)`, **plan 01** · `offensive-security`, `defensive-security`, `detection-engineering-and-siem-operations`, `vulnerability-management-and-assessment` — all **plan 08** (Band 7) · `just-enough-typescript` — origin `E`, **plan 01**                                                                                                                                                                                                                                                                                                                             | `syllabus/courses/capstone-build-your-own-pentest-engine.md` §Prerequisites, read in full                                                                                                                                                                                                                                                                                                                                                                                              |
| `capstone-real-world-delivery`           | `capstone-solid-core` — origin `Ecap`, **plan 01** (already re-homed, live on disk) · `backend-at-scale` — origin `T(39)`, **plan 04** (Band 2, already on disk) · `system-design`, `event-driven-architecture` — origin `T(44)`/`T(45)`, **plan 06** (Band 5) · `software-architecture` — origin `T(42)`, **plan 06** (Band 5; **confirmed absent on disk** as of this plan's authoring time) · `domain-driven-design` — origin `T(43)`, **plan 06** (Band 5; **confirmed absent on disk**) · `containers-and-orchestration`, `cloud-and-iac`, `cicd-and-release-engineering` — origin `T(50)`/`T(51)`/`T(55)`, **plan 04** (Band 2) · `it-and-application-security`, `offensive-security`, `defensive-security` — origin `T(58)`/`T(59)`/`T(60)`, **plan 08** (Band 7) | `syllabus/courses/defensive-security.md` lines 303–338 (embedded inter-topic capstone spec's own "Integrates topics" list: "34 NoSQL · 35 Graph (where it fits) · 39 Backend at Scale · 42 Architecture · 43 DDD · 44 System Design · 45 Event-Driven · 50 Containers/K8s · 51 Cloud/IaC · 55 CI/CD · 58 IT Security · 59 Offensive (validation) · 60 Defensive (detection)"; topics 34/35 excluded as explicitly optional ("where it fits")) + plan 04 catalog row, both read in full |
| `capstone-secure-service`                | `security-essentials` — origin `E`, **plan 01** (already re-homed) · `backend-at-scale` — origin `T(39)`, **plan 04** (Band 2, already on disk; **corrected from `backend-essentials`** — the spec's own topic-39 citation is "Backend (auth surface)", and topic 39 corpus-wide unambiguously resolves to `backend-at-scale`, confirmed by cross-checking `syllabus/courses/backend-at-scale.md`'s own "Content originated in the now-closed FS-SE plan (topic 39)" line and every other topic-39 cross-reference in the corpus) · `it-and-application-security`, `offensive-security`, `defensive-security` — all **plan 08** (Band 7)                                                                                                                                 | `syllabus/courses/defensive-security.md` lines 339–366, read in full                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `capstone-data-pipeline`                 | `sql-essentials`, `advanced-sql-and-query-performance` — both origin `E`, **plan 01** (already re-homed) · `backend-at-scale` — origin `T(39)`, **plan 04** (Band 2, already on disk; **corrected from `backend-essentials`** — the spec's own topic-39 citation is "Backend at Scale (serving)", confirmed to resolve to `backend-at-scale`, same cross-check as above) · `data-engineering` — origin `T(37)`, **plan 04** (Band 1) · `creating-ai-powered-apps` — origin `T(56)`, **plan 06** (Band 5)                                                                                                                                                                                                                                                                 | `syllabus/courses/defensive-security.md` lines 368–395, read in full — the embedded spec's own "Integrates topics" list names only `10 SQL · 26 Advanced SQL · 34 NoSQL/35 Graph · 39 Backend at Scale · 37 Data Engineering · 56 AI-Powered Apps`; **no security-suite topic is named**, despite the spec being physically embedded inside `defensive-security.md` for organizational reasons alongside the other two DD-20 capstones from the same pass                              |
| `capstone-concurrency-and-systems`       | `csp-style-concurrency`, `actor-model-concurrency` — origin `T(65)`/`T(67)`, **plan 05** (Band 4) · `containers-and-orchestration` — **plan 04** (Band 2) · `site-reliability-engineering` — origin `T(94)`, **plan 08** (Band 7)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `syllabus/courses/compilers-parsers-and-transpilers.md` lines 266–291 + its own "In which paths" note (lines 350–358), which states explicitly: "Its ordered steps require `site-reliability-engineering` … so it is placed after that course" — confirms the Band-7 edge is a genuine authoring-order dependency, not incidental                                                                                                                                                      |
| `capstone-concurrency-showdown`          | `csp-style-concurrency`, `actor-model-concurrency` **only** — **plan 05** (Band 4)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `syllabus/courses/compilers-parsers-and-transpilers.md` lines 293–316 + its own "In which paths" note (lines 340–348): "Its only prerequisites … are already satisfied by the end of this course's own section" — explicitly confirms no further prerequisite exists                                                                                                                                                                                                                   |
| `capstone-lead-at-altitude`              | **one of** `capstone-concurrency-and-systems` **or** `capstone-real-world-delivery` — **intra-band, this plan's own Cohort B; the spec's own framing is disjunctive ("take one of the earlier runnable systems... or...")**, not a requirement for both · `site-reliability-engineering` — **plan 08** (Band 7) · `software-product-engineering`, `engineering-management` — both origin `E(32)`/`E(33)`, **plan 01** (already re-homed)                                                                                                                                                                                                                                                                                                                                 | `syllabus/courses/site-reliability-engineering.md` lines 232–234 (the disjunctive "one of ... or ..." goal statement), read in full                                                                                                                                                                                                                                                                                                                                                    |

### Plan-level rollup (what this table implies for `Depends-on`)

- **plan 01** (`url-restructure`) — transitive hard, already done; every `E`/`Ecap`-origin course cited
  above is confirmed already on disk (verified by direct `test -d` at this plan's authoring time:
  `capstone-solid-core`, `security-essentials`, `just-enough-typescript`,
  `sql-essentials`, `advanced-sql-and-query-performance`, `software-engineering-practices`,
  `agentic-coding`, `software-product-engineering`, `engineering-management` all present).
  **`backend-essentials` was removed from this list** during this plan's dependency re-audit: neither
  `capstone-secure-service` nor `capstone-data-pipeline` actually cite it — both capstones' own
  "Integrates topics" text names topic 39 as "Backend (auth surface)" / "Backend at Scale (serving)"
  respectively, which resolves corpus-wide to `backend-at-scale` (plan 04), not `backend-essentials`
  (plan 01). See the corrected dependency-map rows above.
- **plan 02** (`schema-and-prerequisite-dag`) — transitive hard, already done; the syllabus specs cited
  throughout this table are its custodied corpus.
- **plan 04** (`course-authoring`, Band 1/2 baseline) — hard; cited by `async-python-and-fastapi-services`,
  `containers-and-orchestration`, `cloud-and-iac`, `cicd-and-release-engineering`, `data-engineering`,
  `backend-at-scale` (topic 39, cited by `capstone-real-world-delivery` — see the corrected dependency
  map row above).
  [Repo-grounded] — all six were confirmed already present under `<COURSES>` at this plan's
  authoring time (`test -d` on each returned true), meaning plan 04's own Band 1/2 authoring has
  already progressed past these six specific courses, though this plan still treats the dependency
  as the full plan-level precondition rather than a partial phase-level one (plan 04 is still
  in-progress as a whole).
- **plan 05** (`platform-and-concurrency`, Band 4) — hard; cited by both concurrency capstones via
  `csp-style-concurrency` and `actor-model-concurrency`.
- **plan 06** (`architecture-and-ai-harness`, Band 5) — hard; cited by four of the eight capstones
  (`capstone-build-your-own-coding-agent`, `capstone-build-your-own-pentest-engine`,
  `capstone-real-world-delivery`, `capstone-data-pipeline`) via the harness cluster,
  `browser-automation-with-cdp`, `agentic-ai`, `system-design`, `event-driven-architecture`,
  `creating-ai-powered-apps`, and — newly confirmed for `capstone-real-world-delivery` —
  `software-architecture` (topic 42) and `domain-driven-design` (topic 43). **Both are confirmed
  absent on disk** as of this plan's authoring time (`test -d` on each returns false); see
  [delivery.md Phase 0](./delivery.md#phase-0-environment-setup--baseline) for the corresponding
  precondition check. This is this band's single heaviest-cited upstream plan.
- **plan 08** (`security-and-ops`, Band 7) — hard; cited by five of the eight capstones
  (`capstone-build-your-own-pentest-engine`, `capstone-real-world-delivery`, `capstone-secure-service`,
  `capstone-concurrency-and-systems`, `capstone-lead-at-altitude`) via
  `offensive-security`, `defensive-security`, `detection-engineering-and-siem-operations`,
  `vulnerability-management-and-assessment`, `it-and-application-security` (newly confirmed for
  `capstone-real-world-delivery` — see the corrected dependency map row above), and
  `site-reliability-engineering`.
- **plan 07** (`low-level-systems`, Band 6a) and **plan 10** (`jvm-and-build-your-own`, Band 6b) —
  **no confirmed edge**. Verified absent: none of the eight capstones' prerequisite lists cites any of
  `just-enough-c`, `just-enough-cpp`, `linux-os`, `windows-os`, `system-programming`,
  `just-enough-rust`, `modern-system-programming`, `just-enough-java`, `enterprise-java-and-the-jvm`,
  `lisp`, `just-enough-fsharp`, `type-systems`, `compilers-parsers-and-transpilers` (the course, as
  opposed to the file two capstones happen to be embedded in), `build-your-own-git`,
  `build-your-own-database`, or `build-your-own-raft`.
- **plan 09** (`interview-technique`, Band 9) — **no confirmed edge**. Verified absent: none of the
  eight capstones cites `coding-interview`, `take-home-and-live-coding`, `system-design-interview`,
  `behavioral-and-leadership-interviews`, or `capstone-interview-loop`.
- **`vercel-function-cost-reduction`** — repository baseline; see [README.md §Why the cost-reduction dependency
  is hard](./README.md#depends-on).

### Two cross-plan documentation discrepancies — found, and now reconciled upstream

Found during this plan's dependency verification and originally recorded here for reconciliation.
**Both are now reconciled**: the two sibling plans' own folders have since been corrected in place
(2026-08-01), so the historical discrepancy is recorded below for traceability, not as an open item.

1. **`ayokoding-learning-path-08-course-authoring-security-and-ops`'s own `README.md` originally
   asserted that `capstone-data-pipeline` needs Band 7's security/ops bodies** ("Band 7 → Band 8,
   hard: capstones need Band 7's security/ops bodies"). This plan's own direct read of
   `syllabus/courses/defensive-security.md` lines 368–395 (the embedded `capstone-data-pipeline` spec)
   found **no security-suite topic** in either its "Integrates topics" list or its catalog-table
   `prerequisites` cell — only SQL, NoSQL/Graph, Backend-at-Scale, Data Engineering, and
   AI-Powered-Apps. This plan's table above never carried a `capstone-data-pipeline` → plan 08 edge.
   **Reconciled**: plan 08's own `README.md` now carries a "Correction (2026-08-01)" note that removes
   `capstone-data-pipeline` from its `blocks` row for this plan and adds `capstone-real-world-delivery`
   and `capstone-concurrency-and-systems` instead (both confirmed by the same audit to need Band 7's
   `defensive-security`/`site-reliability-engineering`) — see
   `plans/backlog/ayokoding-learning-path-08-course-authoring-security-and-ops/README.md`.
2. **`ayokoding-learning-path-05-course-authoring-platform-and-concurrency`'s own `README.md`
   originally attributed its `capstone-concurrency-and-systems`/`capstone-concurrency-showdown`
   downstream dependency to `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`**,
   not to this plan. This plan's own read of `ayokoding-learning-path-10-...`'s `README.md` found
   **no** Band-8 capstone content in its scope at all (it owns Band 6b — JVM, advanced languages, and
   build-your-own-git/database/raft only). The two concurrency capstones are authored **here**, in
   this plan, not in plan 10. Plan 05's own text hedged this itself at the time — it stated the brief
   that supplied its dependency claim did not name the authoring plan with certainty. **Reconciled**:
   plan 05's own `README.md` now carries a "reconciliation pass" row (added 2026-08-01) that redirects
   its `blocks` edge from plan 10 to this plan (`ayokoding-learning-path-11-course-authoring-capstones`)
   — see `plans/done/2026-08-04__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/README.md`.

Neither discrepancy ever changed this plan's own dependency table above, which is grounded directly in
the primary syllabus specs rather than in either sibling plan's assertion.

## Course Library Catalog

Eight rows, all origin `N` (net-new courses, first authored in this plan) except `capstone-solid-core`
which is `Ecap` and already re-homed elsewhere — not one of this plan's eight. Full per-course detail
is the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md).

| Course ID                                | Cohort   | Kind                    | Primary language  | Prerequisites (owning plan in parens)                                                                                                                                                                                                                                            | One-line scope                                                                             |
| ---------------------------------------- | -------- | ----------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `capstone-build-your-own-coding-agent`   | A        | Harness milestone       | Python            | harness cluster ×5, `browser-automation-with-cdp` (06); `async-python-and-fastapi-services` (04); `software-engineering-practices` (01)                                                                                                                                          | Assemble the harness cluster into a working coding-agent CLI                               |
| `capstone-build-your-own-pentest-engine` | A        | Security milestone      | TypeScript        | `agentic-ai`, harness cluster ×5, `browser-automation-with-cdp` (06); `offensive-security`, `defensive-security`, `detection-engineering-and-siem-operations`, `vulnerability-management-and-assessment` (08); `security-essentials`, `just-enough-typescript` (01)              | Agentic pentest engine — lab-local, authorized-scope-only                                  |
| `capstone-secure-service`                | A        | Security milestone      | Python + shell    | `security-essentials` (01); `backend-at-scale` (04); `it-and-application-security`, `offensive-security`, `defensive-security` (08)                                                                                                                                              | End-to-end secured HTTP service, red-team validated + blue-team detected                   |
| `capstone-data-pipeline`                 | A        | Data milestone          | SQL + Python      | `sql-essentials`, `advanced-sql-and-query-performance` (01); `backend-at-scale`, `data-engineering` (04); `creating-ai-powered-apps` (06)                                                                                                                                        | Medallion pipeline → governed warehouse → RAG-grounded query interface                     |
| `capstone-concurrency-showdown`          | A        | Comparison milestone    | Go + Elixir       | `csp-style-concurrency`, `actor-model-concurrency` (05)                                                                                                                                                                                                                          | Same problem solved CSP-Go vs actor-Elixir, compared head-to-head                          |
| `capstone-concurrency-and-systems`       | B        | Systems milestone       | Go or Elixir + C  | `csp-style-concurrency`, `actor-model-concurrency` (05); `containers-and-orchestration` (04); `site-reliability-engineering` (08)                                                                                                                                                | Concurrent, containerized, SRE-instrumented service                                        |
| `capstone-real-world-delivery`           | B        | Full-stack milestone    | Python + TS + IaC | `capstone-solid-core` (01); `system-design`, `event-driven-architecture` (06); `containers-and-orchestration`, `cloud-and-iac`, `cicd-and-release-engineering` (04); `defensive-security` (08)                                                                                   | Deploy-as-code, secured, observable delivery of the Pass-2 app                             |
| `capstone-lead-at-altitude`              | B (last) | Whole-journey milestone | polyglot + prose  | one of `capstone-concurrency-and-systems` **or** `capstone-real-world-delivery` (this plan, intra-band; spec is disjunctive — reader's/author's choice of starting artefact); `site-reliability-engineering` (08); `software-product-engineering`, `engineering-management` (01) | Whole-journey leadership synthesis: SLOs, strategy, prioritization, six-pass retrospective |

**Count check**: 8 new capstone bodies authored here. Combined with the 90 (plan 04) + 14 (plan 05) +
15 (plan 06) + 7 (plan 07) + 11 (plan 08) + 5 (plan 09) + 9 (plan 10) + 8 (this plan) = 159 course
bodies across all course-authoring successor plans, plus the 37 already re-homed by plan 01 — this
plan does not itself assert the grand total; that remains the eventual manifest-growth plans'
terminal assertion, exactly as plan 04 established for its own 90.

## Capstone dependency diagram

Every one of the 5 upstream plans (`01`, `04`, `05`, `06`, `08`) feeds at least one capstone, and 4 of
the 8 capstones each depend on 3+ of those 5 plans — a bipartite graph too dense for a single
width-bounded diagram (see the [Confirmed per-capstone dependency map](#confirmed-per-capstone-dependency-map)
above for the full, evidence-linked detail). This table is the compact summary; **✓** marks an edge:

| Capstone (cohort)                            | 01  | 04  | 05  | 06  | 08  | Intra-band                                                  |
| -------------------------------------------- | --- | --- | --- | --- | --- | ----------------------------------------------------------- |
| `capstone-build-your-own-coding-agent` (A)   | ✓   | ✓   | —   | ✓   | —   | —                                                           |
| `capstone-build-your-own-pentest-engine` (A) | ✓   | —   | —   | ✓   | ✓   | —                                                           |
| `capstone-secure-service` (A)                | ✓   | —   | —   | —   | ✓   | —                                                           |
| `capstone-data-pipeline` (A)                 | ✓   | ✓   | —   | ✓   | —   | —                                                           |
| `capstone-concurrency-showdown` (A)          | —   | —   | ✓   | —   | —   | —                                                           |
| `capstone-concurrency-and-systems` (B)       | —   | ✓   | ✓   | —   | ✓   | —                                                           |
| `capstone-real-world-delivery` (B)           | ✓   | ✓   | —   | ✓   | ✓   | —                                                           |
| `capstone-lead-at-altitude` (B)              | ✓   | —   | —   | —   | ✓   | one of `-concurrency-and-systems` or `-real-world-delivery` |

**Accessibility note.** This is a plain data table (screen-reader-native); cohort membership is
stated in every row label rather than relying on colour, and the one intra-band constraint is spelled
out in its own column rather than as an unlabelled edge.

## Named decisions this plan makes

Plan-specific ids (`DD-N`) are not minted here to avoid colliding with ids concurrently claimed by
sibling split plans authored in the same swarm event; decisions are instead named descriptively.

- **Cohort split by the single confirmed intra-band edge, not by list position.** `capstone-lead-at-altitude`
  is the only capstone with an intra-band prerequisite — the spec's own framing is disjunctive: it
  takes **one of** `capstone-concurrency-and-systems` **or** `capstone-real-world-delivery` as its
  starting artefact, not both; the other five have zero cross-references among themselves. Cohort
  A = the five independent capstones; Cohort B = the three-course group, authored in chain order.
  **[Judgment call]**: this plan still authors both Cohort-B leaves before `capstone-lead-at-altitude`
  and keeps both landed on disk as a safety margin beyond the spec's strict minimum (so the author
  has an actual free choice between them at authoring time, rather than being forced into whichever
  one happened to land first) — the ordering itself is a deliberate authorial choice, not a spec
  requirement for both. See
  [README.md §Exact scope](./README.md#exact-scope-8-courses-in-two-cohorts) for the full rationale.
- **`vercel-function-cost-reduction` treated as a repository-baseline verification, not a per-course one.**
  Every one of the eight capstones renders into the same `apps/ayokoding-www` route tree that plan is
  restructuring; gating the whole plan (rather than only the capstones that happen to touch a
  particular route) avoids a scenario where some of the eight pages ship statically and others ship
  dynamically depending on merge order.
- **Security-capstone licensing discipline restated, not re-derived.** `capstone-build-your-own-pentest-engine`'s
  own syllabus spec already states its authorization-and-scope rule as non-negotiable; this plan's
  authoring convention treats that rule as a hard authoring-time gate (see
  [delivery.md](./delivery.md)), not merely prose to transcribe.
- **No new `DD-N` ids minted.** This plan's design decisions are stated by name (as above) rather than
  by number, since the `DD-N` sequence is actively being extended by multiple sibling plans
  concurrently and a collision-safe global allocation was not available at this plan's authoring
  time. A future reconciliation pass MAY assign this plan formal `DD-N` ids once the full sibling set
  is known.

## UI-gate and API-gate posture (R9)

### UI gate — **exempt**

Identical reasoning to plan 04 and every sibling split plan. `swe-ui-checker` validates component
**source** — it globs for `.tsx` files. This plan's entire output is 8 markdown page bundles under
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`. A checker run scoped to this plan's diff
scans **zero** `.tsx` files. The components that render these bodies are owned and gated by
`ayokoding-learning-path-03-navigation-ui`.

**The exemption is narrow.** Manual behavioural verification via Playwright MCP is **mandatory and
performed** ([delivery.md](./delivery.md) Phase 4) — a sample of the eight authored pages, all three
breakpoints, `en` locale, committed screenshot evidence. The Rule-15 three-tester retest is separately
exempted with its own stated reasons in
[README.md §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded).

### API gate — **exempt**

This plan never edits a manifest file — forbidden outright by
[§The manifest ownership invariant](#the-manifest-ownership-invariant-binding) — and ships no code, no
JSON manifest data, no route. The `prerequisites` frontmatter this plan writes into each of the 8 `_index.md` files
is inert until a downstream manifest-growth plan reads it. This plan's own structural check verifies
only that the field is present and well-formed, never that it resolves against a manifest.

**Rule-16 API exploratory retest — not applicable.** No REST or GraphQL endpoint changes.

## Licensing posture (programme A8)

Programme `A8` binds this plan's security capstones with particular force —
`capstone-build-your-own-pentest-engine` and `capstone-secure-service` both touch offensive-security
material. **Describe, cite, and link; never reproduce.**

- **Code examples.** Every worked example (the pentest engine's TypeScript agent loop, the secure
  service's mitigations, the attack/detection scripts) is authored originally, never copied from a
  security tool's documentation, a CTF writeup, or Stack Overflow (CC-BY-SA — a licence course
  material generally cannot satisfy).
- **The pentest capstone's own hard authorization rule.** Its syllabus spec states, verbatim in its
  own text: "every example and the capstone run **only** against a lab target the reader owns and has
  explicit authorization to test; the engine hard-enforces scope. This is stated as an ethical + legal
  hard rule, not a tunable." This plan's authoring convention treats that line as a non-negotiable
  authoring-time gate, not merely prose to preserve.
- **The `vacti-pentest-engine` reference is `[Unverified]`, maintainer-supplied, not publicly
  discoverable** as of the syllabus spec's own authoring date. This plan's own body must not upgrade
  that citation to a verified fact.
- **Figures and diagrams** are Mermaid, authored here, never a lifted screenshot.
- **Datasets** (the data-pipeline capstone's medallion pipeline, the pentest lab target) are authored
  for the example, not lifted from an unexamined-licence source.

## Exemptions (stated explicitly, not silently taken)

### UI-design-funnel exemption (not UI-bearing)

This plan adds or changes no user-facing screen or component under `apps/` or `libs/`. Every artefact
is a markdown page bundle rendered by components this plan does not touch. The complete UI-design
funnel is owned by `ayokoding-learning-path-03-navigation-ui`.

### Specs & Gherkin (app-code) exemption

The [Feature Change Completeness Convention](../../../repo-governance/development/quality/feature-change-completeness.md)
binds app/lib code changes to companion `specs/` Gherkin. This plan changes no app or lib code — it
adds content under `apps/ayokoding-www/content/`, classified content-exempt from `specs:coverage`, per
plan 04's own precedent. The Gherkin scenarios in [`prd.md`](./prd.md#acceptance-criteria-gherkin) are
content-level acceptance criteria bound to delivery steps, not to `specs:behavior:coverage`. This plan
still runs `npm exec nx affected -t specs:behavior:coverage` in its verification phase to prove no
regression.

### TDD exemption (this plan ships no application code)

Identical to plan 04's own exemption. This plan's delivery steps produce prose and colocated runnable
`code/` samples that are course material, not application code — no importable module, no test
target, no runtime behaviour the app depends on. Correctness is established by the maker-checker-fixer
pipeline, not RED→GREEN→REFACTOR.

### Rule-15 / Rule-16 exemptions

Recorded with full reasoning in [README.md](./README.md#rule-15-three-tester-retest--exemption-recorded).

## File-Impact Analysis

Root-relative annotated tree — the scan-first source of truth for this plan's scope. **[E]** edit,
**[N]** new file/pattern, **[D]** delete, **[G]** generated/regenerated.

```text
.
├── apps/ayokoding-www/content/en/learn/courses/
│   ├── _index.md [E] — append one catalog row per landed capstone ID
│   └── <capstone-id>/ [N] — 8 bundles; bounded family, members enumerated verbatim in
│       │                  evidence/authored-body-slugs.txt (written in Phase 0), never by glob
│       ├── _index.md [N] — declares `prerequisites: [course-id, ...]`
│       ├── overview.md [N] — purpose, prerequisites, register, scope boundary
│       ├── learning/ [N] — `_index.md`, co-NN/ex-NN pages, `code/`, `capstone/`
│       └── drilling/ [N] — `_index.md` + `overview.md` (fixed five-section order)
│       └── <per-capstone code subfolders> [N] — the exact set each capstone's embedded
│                                                spec names (e.g. `code/core/`, `target/`,
│                                                `engine/`, `design/`, `attack/`, `go/`);
│                                                see §File Impact detail below
├── plans/in-progress/ayokoding-learning-path-11-course-authoring-capstones/
│   ├── tech-docs.md [E] — this file; the Course Library Catalog rows
│   ├── delivery.md [E] — checkbox ticks + the five-field band-completion signal
│   ├── learnings.md [E] — running log, drained by the Knowledge Capture phase
│   └── evidence/ [N] — phase-0 snapshot, authored-body-slugs.txt, Playwright screenshots
└── apps/ayokoding-www/src/features/course-paths/ — NOT TOUCHED (zero-diff gate every phase)
```

### More Detail

The `<capstone-id>/` bundles are the only `*`-shaped family in the tree, and they are bounded by
construction: the exact member list is written to `evidence/authored-body-slugs.txt` during Phase 0,
and every later assertion reads that register rather than globbing the directory — so a slug that
drifted into the tree from a sibling band plan can never be silently adopted as this plan's work.

`apps/ayokoding-www/content/en/learn/courses/_index.md` is generated from course directories; this plan does not edit it manually outside
its own plan folder. It is **appended to**, never rewritten, so a concurrent sibling band plan adding
its own rows produces a mergeable diff rather than a conflict.

Nothing under `apps/ayokoding-www/src/` carries an action annotation because this plan writes no
application code at all. That absence is **asserted** by the zero-diff manifest gate in every phase,
not merely assumed — the manifest subtree is named separately below because reading it is permitted
and writing it is a boundary violation, a distinction the tree alone cannot carry.

**New directories created** (8 total, one per capstone, zero overlap with any other plan's slugs —
verified absent at this plan's authoring time):

- `apps/ayokoding-www/content/en/learn/courses/<course-id>/` — the fixed course-page bundle anatomy
  (`_index.md`, `overview.md`, `learning/`, `drilling/`), one per capstone. `capstone-build-your-own-pentest-engine`
  additionally carries a `target/` subfolder (isolated lab target) and `engine/` (the TypeScript agent
  loop); `capstone-build-your-own-coding-agent` carries `code/core/`; the three cross-cutting
  capstones (`capstone-real-world-delivery`, `capstone-secure-service`, `capstone-data-pipeline`)
  carry the subfolder structure their embedded specs name (`design/`, `app/`, `deploy/`, `security/`;
  `attack/`, `detect/`; `pipeline/`, `serve/`, `interface/`); `capstone-concurrency-and-systems` and
  `capstone-concurrency-showdown` carry `code/` and `go/`/`elixir/` respectively;
  `capstone-lead-at-altitude` carries `code/`, `strategy.md`, `prioritization.md`, `retrospective.md`.

**Existing files modified** (this plan edits these; it never creates them):

| File                                                    | Change                                                                                            |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `apps/ayokoding-www/content/en/learn/courses/_index.md` | regenerated from course directories; verify with `npm exec nx run ayokoding-www:validate-indexes` |
| `tech-docs.md` (this file) — §Course Library Catalog    | already carries all 8 rows                                                                        |
| `delivery.md` (this plan's own file)                    | the single five-field band-completion signal appended at the close of Cohort B                    |

**Never touched, by construction**:

- `apps/ayokoding-www/src/features/course-paths/` (`<FEAT>`) — no application code
- `apps/ayokoding-www/src/features/course-paths/manifests/` (`<MANIFESTS>`) — read-only; confirmed
  every phase by a zero-diff gate check
- `apps/ayokoding-www/content/en/learn/paths/` (`<PATHS>`) — read-only reference
- Any other course-authoring successor plan's own folder
- `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` — consumed, never copied or edited

**No package-manifest changes.**

## Execution dependency

This plan has one direct execution prerequisite: `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`, fully merged and archived on `origin/main`. Course-level source citations and repository facts are implementation context, not extra plan dependencies.

## Rollback

Every artefact is an **additive** new directory under `<COURSES>`. Rollback is subtractive and total:

- **Per cohort**: revert that cohort's merge commit. Cohort A's five bodies disappear independently of
  Cohort B's three (and vice versa), since no capstone in Cohort A cites any Cohort B capstone.
- **Per course**: `git rm -r <COURSES><course-id>/` plus removing its catalog row and its
  `<COURSES>_index.md` entry. **Not safe for `capstone-lead-at-altitude`'s two prerequisites** once
  `capstone-lead-at-altitude` itself has merged — check the intra-band reference direction first.
- **Whole plan**: revert both cohort merges in reverse order. The `courses/` bucket returns to
  whatever state it held before this plan started.

**The one-way door**: once a manifest references one of these 8 course IDs, deleting that body breaks
`checkManifestIntegrity` downstream — bodies-first, manifests-after, and this plan never grows a
manifest itself.

## Testing / Verification Strategy

| Level                     | What it verifies                                                                                                        | Mechanism                                                                   |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Per-course content checks | concept-assembly coverage, register, worked-example structure, scope boundary against assembled courses                 | matching `apps-ayokoding-www-*-checker`                                     |
| Per-course fact checks    | version-pinned / benchmark claims (METR/Scale-AI citations, dependency versions) confined to dated sidebars             | `apps-ayokoding-www-facts-checker`                                          |
| Per-course link checks    | intra-course and cross-course links resolve, including to the 4+ upstream plans' courses                                | `apps-ayokoding-www-link-checker`                                           |
| Contract assertions       | authorization/scope hard-rule stated (pentest capstone); intra-band prerequisite declared (`capstone-lead-at-altitude`) | grep-checkable acceptance clauses                                           |
| Structural                | bundle anatomy present; `prerequisites` declared                                                                        | `test -d` / `test -f` + frontmatter grep                                    |
| Section build             | the authored tree renders                                                                                               | `npm exec nx run ayokoding-www:build`                                       |
| Markdown quality          | markdownlint, link validation, heading hierarchy                                                                        | `npm run lint:md` + the two `rhino-cli md` subcommands                      |
| Regression                | no existing project's gates broke                                                                                       | `npm exec nx affected -t typecheck lint test:quick specs:behavior:coverage` |
| Manual behavioural        | a sample of the 8 pages renders correctly at three breakpoints in `en`                                                  | Playwright MCP + committed `evidence/` screenshots                          |

**Deliberately absent**: unit, integration, and e2e tests for this plan's own artefacts — no
application code exists here to test, identical to every sibling course-authoring plan's own
reasoning.
