---
title: "Valid Commit Types"
description: The full table of commit types with examples, and a detailed description of what each type covers.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when choosing which commit type (feat, fix, docs, etc.) applies to a change.
---

# Valid Commit Types

The project uses the following types based on [Angular's commit convention](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#type) (verified 2026-02-08):

| Type       | Purpose                                     | Example                                                |
| ---------- | ------------------------------------------- | ------------------------------------------------------ |
| `feat`     | New feature                                 | `feat(auth): add two-factor authentication`            |
| `fix`      | Bug fix                                     | `fix: prevent race condition on startup`               |
| `docs`     | Documentation changes                       | `docs: update API reference`                           |
| `style`    | Code style changes (formatting, whitespace) | `style: remove unused imports`                         |
| `refactor` | Code refactoring (no behavior change)       | `refactor(parser): extract common logic`               |
| `perf`     | Performance improvement                     | `perf: optimize database query`                        |
| `test`     | Test changes                                | `test: add unit tests for auth module`                 |
| `build`    | Build system or external dependency changes | `build(nx): wire namedInputs for cache invalidation`   |
| `chore`    | Other changes to tooling or housekeeping    | `chore: update dependencies`                           |
| `ci`       | CI/CD configuration changes                 | `ci: add GitHub Actions workflow`                      |
| `revert`   | Revert a previous commit                    | `revert: feat(auth): remove two-factor authentication` |

## Type Descriptions

**`feat`** - A new feature for the user (not a new feature for build script)

- Adds new functionality
- User-facing changes
- May include internal changes to support the feature

**`fix`** - A bug fix for the user (not a fix to a build script)

- Resolves incorrect behavior
- Patches security vulnerabilities
- Fixes regression issues

**`docs`** - Documentation only changes

- README updates
- Code comments
- API documentation
- Inline documentation

**`style`** - Changes that don't affect code meaning

- Formatting (indentation, whitespace)
- Missing semicolons
- Code style adjustments
- Not CSS changes (those are `feat` or `fix`)

**`refactor`** - Code restructuring without behavior change

- Improving code structure
- Extracting functions
- Renaming for clarity
- No functional changes

**`perf`** - Performance improvements

- Optimization changes
- Reducing computation time
- Improving memory usage
- Measurable performance gains

**`test`** - Adding or correcting tests

- New test cases
- Fixing broken tests
- Improving test coverage
- Test refactoring

**`build`** - Build system or external dependency changes

- Build tool configuration
- Dependency manifests and lockfiles
- Compilation and packaging setup

**`chore`** - Maintenance tasks

- Release preparation
- Tooling changes
- Housekeeping that touches neither source nor tests

**`ci`** - Continuous Integration changes

- GitHub Actions
- Build pipelines
- Deployment scripts
- CI configuration

**`revert`** - Reverting previous commits

- Undoing changes
- Rolling back features
- Include original commit reference
