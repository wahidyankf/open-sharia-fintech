---
title: Code Quality Convention
description: Automated code quality tools (Prettier, Husky, lint-staged, Commitlint) and git hooks
  for consistent formatting and commit message standards
tags:
  - development
  - code-quality
  - prettier
  - husky
  - lint-staged
  - git-hooks
  - automation
category: explanation
subcategory: development
---

# Code Quality Convention

This document explains the automated code quality tools and git hooks used in this repository to maintain consistent code formatting and commit message standards.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Git hooks (Husky) automatically run Prettier and Commitlint before commits. Humans write code, machines enforce formatting and standards. No manual formatting or message validation required.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Prettier uses default settings - no custom configuration file. Commitlint uses standard Conventional Commits spec. Minimal tooling configuration reduces complexity.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Commit Message Convention](../workflow/commit-messages.md)**: Git hooks enforce Conventional Commits format through Commitlint, validating commit message structure before commits are created.

- **[Indentation Convention](../../conventions/formatting/indentation.md)**: Prettier enforces consistent indentation (2 spaces for YAML frontmatter) across all formatted file types.

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: Pre-commit hook formats all files matching the repository's file naming patterns without altering the naming structure.

- **[No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md)**: The hard iron
  rule that no system secret may ever be committed applies to every file touched by this practice —
  source code, config files, hook scripts, and staged content alike. Real secrets belong in
  gitignored `.env*` files; committed files use only placeholders or env-var references.

## Overview

This project enforces code quality through automated tools that run during the development workflow:

- **Prettier** - Automatic code formatting
- **Husky** - Git hooks management
- **Lint-staged** - Run tools on staged files only
- **Commitlint** - Commit message validation (see [Commit Message Convention](../workflow/commit-messages.md))

These tools work together to ensure code consistency and quality without manual intervention.

## Prettier - Code Formatting

**Purpose**: Automatically format code to maintain consistent style across the codebase.

**Supported File Types**:

- JavaScript/TypeScript: `*.{js,jsx,ts,tsx,mjs,cjs}`
- JSON: `*.json`
- Markdown: `*.md`
- YAML: `*.{yml,yaml}`
- CSS/SCSS: `*.{css,scss}`

**When It Runs**: Automatically on staged files before each commit via the pre-commit hook.

**Configuration**: Prettier uses default settings (no custom configuration file). This ensures maximum compatibility and reduces configuration overhead.

**Manual Formatting**: You can manually format files with:

```bash
npx prettier --write [file-path]
```

## Husky - Git Hooks

**Purpose**: Manage git hooks to run automated checks at specific points in the git workflow.

**Hooks Configured**:

- `.husky/pre-commit` - Runs before commit is created
- `.husky/commit-msg` - Runs after commit message is entered
- `.husky/pre-push` - Runs before pushing to remote

**Why Husky**: Ensures all developers have the same git hooks configured automatically after running `npm install`. Hooks are stored in the repository (`.husky/` directory) for version control.

## Lint-staged

**Purpose**: Run linters and formatters only on staged files (not the entire codebase).

