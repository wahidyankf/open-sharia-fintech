# 🛠️ Correction-Unit Execution Record: Iteration `@01`

Phase 6 execution record for correction iteration `@01`.

## Why This Iteration Exists

Phase 6 was first recorded **not applicable**, and that disposition was correct on the evidence
available at the time: both Phase 5 journeys passed with zero documentation defects, so there was
nothing to correct and no branch or PR was created.

Phase 7 then did its job. Two of its items independently routed defects back here:

- **P7-005** cross-read the repeated repository-wide claims and found `CONTRIBUTING.md` teaching a
  native-Windows setup path that the recorded platform contract forbids.
- **P7-003** ran two strict read-only checkers, which converged on that same defect and surfaced a
  second one neither the journeys nor the cross-read had caught: `CONTRIBUTING.md` never names the
  Rust/Cargo prerequisite that `npm install` depends on.

This iteration is that loopback. It gets its own branch, its own PR, and this record, per the phase
preamble's rule that a merged unit is never reused.

- **Branch**: `docs/repository-onboarding-corrections`
- **Base**: `origin/main` at `1542ea044`
- **Opened**: 2026-08-21

## Correction Rows

Each row is one exact defect, its source, and what was changed. No row bundles two defects.

| ID   | Source         | Severity | File                                           | Defect                                                                                                    | Correction                                                                                                                        |
| ---- | -------------- | -------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| C-01 | P7-005, P7-003 | HIGH     | `CONTRIBUTING.md`                              | A `**Windows**:` heading plus "Download the installer from volta.sh" — a native-Windows setup path.       | Replaced with the contract's three-state platform sentence (macOS/Ubuntu supported, WSL2 unverified, native Windows unsupported). |
| C-02 | P7-003         | HIGH     | `CONTRIBUTING.md`                              | Rust and Cargo never mentioned, though `postinstall` runs `npm run doctor`, which is `cargo run …`.       | Prerequisites now name both toolchains and link the setup guide's rustup instructions.                                            |
| C-03 | P7-003         | MEDIUM   | `CONTRIBUTING.md`                              | Node and npm versions hardcoded in prose, against the repository's own single-source-of-truth rule.       | Replaced with a pointer to the versions pinned in `package.json`.                                                                 |
| C-04 | P7-003         | LOW      | `CONTRIBUTING.md`                              | "Getting Started" lists contributor steps with no in-section signal that intake is closed.                | The section opening now says so and anchors to § External Contributions.                                                          |
| C-05 | P7-003         | MEDIUM   | `CONTRIBUTING.md`                              | "Diátaxis" used twice with no gloss.                                                                      | The first normative use now defines it as a four-category documentation taxonomy.                                                 |
| C-06 | P7-003         | HIGH     | `docs/how-to/setup-development-environment.md` | Quick Start promises "this is all you need", then verifies with `npm run doctor` without installing Rust. | Added the documented rustup step, and reclassified Rust from Full to Minimal so the surrounding text agrees.                      |
| C-07 | P7-003         | LOW      | `docs/how-to/setup-development-environment.md` | Quick Start steps numbered `1, 2, 3, 4, 6` — no content missing, a renumbering slip.                      | Renumbered so the sequence is contiguous.                                                                                         |
| C-08 | P7-003         | MEDIUM   | `README.md`                                    | "WSL2" never expanded on first use, for an audience that includes non-engineers.                          | Expanded once to "WSL2 (Windows Subsystem for Linux 2)", within the 900-word budget.                                              |

**Two LOW findings were deliberately not actioned**, with reasons rather than silence: glossing
Husky and commitlint (that section's readers are already running `npm install` and reading
`package.json`), and the Quick Reference command repetition (an intentional cheat sheet, not
accidental duplication). Neither sits at a severity this program's gates block on.

## Follow-Up Sweep (P6-003B Review Findings)

The independent review of the staged diff found that two corrections had been applied only at the
site the finding named, not across the class — the exact failure mode this program has hit before.
The review's observations were resolved as follows.

