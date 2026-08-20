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
Both were swept before commit, and the review's other observations were resolved as follows.

| Review finding                                                                                                                     | Severity | Resolution                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-03 half-applied: two more hardcoded versions survived, so the new "can never drift apart" sentence contradicted its own document | MEDIUM   | Both swept — the post-install prose now names no version, and the troubleshooting command reads the pin from `package.json`.                                         |
| C-06 half-applied: three statements still classified Rust as a Full-setup tool                                                     | MEDIUM   | All three corrected; Rust is now classified Minimal, with the reason (bootstrap runs the Rust tool checker) stated.                                                  |
| C-05 partial: `Diátaxis` still appeared cold in the project-structure tree                                                         | LOW      | The tree entry now points at the four categories listed directly beneath it.                                                                                         |
| Orphaned `**macOS/Linux**:` label left by removing its Windows peer                                                                | LOW      | Block restructured: the platform statement leads, the install command follows unlabelled.                                                                            |
| C-04's justification overstated — the closed-intake caveat was already the opening paragraph                                       | LOW      | The row was **corrected rather than defended**: reworded and downgraded MEDIUM → LOW, since the edit adds an in-section signal and an anchor, not a first surfacing. |
| README headroom: C-08 consumed 5 of an 8-word budget margin                                                                        | LOW      | Accepted and recorded. 897 of 900, gate green; any later addition must name an offsetting cut.                                                                       |

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

## Scope Discipline

No correction here is a product change. All eight rows edit prose in three reader-facing documents;
none touches source, configuration, a test, or a generated mirror. P6-002A and P6-002B therefore
remain not applicable in this iteration too — no defect was a product bug, so no red coverage was
needed and none was written.

## File-Touch Ledger

| Path                                           | Change                                                           | Owning Row   |
| ---------------------------------------------- | ---------------------------------------------------------------- | ------------ |
| `CONTRIBUTING.md`                              | Platform statement, prerequisites, intake caveat, Diátaxis gloss | C-01…C-05    |
| `docs/how-to/setup-development-environment.md` | Quick Start Rust step and renumbering                            | C-06, C-07   |
| `README.md`                                    | WSL2 expansion                                                   | C-08         |
| `plans/in-progress/…/delivery.md`              | Phase 5–7 ticks and notes                                        | plan records |
| `plans/in-progress/…/artifacts/*.md`           | Ledger re-run, public record, this record                        | plan records |
| `plans/in-progress/…/evidence/*`               | Phase 5A and 5B journey evidence                                 | plan records |
