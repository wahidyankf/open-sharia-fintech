# Executor-Tag/Phase-Gate, Anti-Hallucination, and Knowledge Capture Fixes

## Executor-Tagging and Phase-Gate Fixes (Step 5h Findings)

Per
[Plans Organization Convention §Execution Markers](../../../../repo-governance/conventions/structure/plans/17-executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)
and
[§Phase Gates and Natural Pauses](../../../../repo-governance/conventions/structure/plans/20-phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule).

**1. Missing Executor Legend** — **HIGH**: insert the canonical legend as the first lines of
`delivery.md` (before `## Worktree`), or at the top of a single-file plan's Delivery Checklist:

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
```

**2. Human-Only Step Tagged `[AI]`** — **HIGH** when unambiguously human-only (physical action,
out-of-band approval, real-credential handling outside a sanctioned `[AI]` channel): prepend
`[HUMAN]`, phrase the acceptance criterion as a human confirmation. **MEDIUM** when it's unclear
whether a sanctioned `[AI]` channel exists — don't guess.

**3. Over-Tagged `[HUMAN]` Mechanical Step** — **HIGH** when a file edit, shell command, or grep is
tagged `[HUMAN]` with no justification: retag `[AI]`. **FALSE_POSITIVE** when the plan documents a
real reason (a sanctioned-channel exception explicitly declined). The three git-mechanical lifecycle
steps are the most common over-tags — retag each `[AI]` at **HIGH**:
`[HUMAN] Create worktree: git worktree add …` → `[AI]`;
`[HUMAN] Review the diff and approve push …` → rewrite as `[AI] Commit and push to origin
<pr-branch>` (default `worktree-to-pr`) or `[AI] Commit and push to origin main` (direct-push) —
drop the approve-push gate either way, pushing to a PR branch is not a merge;
`[HUMAN] Remove the worktree: git worktree remove …` → `[AI]`.

**Never apply this recipe to a merge step.** The PR merge is a separate step from the push; `[AI]`
is its default actor, and a `[HUMAN]` tag on it is itself the legitimate opt-in — the tag IS the
declaration, no separate field to check. See the merge-step guard in
`01-merge-step-guard-and-confidence.md`. Retagging a declared `[HUMAN]` merge step to `[AI]` — or
rewriting it into a direct push to `origin main` — would strip a deliberate gate and bypass the PR
entirely. **FALSE_POSITIVE** only when the user's prompt or the plan explicitly requested an
out-of-band sign-off for that change.

**4. Missing `### Phase N Gate`** — **HIGH**: append a gate derived from that phase's work items:

```markdown
### Phase N Gate

> All checks below must pass before starting Phase N+1.

- [ ] [AI] `<verification command derived from a phase work item>` — <acceptance>

> **Pause Safety**: <coherent state after this phase>. Safe to stop. To resume: `<re-verify command>`.
```

If work items lack concrete acceptance criteria to derive gate checks from, classify **MEDIUM**
rather than inventing verification commands.

**5. Missing Pause Safety Note** — **HIGH** when a gate exists but has no following
`> **Pause Safety**:` blockquote — add one stating the safe-to-stop state and the resume command,
derived from the phase's effect. **MEDIUM** if the end-state cannot be confidently summarized.

**6. Missing Handoff/Resume Signal on a `[HUMAN]` Step** — a merge step is exempt (its human gate
IS the signal — adding a resume signal here must never become the route by which a merge step
acquires a scripted git command). Every other `[HUMAN]` step needs (a) what the human does and (b)
the observable resume signal:

```markdown
- [ ] [HUMAN] <existing step description>. Observable resume signal: <describe signal>;
      verify with `<runnable command>`.
```

**7. Missing Legend When `[HUMAN]` Markers Are Present** — insert immediately after the
`# Delivery…` heading (or after `## Worktree` if present):

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: reserved for steps only a human can perform — physical/hardware actions,
> out-of-band approvals (sign a contract, pay an invoice), or interactive credential/SSO gates
> an agent cannot script. `[AI+HUMAN]`: agent prepares, human approves or finishes. Every
> `[HUMAN]` step states what the human does and the observable signal the agent checks to resume.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification
> checklist plus a **Pause Safety** note (the safe-to-stop state after the phase and the
> single command to resume). A phase is **not complete until its gate is green**; do not start
> phase N+1 while any check in phase N's gate is failing.
```

**Confidence**: **HIGH** — missing legend/gate/Pause-Safety note, unambiguous human-only step
mis-tagged `[AI]`, unjustified `[HUMAN]` on a mechanical step — all mechanically derivable.
**MEDIUM** — sanctioned-channel ambiguity, or a gate/note that can't be derived without authoring
judgment. **FALSE_POSITIVE** — a documented sanctioned-channel exception, or a legend/gate under
different wording.

## Anti-Hallucination Fixes (Step 5f Findings)

Per the
[Plan Anti-Hallucination Convention](../../../../repo-governance/development/quality/plan-anti-hallucination.md):
apply a fix only AFTER running the verification recipe for that claim category. If the recipe cannot
establish the correct value, classify MEDIUM — never invent a replacement. Replacing one
hallucination with another that looks more plausible is the single most damaging fixer behaviour.

**Mandatory repo-grounding before apply** — per
[§Repo-Grounding Rule](../../../../repo-governance/development/quality/plan-anti-hallucination/05-repo-grounding-rule-hard.md#repo-grounding-rule-hard):

```bash
# File path replacement — confirm the target exists OR mark _New file_
test -f <new-path> && echo "HIGH apply" || echo "MEDIUM manual"

