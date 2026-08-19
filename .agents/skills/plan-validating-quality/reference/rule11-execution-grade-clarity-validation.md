# Rule 11: Execution-Grade Clarity Validation (Step 5e — MANDATORY HARD RULE)

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
