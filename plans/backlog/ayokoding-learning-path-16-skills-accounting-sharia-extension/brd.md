# Business Requirements — Skills Paths: Accounting Sharia Extension

> **Programme decisions** — the `R*`/`A*` decisions cited below are restated verbatim from
> `ayokoding-learning-path-14-skills-accounting-foundations/tech-docs.md`, itself restated from the
> retired the superseded accounting-programme draft; see
> [tech-docs.md §Programme decisions](./tech-docs.md#programme-decisions).

## Business Goal

Complete the **Sharia half** of the two-path accounting corpus (A10), and with it, the whole
three-plan chain and the whole 24-course corpus. This plan is the third and final plan and carries
`sharia-accounting` from its plan-15 starting state (19 of 24 courses) to full completion: courses
\#20–#24 — the standards landscape (AAOIFI, PSAK Syariah, MFRS-plus-BNM), Islamic contract
modelling, Zakah computation, Sukuk accounting, and the terminal Sharia-ledger-architecture course.

The goal is not "teach accounting." The goal is **accounting for people who build Sharia-compliant
financial systems**: by the end of this plan a reader on `sharia-accounting` leaves able to model
murabaha, ijara, mudaraba, musharaka, zakah and sukuk correctly — as their own instruments, never as
conventional instruments with different labels — and to **architect** (never build, A6) a
Sharia-compliant ledger.

Three business consequences follow, all load-bearing:

1. **It completes `sharia-accounting` as a genuinely standalone, production-shippable path**, and
   with it, the whole three-plan accounting programme.
2. **It emits the second and final cross-plan ERP-facing signal in this chain** — unblocking
   `ayokoding-learning-path-18-skills-erp-enterprise-depth`'s Sharia-specific
   courses (Sharia-compliant ERP capability and founding-architecture capability).
3. **It is a materially stronger Sharia offering than the retired single-path design's own
   predecessor** — five dedicated courses instead of the pre-A9-expansion original's two, covering
   the standards landscape, contract modelling, Zakah, Sukuk, and ledger architecture in full.

## Why this plan's course range (#20–#24) closes the whole chain

Restated from plan 14's own `brd.md`: the retired plan's own Stage 3 (Sharia-only, #20–#24 in its
own numbering) maps unchanged onto this plan's own course range — this three-plan split does not
touch the Sharia stage's own course count or numbering, only the plans that precede it.

- **Sharia standards landscape** (#20) — presents AAOIFI, PSAK Syariah, and MFRS-plus-BNM as three
  coexisting models, never one universal standard.
- **Islamic contract modelling** (#21) — the load-bearing modelling fact: murabaha's markup is
  fixed and disclosed at the point of sale in a trade with an underlying asset, not accrued
  interest.
- **Zakah computation** (#22) and **Sukuk accounting** (#23) — both **new courses added past the
  retired single-path design's original two-course Sharia tail** (A9): AAOIFI FAS 9 (Zakah) and FAS
  32–34 (Sukuk) are `[Verified]` in the seeding research, yet the original catalog never taught
  either.
- **Sharia-ledger-system-architecture** (#24) — the terminal architecture course, replacing the
  retired single-path design's deleted `capstone-sharia-compliant-ledger` capstone (A6).

## Business Impact

**Pain points addressed** (restated, applicable to this plan's slice)

- **`sharia-accounting` was incomplete after plan 15** (19 of 24 courses) — this plan finishes it.
- **Sharia-compliant financial systems have no learning surface anywhere on the platform, until
  this plan lands.** This gap is deeper than the retired plan's own original design recognised:
  Zakah and Sukuk accounting had no course at all, even in the pre-split twenty-course single-path
  design.
- **ERP is blocked on its Sharia-specific stage with no path forward** — this plan's own Stage-3
  signal is the concrete unblock.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **A materially stronger position on Sharia accounting than the retired plan's own original
  design**: five dedicated courses instead of two.
- **A complete, standalone-shippable `sharia-accounting` path**, and with it, the whole three-plan
  accounting programme complete.
- **The ERP chain's second and final unblock**, at Stage-3/Dangerous-3 (Sharia-specific capability)
  granularity.
- **A defensible licensing posture carried through to the corpus's most legally sensitive
  content** — IAI's strict no-educational-exception posture and AAOIFI's closed-by-default posture
  both bind this plan's range in full.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears the same six roles plan 14's and
plan 15's `brd.md` name, now additionally acting as this three-plan chain's own **verification-debt
closer** (OI-1 through OI-4, all of which are Sharia-specific and land squarely in this plan's own
scope) and **final retest coordinator** for `sharia-accounting`'s own Rule-15 dispatch.

Consuming agents: `apps-ayokoding-www-annotated-concept-maker` (two of this plan's five courses: #20,
\#23), `apps-ayokoding-www-by-example-maker` (the remaining three: #21, #22, #24), their matching
checkers and fixers, `apps-ayokoding-www-general-maker`, `apps-ayokoding-www-facts-checker`,
`apps-ayokoding-www-link-checker`, `web-researcher` (the residual OI-1/OI-2/OI-3 resolution work),
`apps-ayokoding-www-deployer`, and the three live-site testers for this plan's own Rule-15 retest
[Repo-grounded — each verified present under `.claude/agents/`].

## Business-Level Success Metrics

- **`sharia-accounting.json` grown from 19 to 24 entries** (observable): the file holds exactly 24
  IDs, the last five of which are this plan's own courses.
- **`conventional-accounting.json` is provably untouched by this plan** (observable):
  `git diff --quiet -- conventional-accounting.json` exits 0, measured from plan 15's own merge
  point to this plan's own end.
- **Five course bundles resolve** (observable): each of courses #20–#24 resolves to a directory
  under `content/en/learn/courses/`.
- **The silent-failure requirement is met for all five courses** (observable): every course
  #20–#24 carries an explicit "what still balances while being wrong" section.
- **Zero laundered verification claims** (observable): at this plan's Phase 2 gate, no
  `[Needs Verification]` marker is unaccounted for — every one still standing is named, with a
  reason, in this plan's own tech-docs. **OI-2 (the riba doctrinal basis) remains explicitly OPEN**
  — never restated as resolved.
- **Three jurisdictional models, not one** (observable): every Sharia-specific course that
  discusses standards names AAOIFI, PSAK Syariah **and** MFRS-plus-BNM, and none describes AAOIFI
  as "the" standard.
- **The Stage-3 signal is recorded with a real, verifiable commit** (observable).
- **`sharia-accounting` passes its full Rule-15 retest** (observable): every EWT/UWT/DWT finding
  against that landing and its 24-course walk is resolved or explicitly deferred with recorded
  permission.
- **No regressions** (observable): `ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **Courses #1–#19.**
- **Any edit to `conventional-accounting.json`, its landing, or its unit test.**
- **Any ERP content.**
- **Any structural `_index.md` under `paths/`.**
- **Accountancy certification coverage, tax jurisdiction depth, corporate finance.**
- **An Indonesian mirror of either path.**
- **Building a system, anywhere in the corpus (A6).**
- **A Rule-15 retest for `conventional-accounting`** — already run, in plan 15.
- **Resolving OI-2 (the riba doctrinal basis) as settled fact.** A4 forbids it regardless of any
  research pressure to close every open item; the corpus scopes around the unresolved claim
  instead.

## Business Risks and Mitigations

| Risk                                                                                                                 | Mitigation                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AAOIFI is presented as "the" Sharia accounting standard.**                                                         | Three jurisdictional models are a stated content invariant across every Sharia-specific course, re-asserted at the Phase 4 gate.                                                                                                                                |
| **An `[Unverified]` research claim (especially OI-2's riba doctrine) is restated as fact.**                          | This plan's own Phase 2 gates the entire Sharia stage; OI-2's `OPEN` status is verified, not assumed, at every later gate; `apps-ayokoding-www-facts-checker` runs on every body.                                                                               |
| **`conventional-accounting.json` is accidentally touched by this plan's own manifest-growth work.**                  | The Phase 3 and Phase 4 gates (the phases that touch or verify the manifests) explicitly assert `git diff --quiet -- conventional-accounting.json`, a falsifiable clause specific to this plan's own risk profile; no later phase touches either manifest file. |
| **Licensing exposure (A8)** — IAI's strictest-of-four posture and AAOIFI's closed-by-default posture.                | The eleven safe-authoring rules bind every course; every chart of accounts is originally authored; a Phase 4 reading audit runs specifically against this plan's five courses.                                                                                  |
| **A course teaches a plausible, silently wrong model** (murabaha-as-interest is the headline risk).                  | Every course carries the mandatory silent-failure section; course #21 explicitly contrasts murabaha against a conventional amortising loan.                                                                                                                     |
| **Deferring `conventional-accounting`'s own retest earlier (to plan 15) leaves this plan's retest scope ambiguous.** | Scoped explicitly: this plan's retest covers `sharia-accounting` only, and that scoping is stated in README.md, not silent.                                                                                                                                     |
| **Scope collision with the library or with plans 14/15's own course ranges.**                                        | Each course's overview states its scope boundary; the Phase 3 gate asserts exactly 5 new course directories exist, never more.                                                                                                                                  |
| **Cross-plan file collision** — this plan editing a file plan 14 or plan 15 already owns.                            | Ownership is scoped to exactly one manifest data file (`sharia-accounting.json`) plus its test; `conventional-accounting.json` and its test are read-only to this plan.                                                                                         |
