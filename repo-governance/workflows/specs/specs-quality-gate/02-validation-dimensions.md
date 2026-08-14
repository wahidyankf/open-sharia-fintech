---
title: "Specs Quality Gate — Validation Dimensions"
description: "Lists the nine validation categories the specs-checker enforces and which categories are offloaded to deterministic rhino-cli subcommands versus LLM reasoning."
when_to_use: "Use when checking exactly what a specs-quality-gate audit report is scoring, or which rhino-cli command backs a given category."
---

# Validation Dimensions

The checker validates nine categories across all spec areas:

| #   | Category                         | What It Checks                                                                                                            | Method                      |
| --- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| 1   | Structural Completeness          | Every directory has README.md                                                                                             | LLM                         |
| 2   | Feature File Inventory           | README counts match actual .feature files and scenarios                                                                   | LLM                         |
| 3   | Gherkin Format Compliance        | Feature headers, user stories, Background steps, naming                                                                   | LLM                         |
| 4   | Cross-Spec Consistency           | Shared domains align between related specs (demo-be ↔ demo-fe)                                                            | LLM                         |
| 5   | C4 Diagram Consistency           | Accessible colors, actor consistency, file references                                                                     | LLM                         |
| 6   | Cross-Reference Integrity        | All markdown links resolve to existing files                                                                              | LLM                         |
| 7   | Spec-to-Implementation Alignment | Spec READMEs reference implementations that exist                                                                         | LLM                         |
| 8   | Spec Tree Shape                  | C4-aware five-folder tree compliance per surface profile (product/, system-context/, containers/, components/, behavior/) | Deterministic via rhino-cli |
| 9   | Adoption Gaps                    | BDD/DDD/Contracts adoption check per surface profile (full-stack, web-only, CLI)                                          | LLM with rhino-cli assist   |

## Deterministic Offload

Category 8 (Spec Tree Shape) is a **deterministic check** owned by
`rhino-cli specs <subcmd>` Rust code (per FR-14 of the App README vs Specs Convention). Agents shell
out to these commands rather than re-implementing the check in prompt logic. Category 9 (Adoption
Gaps) uses `rhino-cli specs validate-adoption` for the structural portion and LLM reasoning for
the narrative justification assessment.

Drift detection commands (`drift-routes`, `drift-endpoints`, `drift-contracts`) were removed in
the BDD+DDD tooling gap-fill plan (2026-05) because reservation-pattern stubs that print "Not yet
implemented" mislead callers into believing functionality exists. Reintroduction requires a
dedicated plan implementing real drift logic.

| rhino-cli command                         | Validates                              | Maps to Category |
| ----------------------------------------- | -------------------------------------- | ---------------- |
| `rhino-cli specs validate-tree <app>`     | Five-folder C4-aware tree shape        | 8                |
| `rhino-cli specs validate-counts <app>`   | README count claims vs actual          | 8                |
| `rhino-cli specs validate-links <app>`    | Markdown link integrity                | 6                |
| `rhino-cli specs validate-adoption <app>` | BDD/DDD/Contracts adoption per profile | 9 (partial)      |

Agents MUST NOT re-implement these checks with file-glob heuristics or LLM inference when the
`rhino-cli` command exists. If the command is unavailable (pre-implementation), mark the finding
as `[rhino-cli pending]` and skip rather than substitute a weaker heuristic.