**One row in this table was itself false when written, and is corrected below.** The C-03 row
claimed both surviving versions had been swept before commit. They had not: commit `cb489b874`
shipped with four hardcoded version literals still in
`docs/how-to/setup-development-environment.md`, and the sweep that row asserts was scoped to
`CONTRIBUTING.md` only. The commit message and the PR body repeated the same overstatement
("all hardcoded versions are removed"). The PR review caught it; see C-20 for the actual fix and
the corrected claim. The lesson is recorded rather than smoothed over: a sweep verified against
one file is not a class sweep, and stating it as one turned a scoping mistake into a false
gate-pass claim.

| Review finding                                                                                                                     | Severity | Resolution                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-03 half-applied: two more hardcoded versions survived, so the new "can never drift apart" sentence contradicted its own document | MEDIUM   | **This resolution was false as written.** Only `CONTRIBUTING.md` was swept; four literals survived in the setup guide and shipped in `cb489b874`. Corrected in C-20.                                                                               |
| C-06 half-applied: three statements still classified Rust as a Full-setup tool                                                     | MEDIUM   | All three corrected; Rust is now classified Minimal, with the reason (bootstrap runs the Rust tool checker) stated.                                                                                                                                |
| C-05 partial: `Diátaxis` still appeared cold in the project-structure tree                                                         | LOW      | The tree entry now points at the four categories listed directly beneath it.                                                                                                                                                                       |
| Orphaned `**macOS/Linux**:` label left by removing its Windows peer                                                                | LOW      | Block restructured: the platform statement leads, the install command follows unlabelled.                                                                                                                                                          |
| C-04's justification overstated — the closed-intake caveat was already the opening paragraph                                       | LOW      | The row was **corrected rather than defended**: reworded and downgraded MEDIUM → LOW, since the edit adds an in-section signal and an anchor, not a first surfacing.                                                                               |
| README headroom: C-08 consumed 5 of an 8-word budget margin                                                                        | LOW      | Accepted and recorded. `governance word-budget validate` reported 894 words at `cb489b874`; later rows moved it, and it stays under the 900-word fail threshold at every commit in this iteration. Any addition must still name an offsetting cut. |

The review confirmed the two things that most needed confirming: the added rustup command is
byte-identical to the one the same document already teaches in its full-setup section, and no
product or behavioral change is smuggled into this documentation unit.

## Voice Correction Rows (P7-004)

The independent read-aloud pass against the twelve-clause Human Voice Contract failed all five
documents on at least one clause. These rows are its corrections.

| ID   | Clause      | File                 | Defect                                                                                                         | Correction                                                    |
| ---- | ----------- | -------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| C-09 | V1          | tutorial             | Three sentences of product definition before the reader's task, the first verbatim from the README.            | Task paragraph now leads; the duplicated sentence is gone.    |
| C-10 | non-clause  | tutorial             | "recognise" — British spelling against an American corpus.                                                     | Aligned to "recognize".                                       |
| C-11 | V3          | `CONTRIBUTING.md`    | Nx and monorepo used cold at an audience directed to fork.                                                     | Both glossed on first use, with a link to Nx.                 |
| C-12 | V9          | `CONTRIBUTING.md`    | `npm install` failure answered only with a cache clean, though the file itself names missing Cargo as a cause. | Added a missing-Cargo entry with the real route out.          |
| C-13 | V10, V12    | `CONTRIBUTING.md`    | Closed on a bare 🚀 whose celebratory tone fights the closed-intake message, with no next step.                | Emoji removed; the file now ends on two concrete moves.       |
| C-14 | V9          | setup how-to         | Quick Start runs `source ~/.zshrc` for a path that explicitly invites Ubuntu readers.                          | Now `source ~/.zshrc   # or source ~/.bashrc on Ubuntu`.      |
| C-15 | V8          | setup how-to         | Rust step ended blind while the neighbouring Node step showed expected output.                                 | Added an expected-output line after `rustc --version`.        |
| C-16 | V3          | setup how-to         | "E2E" never expanded.                                                                                          | Expanded on first use.                                        |
| C-17 | non-clause  | setup how-to         | "Two setup paths" above three bullets.                                                                         | Corrected to "Three setup paths".                             |
| C-18 | V8          | `README.md`          | `nx show projects` block stated no outcome.                                                                    | Now says what the list contains, funded by an offsetting cut. |
| C-19 | V3, factual | related-repositories | Table described `ose-private` as doing "local CoralPolyp sandbox work" — a codename removed on 2026-08-18.     | Row now reads "infrastructure work".                          |

