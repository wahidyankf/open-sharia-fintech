---
title: "Type Vocabulary"
description: The five valid workflow type tokens (quality-gate, execution, setup, planning, grooming), their semantics, and disambiguation notes for composed workflows and planning-vs-execution
when_to_use: Read this when picking or validating the type token (last segment) of a workflow filename, or distinguishing planning from execution workflows.
category: explanation
subcategory: conventions
tags:
  - workflows
  - naming
  - conventions
created: 2026-04-17
---

# Type Vocabulary

Exactly one of the following tokens MUST appear as the last token of every workflow filename:

| Type           | Semantics                                                                                                                                                                                                                                                                                                                                                                                                 | Example workflows                                            |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `quality-gate` | Iterative maker → checker → fixer loop that terminates on a zero-finding condition (usually two consecutive clean audits)                                                                                                                                                                                                                                                                                 | `ci-quality-gate`, `plan-quality-gate`, `specs-quality-gate` |
| `execution`    | Executes a defined procedure or plan against inputs; no iterative fix loop; success is defined by the procedure completing                                                                                                                                                                                                                                                                                | `plan-execution`                                             |
| `setup`        | One-time environment, tooling, or resource provisioning; idempotent on re-run but not iterative in the maker/checker/fixer sense                                                                                                                                                                                                                                                                          | `development-environment-setup`                              |
| `planning`     | Surveys/analyzes repository or domain state and produces a plan in `plans/` (backlog or in-progress) as its terminal deliverable; a single forward procedure that completes when the validated plan exists and never implements it                                                                                                                                                                        | `repo-dependency-bump-planning`                              |
| `grooming`     | Recurring sweep/reorganization workflow over already-existing documentation or artifact state (the Scrum "backlog grooming" analogy); does not converge to zero findings (unlike `quality-gate`), does not produce a new plan as terminal deliverable (unlike `planning`), and is not one-time provisioning (unlike `setup`) — it re-sweeps and re-organizes existing docs on a stated cadence or trigger | `plan-ideas-grooming`                                        |

No other type suffixes are permitted. Introducing a new type requires amending this table first.

**Note on composed workflows**: A workflow step can be an agent, a procedure, or another workflow (nested). The type suffix describes the execution model of the workflow as a whole, not the nature of its individual steps. A `quality-gate` workflow may orchestrate sub-workflows internally; it still carries the `quality-gate` suffix because that describes its overall iterative loop-to-zero-findings model.

**Note on `planning` vs `execution`**: A `planning` workflow performs domain analysis to decide WHAT a future plan should contain, then typically delegates the generic plan-authoring lifecycle (grill → research → write → gate → push) to `plan-planning`; its deliverable is a plan document in `plans/`. `plan-planning` is itself a `planning` workflow — the generic plan-authoring lifecycle whose terminal deliverable is a validated plan in `plans/`; domain-specific `planning` workflows run their own survey/analysis and feed that lifecycle. An `execution` workflow, by contrast, runs a fixed defined procedure against inputs and is distinguished by completing that procedure rather than producing a plan as its deliverable.
