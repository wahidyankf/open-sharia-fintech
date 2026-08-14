# Rules 12-15: Anti-Hallucination, Harness-Neutrality, Executor-Tag, Phase-Gate

## 12. Anti-Hallucination Scan (Step 5f — MANDATORY HARD RULE)

After Step 5e, scan the whole plan for unverified factual claims matching the
[Plan Anti-Hallucination Convention §Anti-Pattern Catalog](../../../../repo-governance/development/quality/plan-anti-hallucination/14-anti-pattern-catalog-ap-1-through-ap-4.md#anti-pattern-catalog).

**A. Confidence-label coverage** — every non-trivial claim about a file path, Nx target, package
version, API signature, agent/skill name, behavior, external standard, or numeric KPI carries
`[Repo-grounded]`, `[Web-cited]`, `[Judgment call]`, or `[Unverified]` inline, or appears inside a
repo-file-quoting code fence. Bare unlabeled claims default to `[Unverified]`: **MEDIUM** per claim.

**B. Anti-Pattern Catalog scan**:

- **AP-1** version cited without `package.json`/lockfile evidence: **HIGH**
- **AP-2** file path cited that doesn't exist and isn't marked `_New file_`: **HIGH**
- **AP-3** Nx target cited absent from the project's `project.json`: **HIGH**
- **AP-4** function/method name cited without import-path evidence or web citation: **HIGH**
- **AP-5** numeric KPI presented as measured fact with no baseline: **HIGH**
- **AP-6** test name cited that doesn't exist and isn't marked `_New test_`: **HIGH**
- **AP-7** agent/skill name cited that doesn't resolve to `.claude/agents/<name>.md` or
  `.claude/skills/<name>/SKILL.md`: **HIGH**
- **AP-8** CLI flag cited without `<cmd> --help` evidence or repo-doc reference: **MEDIUM**
- **AP-9** behavior claim cited without a source: **MEDIUM**
- **AP-10** cross-link target resolving to a non-existent file: **HIGH**

(all per occurrence)

**C. Suggested-executor annotation validity** — where a checkbox carries `_Suggested executor:
<agent-name>_`: the agent file exists at `.claude/agents/<name>.md` (missing: **HIGH**, counts as
AP-7); the agent's role suits the action (e.g. `swe-fsharp-dev` for a `.fs` edit, not
`swe-typescript-dev`; mismatch: **MEDIUM**).

**D. Web-citation completeness** — every `[Web-cited]` claim includes URL, access date, and excerpt
inline; missing any element: **MEDIUM** per occurrence; URL-only citation is forbidden.

