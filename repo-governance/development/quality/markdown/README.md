---
title: "Markdown Quality Standards"
description: "Automated markdown linting and formatting standards using Prettier and markdownlint-cli2"
when_to_use: "Read this index to find the right Markdown Quality Standards child document."
---

# Markdown Quality Standards

- [Overview](./01-overview.md) — The two tools (Prettier, markdownlint-cli2) that maintain markdown quality. Use when orienting to which tool owns a markdown quality concern.
- [Tools](./02-tools.md) — Version, config file, ignore patterns, and triggers for Prettier and markdownlint-cli2. Use when checking which config or script controls markdown formatting or linting.
- [Running Linting Locally](./03-running-linting-locally.md) — npm commands to check and auto-fix markdown lint/format violations locally. Use when you need to check or fix markdown violations before committing.
- [Enabled Rules](./04-enabled-rules.md) — The structural, formatting, link, and code markdownlint rules enforced here. Use when checking which markdownlint rule is active and why.
- [Disabled Rules](./05-disabled-rules.md) — The markdownlint rules intentionally disabled, and why each is off. Use when confirming whether a markdownlint rule was deliberately disabled.
- [Common Violations and Fixes](./06-common-violations-and-fixes.md) — Before/after examples for common markdown violations. Use when fixing a markdown lint violation and you want a concrete example.
- [Git Hooks](./07-git-hooks.md) — What pre-commit and pre-push do for markdown, and where configured. Use when a markdown git hook misbehaves or you need its config location.
- [Coding Agent Hook Integration](./08-coding-agent-hook-integration.md) — The PostToolUse hook that formats/lints markdown after Edit/Write, and its jq requirement. Use when the markdown auto-format hook is not firing.
- [Configuration Details](./09-configuration-details.md) — Files touched by markdown-quality setup, and directories excluded from it. Use when auditing which files or directories implement markdown quality tooling.
- [Troubleshooting](./10-troubleshooting.md) — Fixes for a blocked push, a silent hook, and a violation backlog. Use when a markdown quality gate blocks you and you need a diagnostic path.
- [Related Documentation](./11-related-documentation.md) — Cross-references to the conventions markdown quality tooling enforces. Use when you need the rationale behind a specific markdown quality rule.
- [Maintenance](./12-maintenance.md) — How to update markdownlint rules and the Prettier/markdownlint-cli2 dependencies. Use when changing a rule or bumping a markdown-tooling dependency.
- [Metrics](./13-metrics.md) — Repository-wide violation counts from the markdown-quality rollout. Use when you need the historical baseline for the markdown-quality rollout.
- [Principles and Conventions Implemented/Respected](./14-principles-and-conventions-implemented-respected.md) — How markdown tooling implements core principles and aligns with related conventions. Use when tracing markdown quality tooling to the principles/conventions it implements.
- [Archive Exclusion](./15-archive-exclusion.md) — Why plans/done/ and archived/ are excluded from markdown linting. Use when deciding whether archived content should be linted.
