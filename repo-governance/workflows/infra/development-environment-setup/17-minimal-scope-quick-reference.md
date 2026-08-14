---
title: "Minimal Scope Quick Reference"
description: "Table mapping scope=minimal to the specific phases/steps and tools it installs (core TypeScript/Go development only)."
when_to_use: "Use when you only need a minimal environment for TypeScript/Go work, not the full polyglot toolchain."
---

# Minimal Scope Quick Reference

For `scope: minimal` (core development only — TypeScript/Go projects, git hooks, unit tests):

| Phase | Steps     | Tools Installed                  |
| ----- | --------- | -------------------------------- |
| 1     | 1.1-1.2   | Homebrew                         |
| 2     | 2.1-2.3   | Git, Docker, jq                  |
| 3     | 3.1-3.2   | Volta, Node.js 24, npm           |
| 5     | 5.1       | Go                               |
| 11    | 11.1-11.4 | npm deps, env restore, git hooks |
| 12    | 12.1      | Playwright browsers              |
| 13    | 13.1-13.2 | Verification                     |

This covers: pre-commit hooks, pre-push hooks, TypeScript/Go unit tests, and basic E2E tests.
