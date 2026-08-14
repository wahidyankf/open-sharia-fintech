# Rules 8-11: Operational Readiness, Manual Assertion, Worktree, Execution Clarity

## 8. Operational Readiness Validation (Step 5b — MANDATORY)

After delivery-checklist structure (Step 5), verify **operational readiness** items — CRITICAL when
entirely missing, since plans lacking them are incomplete regardless of other quality.

**What to validate**:

1. **Local Quality Gates Before Push** — steps run affected tests/checks locally before pushing,
   referencing `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` (the registry-declared
   gate set `.husky/pre-push` invokes, including `nx affected -t test:quick`); mentions blast radius
   (affected projects only); specifies unit/integration/e2e as applicable; includes lint and typecheck.
2. **Post-Push CI/CD Verification** — steps manually verify related GitHub Actions pass after push,
   against the plan's declared delivery target (the PR's check run under `*-to-pr`; `origin main`
   under direct-push modes — hardcoding `main` while declaring `*-to-pr` is itself a finding);
   specifies which workflows to monitor; instructs watching for and fixing failures.
3. **Development Environment Setup** — steps set up the dev/execution environment (dependency
   install, env vars, database setup, dev server startup as needed), specific enough for someone
   unfamiliar to follow.
4. **Fix-All-Issues Instruction** — instructs fixing ALL issues found during quality gates, even
   unrelated to current changes (root-cause orientation), explicitly: "Fix all failures, not just
   those caused by your changes."
5. **Thematic Commit Guidance** — instructs committing thematically (logically cohesive groups),
   references Conventional Commits, instructs splitting different domains/concerns, forbids bundling
   unrelated fixes into one commit.

**Finding severity**: missing ALL items: **CRITICAL**. Missing an individual item (1-5): **HIGH**
per missing item. Present but vague/incomplete: **MEDIUM**.

## 9. Manual Behavioral Assertion Validation (Step 5c — MANDATORY)

After Step 5b, verify manual behavioral assertion steps when applicable.

**What to validate**:

1. **Playwright MCP steps for web UI plans** — any web-frontend change (Next.js, Flutter Web, any UI
   project) needs `browser_navigate`, `browser_snapshot`, `browser_click`/`browser_fill_form`,
   `browser_console_messages`, `browser_take_screenshot` steps naming which pages/flows. Missing
   entirely: **CRITICAL**.
2. **curl steps for API plans** — any endpoint change (REST, tRPC, backend service) needs curl steps
   naming endpoint URLs, expected response shapes, error-case testing, health check, and affected
   endpoints. Missing entirely: **CRITICAL**.
3. **End-to-end flow assertion for full-stack plans** — UI-plus-API plans need full-flow assertion
   (UI → API → response → UI update). Missing entirely: **HIGH**.
4. **Locale coverage for multi-locale UI plans** — a frontend serving more than one locale (detect via
   `apps/<app>/src/features/i18n/` or locale-prefixed routes) needs verification across ALL supported
   locales (explicit "for each locale" or named locale URLs `/en/...`, `/id/...`). Single-locale-only:
   **HIGH**. Per
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)
   and
   [Manual Behavioral Verification](../../../../repo-governance/development/quality/manual-behavioral-verification.md).
5. **Evidence Capture Steps** — every manual-verification section needs evidence-capture steps:
   screenshots to `evidence/` (named `phase-N-<description>-<locale>-<breakpoint>px.png`) referenced
   in `delivery.md`; curl responses inlined as fenced code blocks or saved to `evidence/`. Section
   present but no evidence-capture step: **HIGH**.
6. **Not-applicable exemption** — plans touching only docs/governance/non-code files don't need
   manual assertions; verify the exemption is legitimate (genuinely no UI/API changes).

**Finding severity**: missing Playwright steps for UI plan: **CRITICAL**. Missing curl steps for API
plan: **CRITICAL**. Missing end-to-end flow for full-stack plan: **HIGH**. Single-locale-only on
multi-locale app: **HIGH**. Missing evidence-capture steps: **HIGH**. Steps present but vague (no
specific pages/endpoints): **MEDIUM**.

