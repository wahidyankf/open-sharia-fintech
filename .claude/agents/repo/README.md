---
title: "Repo Governance"
description: "Repository-wide agents: rules and workflow governance, harness-compatibility parity, and plan Phase-0 setup."
---

# Repo Governance

- [Repo Harness Compatibility Checker](./repo-harness-compatibility-checker.md) — Validates cross-vendor parity invariants (Phase 0, deterministic) and detects external drift between each supported coding-agent harness's current upstream configuration conventions and the platform-binding catalog (Phase 1, web-research-backed). Emits a combined dual-labelled audit report to local-tmp/harness-compat/.
- [Repo Harness Compatibility Fixer](./repo-harness-compatibility-fixer.md) — Applies validated fixes from a repo-harness-compatibility-checker audit report. Auto-remediates Phase 0 parity sync drift (Invariant 3 via npm run generate:bindings) and Phase 1 catalog/binding updates. Also updates specs/apps/rhino/ when harness changes alter documented CLI behaviour. Flags all other findings for human resolution.
- [Repo Rules Checker](./repo-rules-checker.md) — Validates repository-wide consistency including file naming, linking, emoji usage, convention compliance, agent-to-agent duplication, agent-Skill duplication, Skill-to-Skill consolidation opportunities, and rules governance (contradictions, inaccuracies, inconsistencies). Outputs to local-tmp/repo-rules/ with progressive streaming.
- [Repo Rules Fixer](./repo-rules-fixer.md) — Applies validated fixes from repository rules audit reports including agent-Skill duplication removal, Skills coverage gap remediation, rules governance fixes (contradictions, inaccuracies, inconsistencies), licensing convention fixes, and software-documentation fixes.
- [Repo Rules Maker](./repo-rules-maker.md) — Creates repository rules and conventions in repo-governance/ directories. Documents standards, patterns, and quality requirements.
- [Repo Setup Manager](./repo-setup-manager.md) — Executes Phase 0 of any plan delivery checklist: installs dependencies, converges the polyglot toolchain via npm run doctor, runs baseline tests for projects in scope, and resolves all preexisting failures before plan work begins. Use at the start of every plan execution to establish a clean, known-good baseline.
- [Repo Workflow Checker](./repo-workflow-checker.md) — Validates workflow documentation quality and compliance with workflow pattern convention.
- [Repo Workflow Fixer](./repo-workflow-fixer.md) — Applies validated fixes from workflow-checker audit reports. Re-validates before applying changes.
- [Repo Workflow Maker](./repo-workflow-maker.md) — Creates workflow documentation in repo-governance/workflows/ following workflow pattern convention.
