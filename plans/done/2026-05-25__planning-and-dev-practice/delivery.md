# Delivery Checklist — Planning and Dev Practice Improvement

## Worktree

**Path**: `worktrees/planning-and-dev-practice/`

**Provision**:

```bash
claude --worktree planning-and-dev-practice
```

After the worktree is created, follow
[worktree-setup.md](../../../repo-governance/development/workflow/worktree-setup.md) to
run `npm install` and `npm run doctor -- --fix` from the **repo root** (not from inside
the new worktree directory).

See [worktree-path.md](../../../repo-governance/conventions/structure/worktree-path.md) for the
routing convention. Per [plans.md §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification),
the canonical Worktree section lives in this `delivery.md`.

## Development Environment Setup

No compilation or runtime required. All deliverables are markdown files.

Verify prerequisites:

```bash
node --version    # expect: v24.x.x (managed by Volta)
npm --version     # expect: v11.x.x
which rtk         # expect: path to rtk binary (token-optimized CLI proxy)
```

## Phase 1: Create Grill-Me Skill

### Step 1.1 — RED: Specify expected behavior

- [ ] Read `repo-governance/development/workflow/test-driven-development.md` — confirm
      RED-GREEN-REFACTOR mandate [Repo-grounded]
- [ ] Read `.claude/skills/plan-creating-project-plans/SKILL.md` — confirm skill frontmatter
      format [Repo-grounded]
- [ ] Read `.claude/skills/repo-applying-maker-checker-fixer/SKILL.md` — confirm body
      structure pattern [Repo-grounded]
- [ ] Write manual test spec: trigger "grill me" in a planning session and observe that:
  - First response is exactly one question
  - Question has 2-4 options with trade-off descriptions
  - One option is marked as recommended
  - Codebase is explored before asking answerable questions

Acceptance criterion: behavior spec matches all four Gherkin scenarios in `prd.md` and is
understood before writing `SKILL.md`.

### Step 1.2 — GREEN: Create skill file

- [ ] Create directory: `mkdir -p .claude/skills/grill-me/`
- [ ] Write `.claude/skills/grill-me/SKILL.md` with content from `tech-docs.md §Skill File`
- [ ] Verify file exists: `ls .claude/skills/grill-me/SKILL.md`
- [ ] Verify frontmatter is valid YAML: `head -10 .claude/skills/grill-me/SKILL.md`

Acceptance criterion: file present, frontmatter contains `name` and `description`, body
contains choice-format question template.

### Step 1.3 — REFACTOR: Validate skill behavior

- [ ] Manually invoke the skill in a planning context: say "grill me on [any topic]"
- [ ] Verify: first response is exactly one question with 2-4 options
- [ ] Verify: recommended option is marked `**(Recommended)**`
- [ ] Verify: when asked about existing repo structure, agent reads files instead of asking
- [ ] If any of the four Gherkin scenarios in `prd.md §Feature: Grill-Me Skill Activation`
      fail, identify which scenario fails, then edit `.claude/skills/grill-me/SKILL.md` to
      address the failing rule (e.g. if questions are bundled → strengthen Rule 1; if no
      recommendation is marked → strengthen Rule 3; if codebase is not explored → strengthen
      Rule 4)

Acceptance criterion: all four Gherkin scenarios in `prd.md §Feature: Grill-Me Skill
Activation` pass via manual observation — no scenario fails.

## Phase 2: Update Related Files

### Step 2.1 — Update `repo-governance/workflows/plan/plan-quality-gate.md`

- [ ] Read `repo-governance/workflows/plan/plan-quality-gate.md`
- [ ] Add **Step 5g — Harness-Neutrality Scan** after the existing Step 5f
      (Anti-Hallucination Scan) with the content described in `tech-docs.md §plan-quality-gate.md`
- [ ] Ensure the step is conditional: fires only when the plan touches agents, skills,
      rules, or `repo-governance/` paths
- [ ] Verify markdown linting passes: `npm run lint:md`

Acceptance criterion: `plan-quality-gate.md` contains Step 5g describing a conditional
harness-neutrality check that covers all five validation points from tech-docs.md.

### Step 2.2 — Update `repo-governance/workflows/plan/plan-execution.md`

- [ ] Read `repo-governance/workflows/plan/plan-execution.md`
- [ ] In the `**When to use**:` bullet list (lines ~39-46 of `plan-execution.md`), add a
      new bullet: `- Before executing, invoke the \`grill-me\` skill
      (`.claude/skills/grill-me/SKILL.md`) to stress-test any unresolved design decisions
      in the plan.`
- [ ] Verify markdown linting passes: `npm run lint:md`

Acceptance criterion: `plan-execution.md` `**When to use**:` block contains a bullet
referencing the `grill-me` skill for pre-execution design stress-testing.

### Step 2.3 — Verify `repo-governance/development/workflow/test-driven-development.md`

- [ ] Read `repo-governance/development/workflow/test-driven-development.md`
- [ ] Verify it explicitly states that delivery checklists for code steps must use
      RED → GREEN → REFACTOR shape
- [ ] If absent: add a `## TDD Shape for Delivery Checklists` section using the verbatim
      three-substep template from `tech-docs.md §TDD Shape for Delivery Checklists` — copy
      the RED/GREEN/REFACTOR template block exactly