**C-19 is the row worth noting.** It entered as a voice finding about an unexplained term and turned
out to be a staleness defect: the sandbox it named had already been retired, and the comparison table
meant to help a reader choose a repository was describing work that no longer exists. A jargon lens
caught a fact error.

### Declined, With Reasons

| Finding                                                           | Why not actioned                                                                                                                                                                                                                 |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| README `🌙` title mark flagged under V10                          | It is the project's brand mark. Removing branding is the owner's decision, not a voice pass's.                                                                                                                                   |
| README V11 — the 386-word local-setup section is not "map" shaped | Reversing it would undo a structure that already passed a maker-checker-fixer cycle and an independent voice review in Phase 3, and the proposed rewrite would cut the file to ~700 words. That is a redesign, not a correction. |
| CONTRIBUTING V2/V5/V8 and reference-page V12 findings             | Real, but they amount to rewriting two long documents wholesale — beyond this plan's File-Impact footprint. Recorded here so a later plan can pick them up.                                                                      |
| Husky/commitlint gloss; Quick Reference repetition                | LOW, and the second is an intentional cheat sheet.                                                                                                                                                                               |

## PR #239 Review Rows (P6-007@01)

Cycle 1 of the PR-review pipeline ran the scout plus eight discipline specialists against
`cb489b874`. It surfaced defects the pre-commit review had missed, including one the pre-commit
review had wrongly reported as fixed. Every row below is a real finding acted on, not a
restatement.

**How to read this section.** It is a chronological log, not a current-state summary. The review
cycles for PR #239 land here, beginning at C-20, and later cycles corrected earlier ones, including
several that corrected a correction. The range deliberately carries no upper bound: naming one made
it false the moment the next row landed, which is how C-50 came to exist. Where a row's fix was later found wrong, the row says so and names the
row that superseded it, rather than being rewritten to look right. The chains are: C-21 → C-31 →
C-32 → C-36 (the Cargo prerequisite wording, wrong three times); C-30 → C-35 (the README word
count); C-34 → C-37 (the breakpoint amendment, first applied to too few items) → C-45 (a wrong
line-distance inside that row); and C-42 → C-46 (the rollup amendment, first argued from a label
instead of a measurement). To read what the branch currently asserts about any of those, read the
last row in the chain, not the first.

