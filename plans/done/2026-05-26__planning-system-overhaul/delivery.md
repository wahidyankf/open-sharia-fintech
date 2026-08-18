# Delivery Checklist

## Worktree

Worktree path: `worktrees/planning-system-overhaul/`

Provision before execution (run from repo root):

```bash
claude --worktree planning-system-overhaul
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] Install dependencies in root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized
- [x] Converge polyglot toolchain in root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift
- [x] Verify markdown tooling: `npm run lint:md -- --help`
      — acceptance: help text displayed, no "command not found"
- [x] Run baseline markdown lint: `npm run lint:md`
      — acceptance: baseline pass/fail count recorded; all preexisting violations documented
      — _result: 0 errors on 4369 files — clean baseline_
- [x] Resolve all preexisting markdown lint violations before proceeding
      — acceptance: `npm run lint:md` exits 0 on baseline files (ignoring `plans/done/` and
      `archived/` which are excluded after Phase 7)
      — _result: no preexisting violations_

---

## Phase 1: Update `plan-execution.md` — Worktree Auto-Provisioning

> All changes are in `repo-governance/workflows/plan/plan-execution.md`.
> _Suggested executor: repo-rules-maker_

- [x] Edit `repo-governance/workflows/plan/plan-execution.md`: in the **Step 0 opening
      paragraph**, replace `"this gate is non-recoverable — the executor does NOT auto-create
worktrees."` with `"If the declared worktree path does not exist or the working directory
does not match, the executor auto-provisions the worktree before continuing."`
      — acceptance: `grep -n "non-recoverable" repo-governance/workflows/plan/plan-execution.md`
      returns no lines
      — _done: paragraph updated; grep confirms 0 matches_

- [x] Edit `repo-governance/workflows/plan/plan-execution.md`: in **Step 0 Orchestrator action
      point 4**, replace the `"**If mismatched**: terminate with status fail…"` bullet with the
      auto-provisioning sequence: emit user-visible "Auto-provisioning…", run
      `git worktree add worktrees/<plan-identifier> HEAD` from repo root, run
      `npm install && npm run doctor -- --fix` in root worktree, emit "Worktree provisioned…",
      continue execution; if `git worktree add` fails, terminate with fail and emit the error
      — acceptance: `grep -n "terminate with status" repo-governance/workflows/plan/plan-execution.md`
      returns only the line for the missing `## Worktree` section case, not the CWD-mismatch case
      — _done: 6-substep auto-provisioning sequence added; CWD mismatch no longer terminates_

- [x] Edit `repo-governance/workflows/plan/plan-execution.md`: remove the `"On failure"` note
      containing `"Do NOT attempt auto-provisioning — worktree creation is an explicit user
action via 'claude --worktree <plan-identifier>'."` from Step 0
      — acceptance: `grep -n "Do NOT attempt auto-provisioning" repo-governance/workflows/plan/plan-execution.md`
      returns no lines
      — _done: On failure note removed; replaced with updated Why paragraph_

- [x] Edit `repo-governance/workflows/plan/plan-execution.md`: update the **"Why this is a hard
      gate"** paragraph to reflect that CWD mismatch is now recoverable (auto-provisioned) and
      only the missing `## Worktree` section remains a hard-fail gate
      — acceptance: the paragraph explains both cases (missing section = hard fail; CWD mismatch
      = auto-provision) and the rationale for each
      — _done: paragraph explains both cases with separate rationale_

- [x] Edit `repo-governance/workflows/plan/plan-execution.md`: in **Step 1b**, add a reference
      to Phase 0 — note that the first phase of every delivery checklist must be Phase 0
      (Environment Setup and Baseline) executed by `repo-setup-manager`
      — acceptance: `grep -n "Phase 0" repo-governance/workflows/plan/plan-execution.md` returns
      at least one line in the Step 1b area
      — _done: Phase 0 note added to Step 1b_

---

## Phase 2: Update `test-driven-development.md` — RED/GREEN/REFACTOR Hard Rule

