# Rule 14: Executor-Tag Validation (Step 5h — MANDATORY HARD RULE)

Enforces
[Plans Convention §Executor Tagging](../../../../repo-governance/conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule):
every checkbox marks who executes it so an execution agent never attempts a physically impossible
action.

**What to validate**:

1. **Legend present** — `delivery.md` (or a single-file plan's Delivery Checklist section) defines the
   `[AI]`/`[HUMAN]`/`[AI+HUMAN]` legend at the top. Missing: **HIGH**.
2. **Human-only steps tagged `[HUMAN]`** — physical acts, BIOS/firmware/hardware changes, external
   vendor-portal actions needing human auth/2FA/biometrics, account creation, real-world-presence
   steps. Untagged: **HIGH**.
3. **`[AI]` steps genuinely AI-executable** — a step tagged `[AI]` (or unmarked) that actually needs a
   human is **HIGH**. Where a human must supply a value an agent then consumes, split into a separate
   `[HUMAN]` checkbox (supply) and `[AI]` checkbox (consume) — a merged single-checkbox attempt is
   **MEDIUM** (imprecise granularity); `[HUMAN → AI]` is not this repo's vocabulary (only three tags
   exist).
4. **Tagging is orthogonal to suggested-executor** — don't conflate `[AI]`/`[HUMAN]` with `_Suggested
executor: <agent>_`; both may appear on one step. Confusion: **MEDIUM**.
5. **Git-mechanical steps must be `[AI]`** — worktree provisioning (`git worktree add`), commit and
   push (to the PR branch or `origin main`), and worktree removal are git-mechanical and an agent
   performs them directly. A `[HUMAN]`-tagged worktree-create/-remove/push step is **HIGH** — including
   a `[HUMAN]` "review the diff and approve push" gate (pushing to a PR branch is not a merge).
   Exception: the user or plan explicitly requested an out-of-band sign-off. See
   [Git Push Default Convention](../../../../repo-governance/development/workflow/git-push-default.md).
   This rule governs the push, NEVER the merge — the merge is a separate step, `[AI]` by default, and
   a plan may explicitly opt into a `[HUMAN]` merge gate (see rule 19/Step 5m). A `[HUMAN]` merge step
   is NOT a finding under this rule.

**Finding severity**: missing legend: **HIGH**. Untagged (or `[AI]`-tagged) human-only step: **HIGH**
per occurrence. `[HUMAN]`-tagged git-mechanical step (worktree/push) absent explicit sign-off request:
**HIGH** per occurrence (does not apply to a `[HUMAN]` merge step — governed by rule 19).
Executor-tag/suggested-executor conflation: **MEDIUM**.

**Capability-dependent tags**: a step may also be mis-tagged for assuming a tool the agent lacks — for
Vercel-deployed surfaces that judgement belongs to rule 21; never double-report the same step under
both rules.