**How to audit**: read each file top-to-bottom; for every sentence asserting a file path, Nx target,
version, API surface, agent/skill name, behavior, or metric, check the corresponding recipe row from
[Plan Anti-Hallucination Convention §Repo-Grounding Rule](../../../../repo-governance/development/quality/plan-anti-hallucination/05-repo-grounding-rule-hard.md#repo-grounding-rule-hard);
run the recipe (`Bash test -f`, `Glob`, `Grep`, `jq` against `project.json`, etc.); file a finding
under the matching Anti-Pattern on failure. For external claims, verify URL/access-date/excerpt; if
multi-page research was warranted, verify `web-researcher` delegation is documented.

**Re-validation caching (iterations 2+)**: `[Repo-grounded]` claims re-run only if the file changed;
`[Web-cited]` claims trusted unless newly invalidated; new claims from fixer edits verified normally.

**Finding severity**: AP-1/2/3/4/5/6/7/10: **HIGH** per occurrence. AP-8/9, missing `[Web-cited]`
excerpt, executor mismatch: **MEDIUM** per occurrence. Bare unlabeled claim (defaults
`[Unverified]`): **MEDIUM** per claim. Missing `web-researcher` delegation when the multi-page
threshold was crossed: **MEDIUM**.

## 13. Harness-Neutrality Scan (Step 5g — CONDITIONAL)

Run only when the plan touches agents, skills, rules, or `repo-governance/` paths; skip when it
touches only application code and tests. Skipping this check when in scope is **CRITICAL**.

**What to validate**:

1. **Agent definitions follow multi-harness-binding conventions** — frontmatter fields (`name`,
   `description`, `tools`, `model`, `color`, `skills`) present and correctly formatted per
   [AI Agents Convention](../../../../repo-governance/development/agents/ai-agents.md); `color` uses a
   named value (not an OpenCode theme token or hex code); `tools` uses the Claude Code array format.
   Non-conforming agent: **HIGH** per violation.
2. **Agent mirrors are generated, not hand-written** — no step instructs manual editing or direct
   creation of `.opencode/agents/` files. Hand-written secondary binding: **HIGH**.
3. **Skill body is plain markdown** — `SKILL.md` files contain no Claude-Code tool invocations or
   OpenCode-specific YAML beyond skill metadata. Harness-specific syntax in skill body: **HIGH**.
4. **No manual OpenCode skill mirror** — OpenCode reads `.claude/skills/<name>/SKILL.md` natively; no
   `.opencode/skill/` or `.opencode/skills/<name>/` mirror should exist. Manual mirror: **HIGH**.
5. **Governance doc changes outside "Platform Binding Examples" heading** — proposed
   `repo-governance/` content changes live outside any `## Platform Binding Examples` heading unless
   intentionally vendor-specific. Violation: **MEDIUM**.

Reference:
[Multi-Harness Binding Convention](../../../../repo-governance/conventions/structure/multi-harness-binding.md)
and
[Governance Vendor-Independence Convention](../../../../repo-governance/conventions/structure/governance-vendor-independence.md).

**Finding severity**: missing this check when in scope: **CRITICAL**. Hand-written secondary
binding: **HIGH**. Agent frontmatter violation: **HIGH** per violation. Skill body harness-specific
syntax: **HIGH**. Manual OpenCode skill mirror: **HIGH**. Governance change under vendor-specific
heading: **MEDIUM**.

## 14. Executor-Tag Validation (Step 5h — MANDATORY HARD RULE)

Enforces
[Plans Convention §Executor Tagging](../../../../repo-governance/conventions/structure/plans/17-executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule):
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

## 15. Phase-Gate and Natural-Pause Validation (Step 5i — MANDATORY HARD RULE)

Enforces
[Plans Convention §Phased Delivery: Natural Pauses and Phase Gates](../../../../repo-governance/conventions/structure/plans/20-phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule):
every phase ends at a natural pause and closes with an explicit gate.

**What to validate**:

1. **Every phase has a `### Phase N Gate`** — including Phase 0 and the final verification phase.
   Missing: **HIGH** per phase.
2. **Gate has both required parts** — (a) a must-pass verification checklist opening with "all checks
   must pass before starting Phase N+1", executor-tagged with explicit commands and expected results,
   and (b) a `**Pause Safety**` blockquote stating the safe-to-stop state and the resume command.
   Missing either: **MEDIUM**.
3. **Each phase is a natural pause** — after the phase, the repo reaches a self-consistent,
   safe-to-stop state (clean tree or intentional no-op; no half-applied migration, broken build,
   staged secret, or resource left mid-mutation). Unsafe stop-state: **MEDIUM** — remedy: merge with
   an adjacent phase rather than weaken the gate.
4. **No invented pauses** — two adjacent phases each claiming a pause that isn't actually safe: flag
   the split **MEDIUM**, recommend merging.

**Grandfathering — in-progress plans predating the convention**: per
[Plans Organization Convention §Applicability](../../../../repo-governance/conventions/structure/plans/20-phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule),
the Execution-Marker and Phase-Gate HARD RULES apply to net-new plans at authoring time. Plans already
under `plans/in-progress/` when the convention landed are grandfathered — do not raise HIGH findings
against them solely for missing `[AI]`/`[HUMAN]` markers or missing gate/Pause-Safety notes; flag
those omissions only on phases newly added or edited. A net-new plan gets no grace. Note grandfathered
skips as below-threshold informational items, not HIGH findings.

**Finding severity**: phase missing its Gate: **HIGH** per phase. Gate missing the checklist or Pause
Safety note: **MEDIUM** per phase. Non-genuine-pause phase (should merge): **MEDIUM** per phase.