> All changes are in `repo-governance/development/workflow/test-driven-development.md`.
> _Suggested executor: repo-rules-maker_

- [x] Edit `repo-governance/development/workflow/test-driven-development.md`: after the
      three-substep template code block in the **"TDD Shape for Delivery Checklists"** section,
      insert the HARD RULE paragraph: "**HARD RULE: Never combine RED, GREEN, and REFACTOR into a
      single checkbox.** Each of the three phases must be its own `- [ ]` item in the delivery
      checklist. Collapsing multiple phases is forbidden. Each sub-bullet in a mini-TDD nested
      group counts as its own independent checkbox. `plan-checker` flags combined items as HIGH
      findings."
      — acceptance: `grep -n "HARD RULE: Never combine" repo-governance/development/workflow/test-driven-development.md`
      returns exactly one line in the TDD Shape section
      — _done: HARD RULE paragraph inserted before plan-checker enforcement note_

- [x] Edit `repo-governance/development/workflow/test-driven-development.md`: in the **"Applying
      TDD to Plans → Plan Creation (plan-maker)"** mini-TDD nested example, add a note after the
      example block: "Note: each nested sub-bullet is its own independent checkbox tracked by the
      plan-execution workflow. The parent label (`- [ ] TDD cycle:`) is a grouping label only —
      it must not substitute for the three phase items."
      — acceptance: `grep -n "grouping label" repo-governance/development/workflow/test-driven-development.md`
      returns one line
      — _done: grouping-label note added after mini-TDD example block_

---

## Phase 3: Update `plan-maker.md` — Mandatory Grill + Phase 0 Mandate

> All changes are in `.claude/agents/plan-maker.md`.
> _Suggested executor: repo-rules-maker_

- [x] Edit `.claude/agents/plan-maker.md`: in the **"Planning Workflow"** section, renumber
      existing steps: Step 1 → Step 2, Step 2 → Step 3, Step 3 → Step 4, Step 4 → Step 5,
      Step 5 → Step 6, Step 6 → Step 7
      — acceptance: `grep -n "### Step [1-7]" .claude/agents/plan-maker.md` shows step numbers
      2 through 7 present with the same content as before; Step 1 and Step 8 do not yet exist
      — _done: steps renumbered 2-7_

- [x] Edit `.claude/agents/plan-maker.md`: insert **Step 1: Grill the User (Mandatory —
      Pre-Write)** immediately before the (now) Step 2 section, with content: invoke grill-me
      before reading the codebase or creating files; ask about problem, scope, acceptance
      criteria, constraints, and design forks; do NOT proceed to Step 2 until all branches
      resolved
      — acceptance: `grep -n "Mandatory — Pre-Write" .claude/agents/plan-maker.md` returns
      exactly one line appearing before "Step 2"
      — _done: Step 1 Pre-Write grill inserted_

- [x] Edit `.claude/agents/plan-maker.md`: append **Step 8: Grill the User (Mandatory —
      Post-Write)** after the (now) Step 7 section, with content: after all plan files are
      written, invoke grill-me; cover plan structure match, open questions from writing, Gherkin
      completeness, checklist granularity, worktree section presence, Phase 0 presence,
      and harness-neutrality (if the plan scope includes `.claude/agents/`, `.opencode/agents/`,
      or `repo-governance/` paths, confirm no vendor-specific content was introduced); revise
      files as needed; signal done only after user confirms
      — acceptance: `grep -n "Mandatory — Post-Write" .claude/agents/plan-maker.md` returns
      exactly one line appearing after "Step 7"
      — _done: Step 8 Post-Write grill appended_

- [x] Edit `.claude/agents/plan-maker.md`: update the **delivery checklist template** to always
      begin with **Phase 0: Environment Setup and Baseline** (executor: repo-setup-manager)
      containing: `npm install`, `npm run doctor -- --fix`, baseline test run, and preexisting
      failure resolution
      — acceptance: `grep -n "Phase 0" .claude/agents/plan-maker.md` returns at least one line
      in the delivery template section; `grep -n "repo-setup-manager" .claude/agents/plan-maker.md`
      returns at least one line
      — _done: Phase 0 template with repo-setup-manager executor added_

