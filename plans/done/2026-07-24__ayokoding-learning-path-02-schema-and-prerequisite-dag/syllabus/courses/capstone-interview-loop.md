# Capstone: Interview Loop (Interview milestone, Python + prose)

**Course ID**: `capstone-interview-loop` · **Kind**: Interview milestone · **Language**: Python +
prose. **NEW** — an interview phase without a capstone breaks the every-phase-has-a-capstone rhythm;
a full mock loop is the natural cement.

**Scope note**: the Phase 1 milestone bundle — a **complete simulated interview loop** integrating
everything the Interview Preparation phase teaches: a coding round (`coding-interview`), a take-home +
live round (`take-home-and-live-coding`), a system-design round (`system-design-interview`), and a
behavioral/leadership round including the layoff/gap narrative
(`behavioral-and-leadership-interviews`), drawing on the interview-facing fundamentals (DS&A, advanced
algorithms, OOP, OO design, SQL, technical communication). It proves the experienced re-entrant can
walk a full loop end to end and self-diagnose.

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

- **Prior courses**: all of Phase 1 (`just-enough-python` through `behavioral-and-leadership-interviews`
  — see [README.md](./README.md) for the full course catalog), and especially the four NEW interview
  courses (`coding-interview`, `take-home-and-live-coding`, `system-design-interview`,
  `behavioral-and-leadership-interviews`).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x + `pytest`; `git`; a timer; a plain
  editor driven without autocomplete for the mock coding/live rounds; a story bank document.
- **Assumed knowledge**: each round's rubric and technique from its course; the reader's own real work
  history for the behavioral stories.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — the multi-round loop structure (recruiter → coding × 1–2 → system design → behavioral,
  in varying orders) is **stable, vendor-independent** practice; keep specific company formats
  illustrative and `[Needs Verification]`.

## Concepts integrated

This capstone does not introduce new concepts; it integrates the Phase 1 courses' concepts under
realistic loop conditions:

- [ ] Coding round: clarify → plan+Big-O → code → verify, ≥ 2 patterns (`coding-interview` co-01–co-24).
- [ ] Take-home + live round: scoped tested deliverable + narrated incremental live build
      (`take-home-and-live-coding` co-01–co-22).
- [ ] System-design round: full spine + one deep dive + bottlenecks + trade-offs
      (`system-design-interview` co-01–co-22).
- [ ] Behavioral round: STAR story bank + leadership dimensions + layoff/gap narrative
      (`behavioral-and-leadership-interviews` co-01–co-22).
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

## In which paths

- `interview-ready/software-engineer` — Phase 1 · Interview preparation (through senior).
- `immediately-effective/software-engineer` — Optional tail · Ready to job-hunt? (bridge into the interview courses) — optional deepening tail, not in the required spine.
- `fundamentally-strong/software-engineer` — Optional tail · Ready to job-hunt? (bridge into the interview courses) — optional deepening tail, not in the required spine.

---

← Back to [README.md — course library catalog](./README.md)
