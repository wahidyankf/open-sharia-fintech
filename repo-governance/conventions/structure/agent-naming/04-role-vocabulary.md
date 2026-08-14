---
title: "Role Vocabulary"
description: The closed set of role tokens that MUST appear as the last token of every agent filename.
when_to_use: Use when choosing (or adding) the role token for a new agent filename.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# Role Vocabulary

Exactly one of the following tokens MUST appear as the last token of every agent filename:

| Role         | Semantics                                                                        | Example agents                                                        |
| ------------ | -------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `maker`      | Produces a content or research artifact                                          | `docs-maker`, `docs-tutorial-maker`                                   |
| `checker`    | Validates an artifact against standards                                          | `plan-checker`, `plan-execution-checker`, `swe-code-checker`          |
| `fixer`      | Applies validated checker findings                                               | `plan-fixer`, `swe-ui-fixer`                                          |
| `dev`        | Writes code in a language or test framework                                      | `swe-rust-dev`, `swe-e2e-dev`                                         |
| `deployer`   | Deploys an application to an environment                                         | `apps-ayokoding-www-deployer`                                         |
| `manager`    | Performs file or resource operations (rename, move, delete)                      | `docs-file-manager`                                                   |
| `tester`     | Explores or evaluates a running system or live site and reports defects/friction | `web-exploratory-tester`, `web-usability-tester`, `web-design-tester` |
| `researcher` | Gathers and verifies external information; read-only research                    | `web-researcher`                                                      |

No other role suffixes are permitted. Introducing a new role requires amending this table first.