# Nx target replacement — confirm target appears in project.json
jq -r '.targets | keys[]' apps/<project>/project.json | grep -qx '<target>' && echo "HIGH apply" || echo "MEDIUM manual"

# Package version replacement — confirm value matches the manifest
jq -r '.dependencies.<pkg> // .devDependencies.<pkg>' package.json

# Symbol replacement — confirm grep evidence
rg -l "<symbol>" apps/ libs/

# Agent / skill name replacement — confirm definition exists
test -f .claude/agents/<name>.md && echo "HIGH apply" || echo "MEDIUM manual"
```

If the recipe fails: search for a correct value, re-run the recipe with it; if still no correct
value, classify MEDIUM, write into `## Manual Review Required`, do NOT apply.

**Per-Anti-Pattern fix strategy**: AP-1 (version without manifest evidence) → `jq` the manifest,
replace + `[Repo-grounded]` label. AP-2 (file path doesn't exist, not marked NEW) → `Glob` for the
intended file; replace if found, else append `_New file_` and add a creation step. AP-3 (invalid Nx
target) → read `project.json`, replace with closest real match, else MEDIUM. AP-4 (fabricated
function/method name) → delegate to `web-researcher` (or escalate MEDIUM). AP-5 (fabricated numeric
KPI) → rewrite as observable check/cited measurement/qualitative reasoning/`_Judgment call:_` (never
invent a number). AP-6 (fabricated test name) → `Grep` for the real name if pre-existing, else append
`_New test_` and ensure the checklist creates it. AP-7 (agent/skill name doesn't resolve) → list
`.claude/agents/`/`.claude/skills/`, find closest match, else MEDIUM. AP-8 (CLI flag without
evidence) → run `<cmd> --help`, append `[Repo-grounded]` if confirmed, else replace with verified
usage. AP-9 (behavior claim without source) → delegate to `web-researcher`, embed inline excerpt +
URL + access date, classify HIGH only after citation appended. AP-10 (broken cross-link) → resolve
relative path, update if moved, else MEDIUM.

**Confidence**: **HIGH** — verification recipe passes after replacement, mechanically derived.
**MEDIUM** — replacement value can't be mechanically derived (interpretation/judgment/multi-page
research needed) — write to `## Manual Review Required`. **FALSE_POSITIVE** — claim WAS verifiable
but the checker missed the confidence label or recipe context (e.g. inside a code-fence quoting a
repo file) — document per the Skip-List protocol.

**Refuse-on-uncertainty applies to fixes too**: (1) skip the line if the surrounding content stays
coherent; (2) add `[Unverified]`, classify MEDIUM, escalate; (3) convert to `_Judgment call:_` when
genuinely subjective; (4) convert to `_Unknown — verify before authoring_` placeholder with an Open
Questions delivery item. Forbidden: a more-plausible-sounding hallucination.

**Never apply refusal option 1 — or any option here — to a merge step.** Removing a merge step's
line to resolve an unverified claim inside it deletes the plan's human-gate opt-in as a side effect
of an unrelated fix — merge steps commonly carry a relative link to the PR Merge Protocol, and plan
folders sit deep enough that such links break routinely, so this path is reached in normal operation.
On a merge step, fix the claim in place or classify MEDIUM; never remove the line.

## Knowledge Capture Phase Scaffolding Fixes (Step 5l Findings)

Per the
[Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md):
when silent absence is flagged (no phase, no explicit "none" record anywhere), scaffold the missing
phase and `learnings.md`. Never fabricate learnings execution never actually surfaced — scaffold
structure, not content.

**Confidence**: **HIGH** — the phase is completely absent AND `learnings.md` doesn't exist —
scaffold both. **MEDIUM** — unclear from the plan's history whether execution genuinely surfaced no
learnings — scaffold the phase with the routing rubric and both safety gates intact, but don't
auto-write the explicit "none" escape; flag under `## Manual Review Required`. **FALSE_POSITIVE** — a
phase already exists under different heading wording, or `learnings.md` already carries the explicit
"none" record — don't duplicate; at most rename the heading.

**How to scaffold `learnings.md`** (if absent, at the plan-folder root, sibling to `delivery.md`):

```markdown
<!-- Running log of generalizable learnings surfaced during execution. Triage every entry at
     the Knowledge Capture phase before archival. See
     repo-governance/development/quality/knowledge-capture.md -->
```

**How to scaffold the Knowledge Capture phase** — insert as the FINAL substantive phase in
`delivery.md`, immediately before Plan Archival:

```markdown
## Phase N: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason
- [ ] [AI] Apply the secret/sensitivity gate — sanitize any secret, credential, token, or private
      hostname to a `<placeholder>` token, or discard if unsanitizable
- [ ] [AI] Apply the repo-relevance gate — infra-private content stays in `ose-private` only and is
      NEVER cross-routed into `ose-public`/`ose-primer`
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix; code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate
      `plans/backlog/<slug>/` plan, NEVER landed inline (the only carve-out is a genuine blocker
      required to finish this plan's own scope)
- [ ] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same area — fold in rather than creating a
      new file
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>`
      in `learnings.md`

### Phase N Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded
      with reason), or the explicit "none" escape is recorded
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly empty). Safe to stop. To
> resume: re-read `learnings.md` and confirm every entry is terminal.
```

After scaffolding, re-read both the inserted phase and `learnings.md`; confirm the phase sits
immediately before Plan Archival and the file exists at the plan-folder root. Do not auto-tick any
scaffolded checkbox — they are the author's/executor's remaining work.
