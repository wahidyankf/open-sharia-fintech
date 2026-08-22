# Operational Readiness (Mandatory Delivery Sections)

Every delivery plan MUST include these operational readiness sections. Plans missing them are considered incomplete regardless of other quality.

## Local Quality Gates (Before Push)

Every plan must include steps for running affected quality checks locally before pushing:

```markdown
### Local Quality Gates (Before Push)

- [ ] Run affected typecheck: `nx affected -t typecheck`
- [ ] Run affected linting: `nx affected -t lint`
- [ ] Run affected quick tests: `nx affected -t test:quick`
- [ ] Run affected spec coverage: `nx affected -t specs:coverage`
- [ ] Fix ALL failures found — including preexisting issues not caused by your changes
- [ ] Verify all checks pass before pushing
```

Adapt targets to the plan's affected projects (add `test:integration`, `test:e2e` if applicable).

## Post-Push CI/CD Verification

Every plan must include steps to verify CI after pushing:

```markdown
### Post-Push Verification

- [ ] Push changes to the delivery target for the declared Delivery Mode (the PR branch under `worktree-to-pr` / `main-to-pr`; `origin main` under the direct-push modes)
- [ ] Monitor GitHub Actions workflows for that push — the PR's check run under `*-to-pr`
- [ ] Verify all CI checks pass
- [ ] If any CI check fails, fix immediately and push a follow-up commit
- [ ] Do NOT proceed to next delivery phase until CI is green
```

## Development Environment Setup

Every plan must start with environment setup steps:

```markdown
### Environment Setup

- [ ] Enter the worktree this plan was authored in — provision only if absent: `claude --worktree <plan-identifier>` (`worktrees/<plan-identifier>/` in repo root; see [Worktree Path Convention](../../../../repo-governance/conventions/structure/worktree-path.md))
- [ ] Initialize toolchain in the root worktree (not the new worktree): `npm install && npm run doctor -- --fix` (see [Worktree Toolchain Initialization](../../../../repo-governance/development/workflow/worktree-setup.md))
- [ ] [Add project-specific setup: env vars, DB, Docker, etc.]
- [ ] Verify dev server starts: `nx dev [project-name]`
- [ ] Verify existing tests pass before making changes
```

> **Note**: Worktrees are created at `worktrees/<name>/` in the repo root (not `.claude/worktrees/<name>/`). This is enforced by the `WorktreeCreate` hook.

## Fix-All-Issues Instruction

Every plan must include this instruction in quality gate sections:

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting
> errors encountered during work.

## Thematic Commit Guidance

Every plan must include commit guidance:

```markdown
### Commit Guidelines

- [ ] Commit changes thematically — group related changes into logically cohesive commits
- [ ] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [ ] Split different domains/concerns into separate commits
- [ ] Do NOT bundle unrelated fixes into a single commit
```