Acceptance criterion: `test-driven-development.md` contains a section (existing or newly
added) that includes the RED/GREEN/REFACTOR three-substep template pattern.

### Step 2.4 — Run `repo-rules-maker` to propagate convention

- [ ] Invoke `repo-rules-maker` agent with context: "The planning-and-dev-practice plan has
      been executed: a new `grill-me` planning skill was added at
      `.claude/skills/grill-me/SKILL.md`, `plan-quality-gate.md` was extended with a
      harness-neutrality check (Step 5g), and TDD delivery checklist shape was formalized.
      Update all related governance docs, agent definitions, and rules to reference these
      conventions where planning skills, plan quality, or TDD practices are mentioned."
- [ ] For each file the agent creates or modifies: read the file and verify it contains no
      contradictions with `AGENTS.md`, `repo-governance/conventions/`, or other referenced
      governance docs
- [ ] Run `npm run lint:md` — all new/modified files must pass with zero violations

Acceptance criterion: `repo-rules-maker` exits without errors; every new/modified file
passes `npm run lint:md`; no file contradicts an existing governance convention (verified
by reading each changed file).

## Phase 3: Quality Gates

### Step 3.1 — Local markdown lint

Run and fix ALL failures, including preexisting issues not caused by this change:

```bash
npm run lint:md
npm run lint:md:fix  # auto-fix if violations found
npm run lint:md       # re-run to verify zero violations
```

Acceptance criterion: `npm run lint:md` exits 0 with zero violations.

### Step 3.2 — Local Nx quality gates

Run affected quality gates and fix ALL failures:

```bash
npx nx affected -t typecheck lint test:quick spec-coverage
```

Fix ALL failures found — including preexisting issues encountered during this work
(root cause orientation principle). Do not defer any failure to a follow-up task.

Acceptance criterion: all affected Nx targets pass.

### Step 3.3 — Repo-rules quality gate

- [ ] Run `repo-rules-quality-gate` workflow scoped to the changed governance files
- [ ] Fix all CRITICAL and HIGH findings before proceeding
- [ ] Re-run until zero CRITICAL and zero HIGH findings

Acceptance criterion: `repo-rules-quality-gate` exits with zero CRITICAL and zero HIGH.

### Step 3.4 — Thematic commits

Commit each domain separately using Conventional Commits format
[Repo-grounded: `repo-governance/development/workflow/commit-messages.md`]:

```bash
# New skill file
rtk git add .claude/skills/grill-me/
rtk git commit -m "feat(skills): add grill-me planning interrogation skill"

# Governance and workflow doc updates
rtk git add repo-governance/
rtk git commit -m "docs(governance): add grill-me, tdd checklist, and harness-neutrality plan-quality-gate step"

# Plan files
rtk git add plans/in-progress/planning-and-dev-practice/
rtk git commit -m "docs(plans): add planning-and-dev-practice improvement plan"
```

Split different concerns into separate commits. Do not bundle skill, governance, and plan
changes into a single commit.

### Step 3.5 — Push and verify CI

```bash
rtk git push origin main
```

After pushing, monitor GitHub Actions CI every 3 minutes:

```bash
gh run list --branch main --limit 5
gh run view [run-id] --json status,conclusion
```

Do not use `gh run watch` (stream-watching is prohibited per
[ci-monitoring.md](../../../repo-governance/development/workflow/ci-monitoring.md)).
Fix any CI failures immediately. Do not declare work done until CI passes.

Acceptance criterion: all GitHub Actions workflows pass on `origin main`.

## Manual Behavioral Assertions

This plan does not touch UI or API code, so Playwright/curl are not required
[Judgment call: no HTTP endpoints or browser UI in scope]. Manual verification is
skill invocation:

- [ ] In a Claude Code session, say "grill me on the database migration approach"
- [ ] Observe: first response is exactly one question with 2-4 options
- [ ] Observe: one option is clearly marked as recommended
- [ ] Observe: the agent reads relevant repo files before asking questions answerable
      from existing code
- [ ] After several exchanges, observe: agent summarizes all decisions and signals readiness

Acceptance criterion: all five observations pass.

## Fix-All-Issues Instruction

When quality gates surface failures, fix ALL of them — not only those caused by this
change. Root cause orientation principle: preexisting issues encountered during this work
must be resolved proactively, not deferred.

## Definition of Done

- [ ] `.claude/skills/grill-me/SKILL.md` exists with correct frontmatter and body
- [ ] Skill asks one question at a time with 2-4 options, marks recommendation
- [ ] `repo-governance/workflows/plan/plan-quality-gate.md` contains Step 5g
      (Harness-Neutrality Scan, conditional on agent/skill/governance changes)
- [ ] `repo-governance/workflows/plan/plan-execution.md` references grill-me
- [ ] `repo-governance/development/workflow/test-driven-development.md` covers delivery
      checklist TDD shape
- [ ] `repo-rules-maker` propagation complete and reviewed
- [ ] `npm run lint:md` exits 0
- [ ] `npx nx affected -t typecheck lint test:quick spec-coverage` passes
- [ ] `repo-rules-quality-gate` zero CRITICAL + HIGH findings
- [ ] All changes committed thematically with Conventional Commits
- [ ] CI passes after push to `origin main`
- [ ] Manual behavioral assertions all pass