| Row  | Discipline   | Defect                                                                                                                                                                                     | Severity | Fix                                                                                                                                                                                                                                                                                                    |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| C-20 | Integrity    | The Follow-Up Sweep claimed the version sweep was complete; four literals still shipped in the setup guide, and the commit message and PR body repeated the claim                          | CRITICAL | All four replaced with commands reading the `package.json` pin; the false row and this record's framing corrected in place rather than quietly amended; PR body corrected                                                                                                                              |
| C-21 | Logic        | New troubleshooting text asserted `npm install` fails without Cargo. `postinstall` is `npm run doctor \|\| true`, so it never fails — verified by running both forms with Cargo off `PATH` | HIGH     | Every site restated: the check is silently skipped, the install still succeeds, and the failure only surfaces at an explicit `npm run doctor`. Fixed in README, CONTRIBUTING ×2, setup guide ×4, tutorial. **Superseded by C-31, C-32, and C-36**, which found this replacement wrong three times over |
| C-22 | Governance   | 34 ticked items from P5B-002 to P7-007 carried no Atomic Sync Ritual evidence block, against 84 that did                                                                                   | HIGH     | Blocks added to all 34; the count now equals the ticked count                                                                                                                                                                                                                                          |
| C-23 | Governance   | Evidence captured at 390/768/1440 px; conventions require 375/768/1280 px, and 390 is wider than 375, so the narrowest documented breakpoint was never exercised                           | MEDIUM   | Landing page re-inspected at all three documented widths; no horizontal overflow at any, zero console errors. Recorded as a supplementary capture, not a re-run of either journey                                                                                                                      |
| C-24 | Architecture | The C-18 offsetting cut removed README's only guidance for the changed-port case                                                                                                           | MEDIUM   | Restored, funded by shortening the Rust bullet, which the C-21 rewrite made shorter and more accurate at once                                                                                                                                                                                          |
| C-25 | Architecture | The platform statement had drifted: the setup guide said "not supported or verified" against "neither supported nor verified" elsewhere                                                    | MEDIUM   | Setup guide and tutorial harmonized to the P2-003 contract wording; all four documents now match                                                                                                                                                                                                       |
| C-26 | Docs         | The P7-001 ledger block asserted this file "will never be created" and that `evidence/README.md` comes later, while the same commit created this file and added eight evidence files       | MEDIUM   | Both statements amended to record what was true at the observation point without asserting a future the commit falsifies                                                                                                                                                                               |
| C-27 | Instruction  | "Minimal path" (what you install by hand) collided with `doctor --scope minimal` (which installed tools get inspected), making the linked governance workflow look contradictory           | MEDIUM   | The two senses distinguished in the setup guide; Rust's absence from the flag's set explained rather than treated as an error                                                                                                                                                                          |
| C-28 | Security     | `delivery.md` recorded a literal Docker bridge IP                                                                                                                                          | LOW      | Replaced with a placeholder. The address was private and the container destroyed, but the plan's rule has no private-range carve-out                                                                                                                                                                   |
| C-29 | Performance  | The three Phase 5B screenshots are byte-identical to their 5A counterparts                                                                                                                 | LOW      | Kept, with the reason stated: both were rendered by the same host browser against identical page bytes, so the 5B images evidence delivery from the container, not Ubuntu-side rendering                                                                                                               |
| C-30 | Self         | This record cited the README at 897 words                                                                                                                                                  | LOW      | Corrected. The figure is now pinned to a named revision, because an unpinned count goes stale the moment a later row edits the file — which is exactly what happened once before it was caught. **Superseded by C-35**, which found this corrected figure stale too                                    |

### A Gate I Reported Green That Was Not Measured (Cycle 1)

Worth recording because it is the same failure mode as C-20, caught a second time.

Every gate re-run in this iteration reported `md links validate` as "0 failures", derived from
`grep -c '[FAIL]'` over its output. That validator does not emit `[FAIL]` lines. It prints
`Error: found N broken links` and exits non-zero. The grep therefore returned a meaningless zero on
every run, and the non-zero exit code was never read — a green that measured nothing.

Reading it properly: 312 broken links across 116 files. All 116 are under `plans/done/`, none is a
file this branch touches, and each is byte-identical to `origin/main` (116 identical, 0 modified, 0
absent) — so they are a pre-existing archived-plan baseline, matching how the 58 `format:md:check`
failures were classified. The conclusion this iteration reached was right. The method that reached
it was not, and would have reported green just as confidently had the links been broken by this
branch.

The general rule, now applied: assert the exit code first, and confirm a validator actually emits
the token being counted before treating a count of zero as evidence.

### Declined, With Reasons — Cycle 1

| Finding                                                                                       | Why not acted on                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single-source the Rust/Cargo rationale and platform statement across the four entry documents | Real duplication, and the drift it predicted did occur (C-25). But Markdown here has no include mechanism, and building one is a different plan. The wording is harmonized instead; the structural fix is deferred. |
| Add Rust to the governance workflow's `scope: minimal` table                                  | Would be wrong. `doctor --scope minimal` inspects already-installed tools, and Cargo built the checker before it ran. The collision is terminological and is fixed in the reader-facing document (C-27).            |
| Sweep the hardcoded versions in the TypeScript style guide                                    | About eight occurrences in a 1,500-line explanation document outside this plan's onboarding reader path. Named here as a deferred follow-up rather than silently widening the delivery unit.                        |
| Recapture the Phase 5A and 5B journeys at the documented breakpoints                          | The environments were torn down at the end of their phases. C-23 closes the coverage gap directly and says plainly what the new capture does and does not evidence.                                                 |

### Cycle 2 Rows (P6-007B@01)

Cycle 2 re-reviewed the remediation commit, with each specialist briefed to verify its own cycle-1
finding rather than re-file it. It found that the C-21 fix — the rewrite of the Cargo prerequisite
wording — was itself wrong in two ways. Recording that plainly: the correction for a false claim
contained two more.