## 10. Worktree Specification Validation (Step 5d — MANDATORY)

After Step 5c, verify the plan declares a worktree path. Applies to ALL plans regardless of size —
pure-docs, single-file, trivial plans included.

**What to validate**:

1. **`## Worktree` section exists** — multi-file plans: top-level section in `delivery.md` before any
   phase heading; single-file plans: in `README.md` before `## Delivery Checklist`. Missing: **HIGH**
   (plan-execution Step 0 hard gate refuses to start).
2. **Path format** — `worktrees/<plan-identifier>/` where the identifier matches the plan-folder
   identifier (folder name minus the `YYYY-MM-DD__` prefix). Wrong format or identifier mismatch:
   **HIGH**.
3. **Provisioning command present** — the `claude --worktree <plan-identifier>` command shown verbatim
   as the optional manual pre-provisioning path (plan-execution Step 0 auto-provisions from latest
   `origin/main` by default, but the manual command must still be documented). Missing or wrong:
   **MEDIUM**.
4. **Cross-reference** — link to
   [Worktree Path Convention](../../../../repo-governance/conventions/structure/worktree-path.md)
   and/or
   [Plans Organization Convention §Worktree Specification](../../../../repo-governance/conventions/structure/plans/29-worktree-specification.md#worktree-specification).
   Missing: **LOW**.
5. **Worktree cap — at most one worktree path per repository** (enforces
   [Worktree Cap](../../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
   Scoped to the single repository `plan-checker` runs in (confirm via `git remote get-url origin` or
   `repo-config.yml`). Collect every worktree path named: the top-level declaration, every `Worktree`
   column value in `### Delivery Boundaries`, and any other `worktrees/<...>/` path mentioned. More
   than one distinct path for this repo: **HIGH** — the cap permits exactly one worktree per
   repository per plan, reused across every delivery unit; a second distinct path is a defect even if
   each is individually well-formatted.

**Finding severity**: missing section: **HIGH**. Wrong format/identifier mismatch: **HIGH**. Missing
provisioning command: **MEDIUM**. Missing cross-reference: **LOW**. More than one distinct worktree
path for this repository: **HIGH**.

## 11. Execution-Grade Clarity Validation (Step 5e — MANDATORY HARD RULE)

After Step 5d, audit every delivery checkbox — plans are executed by sonnet-tier agents,
authoring-grade hand-waving is a HARD RULE violation.

**What to validate**: every checkbox satisfies all that apply:

1. **Explicit file path(s)** for file-touching actions. When unknowable at authoring time, give the
   maximum-detail target (parent directory, naming pattern, sibling reference). Bare "the auth file",
   "the relevant config", "wherever needed": **HIGH**.
2. **Explicit shell command(s)** for command actions (e.g. `npx nx run ose-web:test:quick`). Bare
   "run the lint", "run tests", "validate": **HIGH**.
3. **Concrete acceptance criterion** stating the observable proof of done (e.g. "`nx run
ose-web:typecheck` exits 0"). Bare "implement X", "set up Y", "configure Z", "add caching", "fix
   the bug": **HIGH**.

**How to audit**: for each `- [ ]` line, identify whether it edits a file, runs a command, verifies an
outcome, then check the corresponding element is present. **Exempt the final PR-merge step** from (b)
and (c) — a governance gate whose acceptance criterion is the PR Merge Protocol's five preconditions,
not a scripted command; this exemption does not extend to (a), nor to phase-gate/verification
checkboxes merely mentioning merging. Treat each missing element as a separate **HIGH** finding (one
per element per checkbox — plan-fixer batch-resolves).

**Finding severity**: bare action verbs without path/command/criterion: **HIGH** per checkbox. Path
placeholder without resolution: **HIGH**. Command placeholder without verbatim invocation: **HIGH**.
Missing acceptance criterion where the action could partially complete without external proof:
**HIGH**. Multiple missing elements on one checkbox: still ONE finding. Final PR-merge step missing
(b)/(c): not a finding.
