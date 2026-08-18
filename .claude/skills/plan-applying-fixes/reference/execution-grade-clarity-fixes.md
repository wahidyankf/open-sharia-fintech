# Execution-Grade Clarity Fixes (HARD RULE)

When a delivery checkbox lacks explicit file paths, verbatim commands, or a concrete acceptance
criterion, rewrite with maximum detail.

**Confidence**: **HIGH** — the missing element can be derived from plan context (`tech-docs.md`
names the file, the project list implies the Nx command, the Gherkin criterion implies the test
command) — apply automatically. **MEDIUM** — genuinely ambiguous even on careful read — skip and
flag, invent nothing. **FALSE_POSITIVE** — the checkbox describes a non-mechanical decision (e.g.
"Decide whether to keep dual-write enabled") that legitimately has no path/command/criterion — rare;
convert to a `> Decision:` blockquote if appropriate, otherwise classify FALSE_POSITIVE.

**Rewrite recipe**: (1) file path — search `tech-docs.md` for the named subsystem, check "Files to
modify"/"Files to create", for new files give parent directory + naming pattern + sibling reference;
(2) shell command — match the project's Nx target conventions, quote verbatim in backticks; (3)
acceptance criterion — express as the observable change (passing test, typecheck exit 0, a grep
returning a specific count, a file containing a specific string).

**Rewrite examples**: see the Bad/Good Examples section of
`.claude/skills/plan-creating-project-plans/SKILL.md` for the three canonical before/after pairs
(caching, middleware, lint) — apply the same transformation shape.

After rewriting, re-read the checkbox and confirm a sonnet-tier agent could execute it without
consulting any other section. Repeat until self-contained.

**Never apply this rewrite to a merge step.** A merge step missing a verbatim command or acceptance
criterion is out of scope here and stays governed by How to Fix a Merge-Tag Mismatch above —
supplying a scripted `gh pr merge` command must never become the mechanism that converts a `[HUMAN]`
gate to `[AI]`.
