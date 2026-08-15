---
title: "Drilling overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q1 (co-01, co-02).** What is the first deliverable after reading a take-home brief?

<details>
<summary>Answer</summary>

Turn each explicit requirement into a check, list assumptions that need clarification, and mark what is not requested. The smallest complete solution to that list is better evidence than a broad, unfinished architecture.

</details>

**Q2 (co-03 through co-08).** What should a reviewer be able to find and run quickly?

<details>
<summary>Answer</summary>

An obvious entry point, focused modules, tests, README run and test commands, decisions and trade-offs, and only justified dependencies. A clean shell should follow those commands without hidden setup; a cohesive Git history makes the work easier to audit.

</details>

**Q3 (co-09 through co-12).** Which limitations should be documented rather than hidden?

<details>
<summary>Answer</summary>

State deliberately deferred work, assumptions, validation boundaries, and what additional time would buy. Make errors actionable and code readable; a documented proportionate cut demonstrates judgment rather than a missing feature.

</details>

**Q4 (co-13 through co-17).** What makes a live round collaborative?

<details>
<summary>Answer</summary>

Ask clarifying questions, narrate intent and invariant, pause for the partner, accept a useful steer, preserve a runnable minimum slice, and use a simple edit/run/test loop fluently. It is pairing, not a silent attempt to impress.

</details>

**Q5 (co-18 through co-22).** What is a credible recovery when a test fails or you do not know an answer?

<details>
<summary>Answer</summary>

Reproduce the smallest failure, state a hypothesis, isolate the boundary, repair it, and rerun the focused suite while narrating. If knowledge is missing, name what you would verify and offer a safe scoped alternative. Finish with a clean run, README reread, diff skim, and explicit next step.

</details>

## Calculation practice

1. A 120-minute brief has core parsing (25 min), tests (25), README/decisions (15), review (15), and an optional export (40). Allocate a protected review reserve and decide whether the optional export belongs before the core is proven.
2. A parser has 18 required examples: 12 happy, 4 edge, 2 error. Calculate the percentage split, then explain why the score is not a coverage target by itself.
3. A live round is 45 minutes. Budget clarification, a first green slice, tests, one extension, recovery reserve, and closeout. Name what should be cut first if time slips.

## Scenario judgment

The brief asks for a command that summarizes a local file. A candidate adds an HTTP service, ORM, retry queue, and a dashboard, but has no README and one broken test. Decide what to do with ten minutes remaining.

<details>
<summary>Reasoned answer</summary>

Stop expanding. Restore the smallest command that satisfies the actual brief, make the test suite pass, document exact run/test commands, and state the larger design as deferred only if it clarifies a real trade-off. The additional systems create setup and review surface without proving the requested outcome.

</details>

## Design exercise

Write a one-page plan for a fictional “deduplicate contacts in a local CSV” take-home. Include a requirements checklist, explicit non-goals, tree, run and test commands, three tests (happy, edge, error), a time-box, a two-commit history, and a final review checklist. Then script the first five minutes of a live pair version: questions, minimal slice, narration, and the pause where you invite a steer.

## Code kata

From `learning/capstone/take-home`, add a fully type-annotated `record_count(lines)` function that returns the count of valid non-blank records while preserving the existing error behavior. Add tests for a blank line and malformed input. Do not add a dependency, network I/O, database, credential, or hidden setup step. From `learning/capstone/live/code`, explain aloud why `add_ticket` returns a new list before you modify it.

## Automaticity checklist

- [ ] I translate a brief into requirements, assumptions, and explicit non-goals before coding.
- [ ] I choose the smallest complete slice and reserve time for testing, README, and review.
- [ ] I can make a fresh shell run and test the deliverable from documented commands alone.
- [ ] I test a happy path, an edge, and a meaningful error path with actionable validation.
- [ ] I use small, cohesive commits and can explain the decision behind each.
- [ ] I document a trade-off or cut rather than quietly leaving it ambiguous.
- [ ] I ask questions, narrate intent, invite a steer, and keep the live code runnable.
- [ ] I reproduce and isolate a failure before changing code, and say what I would look up rather than bluff.
- [ ] I close with a clean run, README reread, diff review, evidence-backed self-score, and next action.