**Configuration** (in `package.json`):

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,mjs,cjs}": "prettier --write",
    "*.json": "prettier --write",
    "*.md": "prettier --write",
    "*.{yml,yaml}": "prettier --write",
    "*.{css,scss}": "prettier --write"
  }
}
```

**How It Works**:

1. Identifies files staged for commit (`git add`)
2. Runs Prettier on matching file types
3. Automatically stages formatted files
4. Allows commit to proceed if successful

**Benefits**:

- Faster than running tools on entire codebase
- Only formats files you're committing
- Prevents incorrectly formatted code from being committed

## Git Hook Workflow

### Pre-commit Hook

**Location**: `.husky/pre-commit`

**Execution Order**:

1. You run `git commit`
2. Pre-commit hook triggers (`.husky/pre-commit` — a single `go run` line)
3. `rhino-cli git pre-commit` orchestrates all steps in order, failing fast:

| Step | Trigger                                | Action                                                                       | On failure |
| ---- | -------------------------------------- | ---------------------------------------------------------------------------- | ---------- |
| 1    | `.claude/` or `.opencode/` staged      | Validate → Sync → Validate-sync                                              | exit 1     |
| 2    | `docker-compose.ya?ml` staged          | `docker compose -f <file> config` per file                                   | exit 1     |
| 3    | always                                 | `nx affected -t run-pre-commit --skip-nx-cache`                              | warn only  |
| 4    | always                                 | `git add apps/ayokoding-www/content/`                                        | ignored    |
| 5    | always                                 | `npx lint-staged`                                                            | exit 1     |
| 5b   | `apps/<app>/package.json` staged       | Regenerate + stage `apps/<app>/package-lock.json`                            | exit 1     |
| 6    | `docs/` staged                         | Validate + auto-fix naming, then `git add docs/ repo-governance/ .claude/`   | exit 1     |
| 6m   | staged `.md` files (skip 3 exclusions) | `mermaid:validation` — diagram width, label length, syntax (staged-only)     | exit 1     |
| 6h   | staged `.md` in prose allowlist        | `headings:hierarchy-validation` — single H1, no skipped levels (staged-only) | exit 1     |
| 7    | always                                 | Validate markdown links + `#fragment` anchors (staged only)                  | exit 1     |
| 8    | always                                 | `npm run lint:md`                                                            | exit 1     |

1. Commit proceeds if no errors

**Implementation**: `apps/rhino-cli/src/` — all steps call internal Rust functions directly (no subprocess round-trips for rhino-cli-owned logic); external tools are shelled out via `std::process::Command`.

**`RHINO_CLI_BIN` override**: CI's tier-1 override for the `apps/rhino-cli/scripts/rhino-bin.sh`
shim. Set to an executable path, it is used directly and skips the tier-2 staleness check, so a
stale pinned binary is never detected as stale.

**What It Validates**:

**Configuration Validation** (Added 2026-01-22):

Validates primary and secondary platform binding directory consistency before commit:

1. Detects if binding directories (`.claude/` or `.opencode/`) are in staged files
2. If changed:
   - Validates primary binding directory (`.claude/`) source format (YAML, tools, model, skills)
   - Syncs primary to secondary binding directory (auto-sync)
   - **Mirrors ship in the same commit as their `.claude/` source** — the hook stages them for you; a follow-up "sync commit" publishes a tree where source and mirror disagree ([File-Touch Discipline](../practice/file-touch-discipline.md))
   - Validates secondary binding directory (`.opencode/`) output (semantic equivalence)
3. If unchanged: Skips validation (performance)

**Benefits:**

- Catches config errors before commit (earliest possible)
- Prevents invalid commits from being created locally
- Ensures primary and secondary binding directories stay in sync
- Auto-syncs on commit (no manual step)
- Only runs when config files in staged files (~260ms when needed)

**Markdown:**

- Validates Mermaid diagrams in staged `.md` files (width, label length, syntax) — step 6m
- Validates heading hierarchy in staged prose-allowlist `.md` files (single H1, no skipped levels) — step 6h
- Validates markdown links + `#fragment` anchors in staged files only (fast, targeted) — step 7
- Validates all markdown files meet linting standards (comprehensive) — step 8

**What Happens on Failure**:

- Commit is blocked
- Error message shows which check failed (config, formatting, or markdown)
- Fix the issue and try again

**Example**:

```bash
$ git commit -m "feat: add new feature"
🔍 Validating .claude/ and .opencode/ configuration...
✅ Configuration validation passed
⏭️  Skipping docker-compose validation (no docker-compose.yml changes in staged files)
⏭️  Skipping dotnet formatting (no .cs/.fs files staged)
⏭️  Skipping docs naming validation (no docs/ changes in staged files)
[main abc1234] feat: add new feature
```

### Commit-msg Hook

**Location**: `.husky/commit-msg`

**Execution Order**:

1. Pre-commit hook completes successfully
2. Commit-msg hook triggers
3. Commitlint validates commit message format
4. Commit proceeds if message is valid

**What It Validates**:

- Commit message follows [Conventional Commits](https://www.conventionalcommits.org/)
- See [Commit Message Convention](../workflow/commit-messages.md) for complete rules

**What Happens on Failure**:

- Commit is blocked
- Error message shows what's wrong with the commit message
- Fix the message and try again

**Example**:

```bash
$ git commit -m "added new feature"
⧗   input: added new feature
   subject may not be empty [subject-empty]
   type may not be empty [type-empty]
   found 2 problems, 0 warnings
```

### Pre-push Hook

**Location**: `.husky/pre-push`

**Execution Order**:

1. You run `git push`
2. Pre-push hook triggers
3. Nx detects affected projects since last push
4. `typecheck` runs for each affected project that declares it
5. `lint` runs for each affected project
6. `test:quick` runs for each affected project
7. `specs:coverage` runs for each affected project that declares it
8. Push proceeds if all four gates pass

**What It Validates**:

- **Type correctness** (`typecheck`): Catches type errors in TypeScript, Rust, .NET/F#, and other
  statically typed projects. Projects without a `typecheck` target are silently skipped by Nx.
- **Code quality** (`lint`): Static analysis across all projects (includes static a11y checks via
  oxlint jsx-a11y plugin for TypeScript UI projects). Also enforced remotely in the PR quality gate
  and in all scheduled Test CI workflows.
- **Fast quality gate** (`test:quick`): Unit tests, build smoke tests, or other fast checks
  defined per project. Also enforced remotely as a required GitHub Actions status check before PR
  merge.
- **Spec coverage** (`specs:coverage`): Validates that every Gherkin step in feature files has a
  matching step definition in source code. Compulsory for all apps and E2E runners. Uses
  `rhino-cli specs coverage`.

**What Happens on Failure**:

- Push is blocked
- Error message shows which target and project failed
- Fix the issue and try again

**Example**:

```bash
$ git push origin main

> nx affected -t typecheck

 Running target typecheck for affected projects...
   organiclever-www
 All checks passed

> nx affected -t lint

 Running target lint for affected projects...
   organiclever-www
 All checks passed

> nx affected -t test:quick

 Running target test:quick for affected projects...
   organiclever-www
 All checks passed

> nx affected -t specs:coverage

 Running target specs:coverage for affected projects...
   organiclever-www
 All checks passed

Enumerating objects: 5, done.
[main abc1234] Successfully pushed
```

**Benefits**:

- Prevents broken code from reaching remote repository
- Only runs checks on affected projects (faster than checking everything)
- Catches type errors, lint violations, and test failures before CI/CD
- Nx caching means repeated checks on unchanged code are near-instant

## Bypassing Hooks (Not Recommended)

You can bypass git hooks using `--no-verify`:

```bash
git commit --no-verify -m "message"
```

**WARNING**: Only use this in exceptional circumstances:

- Emergency hotfixes where formatting can be fixed later
- When hooks are malfunctioning (report the issue)
- **NEVER** use this to avoid fixing code quality issues

Bypassing hooks regularly defeats the purpose of automated quality checks.

## Troubleshooting

### Prettier Fails to Format

**Symptom**: Pre-commit hook fails with Prettier errors

**Solutions**:

1. Check if the file has syntax errors (Prettier can't format invalid code)
2. Run Prettier manually to see detailed error: `npx prettier --write [file]`
3. Fix syntax errors, then commit again

### Commitlint Rejects Valid Message

**Symptom**: Commit-msg hook fails but message looks correct

**Solutions**:

1. Verify message follows exact format: `<type>(<scope>): <description>`
2. Check type is lowercase and from valid list
3. Ensure description is in imperative mood
4. See [Commit Message Convention](../workflow/commit-messages.md) for complete rules

### Hooks Not Running

**Symptom**: Git hooks don't execute when committing or pushing

**Solutions**:

1. Run `npm install` to ensure Husky is set up
2. Check `.husky/` directory exists with hook files
3. Verify hook files are executable: `ls -la .husky/`
4. If needed, make executable: `chmod +x .husky/pre-commit .husky/commit-msg .husky/pre-push`

### Pre-push Hook Times Out or Runs Slowly

**Symptom**: Pre-push hook takes too long or times out on large changesets

**Solution** — warm the Nx cache before pushing:

```bash
# Run all four targets first (this warms the cache)
npx nx affected -t typecheck lint test:quick specs:coverage

# Now push — the hook replays from cache (near-instant)
git push
```

**Why this works**: `typecheck`, `lint`, `test:quick`, and `specs:coverage` are all cacheable Nx targets (`cache: true` in `nx.json`). Running them manually stores results in the local Nx cache. When the pre-push hook runs the same targets, Nx replays from cache instead of re-executing — making the hook near-instant regardless of how many projects are affected.

### Tests Fail on Pre-push

**Symptom**: Pre-push hook blocks push due to test failures

**Solutions**:

1. Check which tests failed in the error output
2. Run tests locally: `nx affected -t test:quick`
3. Fix failing tests
4. Commit fixes and push again
5. If tests pass locally but fail in hook, ensure all changes are committed

### Config Validation Fails on Pre-commit

**Symptom**: Pre-commit hook fails with config validation errors

**Solutions**:

1. Identify which step failed:
   - Primary binding directory validation: Fix source files in `.claude/agents/` or `.claude/skills/`
   - Sync: Check rhino-cli output, may be a bug
   - Secondary binding directory validation: Re-run `npm run generate:bindings`

2. Run validation manually to debug:

   ```bash
   npm run validate:claude      # Check .claude/ format
   npm run generate:bindings  # Sync to .opencode/
   npm run validate:opencode    # Check .opencode/ output
   ```

3. Common validation errors:
   - Invalid tool name: Must be Read, Write, Edit, Glob, Grep, Bash, TodoWrite, WebFetch, WebSearch
   - Missing description: All agents/skills need description field
   - Invalid model: Must be empty, or a recognized model identifier (`sonnet`, `opus`, `haiku`)
   - Skill not found: Ensure skill exists in the platform binding skill directory (`.claude/skills/`)

4. Bypass hook temporarily (emergency only):

   ```bash
   git push --no-verify
   ```

   Note: Fix validation errors before merging to main.

## Adding New File Types

To add Prettier formatting for new file types:

1. Update `lint-staged` configuration in `package.json`
2. Add new glob pattern and Prettier command
3. Test with a sample file
4. Commit the configuration change

**Example** (adding a new file type):

```json
{
  "lint-staged": {
    "*.toml": ["prettier --write"]
  }
}
```

## Integration with Development Workflow

### Normal Workflow

```bash
# 1. Make changes to files
vim src/index.ts

# 2. Stage files
git add src/index.ts

# 3. Commit (hooks run automatically)
git commit -m "feat(api): add new endpoint"

# Hooks execute:
#  Prettier formats src/index.ts
#  Commitlint validates message
#  Commit succeeds

# 4. Push to remote (pre-push hook runs)
git push origin main

# Pre-push hook executes:
#  Nx detects affected projects
#  Runs test:quick for affected projects
#  Push succeeds
```

### When Hooks Modify Files

```bash
# 1. Stage and commit
git add src/messy.ts
git commit -m "fix: correct validation logic"

# Prettier formats messy.ts and stages it
# Commit includes formatted version automatically
```

## ayokoding-www Link Validation

Internal links in ayokoding-www content are validated
automatically on every `test:quick` run via `ayokoding-cli links check`.

**Convention:**

- Internal links are validated for correctness
- External links (`http://`, `https://`, `mailto:`) are NOT validated by this tool — use the
  `apps-ayokoding-www-link-checker` AI agent for those
- Same-page anchors (`#section`) are not validated

**Examples:**

```markdown
<!-- Correct internal link -->

[Overview](/en/learn/swe/overview)

<!-- Correct — resolves to _index.md for section pages -->

[Learn](/en/learn)

<!-- Wrong — relative paths break in sidebar/menu contexts -->

[Overview](../overview)

<!-- Wrong — .md extension is not used in internal links -->

[Overview](/en/learn/swe/overview.md)
```

**Validation runs automatically** as part of `test:quick` (pre-push hook and CI):

```bash
# Full quality gate including link check
nx run ayokoding-www:test:quick

# Link check only (standalone)
nx run ayokoding-www:links:check
```

**When broken links are found:**

1. The command exits with code 1 — CI fails
2. Output table shows source file, line number, link text, and broken target
3. Fix by correcting the target path in the source file
4. Re-run `nx run ayokoding-www:links:check` to confirm

**Dependency chain:** `ayokoding-cli:build` → `ayokoding-www:links:check` → `ayokoding-www:test:quick`

## Rust CLI Linting

Rust CLI projects (`apps/ayokoding-cli`, `apps/ose-cli`, `apps/rhino-cli`) use [Clippy](https://github.com/rust-lang/rust-clippy) for static analysis.

**Configuration**: Each project declares lints in its `Cargo.toml` under `[lints.clippy]`. The standard pedantic profile is used with selective allows.

**Standard lint set** (from each project's `Cargo.toml`):

- `pedantic` at `warn` priority -1 (baseline)
- `unwrap_used = "deny"` — no `.unwrap()` in production code
- `panic = "deny"` — no `panic!()` in production code
- `missing_docs = "deny"` / `missing_docs_in_private_items = "deny"` — full doc coverage
- `undocumented_unsafe_blocks = "deny"` — every `unsafe` block must have a comment
- `unsafe_code = "forbid"` (in `[lints.rust]`) — no unsafe code at all

**Usage**:

```bash
# Run via Nx (standard)
nx lint ayokoding-cli
nx lint ose-cli
nx lint organiclever-be

# Run directly
cargo clippy --manifest-path apps/ayokoding-cli/Cargo.toml --all-targets -- -D warnings
```

## Language-Specific Auto-Formatters

The following language-specific formatters run automatically as part of the pre-commit hook or CI pipeline:

| Language  | Tool            | Trigger                  |
| --------- | --------------- | ------------------------ |
| Rust      | `rustfmt`       | Pre-commit (lint-staged) |
| F\# / C\# | `dotnet format` | Pre-commit hook step     |

Each formatter uses its language's standard style conventions. No custom configuration is applied
unless a project-specific config file exists (e.g., `rustfmt.toml`, `.editorconfig`).

## Best Practices

1. **Trust the Tools**: Let Prettier handle formatting - don't fight it
2. **Commit Often**: Smaller commits = faster hook execution
3. **Fix Issues Immediately**: Don't accumulate quality debt
4. **Don't Bypass**: Resist temptation to use `--no-verify`
5. **Keep Updated**: Run `npm install` after pulling changes to sync hook versions

## Related Documentation

- [Commit Message Convention](../workflow/commit-messages.md) - Detailed commit message rules
- [No Machine-Specific Information in Commits](./no-machine-specific-commits.md) - Practice prohibiting machine-specific paths and credentials from committed code
- [Trunk Based Development](../workflow/trunk-based-development.md) - Git workflow and branching strategy
- [Git Push Safety Convention](../workflow/git-push-safety.md) - Requires explicit per-instance user approval before any agent or automation runs `git push --force`, `--force-with-lease`, or `--no-verify`
- [Nx Target Standards](../infra/nx-targets.md) - Canonical target names, `test:quick` composition rules, and caching configuration that the pre-push hook depends on
- [Rust Unsafe Code Policy](../../../docs/explanation/software-engineering/programming-languages/rust/code-quality-standards.md#unsafe-code-policy) - MUST clause: all OSE application Rust crates MUST use `#![forbid(unsafe_code)]` in every crate root (`lib.rs` and `main.rs`)
- [Three-Level Testing Standard](./three-level-testing-standard.md) - Mandatory unit/integration/E2E testing architecture for all projects; defines what `test:unit`, `test:integration`, and `test:e2e` must do at each level

## References

- [Prettier Documentation](https://prettier.io/docs/en/)
- [Husky Documentation](https://typicode.github.io/husky/)
- [lint-staged Documentation](https://github.com/lint-staged/lint-staged)
- [Conventional Commits](https://www.conventionalcommits.org/)
