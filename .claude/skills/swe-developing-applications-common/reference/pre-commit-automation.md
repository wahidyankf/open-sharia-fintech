# Common Development Workflow — Pre-commit Automation

## Automated Quality Gates

When code files are modified, **Husky + lint-staged** automatically run:

**Pre-commit Hooks**:

1. **Format with Prettier**: Automatically formats staged files
2. **Lint markdown**: Validates markdown files with markdownlint
3. **Validate links**: Checks markdown links aren't broken
4. **Auto-stage changes**: Automatically stages formatting fixes

**Commit-msg Hook**:

- **Validate commit format**: Ensures Conventional Commits compliance
- **Blocks invalid commits**: Prevents commit if format wrong

**Pre-push Hook**:

- **Run `test:quick` for affected projects**: Executes the fast quality gate (`nx affected -t test:quick`) — this is the canonical pre-push check. Every project must expose a `test:quick` target.
- **Markdown linting**: Final markdown quality check

> **Note**: `test:e2e` does NOT run in the pre-push hook. It runs on a scheduled GitHub Actions cron job (twice daily per workflow) targeting each `*-e2e` project. See [Nx Target Standards](../../../../repo-governance/development/infra/nx-targets.md) for the full execution model.

## Trust the Automation

**Philosophy**: Focus on code quality, let automation handle style

**What This Means**:

- Don't manually format code (Prettier handles it)
- Don't worry about markdown formatting (automated)
- Don't manually check links (automation validates)
- Trust that tests will run before push

**If Pre-commit Hook Fails**:

1. Read the error message carefully
2. Fix the reported issue
3. Re-stage files if needed
4. Commit again (creates NEW commit, don't amend unless asked)

**Common Failures**:

- **Markdown linting**: Run `npm run lint:md:fix` to auto-fix
- **Test failures**: Fix the failing test, re-commit
- **Link validation**: Fix broken links, re-commit
- **Commit message format**: Rewrite commit message following Conventional Commits