| Row  | Discipline | Defect                                                                                                                                                                                                                                                                                                                               | Severity | Fix                                                                                                                                                                                                                                                                                                                     |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-31 | Logic      | "The failure only becomes visible when you run `npm run doctor`" is too narrow. `npm install` also runs `prepare: husky`, and `.husky/pre-commit` runs under `set -e` calling `rhino-bin.sh`, which runs `cargo build` with no `\|\| true` — so a missing Cargo hard-blocks the first `git commit` and `git push`                    | HIGH     | Every site now names the Git-hook failure alongside `npm run doctor`. Verified by running the hook shim with Cargo off `PATH`: exit 127, not a warning                                                                                                                                                                  |
| C-32 | Logic      | "Silently skipped" is wrong twice over: the `cargo: command not found` line **is** printed in `npm install` output, and the check was attempted and failed rather than skipped — only the exit code was discarded. It also contradicted this program's own adjacent issue title, which correctly said `npm install` prints the error | MEDIUM   | Replaced everywhere with the precise mechanism: the check runs, prints the error, and fails, while `npm install` discards the exit code and still reports success                                                                                                                                                       |
| C-33 | Governance | The script that backfilled the 34 evidence blocks asserted `Files Changed` for `P6-001A` and `P6-002` that their own adjacent prose flatly denies — both items record "not applicable" and "no file was changed in this phase". A fabricated record inside the fix for missing records                                               | HIGH     | Both corrected to "None inside the repository", with a note that the work happened later in iteration `@01`. A sweep now checks every not-applicable item for a non-`None` `Files Changed`; it returns 0                                                                                                                |
| C-34 | Governance | The breakpoint remediation produced conforming new captures but left `P5A-G01` and `P5B-G01` asserting an unqualified all-three-viewport PASS resting on the non-conforming widths, with no cross-reference. A reader of `delivery.md` alone could not discover the gap                                                              | MEDIUM   | Both gates now carry an amendment stating which widths were used, that 390 px is wider than the required 375 px so the narrowest breakpoint went unexercised, that the PASS stands only for what it measured, and where the supplementary capture lives. **Superseded by C-37**, which found this reached too few items |
| C-35 | Integrity  | The C-30 "corrected" word count was itself stale: it cited 894, the figure at `cb489b874`, but C-24 had since added a word, making the committed figure 895 — the same unmeasured-claim class, inside the fix for it                                                                                                                 | MEDIUM   | The figure is now pinned to a named revision rather than left floating, and the durable claim is the invariant that matters: under the 900-word threshold at every commit in this iteration                                                                                                                             |

Cycle 2 also confirmed the C-20 remediation is complete for the reader-path file set — no version
literal remains in any of the four documents — and that the `volta install` commands work at the
point in the sequence where they now appear.

### Cycle 3 Rows (P6-007C@01)

Cycle 3 re-reviewed the cycle-2 remediation, briefed to hunt for a third generation of the same
failure — a false claim inside the fix for the second-order one. It did not find one: the integrity
specialist re-derived every figure in C-33 through C-35 against the committed tree, including
running the real `governance word-budget validate` binary at all three commits on this branch, and
each checked out. What it did find is a wrong quotation and two rendering or record defects.

