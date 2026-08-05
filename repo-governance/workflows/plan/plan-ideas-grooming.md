---
name: plan-ideas-grooming
title: "plan-ideas-grooming"
goal: >
  Sweep one or more OSE repos' plans/ideas/ folders and converge each into a deduplicated,
  Eisenhower-quadrant-organized, strictly-formatted set of two-pagers with truthful filenames, with
  cross-repo residency corrected per the generalizable / secrets-bearing / single-repo-only
  placement rules
termination: >
  Every processed repo's plans/ideas/ contains no unresolved duplicate, every remaining idea sits
  in its correct q1-q4 quadrant folder in its correct repo with a filename matching its content,
  every relocated/renamed idea's provenance and inbound/outbound links are intact, and the run is
  recorded in every touched repo's grooming log
inputs:
  - name: repos
    type: string
    description: >
      Comma-separated paths to the target repos to sweep in this run. No default — supplied
      explicitly at invocation, since this document itself names no repo-specific path. A path may
      be absolute or relative to wherever the invoker is working; the workflow imposes no fixed
      layout.
    required: true
  - name: dry-run
    type: boolean
    description: >
      When true, compute and log every classification / merge / rename / relocation decision
      without writing, moving, renaming, or deleting any file
    required: false
    default: false
  - name: delivery-mode
    type: enum
    values: [main-to-origin-main, worktree-to-pr]
    description: >
      This workflow's own git delivery behavior for the changes it makes to plans/ideas/**. Default
      main-to-origin-main (direct commit + push to each processed repo's own main, per the
      plan-docs-only carve-out — see plan-planning's Delivery Mode carve-out). A caller may override
      to worktree-to-pr for a specific invocation (e.g., a particularly large sweep the maintainer
      wants reviewed before it lands).
    required: false
    default: main-to-origin-main
outputs:
  - name: grooming-log-entries
    type: file-list
    description: >
      Per-repo grooming log entries (appended to that repo's own plans/ideas/README.md, in that
      repo's own tree) recording every merge, split, rename, quadrant reclassification, and
      cross-repo relocation performed this run
  - name: final-status
    type: enum
    values: [pass, partial, fail]
---

# plan-ideas-grooming Workflow

**Purpose**: Sweep one or more repos' `plans/ideas/` folders and converge them into a
deduplicated, Eisenhower-quadrant-organized, strictly-formatted, correctly-resident set of
two-pagers — the direct analogy to Scrum's "backlog grooming" practice applied to this repo's idea
corpus. Concretely, this workflow merges or splits near-duplicate ideas (within a repo and across
the `repos` input's repo set), classifies every surviving idea into an Eisenhower quadrant folder
using two falsifiable rubrics, reshapes each into strict two-pager compliance, corrects cross-repo
residency per three placement rules, and renames a filename that no longer matches its content —
with every rename's inbound/outbound links rewritten by the same mechanism relocation already uses.

## When to use

- A repo's `plans/ideas/` (summed across its quadrant folders, excluding `README.md`) exceeds
  **60** flat idea-doc files.
- **90 days** have elapsed since this workflow's last recorded run against that repo, tracked via
  the `> Last groomed: YYYY-MM-DD` line this workflow appends to that repo's
  `plans/ideas/README.md` on every run.
- Whichever of the two conditions above occurs first is this workflow's own stated **recurrence
  trigger** — it is a real, recurring commitment against `plans/ideas/`, not a one-time migration
  wearing a recurring name. A maintainer or an agent acting on their behalf invokes it explicitly
  against the `repos` it should sweep; it never self-triggers.
- Do **not** use it to file a brand-new idea (write the two-pager directly per the
  [Ideas Folder convention](../../conventions/structure/plans.md#ideas-folder-two-pagers)), and do
  not use it to promote a single ripe idea into a full plan (that is
  [`plan-idea-promotion-planning`](./plan-idea-promotion-planning.md)).

## Scope Boundary (Hard)

This workflow's write scope is strictly `plans/ideas/**` in each processed repo — the idea files
themselves, their quadrant subfolders, and the `## Grooming Log` / `> Last groomed:` lines it
appends to that folder's own `README.md`. It **never** creates, moves, renames into, or otherwise
writes any file under `plans/backlog/` or `plans/in-progress/` in any repo, in any of its ten
steps, under any `delivery-mode`. Promoting a groomed, ripe idea into a full backlog plan is a
categorically separate action, performed only by
[`plan-idea-promotion-planning`](./plan-idea-promotion-planning.md), invoked explicitly and
separately by a maintainer or another workflow — `plan-ideas-grooming` never invokes it and never
performs a promotion itself, even when a surviving idea looks obviously ready. If a step's output
would require writing outside `plans/ideas/**`, that output is out of scope for this workflow:
stop and log it as a follow-up recommendation in the grooming log instead of writing it.

## Execution Mode

**Direct Orchestration** — the calling context (the top-level assistant session that received the
"Groom plans/ideas/ in …" request, or the recurrence trigger noticing the threshold) is the
orchestrator. It resolves the `repos` input to a concrete set of git checkouts, reads every
target repo's `plans/ideas/` tree directly via `Read`/`Glob`/`Bash`, performs the merge/split,
residency, reshape, provenance, classification, and link-rewrite steps below itself (this is
mechanical file reorganization work, not a task that benefits from delegating to a specialized
content-authoring agent), and commits/pushes per the resolved `delivery-mode`. There is no
dedicated `plan-ideas-grooming` delegated agent — the procedure lives entirely in this workflow
document, matching the pattern [`plan-execution`](./plan-execution.md) uses for its own
orchestrator-run steps.

Every git delivery under this workflow's `main-to-origin-main` default follows the
`plans/**`-only **plan-docs-only carve-out**
([`plan-planning`](./plan-planning.md#the-plan-docs-only-carve-out)): since every path this
workflow touches sits under `plans/ideas/**`, a direct push to each processed repo's own `main`
needs no PR review cycle. A caller may still override `delivery-mode` to `worktree-to-pr` for a
specific invocation.

## Steps

### 1. Inventory

For each repo named in the `repos` input, list every `plans/ideas/*.md` file — excluding
`README.md` and excluding any file already sitting inside a `q1-…`–`q4-…` quadrant subfolder from
a prior run — and read each file's title, one-line summary, provenance blockquote, and all seven
body sections defined by the
[Two-Pager Template](../../conventions/structure/plans.md#two-pager-template). This inventory is
the working set every later step operates against; nothing outside `plans/ideas/**` in any of the
`repos` is read or touched.

### 2. Dedup pass (merge/split)

Within each repo first: flag any pair of idea files whose one-line summaries share three or more
significant terms, or whose filenames share a common stem, as a **merge candidate**. Log every
candidate and its rationale to that repo's grooming log (see Step 7 for the log's location), then
merge autonomously — fold the less-complete file's unique content into the more-complete file, and
delete the now-redundant file. Separately, flag any idea whose Problem/context section names two or
more genuinely unrelated concerns as a **split candidate**; split it into two files, each retaining
the shared prior-art links from the original. A merge or a split both leave the survivor(s) subject
to the rename check in Step 9, since folding or dividing content routinely leaves a filename that no
longer describes what remains.

### 3. Cross-repo dedup

Beyond the within-repo pass, compare idea titles and content across every repo in the `repos` set
for the same run. When a title or its content matches an idea already inventoried in a different
target repo, resolve that pair's residency (Step 4) **before** merging — the merge must land in
whichever repo Step 4 determines is correct, never wherever the pair happened to be compared first.
Skipping this ordering risks merging two copies into the wrong repo and then having to relocate the
merged survivor anyway.

### 4. Residency decision

Apply the following three rules, in this fixed order, first match wins, to every surviving idea
(post-merge/split):

1. **Secrets check** — the idea inherently requires a real secret, credential, API key, or other
   infra-state value to be actionable → resident in the repo designated for infra-private content
   only, and in no other repo.
2. **Single-repo-only check** — the idea names a file, app, or concern that provably exists in
   exactly one of the `repos` in this run (verified via `Glob` / `Bash test -f` against that repo's
   own tree, never assumed from the idea's prose alone) → resident in that one repo only.
3. **Default (generalizable)** — neither of the above matches → resident in the repo designated as
   the generalizable, cross-cutting-governance default for this run's `repos` set.

Log the matched rule number for every decision, in every case — including "already correctly
resident, no relocation needed" — so the grooming log records a residency verdict for every
surviving idea, not only the ones that moved.

### 5. Relocation

When Step 4's determined target repo differs from an idea's current repo, relocate it using a
**fail-safe-toward-duplication, never-toward-loss** sequence:

1. Write the file at the destination repo's resolved quadrant folder (with the Step 6 reshape, any
   Step 9 rename, and the Step 7 provenance line already applied — the file that lands is the final
   file, not a draft to be touched again).
2. Commit and push that write directly to the destination repo's `main`, per the resolved
   `delivery-mode` (`main-to-origin-main` by default — see the frontmatter's `delivery-mode` input).
3. **Verify the commit landed** on the destination repo's `origin/main` before doing anything else.
4. **Only after verification succeeds**, delete the original file from the source repo, as its own
   separate commit and push.

If verification in step 3 fails or the run is interrupted before step 4 completes, **stop before
the delete** — the idea now legitimately exists in both repos. Log the duplication explicitly as an
unresolved follow-up in both repos' grooming logs; a future invocation resolves it. The idea is
never silently dropped from either repo as a side effect of an interrupted run.

### 6. Two-pager reshape

Bring every surviving, merged, or relocated file into exact conformance with the
[Two-Pager Template](../../conventions/structure/plans.md#two-pager-template)'s eight sections:
title + one-line summary, Problem/context, Why now, Prior art, Proposed direction, Rough scope &
non-goals, Risks & open questions, and What success looks like. A file with an extra or missing
section, or a missing provenance blockquote in its first ten lines, is reshaped to match — content
is preserved and reorganized into the template's structure, never discarded.

### 7. Provenance

For a file the Step 5 relocation moved, append a line to its existing provenance blockquote —
preserving every line already there, never overwriting it —
`> Relocated from <source-repo>/plans/ideas/<file> on YYYY-MM-DD by plan-ideas-grooming.` For a
file Step 9 renames without relocating it, append the analogous line instead:
`> Renamed from <old-file> on YYYY-MM-DD by plan-ideas-grooming.` Both lines make the file's history
recoverable even though git history does not follow a file across independent repositories, and even
though a same-repo rename's git history, while technically followable via `git log --follow`, still
benefits from an explicit human-readable note at the point of read.

Record every relocation and rename this run performs — including the ones deferred by an
interrupted relocation (Step 5) or a filename collision (Step 9) — as an append-only entry under a
`## Grooming Log` section in that repo's own `plans/ideas/README.md`. Because every repo this
workflow touches, whether as a relocation source or destination, gets its own log entry in its own
tree, the audit trail travels with the repo rather than living in one external file unreachable from
a sibling repo.

### 8. Classification

Apply both of the following rubrics — stated exactly as they must be checked, so classification is
repeatable and auditable rather than a per-run judgment call — to every surviving idea, and file it
into `plans/ideas/q1-urgent-important/`, `plans/ideas/q2-not-urgent-important/`,
`plans/ideas/q3-urgent-not-important/`, or `plans/ideas/q4-not-urgent-not-important/` within its
Step 4 resolved-residency repo:

- **Urgency rubric**: read the idea's Why now section. The idea is classified **urgent** only if it
  names or blocks an active in-progress or backlog plan, or documents an already-observed live
  defect. An idea with no such reference is classified **not-urgent**.
- **Importance rubric**: read the idea's full content. The idea is classified **important** only if
  it affects two or more repos, a security or secrets concern, a data-integrity or data-loss risk, a
  currently-blocking CI gate, or a rule an existing checker enforces. An idea matching none of those
  signals is classified **not-important**.

### 9. Link rewrite (covers move, rename, and move-plus-rename)

This step covers every filename-changing outcome the earlier steps produce — an intra-repo move
into a quadrant folder, a rename, or both together — as one mechanism, never as separate move and
rename procedures:

- **Intra-repo** (a file moving into a quadrant folder and/or being renamed within the same repo):
  rewrite the file's own relative links first, then grep the whole repo for any inbound relative
  link pointing at the file's old path or filename and update each to the new path/filename.
- **Cross-repo** (Step 5's relocation): convert every `./`-relative link inside the moved file to an
  absolute `https://github.com/<org>/<repo>/blob/main/...` URL (the same pattern already used in
  [`deploy-targets-registry.md`](../../../plans/ideas/deploy-targets-registry.md)), and check the
  source repo for (though do not expect to find) any inbound link into the file being relocated.

**Rename criteria**: apply a rename whenever Step 2 (merge/split), Step 4 (residency-driven
relocation revealing the name was scoped to the wrong context), or Step 6 (reshape) leaves a
filename that no longer matches its content, or whenever the current filename never followed
kebab-case (`[a-z0-9-]+\.md`, per the
[File Naming Convention](../../conventions/structure/file-naming.md)). Compute the new filename
from the file's current title. If the computed filename already exists in the destination
directory — a **collision** — defer the rename, log it as an unresolved follow-up in that repo's
grooming log, and leave the file under its current name until a future run resolves the collision;
never overwrite the existing file at the computed name.

### 10. Recurrence trigger

State this workflow's own re-run condition here, in its own "When to use" section above, so the
condition is discoverable without reading design documentation external to this file: run this
workflow against a given repo when either that repo's flat `plans/ideas/` file count (summed
across its quadrant folders, excluding `README.md`) exceeds **60**, or **90 days** have elapsed
since this workflow's last recorded run against that repo — whichever occurs first. Track the
last-run date via a `> Last groomed: YYYY-MM-DD` line this workflow appends to (or updates on) that
repo's own `plans/ideas/README.md` at the end of every run.

## Related Workflows

- [`plan-idea-promotion-planning`](./plan-idea-promotion-planning.md) — promotes a single ripe
  two-pager (post-grooming, already deduplicated and classified) into a full backlog plan. This
  workflow converges the idea corpus that promotion later reads from; it never itself promotes an
  idea to a plan.
- [`plan-planning`](./plan-planning.md) — the generic plan-authoring lifecycle that
  `plan-idea-promotion-planning` hands off to. Not invoked by this workflow.
- [`plan-execution`](./plan-execution.md) — this workflow's `## Execution Mode` (Direct
  Orchestration, no dedicated delegated agent) follows the same orchestration pattern
  `plan-execution` establishes for its own procedural steps.

## Related Documentation

- [Ideas Folder (Two-Pagers) convention](../../conventions/structure/plans.md#ideas-folder-two-pagers) —
  the two-pager template, file layout, and promotion procedure this workflow reshapes every surviving
  idea against.
- [Workflow Naming Convention](../../conventions/structure/workflow-naming.md) — defines the
  `grooming` type token this workflow's own filename uses (scope `plan`, type `grooming`).
- [Plan-docs-only carve-out](./plan-planning.md#the-plan-docs-only-carve-out) — the basis for this
  workflow's `main-to-origin-main` default delivery mode, since every path it touches sits under
  `plans/**`.
- [File Naming Convention](../../conventions/structure/file-naming.md) — the kebab-case rule Step 9's
  rename criteria checks every filename against.
- [Knowledge Capture Convention](../../development/quality/knowledge-capture.md) — names
  `plans/ideas/` as a candidate durable home for a future-work learning; this workflow is what keeps
  that home converging rather than strictly growing.
