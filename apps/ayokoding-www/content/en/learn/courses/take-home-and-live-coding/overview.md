---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Prior topics**: [Just Enough Python](/en/learn/courses/just-enough-python), [Just Enough Bash](/en/learn/courses/just-enough-bash), [Version Control & Git](/en/learn/courses/version-control-and-git), and [Coding Interview](/en/learn/courses/coding-interview). Small programs, test execution, a clean shell loop, and incremental commits are assumed rather than taught again.
- **Tools & environment**: a macOS/Linux terminal, Python 3.x, `pytest`, `git`, and a plain editor you can operate without leaning on autocomplete during a shared session.
- **Assumed experience**: this course assumes an engineer who has shipped and reviewed small changes. It is a technique refresh that rehearses how to make that work legible under evaluation; it is not a from-zero Python, testing, Git, or algorithm course.

## Why this exists

The whiteboard-style coding round is only one interview format. A take-home asks for a small, complete, reviewable deliverable under an explicit time boundary. A live or pair-coding session asks you to collaborate under observation: clarify, narrate, accept a useful steer, keep an executable slice alive, and diagnose a failure honestly.

The durable standard is deliberately modest: a take-home should resemble a small production PR you would be comfortable requesting review for. It answers the brief, has an obvious entry point, gives a fresh reader exact run and test commands, exercises the risky path, and names the trade-offs it chose. A live round is pair programming, not a silent speed test.

This is a **By Example · Python** course. The local Python artefacts are deterministic, fully type-annotated, standard-library-only teaching mechanisms. They demonstrate a brief checklist and incremental live checkpoints; they do not send data, invoke a hosted editor, install packages, store credentials, or claim to be a production submission framework.

## Scope boundary

[Coding Interview](/en/learn/courses/coding-interview) drills isolated, synchronous algorithmic problems: pattern selection, invariants, complexity, and a short problem-solving loop. This course drills the surrounding delivery work: scoping a small real-software task, documentation, tests, Git hygiene, review, collaboration, and recovery under a shared editor. Use the two together; neither replaces the other.

This course does not prescribe a vendor, collaborative-editor product, universal take-home time cap, or company rubric. Those vary by employer and region. Read the actual brief, respect its stated limit, and ask before assuming an unstated constraint.

## The delivery loop

1. Restate the brief as observable acceptance checks; identify what is explicitly out of scope.
2. Choose the smallest complete slice, a readable structure, and the fewest justified dependencies.
3. Write the README as the reviewer’s front door, then ensure a clean checkout can follow it.
4. Add a happy-path, edge-case, and error-path test; validate input with messages a user can act on.
5. Commit coherent milestones, record decisions and cuts, and run a final clean review pass.
6. In a live round, ask clarifying questions, narrate intent, treat hints as collaboration, keep each increment runnable, and recover from a wrong turn with evidence rather than bluffing.

## Concept register

- **co-01 to co-04 · answer the actual brief** — literal reading, scope discipline, reviewer-friendly structure, and README-first communication.
- **co-05 to co-08 · reproducible engineering** — clean-checkout execution, judgment-bearing tests, coherent Git history, and dependency restraint.
- **co-09 to co-12 · honest professional judgment** — recorded trade-offs, validation, readability, and time-boxing.
- **co-13 to co-17 · collaborative execution** — pairing, think-aloud reasoning, accepting a steer, green increments, and editor/shell fluency.
- **co-18 to co-22 · recovery and closeout** — narrated debugging, clarifying questions, incremental delivery, a credible “I don’t know,” and the submission review pass.

## Reference reading

- [Python packaging user guide: creating and using virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) — reproducible local setup vocabulary.
- [pytest good practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) — focused test layout and invocation.
- [Git documentation: git commit](https://git-scm.com/docs/git-commit) — the mechanics behind a coherent, reviewable history.
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) — scope, clarity, feedback, and honest trade-offs.

Next: [Learning overview](./learning/overview.md) →
