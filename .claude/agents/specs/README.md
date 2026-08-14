---
title: "Specs"
description: "Agents that create and validate specs/ Gherkin feature areas and structure."
---

# Specs

- [Specs Checker](./specs-checker.md) — Validates explicitly listed specs/ folders (and their subfolders) for structural completeness, content accuracy, internal consistency, and cross-folder coherence. Use when auditing specification quality or before major spec refactors.
- [Specs Fixer](./specs-fixer.md) — Applies validated fixes from specs-checker audit reports for explicitly listed spec folders. Re-validates findings before applying. Use after reviewing specs-checker output.
- [Specs Maker](./specs-maker.md) — Creates new spec areas, missing README files, and scaffolds Gherkin feature structure at explicitly specified paths under specs/. Use when adding a new app or library to the specs directory.
