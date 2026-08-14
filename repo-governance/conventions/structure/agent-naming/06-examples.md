---
title: "Agent Naming Convention — Examples"
description: Current agents grouped by role, illustrating scope/qualifier/role decomposition for each conforming filename.
when_to_use: Use when you need worked examples of conforming agent filenames grouped by role.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# Examples

Current agents, grouped by role, all conforming to the rule:

- **`maker`** — `docs-maker` (scope `docs`, no qualifier, role `maker`), `apps-ayokoding-www-by-example-maker` (scope `apps`, qualifiers `ayokoding-web-by-example`, role `maker`)
- **`checker`** — `plan-checker` (scope `plan`, role `checker`), `plan-execution-checker` (scope `plan`, qualifier `execution`, role `checker`), `swe-code-checker` (scope `swe`, qualifier `code`, role `checker`)
- **`fixer`** — `plan-fixer` (scope `plan`, role `fixer`), `swe-ui-fixer` (scope `swe`, qualifier `ui`, role `fixer`)
- **`dev`** — `swe-rust-dev` (scope `swe`, qualifier `rust`, role `dev`), `swe-e2e-dev` (scope `swe`, qualifier `e2e`, role `dev`)
- **`deployer`** — `apps-ayokoding-www-deployer` (scope `apps`, qualifiers `ayokoding-web`, role `deployer`)
- **`manager`** — `docs-file-manager` (scope `docs`, qualifier `file`, role `manager`)
- **`tester`** — `web-exploratory-tester` (scope `web`, qualifier `exploratory`, role `tester`), `web-usability-tester` (scope `web`, qualifier `usability`, role `tester`), `web-design-tester` (scope `web`, qualifier `design`, role `tester`)
- **`researcher`** — `web-researcher` (scope `web`, no qualifier, role `researcher`)
