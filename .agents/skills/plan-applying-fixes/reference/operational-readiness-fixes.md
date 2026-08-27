# Operational Readiness Fixes

## Operational Readiness Fixes (Step 5b Findings)

### 1. Missing Local Quality Gates

Add a delivery-checklist section before the final push step, inserting the canonical
`### Local Quality Gates (Before Push)` template from the Operational Readiness section of
`.claude/skills/plan-creating-project-plans/SKILL.md` — adapt targets to the plan's affected
projects (e.g. add `test:integration`/`test:e2e` if warranted).

### 2. Missing Post-Push CI/CD Steps

```markdown
### Post-Push Verification

- [ ] Push changes to the delivery target for the declared Delivery Mode (the PR branch under `worktree-to-pr` / `main-to-pr`; `origin main` under the direct-push modes)
- [ ] Monitor GitHub Actions workflows triggered by that push — the PR's check run under `*-to-pr` (list specific workflow names if known)
- [ ] Verify all CI checks pass
- [ ] If any CI check fails, fix immediately and push a follow-up commit
- [ ] Do NOT proceed to next delivery phase until CI is green
```

### 3. Missing Development Environment Setup

```markdown
### Environment Setup

- [ ] Install dependencies: `npm install`
- [ ] Run doctor to verify tooling: `npm run doctor`
- [ ] [Add project-specific setup: env vars, DB, Docker, etc.]
- [ ] Verify dev server starts: `nx dev [project-name]`
- [ ] Verify existing tests pass before making changes: `nx run [project-name]:test:quick`
```

Customize based on the plan's target projects and tech stacks.

### 4. Missing Fix-All-Issues Instruction

```markdown
> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting
> errors encountered during work. Do not defer or mention-and-skip existing issues.
```

### 5. Missing Thematic Commit Guidance

```markdown
### Commit Guidelines

- [ ] Do not stage or commit until the user explicitly authorizes the named change set
- [ ] Once authorized, use the fewest build-valid, independently reviewable and revertible commits,
      one coherent purpose each; no extra boundary prompt unless the user prescribed one
- [ ] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [ ] Keep required tests, docs, specs, references, migrations/rollback, and generated mirrors with
      the change they complete; split independent concerns
- [ ] Do not extend a commit beyond the user-authorized change set
```

### Confidence Assessment

**HIGH**: item completely missing — add the template section, or the item references wrong
commands/targets — fix with correct Nx commands from CLAUDE.md. **MEDIUM**: item exists but is
vague — flag for manual review (plan author knows context better).