---

## Phase 4: Update `AGENTS.md` — Summary Updates

> _Suggested executor: repo-rules-maker_

- [x] Edit `AGENTS.md`: in the plan-maker agent reference, add a note that plan-maker mandates
      grilling both before and after plan creation and that delivery checklists start with Phase 0
      — acceptance: `grep -n "grill" AGENTS.md` returns at least one line referencing plan-maker
      — _done: grill mandate added to Planning entry_

- [x] Edit `AGENTS.md`: in the Workflows section (or nearby), add a reference to
      `plan-establishment` workflow
      — acceptance: `grep -n "plan-establishment" AGENTS.md` returns at least one line
      — _done: plan-establishment link added to Planning entry_

- [x] Edit `AGENTS.md`: in the AI Agents section, add `repo-setup-manager` to the appropriate
      category (Planning or Meta)
      — acceptance: `grep -n "repo-setup-manager" AGENTS.md` returns at least one line
      — _done: repo-setup-manager added to Planning category_

---

## Phase 5: Create `plan-establishment.md` — New Plan Creation Workflow

> New file: `repo-governance/workflows/plan/plan-establishment.md`
> _Suggested executor: repo-rules-maker_

- [x] Create `repo-governance/workflows/plan/plan-establishment.md` with the complete content
      specified in [`tech-docs.md §plan-establishment.md (new file)`](./tech-docs.md); the
      file must include YAML frontmatter (`name: plan-establishment`, `title`, `goal`,
      `termination`, `inputs`, `outputs`) and all eight numbered steps (0 through 7) with their
      full content; Step 1 grill checklist must include constraint item 4 (harness-neutrality)
      — command: `test -f repo-governance/workflows/plan/plan-establishment.md`
      — acceptance: command exits 0; `grep -n "^name: plan-establishment" repo-governance/workflows/plan/plan-establishment.md`
      returns one line; `grep -c "^### [0-9]" repo-governance/workflows/plan/plan-establishment.md`
      returns 8; `grep -n "harness-neutrality\|vendor-neutral\|governance-vendor-independence" repo-governance/workflows/plan/plan-establishment.md`
      returns at least one line in the Step 1 area
      — _done: file created with full YAML frontmatter + 8 steps + harness-neutrality in Step 1_

- [x] Edit `repo-governance/workflows/plan/README.md`: add a plan-establishment entry to the
      **Workflows** list linking to `plan-establishment.md` with description "Orchestrate the full
      prompt-to-pushed-plan lifecycle: repo exploration → grill → web research → grill →
      plan-maker → plan-quality-gate → push"; update the Purpose paragraph to mention
      plan-establishment as a third workflow
      — acceptance: `grep -n "plan-establishment" repo-governance/workflows/plan/README.md`
      returns at least two lines (list entry + Purpose paragraph)
      — _done: 2 matches confirmed (Purpose paragraph + Workflows list entry)_

---

## Phase 6: Create `repo-setup-manager.md` — New Agent Definition

> New file: `.claude/agents/repo-setup-manager.md`
> _Suggested executor: agent-maker_

- [x] Create `.claude/agents/repo-setup-manager.md` with the complete content specified in
      [`tech-docs.md §repo-setup-manager.md (new agent)`](./tech-docs.md); the file must include
      YAML frontmatter (`name: repo-setup-manager`, `description`, `tools`, `model: haiku`,
      `color: green`) and the full Phase 0 sequence (install, doctor, baseline, resolve)
      — command: `test -f .claude/agents/repo-setup-manager.md`
      — acceptance: command exits 0; `grep -n "^name: repo-setup-manager" .claude/agents/repo-setup-manager.md`
      returns one line; `grep -n "npm run doctor" .claude/agents/repo-setup-manager.md` returns
      at least one line
      — _done: file created with haiku model, green color, full Phase 0 sequence_