| Row  | Discipline | Defect                                                                                                                                                                                                                                                                                                           | Severity | Fix                                                                                                                                                                                                                                                                                                                                                                                                |
| ---- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-36 | Logic      | The C-32 rewrite quoted the missing-Cargo error backwards as `command not found: cargo`, at both CONTRIBUTING.md sites and in C-32's own row. That is zsh's interactive phrasing; npm's default script shell is `/bin/sh` and the Husky shims are `sh`, which emit `cargo: command not found`                    | HIGH     | All three sites corrected. Reproduced first: `env -i PATH=<node and npm dirs> npm run doctor` prints `sh: cargo: command not found` and exits 127. The adjacent volta entry was left alone at this point, because volta is typed interactively where zsh does emit that order; C-43 below later removed its quoted string entirely, on the separate ground that two adjacent orders read as a typo |
| C-37 | Governance | `P5B-005` called 390x844/768x1024/1440x900 "all three mandated viewports" and `P5B-005A` called them "mandated breakpoints". The gate-level amendment landed in cycle 2 sat 175 and 148 lines later respectively, so a reader meeting these items first got an affirmatively false claim, not an unqualified one | MEDIUM   | Both phrases corrected, and the same amendment now appears on `P5A-006`, `P5A-006A`, `P5B-005`, and `P5B-005A`, not only on the two gates. The evidence filenames keep 390/1440 deliberately: renaming them to 375/1280 would misdescribe the images' own bytes. **Superseded in part by C-45**, which found the line distances in this row wrong                                                  |
| C-38 | Docs       | A blank line after the C-32 row terminated the cycle-2 table, leaving C-33 through C-35 as a header-less pipe block that GFM parses as a paragraph. It would have rendered on GitHub as literal pipe characters — inside the rows documenting this program's own corrections                                     | MEDIUM   | Blank line removed. Worth noting that no gate catches this: markdownlint reports 0 errors and Prettier reports the file already conforms, because without a delimiter row neither tool sees a table at all                                                                                                                                                                                         |
| C-39 | Docs       | The `doctor --scope minimal` disambiguation added in cycle 1 introduced a flag this document never demonstrates, in the Overview, before the reader has run `doctor` even once                                                                                                                                   | LOW      | Trimmed to a single clause. The disambiguation is kept, because the cycle-1 concern was real; the tangential aside about why Rust is absent from that flag's set is dropped                                                                                                                                                                                                                        |
| C-40 | Docs       | The Desktop 1280px row in `evidence/phase-6-breakpoint-coverage.txt` broke the table's column alignment                                                                                                                                                                                                          | LOW      | The whole column widened to fit the longest label. Not gated — the file is `.txt`, so no Markdown formatter reads it                                                                                                                                                                                                                                                                               |

Cycle 3 also confirmed, by direct reproduction rather than reading, that the Git-hook exit code is
genuinely preserved end to end: Husky's dispatcher runs the hook as a child process, captures its
exit status, and re-exits with it; each shim runs under `set -e` with no `|| true`; and
`rhino-bin.sh` runs under `set -euo pipefail` and `exec`s the binary. It
found one nuance that does not change any shipped claim: `rhino-bin.sh` skips the Cargo build when
a fresh gate binary already exists, so a contributor who has built before would not see the block —
but every document making the claim is describing a first-time clone, where no such binary can
exist.

### Cycle 4 Rows (P6-007D@01)

The governance specialist returned zero findings — the first clean verdict of this PR — and endorsed
the declined rename by quoting the convention clauses that do and do not require it. The other two
specialists found four defects, including the fourth-generation false claim cycle 3's own narrative
had introduced.

| Row  | Discipline | Defect                                                                                                                                                                                                                                                                                        | Severity | Fix                                                                                                                                                                                                                                                                                                                     |
| ---- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-41 | Integrity  | The Cycle 3 narrative claimed "Husky's dispatcher execs the hook" inside a sentence boasting direct reproduction. `.husky/_/h` runs `sh -e "$s"` as a child, captures `$?`, and calls `exit $c` — fork and wait, the opposite of `exec`. Only `rhino-bin.sh` genuinely `exec`s                | MEDIUM   | Reworded to the mechanism that is actually there. The conclusion the sentence supports is unaffected: fork-wait-`exit $c` propagates the status exactly as `exec` would, so the reader-facing claim about `git commit` still holds                                                                                      |
| C-42 | Docs       | The breakpoint amendment reached six leaf items but never the `P5-G01` rollup, which still summarized both journeys as an unqualified PASS with zero documentation defects. A reader who stops at the rollup — the natural stopping point — would never learn of the gap                      | MEDIUM   | The rollup now carries its own amendment, stating both that the PASS verdicts stand and that the coverage gap is real, and distinguishing a gap in this plan's execution from a defect in the product documentation. **Superseded by C-46**, which found that distinction argued from a label rather than a measurement |
| C-43 | Docs       | Correcting the cargo error string left two adjacent troubleshooting entries quoting shell errors in opposite word orders. Both are accurate — volta is typed interactively under zsh, cargo comes from `/bin/sh` inside an npm script — but that justification lived only in a commit message | LOW      | The volta entry no longer quotes a shell-specific string at all, so the false parallel disappears rather than being explained away                                                                                                                                                                                      |
| C-44 | Docs       | The trimmed `doctor --scope minimal` aside still named a flag the document never demonstrates, in the Overview, before the reader has run the checker once. Two independent docs passes flagged the same placement                                                                            | LOW      | Moved to the Related Documentation entry for the workflow that actually defines `scope: minimal`, which is the only place a reader meets the colliding term. The disambiguation survives; the digression does not                                                                                                       |

