# Idea Grooming — Traps and Termination Audit

## Traps this Skill exists to prevent

- **A same-filename pair across repos is not automatically a duplicate.** Diff it. A copy
  re-derived against its own repo's measured state is an independent **R2** idea; merging it
  destroys real findings. When two such ideas keep one shared filename, Step 9's rename criterion
  applies to **every** member of that class, not just the first one noticed.
- **The urgency rubric misfires on negations.** A _Why now_ opening with "Not now" / "Not yet" /
  "Not urgent" is an authoritative author signal and must win over keyword matching.
- **Index hooks must be harvested per repo.** Keying a one-line hook by slug across repos makes one
  repo's index describe another repo's variant of the idea.
- **Commit the deletions.** Because relocation sources are deleted only after the destination push
  is verified, the destination repo needs a **second** commit for its own post-verification deletes.
- A **pre-push link gate may be scoped** to changed files, so a clean gate does not prove the repo
  has no broken links. Establish the baseline against a clean `HEAD` worktree before attributing any
  breakage to the sweep.

## Termination audit (do not skip)

The workflow's frontmatter states a `termination` condition. Verify it mechanically, clause by
clause, rather than inferring completion from green gates — a run can pass every repo gate and still
violate it:

1. No slug resides in two or more repos.
2. Every surviving idea sits in a `q1`–`q4` folder in its resident repo; nothing left flat but `README.md`.
3. Every filename is kebab-case and its terms are echoed by its own content.
4. Every relocated and renamed file carries its provenance line. Scan the **whole leading
   blockquote** — a long demotion note pushes the appended line past any fixed line window.
5. No broken link points into `plans/ideas/` in any repo.
6. Each touched repo's `plans/ideas/README.md` carries one `## Grooming Log` and a `Last groomed` line.

Report the audit result; if any clause fails, fix it and re-run the audit before declaring the run
complete.
