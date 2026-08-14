# Operational Readiness and Manual Behavioral Assertion Fixes

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

- [ ] Commit changes thematically — group related changes into logically cohesive commits
- [ ] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [ ] Split different domains/concerns into separate commits
- [ ] Do NOT bundle unrelated fixes into a single commit
- [ ] Example: separate `fix(lint): ...` from `feat(api): ...` commits
```

### Confidence Assessment

**HIGH**: item completely missing — add the template section, or the item references wrong
commands/targets — fix with correct Nx commands from CLAUDE.md. **MEDIUM**: item exists but is
vague — flag for manual review (plan author knows context better).

## Manual Behavioral Assertion Fixes (Step 5c Findings)

### 1. Missing Playwright MCP Steps for UI Plans

```markdown
### Manual UI Verification (Playwright MCP)

- [ ] Start dev server: `nx dev [project-name]`
- [ ] Navigate to affected pages via `browser_navigate`
- [ ] Inspect DOM via `browser_snapshot` — verify correct rendering
- [ ] Test interactive flows via `browser_click` / `browser_fill_form`
- [ ] Check for JS errors via `browser_console_messages` — must be zero errors
- [ ] Verify API integration via `browser_network_requests`
- [ ] Take screenshots via `browser_take_screenshot` for visual verification
- [ ] Document verification results in this checklist
```

### 2. Missing curl Steps for API Plans

```markdown
### Manual API Verification (curl)

- [ ] Start backend server: `nx dev [project-name]`
- [ ] Verify health endpoint: `curl -s http://localhost:[port]/api/health | jq .`
- [ ] Verify affected endpoints return expected responses
- [ ] Test error cases with invalid payloads — verify proper error responses
- [ ] Verify response status codes, shapes, and data integrity
- [ ] Document verification results in this checklist
```

### 3. Missing End-to-End Flow for Full-Stack Plans

```markdown
### End-to-End Flow Verification

- [ ] Start both frontend and backend dev servers
- [ ] Use Playwright MCP to interact with the UI
- [ ] Verify UI actions trigger correct API calls (`browser_network_requests`)
- [ ] Verify API responses are correctly rendered in the UI
- [ ] Test complete user flows end-to-end
- [ ] Document verification results in this checklist
```

### Confidence Assessment

**HIGH**: section completely missing — add the template, or the section references the wrong
project/port — fix with correct values from plan context. **MEDIUM**: section exists but is
vague — flag for manual review.