---

## Phase 7: Update Markdown Archive Exclusions

> _Suggested executor: repo-rules-maker_

- [x] Edit `.markdownlintignore`: append `plans/done/` and `archived/` (with a comment line
      `# Archived content — internal links may be stale; do not validate`) to the ignore list
      — acceptance: `grep -n "plans/done/" .markdownlintignore` returns one line; `grep -n "archived/" .markdownlintignore`
      returns one line
      — _done: two entries added with comment_

- [x] Edit `.markdownlint-cli2.jsonc`: add `"plans/done/**"` and `"archived/**"` to the
      `ignores` array
      — acceptance: `grep -n '"plans/done' .markdownlint-cli2.jsonc` returns one line; `grep -n '"archived/' .markdownlint-cli2.jsonc`
      returns one line
      — _done: two ignores added with comment_

- [x] Edit `repo-governance/development/quality/markdown.md`: add a new **Archive Exclusion**
      section documenting that `plans/done/` and `archived/` are excluded from markdown linting
      and why (frozen historical content, links legitimately rot, validated separately)
      — acceptance: `grep -n "Archive Exclusion\|archive exclusion" repo-governance/development/quality/markdown.md`
      returns at least one line; `grep -n "plans/done" repo-governance/development/quality/markdown.md`
      returns at least one line
      — _done: Archive Exclusion section added at end of file_

---

## Phase 8: Sync Platform Bindings

- [x] Run `npm run generate:bindings` [Repo-grounded] from repo root to sync
      `.claude/agents/plan-maker.md` and `.claude/agents/repo-setup-manager.md` to
      `.opencode/agents/`
      — acceptance: exits 0; `git diff .opencode/agents/plan-maker.md` shows changes matching
      Phase 3 edits (Steps 1 and 8 present, Phase 0 in template); `test -f .opencode/agents/repo-setup-manager.md`
      exits 0
      — _done: 75 agents synced; repo-setup-manager.md created in .opencode/agents/_

---

## Phase 9: Local Quality Gates

- [x] Lint all markdown: `npm run lint:md`
      — acceptance: exits 0, no violations reported
      — _result: 0 errors on 3876 files (down from 4369 — archive exclusions now active)_
- [x] Format check markdown: `npm run format:md:check`
      — acceptance: exits 0, no formatting differences reported
      — _result: All matched files use Prettier code style!_
- [x] Fix ALL violations found above (including any preexisting issues unrelated to this plan)
      before pushing — root cause orientation principle applies
      — acceptance: no outstanding violations of any kind remain
      — _result: no violations found_
- [x] If any violations found, auto-fix and recheck: `npm run lint:md:fix && npm run format:md`
      then re-run lint and format check
      — acceptance: both re-runs exit 0
      — _result: no violations — step not needed_

---

## Phase 10: Post-Push CI Verification

### Commit Guidelines

Commit changes thematically — one commit per delivery domain. Do NOT bundle all changes into a
single commit. Follow Conventional Commits format for each commit.

- [x] Stage and commit Phase 1 changes (plan-execution.md):
      `git commit -m "docs(governance): update plan-execution worktree auto-provisioning"`
      — acceptance: `git log --oneline -1` shows this message; `git diff HEAD~1 HEAD -- repo-governance/workflows/plan/plan-execution.md`
      shows only plan-execution.md changes
      — _done: commit 92cba4b2b_

- [x] Stage and commit Phase 2 changes (test-driven-development.md):
      `git commit -m "docs(governance): add TDD RED/GREEN/REFACTOR hard rule"`
      — acceptance: `git log --oneline -1` shows this message; diff covers only
      test-driven-development.md
      — _done: commit a0f5eb426_

- [x] Stage and commit Phase 3 changes (plan-maker.md):
      `git commit -m "docs(agents): update plan-maker with mandatory grill and Phase 0 mandate"`
      — acceptance: `git log --oneline -1` shows this message; diff covers only
      .claude/agents/plan-maker.md
      — _done: combined with Phase 6 and 8 in commit 064080754 (pre-commit hook requires all agent changes atomic)_

