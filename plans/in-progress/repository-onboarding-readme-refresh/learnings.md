# Learnings: repository-onboarding-readme-refresh

<!-- Append generalizable, sanitized observations during execution. -->
<!-- Never copy secrets or sensitive private-repository facts into this file. -->
<!-- Triage every entry before archival, or record the explicit none escape. -->

## L-001 — `rhino-cli` exit codes cannot prove a subcommand exists

**Phase**: 0 (P0-003A) · **Date**: 2026-08-20

A `rhino-cli` command group requires a subcommand, so `rhino-cli md --help` exits `2` with
`error: 'rhino-cli md' requires a subcommand but one was not provided`. `rhino-cli help md mermaid`
also exits `2` even though it prints the full help page successfully. Any existence check written as
`cmd --help && echo ok` therefore reports every real subcommand as missing.

**How to apply**: verify a subcommand by parsing the `Commands:` section of
`rhino-bin.sh --no-color help <group> <subcommand>`, never by its exit status. Pass `--no-color`
so ANSI escapes do not defeat the parser.

## L-002 — A plan's transcribed gate list is a subset, not the registry

**Phase**: 0 (P0-003/P0-003A) · **Date**: 2026-08-20

The live `pre-commit` registry declares 29 entries; this plan transcribed eight. The gap was benign
for most of them (language formatters a documentation diff never triggers) but hid three gates that
genuinely fire on this plan's own footprint: `repo-config validate`, `convention emoji validate`,
and `git lockfile sync`.

**How to apply**: when a plan transcribes a gate list, reconcile it in both directions at Phase 0 —
not only "does every transcribed command exist" but also "which live gates does the transcription
omit that this plan's declared file footprint can trip."

## L-003 — `npm run lint:md` walks into the untracked `.fvm-cache/` SDK

**Phase**: 0 (P0-005) · **Date**: 2026-08-20 · **Routing**: repository configuration — file as a
`plans/backlog/` item at Phase 8, do not fix inline

`.fvm-cache/` is gitignored (`.gitignore:198`) and holds a vendored Flutter SDK, but it appears in
neither `.markdownlintignore` nor the `ignores` array of `.markdownlint-cli2.jsonc`. The
`markdownlint-cli2 "**/*.md"` glob therefore walks into it, and `npm run lint:md` reports 565 errors
from third-party SDK documentation. Every one of those errors is phantom: zero markdownlint errors
exist in tracked repository content. The failure is invisible to CI, which scopes to affected files.

**How to apply**: a repo-wide `**/*.md` script needs its ignore list kept in sync with `.gitignore`
for vendored trees, or a red baseline trains readers to ignore the gate. Adding one `.fvm-cache/`
line to `.markdownlintignore` would restore the signal.

## L-004 — `governance readme-index validate` prints FAILED but exits 0

**Phase**: 0 (P0-009) · **Date**: 2026-08-20

`gate run --surface=pre-push` exits 0 while its own output contains
`README INDEX AUDIT FAILED: 425 finding(s)`. Running the validator alone reproduces it: the audit
prints `FAILED`, lists every finding, and still exits `0`. The textual verdict and the exit status
disagree, so an executor that trusts either one alone reaches the wrong conclusion — trusting the
exit code hides 425 real findings, and trusting the text blocks a surface the repository considers
green.

**How to apply**: when a gate's acceptance is "exits 0", record the exit code **and** scan the
output for a textual failure verdict. Treat the two as independent signals, and say which one the
acceptance criterion actually depends on.

## L-005 — The per-gate tick/task count assertion is what catches a silent no-op tick

**Phase**: 0 (P0-G01) · **Date**: 2026-08-20

P0-006A's implementation notes were written and its task closed, but its checkbox stayed `- [ ]`.
Nothing errored: the notes edit succeeded, the task list looked correct, and only the phase-gate
assertion `count('- [x]') == count(completed tasks)` exposed the gap — 13 ticks against 14 closed
tasks. Anchoring the tick edit on the literal `- [ ]` marker makes such an edit fail loudly, but it
cannot help when the tick edit is simply never issued.

**How to apply**: run the independent count at **every** phase gate, not only at plan end. It is the
only instrument that detects a tick that was never attempted, as opposed to one that mis-anchored.

## L-006 — `git ls-tree` silently returns nothing for a `*.md` pathspec

**Phase**: 1 (P1-001/P1-002) · **Date**: 2026-08-20

`git ls-tree -r --name-only <sha> -- '*.md'` returns **zero** paths and exits 0. `git ls-tree` does
not accept glob pathspec magic — `:(glob)` fails outright with
`pathspec magic not supported by this command` — so the wildcard is matched literally and nothing
hits. The same wildcard works with `git ls-files`, which is why the form reads as correct. At the
recorded revision the true count is 9,294; the pathspec form reported 0.

This is the dangerous shape of a false zero: an inventory step whose acceptance is "every path is
classified" passes trivially on an empty list. Three plan sites carried the broken form.

**How to apply**: enumerate a revision's files with
`git ls-tree -r --name-only <sha> | grep -E '\.md$'`, and give every inventory acceptance clause a
non-zero floor plus a cross-check against an independent enumerator (`git ls-files '*.md'`) so an
empty result fails instead of passing.

## L-007 — A repo-wide validator cannot serve as a per-row acceptance gate

**Phase**: 1 (P1-G01) · **Date**: 2026-08-20

745 of the ledger's 814 rows shared one acceptance template naming bare `md links validate`. The
command is repo-wide and unscoped, and at the recorded revision it reports `found 312 broken links`
— every one of them inside `plans/done/**`, a tree the same ledger classifies `historical-exempt`
and forbids editing. The clause therefore could never pass for any row, no matter what the executor
did to that row's own document. The inverse failure is just as easy to write: a repo-wide validator
that is already green makes every row's acceptance pass without the row being touched.