One imprecision survives in a place that cannot be corrected: the pushed commit message for
`ab0dc7b4c` says the false "mandated" claim sat "150 lines before the caveat". The real distances
at the parent commit are 175 lines for `P5B-005` and 148 for `P5B-005A`, so the figure describes
neither. Amending a pushed message is not worth a force-push. The `C-37` row above carried the
same wrong figure and _was_ correctable, so it now states both distances — a first pass at this
disclosure named only the commit message, which implied the error was confined to somewhere
unreachable when half of it was sitting in editable document text.

### Cycle 5 Rows (P6-007E@01)

Two findings, one from each specialist, and both are about the same thing: a claim that sounded
better than the fact underneath it. The reader-facing documents themselves came back clean — after
five rounds of patching, the docs specialist read all four end to end and found no accumulated
incoherence, no contradiction between them, and no ordering defect.

| Row  | Discipline | Defect                                                                                                                                                                                                                                                                                                                                | Severity | Fix                                                                                                                                                                                                          |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| C-45 | Integrity  | The Cycle 4 disclosure said the wrong "150 lines" figure lived in a pushed commit message and was not worth a force-push. True but incomplete: the identical figure also sat in `C-37`'s own row, ordinary editable text in a file that same commit was rewriting. Disclosing only the unreachable half made the error look unfixable | MEDIUM   | `C-37` now states both real distances, 175 and 148, and the disclosure says plainly that a first pass named only the commit message. The two figures were re-derived at `9529a117d`: 1840−1665 and 1840−1692 |
| C-46 | Docs       | The new `P5-G01` rollup amendment said the coverage gap "is a coverage gap in this plan's own execution, not a defect in the product documentation, which is why it does not change either verdict". A category label cannot license an unchanged verdict — only a measurement can, and the amendment never gave one                  | MEDIUM   | Rewritten to lead with the measurement: the supplementary capture found no horizontal overflow and a correct `<h1>` at 375, 768, and 1280 px, and that result is what leaves the verdicts standing           |

### Cycle 6 Rows (P6-007F@01)

Both cycle-5 remediations came back verified. The rollup's measured result was checked against
`evidence/phase-6-breakpoint-coverage.txt` word for word and matches exactly; `C-45`'s arithmetic
was re-derived; and `C-37`'s "175 and 148 respectively" was checked for a transposed binding, which
would itself have been a new false claim. It binds correctly. The reader-facing documents were
untouched by that commit and re-confirmed unchanged.

| Row  | Discipline | Defect                                                                                                                                                                                                                                                                                            | Severity | Fix                                                                                                                                                                         |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-47 | Integrity  | `C-42` still asserted, in the present tense, that the rollup amendment works by "distinguishing a gap in this plan's execution from a defect in the product documentation" — the exact framing `C-46`, in the same commit, had retired. A reader stopping at `C-42` got the retired justification | MEDIUM   | `C-42` now names `C-46` as its successor. The same sweep found `C-30`, `C-34`, and `C-37` in the same state, so all four gained markers, not only the row the finding named |
| C-48 | Docs       | `A Gate I Reported Green That Was Not Measured` carried no cycle marker while every sibling heading did, and sat after the Cycle 5 rows despite being the section's oldest narrative. A reader working through by cycle would date it five cycles wrong                                           | LOW      | It and `Declined, With Reasons — Cycle 1` moved to their chronological place before the Cycle 2 rows, and the heading is now labelled `(Cycle 1)`                           |

The docs specialist also observed that six cycles of rows had left the section usable as a log but
not as a current-state reference, since several rows were superseded rather than rewritten. That is
the right trade — rewriting them would erase the record this file exists to keep — so the fix is a
`How to read this section` preamble naming all four supersession chains, plus the in-row markers
`C-47` added. Claim and markers were made to agree in both directions: the preamble says every
superseded row names its successor, so every one of them now does.

