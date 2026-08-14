---
title: "Docs"
description: "Agents that create, check, fix, and manage docs/ documentation, tutorials, and file organization."
---

# Docs

- [Docs Checker](./docs-checker.md) — Expert at validating factual correctness and content consistency of documentation using web verification. Checks technical accuracy, detects contradictions, validates examples and commands, and identifies outdated information. Use when verifying technical claims, checking command syntax, detecting contradictions, or auditing documentation accuracy.
- [Docs File Manager](./docs-file-manager.md) — Expert at managing files and directories in docs/ directory. Use for renaming, moving, or deleting files/directories while maintaining kebab-case conventions, fixing links, and preserving git history.
- [Docs Fixer](./docs-fixer.md) — Applies validated fixes from docs-checker audit reports. Re-validates factual accuracy findings before applying changes. Use after reviewing docs-checker output.
- [Docs Link Checker](./docs-link-checker.md) — Validates both external and internal links in documentation files to ensure they are not broken. Maintains a cache of verified external links in docs/metadata/external-links-status.yaml (the ONLY cache file) with automatic pruning and mandatory lastFullScan updates on every run. HARD REQUIREMENT - cache file usage is mandatory regardless of how this agent is invoked (spawned by other agents, processes, or direct invocation). Use when checking for dead links, verifying URL accessibility, validating internal references, or auditing documentation link health.
- [Docs Maker](./docs-maker.md) — Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.
- [Docs Software Engineering Separation Checker](./docs-software-engineering-separation-checker.md) — Validates software engineering documentation separation between OSE Platform style guides (docs/explanation/) and AyoKoding educational content (apps/ayokoding-www/). Ensures NO DUPLICATION between platforms, proper prerequisite statements, and style guide focus on repository-specific conventions only (not language tutorials).
- [Docs Software Engineering Separation Fixer](./docs-software-engineering-separation-fixer.md) — Applies validated fixes from docs-software-engineering-separation-checker audit reports. Fixes missing prerequisite statements, removes duplicated educational content from style guides, and ensures docs/explanation focuses on repository-specific conventions only. Re-validates findings before applying changes.
- [Docs Tutorial Checker](./docs-tutorial-checker.md) — Validates tutorial quality focusing on pedagogical structure, narrative flow, visual completeness, hands-on elements, and tutorial type compliance. Complements docs-checker (accuracy) and docs-link-checker (links).
- [Docs Tutorial Fixer](./docs-tutorial-fixer.md) — Applies validated fixes from docs-tutorial-checker audit reports. Re-validates pedagogical findings before applying changes. Use after reviewing docs-tutorial-checker output.
- [Docs Tutorial Maker](./docs-tutorial-maker.md) — Creates and updates tutorial documentation following Diátaxis framework and tutorial conventions
