# Execution-Grade Clarity Fixes (HARD RULE)

When a delivery checkbox lacks explicit file paths, verbatim commands, or a concrete acceptance
criterion, rewrite with maximum detail.

Before rewriting, check whether the checkbox is a finite cross-repository lifecycle binding that
satisfies the canonical same-document controlled runbook-reference exception in
`repo-governance/conventions/structure/plans/execution-grade-clarity.md`. A valid binding is not a
finding; an incomplete binding is repaired against that canonical rule rather than by duplicating it.

**Confidence**: **HIGH** — the missing element can be derived from the chosen technical form (its
file-impact section names the file, the project list implies the Nx command, the Gherkin criterion implies the test
command) — apply automatically. **MEDIUM** — genuinely ambiguous even on careful read — skip and
flag, invent nothing. **FALSE_POSITIVE** — the checkbox describes a non-mechanical decision (e.g.
"Decide whether to keep dual-write enabled") that legitimately has no path/command/criterion — rare;
convert to a `> Decision:` blockquote if appropriate, otherwise classify FALSE_POSITIVE.

**Rewrite recipe**: (1) file path — search the chosen technical form for the named subsystem and
file-impact tree (for directory form, follow the map in `tech-docs/README.md`); for new files give
parent directory + naming pattern + sibling reference;
(2) shell command — match the project's Nx target conventions, quote verbatim in backticks; (3)
acceptance criterion — express as the observable change (passing test, typecheck exit 0, a grep
returning a specific count, a file containing a specific string).

**Rewrite examples**: see the Bad/Good Examples section of
`.claude/skills/plan-creating-project-plans/SKILL.md` for the three canonical before/after pairs
(caching, middleware, lint) — apply the same transformation shape.

After rewriting, re-read the checkbox and confirm a sonnet-tier agent could execute it without
consulting any other section. Repeat until self-contained.

For a rule-affecting plan, never repair a missing propagation packet with “run
rules-propagation.” Confirm each affected repository and add separate actions for subject inventory,
conflict/precedence and supersession, placement/eviction, canonical/config/enforcement/index edits,
enforcement dispositions, generated bindings, verification plus `rules-quality-gate`, manifest and
final status, and sibling obligation. Each action carries the exact repository, bounded discovery or
path, invocation, expected observation, failure handling, and evidence destination.

**Never apply this rewrite to a merge step.** A merge step missing a verbatim command or acceptance
criterion is out of scope here and stays governed by How to Fix a Merge-Tag Mismatch above —
supplying a scripted `gh pr merge` command must never become the mechanism that converts a `[HUMAN]`
gate to `[AI]`.