The independent reviewer at the phase gate found this; none of the seven preceding self-checks did,
because each of them read the clause as well-formed rather than executing it.

**How to apply**: when a per-item acceptance names a repository-wide validator, either scope the
command to the item (`--exclude` the exempt trees, or filter its output to the item's own section)
or state explicitly how the executor reads a single item's verdict out of a global report. Then run
it once as literally written and confirm the verdict it returns today is the one the clause expects
**before** the edit — a clause that is already-pass or never-pass is not an acceptance criterion.

## L-008 — A fact check on documentation must know what is a claim

**Phase**: 1 (P1-G01) · **Date**: 2026-08-20

The ledger's shared acceptance clause said "every npm script the document names resolves." Swept
across the corpus that is wrong four times over. `docs/explanation/.../fe-react/build-deployment.md`
names `npm run test:ci` and `npm run deploy` inside a fenced GitHub Actions example teaching a
general React pattern — those are not claims about this repository at all.
`.../c4-architecture-model/tooling-standards.md` names `npm run validate:diagrams` three times, each
explicitly labelled "Future" or "Implementation pending" — the document is already accurate, and a
literal check would fail it for being honest. Meanwhile its sibling
`.../c4-architecture-model/README.md` names the same non-existent script with no qualifier, which is
a real defect the check should catch.

Same string, three different verdicts. A mechanical resolution check cannot tell them apart, so the
clause has to carry the distinction itself.

**How to apply**: before writing "every X the document names must resolve", ask what makes something
a claim. Exempt mentions the document frames as generic illustration or labels future/planned, and
say the exempt mention passes _on that framing being present_ — otherwise the carve-out becomes a
loophole any unresolvable command can hide behind. The check then fails exactly the case that
deserves to fail: an unresolvable command presented as current.

## L-009 — A third repo-wide Markdown validator is red, and one tree is unfixable here

**Phase**: 2 (P2-008) · **Date**: 2026-08-20 · **Routing**: repository configuration — file as a
`plans/backlog/` item at Phase 8, do not fix inline

Run unscoped, `md mermaid validate` reports 786 violations and 17 warnings across 1,165 files:
588 `label_too_long`, 198 `width_exceeded`, 17 `subgraph_density`. They sit in three trees —
`apps/ayokoding-www` (256 files), `plans/done` (32), and `apps/rhino-cli` (4). This is the third
repo-wide Markdown validator found red at a green gate surface, after `format:md:check` and
`lint:md` in Phase 0.

The gate surface stays green because the registry scopes `md-mermaid` to `affected-file-type`, so it
only ever sees staged files. Zero violations exist in this plan's own tree, and both `gate run`
surfaces exit 0 on the staged set.

Two of the three trees are ordinary backlog work. The other two are not what they look like.

All four `apps/rhino-cli` files sit under `tests/fixtures/state/` and are in the parity manifest.
Reading one settles it: `03-long-state-label.md` contains a state literally named
`ThisLabelIsLongerThan30CharsAndFails`. These are **negative fixtures** — inputs authored to make the
validator fail, so that the validator's own tests can assert it does. "Fixing" them would break the
suite that proves the gate works, and they are byte-identical with `ose-private` besides, so an edit
would open a cross-repository obligation for a change that should never be made.

`plans/done` is `historical-exempt` by this plan's own Classification Rule 3, so its 32 files want an
ignore-list entry rather than 32 rewrites of completed work.

**How to apply**: when filing a red-baseline follow-up, split the finding by what can actually be
fixed where, and open one failing file before assuming any of them is a defect. A single "fix 786
mermaid violations" item is not executable — it silently contains a set of deliberate negative
fixtures that must stay broken, a historical subset that wants an ignore-list entry rather than an
edit, and only then some real content to fix.

## L-010 — Enumerate a false claim by vocabulary, not by the line numbers a reviewer hands you

**Phase**: 2 (P2-009) · **Date**: 2026-08-20

An independent reviewer found the ledger asserting that `apps/rhino-cli/**` and
`specs/apps/rhino/behavior/rhino-cli/**` are byte-identical with `ose-private`. The real boundary is
seven pathspecs in `BOUNDARY_PATHS`, and of the 27 `identity-bound` Markdown paths exactly 25 are in
the 603-entry parity manifest. The reviewer named four sites. I fixed those four. The next pass
found the claim alive at two more — including the vocabulary entry that _defines_ the label the fix
was about, sitting 1,150 lines above the correction.

Only the third pass closed it, and it closed because the method changed: instead of patching the
cited line numbers, I grepped the whole plan directory for every term in the claim's vocabulary
(`byte-identical`, `byte identity`, `identity-bound`, `identity boundary`, `zero carve-outs`),
classified all 47 hits as definition, assertion, or incidental reference, and rewrote every
definition and assertion. The reviewer then enumerated independently and found no seventh site.

Two of the six sites were ones neither of us had looked at, and one of those carried a second,
unrelated error — it claimed the paths were audited `verified-unchanged` while the ledger recorded
them `identity-bound`.

**How to apply**: a reviewer's line numbers are a sample, not the population. When a finding is
"this claim is false", the unit of repair is the claim, so enumerate every place the claim's
vocabulary appears across every file in the delivery unit, and give each site a verdict. Check the
definitional sites first — a wrong definition re-injects the error into every downstream use of the
term, including the ones you just fixed. See [[feedback_fix_the_class_not_the_named_sites]].
