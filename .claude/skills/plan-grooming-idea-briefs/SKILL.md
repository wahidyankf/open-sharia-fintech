---
name: plan-grooming-idea-briefs
description: Invocable entry point for the plan-ideas-grooming workflow — sweeps one or more repos' plans/ideas/ folders and converges them into a deduplicated, Eisenhower-quadrant-organized, correctly-resident set of two-pagers. Carries the ten-step procedure, the three residency rules (secrets-bearing, single-repo-only, generalizable), the two classification rubrics (urgency, importance), the fail-safe-toward-duplication relocation sequence, and the six-clause termination audit. Use when a repo's flat idea count exceeds 60, when 90 days have elapsed since the last recorded run, or when a maintainer asks for idea grooming across repos.
---

# Grooming Idea Briefs

## Purpose

This Skill is the **invocable entry point** for the
[`plan-ideas-grooming` workflow](../../../repo-governance/workflows/plan/plan-ideas-grooming.md).
That workflow declares `Execution Mode: Direct Orchestration` and states that "the procedure lives
entirely in this workflow document" — meaning the calling context performs the steps itself and
there is no delegated agent behind it. This Skill exists so that running the workflow is a **named,
callable action** rather than an undifferentiated sequence of file edits: invoking it loads the
procedure below, and the run is attributable.

**Read the workflow document for the full normative text.** This Skill carries the operational
essentials and the traps; it does not restate all ten steps verbatim.

## When to use this Skill

- A repo's `plans/ideas/` (summed across quadrant folders, excluding `README.md`) exceeds **60**
  flat idea files.
- **90 days** have elapsed since the `> Last groomed: YYYY-MM-DD` line in that repo's
  `plans/ideas/README.md`.
- A maintainer explicitly asks for idea grooming across one or more repos.

Do **not** use it to file a new idea (write the two-pager directly) or to promote a ripe idea into a
backlog plan (that is `plan-idea-promotion-planning`).

## Inputs

| Input           | Required | Default               | Notes                                                                                                                   |
| --------------- | -------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `repos`         | yes      | none                  | Comma-separated repo paths. **Supply every repo in one run** — Steps 3 and 4 are inherently cross-repo.                 |
| `dry-run`       | no       | `false`               | Compute and log every decision without writing.                                                                         |
| `delivery-mode` | no       | `main-to-origin-main` | Direct push under the plans-only carve-out; override to `worktree-to-pr` for a large sweep a maintainer wants reviewed. |

## Hard scope boundary

Write scope is strictly `plans/ideas/**`, plus Step 9's explicitly sanctioned rewriting of inbound
links that live elsewhere. **Never** create, move, or write under `plans/backlog/` or
`plans/in-progress/`, and never promote an idea to a plan — even one that looks obviously ready. If
a step's output would require writing outside that scope, log it as a follow-up in the grooming log
instead.

## Procedure

Run the workflow's ten steps in order. The ordering constraints that actually matter:

1. **Inventory** every repo before deciding anything.
2. **Within-repo dedup** first, then **cross-repo dedup** — and resolve **residency before merging**,
   so a merge lands in the correct repo rather than wherever the pair was compared.
3. **Residency**, three rules, first match wins:
   - **R1** the idea needs a real secret, credential, or live infra-state value to be actionable →
     the infra-private repo, and no other.
   - **R2** it names a file, app, or concern that **provably** exists in exactly one repo → that repo
     only. Verify with `Glob` / `test -f` against each tree; **never** infer this from the brief's prose.
   - **R3** otherwise → the generalizable cross-cutting-governance default repo.
     Log the matched rule for **every** surviving idea, including "already correctly resident".
4. **Relocation** is fail-safe-toward-duplication: write the final file at the destination, commit
   and push, **verify it on the destination's `origin/main`**, and only then delete the source. If
   verification fails, stop before the delete and log the duplication in both repos' logs.
5. **Reshape** every survivor to the eight-section two-pager template, preserving content.
6. **Provenance**: append `Relocated from …` / `Renamed from …` to the file's **existing** blockquote,
   never overwriting it. Record every action in the repo's own `## Grooming Log`.
7. **Classify** with both rubrics — urgency from _Why now_ only; importance from the full content.
8. **Link rewrite** covers move, rename, and move-plus-rename as one mechanism: fix the moved file's
   own links, then grep the repo for inbound links to the old path. Cross-repo references become
   absolute `https://github.com/<org>/<repo>/blob/main/…` URLs.
9. Append `> Last groomed: YYYY-MM-DD` so the recurrence trigger stays armed.

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

## Related

- [`plan-ideas-grooming` workflow](../../../repo-governance/workflows/plan/plan-ideas-grooming.md) — the normative procedure.
- [Ideas Folder (Two-Pagers) convention](../../../repo-governance/conventions/structure/plans.md#ideas-folder-two-pagers) — the template every survivor is reshaped against.
- [`plan-idea-promotion-planning`](../../../repo-governance/workflows/plan/plan-idea-promotion-planning.md) — promotes a groomed idea to a plan; this Skill never does.