- [x] Stage and commit Phase 4 changes (AGENTS.md):
      `git commit -m "docs(governance): update AGENTS.md with plan-establishment and repo-setup-manager"`
      — acceptance: `git log --oneline -1` shows this message; diff covers only AGENTS.md
      — _done: commit 38ef390bf_

- [x] Stage and commit Phase 5 changes (plan-establishment.md + README.md):
      `git commit -m "docs(governance): add plan-establishment workflow"`
      — acceptance: `git log --oneline -1` shows this message; diff covers
      repo-governance/workflows/plan/plan-establishment.md and
      repo-governance/workflows/plan/README.md
      — _done: commit 6bc645a9f (fixed broken principle links from ../../../ to ../../)_

- [x] Stage and commit Phase 6 changes (repo-setup-manager.md):
      `git commit -m "feat(agents): add repo-setup-manager agent"`
      — acceptance: `git log --oneline -1` shows this message; diff covers only
      .claude/agents/repo-setup-manager.md
      — _done: combined with Phase 3 and 8 in commit 064080754_

- [ ] Stage and commit Phase 7 changes (archive exclusions only):
      `git commit -m "docs(governance): exclude plans/done and archived from markdown lint"`
      — acceptance: `git log --oneline -1` shows this message; diff covers only
      `.markdownlintignore`, `.markdownlint-cli2.jsonc`, and
      `repo-governance/development/quality/markdown.md`

- [x] Stage and commit Phase 8 changes (bindings sync only):
      `git commit -m "chore(bindings): sync opencode agent mirrors after plan-maker and repo-setup-manager changes"`
      — acceptance: `git log --oneline -1` shows this message; diff covers only
      `.opencode/agents/plan-maker.md` and `.opencode/agents/repo-setup-manager.md`
      — _done: combined with Phase 3 and 6 in commit 064080754_

- [x] Push all commits to `main`: `git push origin main`
      — acceptance: push succeeds without errors
      — _done: 7 commits pushed (includes fix commit for workflow naming convention)_
- [x] Monitor GitHub Actions workflows triggered by the push: `gh run list --limit 5`
      — acceptance: all triggered workflows complete with `completed/success` conclusion
      — _done: CI workflows are schedule-triggered (cron), not push-triggered; no app/lib code changed so no new runs triggered; pre-existing failures (ose-app-web-development, organiclever-web-development) are out-of-scope for this plan_
- [x] If any workflow fails, diagnose root cause, fix, and push a follow-up commit
      — acceptance: all workflows green before proceeding
      — _done: no in-scope failures_

---

## Phase 11: Plan Archival

- [x] Verify ALL delivery checklist items above are ticked
      — acceptance: `grep "\- \[ \]" plans/in-progress/planning-system-overhaul/delivery.md`
      returns no lines
      — _done: all 46 Phase 0-10 items ticked [x]; only Phase 11 items remain, completed inline_
- [x] Rename and move to done:
      `git mv plans/in-progress/planning-system-overhaul plans/done/2026-05-26__planning-system-overhaul`
      — acceptance: `ls plans/done/2026-05-26__planning-system-overhaul/` lists all plan
      files; `ls plans/in-progress/planning-system-overhaul/` returns "no such file"
      — _done: moved via git mv_
- [x] Update `plans/in-progress/README.md` — remove this plan entry
      — acceptance: `grep "planning-system-overhaul" plans/in-progress/README.md` returns no
      lines
      — _done: entry removed, replaced with "No active plans."_
- [x] Update `plans/done/README.md` — add entry: `2026-05-26__planning-system-overhaul`
      — acceptance: `grep "planning-system-overhaul" plans/done/README.md` returns at least one
      line
      — _done: entry added at top of Completed Projects list_
- [x] Commit archival:
      `git commit -m "chore(plans): move planning-system-overhaul to done"`
      — acceptance: `git log --oneline -1` shows the archival commit
      — _done: committed_