One process note, raised twice by specialists and worth recording. Review cycles ran against pushed
commits while this worktree already carried the next cycle's uncommitted fixes. Every specialist
handled it correctly by reading `git show <sha>:<path>`, and one of them found the `C-42` staleness
that the uncommitted draft happened to already fix. But a reviewer using a plain file read would
have judged unreviewed content. Reviews should run against a clean tree, or the brief should say
plainly that it is not one — as these briefs did from cycle 3 onward.

### Cycle 7 Rows (P6-007G@01)

The first cycle to run against a genuinely clean worktree, closing the process gap cycle 6 recorded.
Governance returned zero findings on a fresh pass over the whole branch diff, confirming from the
convention documents themselves — rather than from first principles — that `artifacts/` is properly
declared in this plan's `tech-docs.md` File-Impact Analysis, that `plans/` sits outside both the
word-budget and README-index gate scopes, and that nothing under `apps/rhino-cli/` or the rhino
specs is touched. Integrity found two defects, both inside the preamble written last cycle to fix
this very class.

| Row  | Discipline | Defect                                                                                                                                                                                                                                                                                      | Severity | Fix                                                                                                                                                                      |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| C-49 | Integrity  | The Cycle 6 narrative said the preamble names "all five supersession chains". It names four. Five is the count of in-row markers — the `C-34 → C-37 → C-45` chain carries two of them but is one chain. A completeness claim, miscounted, inside the fix for miscounted completeness claims | MEDIUM   | Corrected to four. The same wrong figure is in the pushed `0db7beda2` message and stays there, disclosed here rather than force-pushed, on the same reasoning as C-45    |
| C-50 | Integrity  | The preamble bounded itself at "C-20 through C-46" while the same commit appended C-47 and C-48 inside the section it was describing. False the instant it was written, with no time-lag excuse                                                                                             | MEDIUM   | The upper bound is gone rather than corrected. Naming one is what made it false, and a bound updated by hand would go stale again at the next row — as it just did twice |

Both findings are the same shape as C-45: a claim about the record's own completeness, stated more
confidently than it had been checked. Worth noting where they were found — not in the reader-facing
documents, which have now been clean for three consecutive cycles, but in the apparatus built to
audit them.

## Scope Discipline

No correction here is a product change. The rows edit prose in five reader-facing documents and the
plan's own records; none touches source, configuration, a test, or a generated mirror. P6-002A and
P6-002B therefore remain not applicable in this iteration too — no defect was a product bug, so no
red coverage was needed and none was written.

C-23 is the one row that produced new evidence rather than new prose. It ran the landing page at
the three documented breakpoints and checked `scrollWidth > clientWidth` at each. That is a
verification, not a product change: nothing in the application was modified, and the check passed
as it stood.

## File-Touch Ledger

| Path                                                | Change                                                           | Owning Row       |
| --------------------------------------------------- | ---------------------------------------------------------------- | ---------------- |
| `CONTRIBUTING.md`                                   | Platform statement, prerequisites, intake caveat, Diátaxis gloss | C-01…C-05        |
| `docs/how-to/setup-development-environment.md`      | Quick Start Rust step and renumbering                            | C-06, C-07       |
| `README.md`                                         | WSL2 expansion; Rust bullet accuracy; changed-port guidance      | C-08, C-21, C-24 |
| `docs/tutorials/getting-started-with-ose-public.md` | Lead paragraph, spelling, platform wording, Cargo reason         | C-21, C-25       |
| `docs/reference/related-repositories.md`            | Retired-sandbox row corrected to infrastructure work             | voice rows       |
| `plans/in-progress/…/evidence/phase-6-*`            | Documented-breakpoint capture and its transcript                 | C-23             |
| `plans/in-progress/…/delivery.md`                   | Phase 5–7 ticks and notes                                        | plan records     |
| `plans/in-progress/…/artifacts/*.md`                | Ledger re-run, public record, this record                        | plan records     |
| `plans/in-progress/…/evidence/*`                    | Phase 5A and 5B journey evidence                                 | plan records     |
