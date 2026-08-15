---
title: "Capstone overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Complete one small take-home and one self-run live round over the same fictional task-record domain. The take-home is a scoped, documented, testable command-line deliverable. The live round is an incremental build with a narrated transcript and green checkpoints. Both must be self-scored against visible evidence.

## Concepts exercised

- [x] turn a brief into explicit scope, requirements, and a reviewer-friendly structure (co-01 through co-04)
- [x] make a clean-checkout artifact, tests, restrained dependencies, and coherent history visible (co-05 through co-08)
- [x] document trade-offs, validation, readability, time boundary, and final review (co-09 through co-12, co-22)
- [x] ask, narrate, accept a steer, preserve runnable increments, and use the shell fluently (co-13 through co-17)
- [x] reproduce and repair a defect, surface assumptions, deliver incrementally, and handle uncertainty honestly (co-18 through co-21)

## Ordered artifacts

1. [Take-home README](./take-home/README.md) — follow the brief, run instructions, decisions, and tests. The `briefcheck.py` program has input validation and deterministic output; `test_briefcheck.py` covers happy, boundary, and error paths.
2. [Live transcript](./live/transcript.md) — rehearse a partner-visible build. Its checkpoints correspond to the small, original code and tests in `live/code/`.
3. [Score sheet](./scoresheet.md) — score take-home and live work separately. A score without a command result, file, transcript line, or concrete repair is incomplete.

## Acceptance criteria

- From `learning/capstone/take-home`, `pytest -q` passes and the program follows the README command without dependencies beyond Python and pytest.
- From `learning/capstone/live/code`, `pytest -q` passes; `transcript.md` shows a clarification, a green minimal slice, a received steer, a reproduced bug, and a green repair.
- The score sheet rates every listed axis with evidence and one next action.

## Suggested execution

Treat the supplied solution as a reference artifact, not a memorization target. First write your own brief checklist and predicted error paths. Then rerun the test suite after every meaningful change. In a real interview, replace this fictional domain with the given prompt and respect its actual instructions and time cap.

← Previous: [Review and recovery examples](../review-and-recovery-examples.md) · Next: [Drilling](../../drilling/overview.md) →
