---
description: "What file types this rule applies to, and the two exclusions (.env files and .gitignore entries)."
when_to_use: "Use when checking whether this rule applies to a specific file type."
---

# Scope

This rule applies to:

- All source code files
- All test files and test fixtures
- All configuration files (including Nx project.json, nx.json, docker-compose files)
- All shell scripts and CI workflow files
- All documentation committed to the repository

It does not apply to:

- `.env` files (which must be gitignored)
- Files listed in `.gitignore` (they are not committed)
