# Capstone · Interview Loop (Phase 1 boundary)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
inter-topic capstone · anchored after N=16 · folder weight **265** (`105 + 10 × 16`) · Python +
prose. **NEW** — optional per DN-4 (an interview phase without a capstone breaks the every-phase-has-a-
capstone rhythm; a full mock loop is the natural cement).

**Scope note**: the Phase 1 milestone bundle — a **complete simulated interview loop** integrating
everything the Interview Preparation phase taught: a coding round ([N=9](./09-coding-interview.md)), a
take-home + live round ([N=10](./10-take-home-and-live-coding.md)), a system-design round
([N=14](./14-system-design-interview.md)), and a behavioral/leadership round including the layoff/gap
narrative ([N=16](./16-behavioral-and-leadership-interviews.md)), drawing on the interview-facing
fundamentals (DS&A, advanced algorithms, OOP, OO design, SQL, technical communication). It proves the
experienced re-entrant can walk a full loop end to end and self-diagnose.

## Why this exists · the big idea

- **The problem before the solution**: each interview module drills one round in isolation. A real loop
  is a **stamina and consistency** test — four to five rounds in a day, each with its own register, with
  the layoff/gap question landing somewhere in the middle. Practicing rounds separately does not
  rehearse the transitions, the fatigue, or the cumulative self-presentation.
- **Keep-this-if-you-forget-everything**: run the whole loop under realistic conditions, record it, and
  score it against the rubric for each round — the gap between your rounds is where the offer is won or
  lost, and only a full-loop rehearsal surfaces it.
- **Big ideas touched**: `correctness-vs-pragmatism` (a consistent good loop beats one brilliant round
  and three weak ones), `taming-state` (composure and a prepared story bank carried across a long day).

## Prerequisites

- **Prior topics**: all of Phase 1 — [N=4 Python](./README.md) through
  [N=16 Behavioral & Leadership Interviews](./16-behavioral-and-leadership-interviews.md), and
  especially the four NEW interview modules ([N=9](./09-coding-interview.md),
  [N=10](./10-take-home-and-live-coding.md), [N=14](./14-system-design-interview.md),
  [N=16](./16-behavioral-and-leadership-interviews.md)).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x + `pytest`; `git`; a timer; a plain
  editor driven without autocomplete for the mock coding/live rounds; a story bank document.
- **Assumed knowledge**: each round's rubric and technique from its module; the reader's own real work
  history for the behavioral stories.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — the multi-round loop structure (recruiter → coding × 1–2 → system design → behavioral,
  in varying orders) is **stable, vendor-independent** practice; keep specific company formats
  illustrative and `[Needs Verification]`.

## Concepts integrated

This capstone does not introduce new concepts; it integrates the Phase 1 modules' concepts under
realistic loop conditions:

- [ ] Coding round: clarify → plan+Big-O → code → verify, ≥ 2 patterns
      ([N=9](./09-coding-interview.md) co-01–co-24).
- [ ] Take-home + live round: scoped tested deliverable + narrated incremental live build
      ([N=10](./10-take-home-and-live-coding.md) co-01–co-22).
- [ ] System-design round: full spine + one deep dive + bottlenecks + trade-offs
      ([N=14](./14-system-design-interview.md) co-01–co-22).
- [ ] Behavioral round: STAR story bank + leadership dimensions + layoff/gap narrative
      ([N=16](./16-behavioral-and-leadership-interviews.md) co-01–co-22).
- [ ] Cross-round consistency: composure, communication, and self-presentation carried across the loop.

## Ordered steps

1. `capstone-interview-loop/code/coding-round/` — a timed coding round of two problems (≥ 2 patterns)
   with reasoning transcripts and `pytest`. Verify both suites pass within their budgets and each solve
   records a plan-and-complexity step.
2. `capstone-interview-loop/code/take-home/` + `live/` — a small scoped take-home (README + tests,
   clean-checkout runnable) and a recorded narrated live build with green checkpoints. Verify the
   take-home runs from a clean checkout and the live artifact runs.
3. `capstone-interview-loop/design/walkthrough.md` + a Mermaid diagram — a full system-design round
   covering the spine, one deep dive, a bottleneck, and two trade-offs. Verify every spine step appears.
4. `capstone-interview-loop/behavioral/mock-round.md` — a behavioral round of ≥ 6 STAR answers including
   the layoff/gap probe, drawn from a story bank. Verify each answer is STAR-structured and within time.
5. `capstone-interview-loop/scoresheet.md` — score every round against its module rubric and write a
   diagnosis of the weakest round + a concrete improvement plan. Verify every round is rated and the
   diagnosis names the next action.

## Acceptance criteria

- The coding round's tests pass within budget with visible plan-and-complexity steps; the take-home runs
  from a clean checkout with green tests and a complete README; the live artifact runs with an unbroken
  narrated transcript; the system-design walkthrough covers the full spine with a legible diagram, a
  named bottleneck, and two trade-offs; the behavioral round delivers STAR answers including a calm,
  forward-looking layoff/gap narrative; the score sheet rates every round and names the single highest-
  leverage improvement.

## Done bar

Runnable end-to-end (every code artifact runs; every non-code round produces its scored artifact) +
web-verified.

---

← Previous: [N=16 · Behavioral & Leadership Interviews](./16-behavioral-and-leadership-interviews.md) ·
Next: N=17 `just-enough-typescript` ([index](./README.md)) →
