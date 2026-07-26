# Learnings: ayokoding-learning-path-04-course-authoring

Transient running log. The executor appends one entry per generalizable learning **during**
execution; the Knowledge Capture phase (Phase 15 of [`delivery.md`](./delivery.md)) triages every
entry to a durable home or an explicit discard before archival.

**Sanitize before writing.** Apply the secret/sensitivity gate at write time, not at triage time — a
secret written here is already in git history by the time triage runs. Replace any credential, token,
private hostname, or inventory detail with a `<placeholder>` token.

**Code learnings never land inline.** A learning whose home is `apps/`, `libs/`, or tests is ALWAYS
filed as a separate `plans/backlog/<slug>/` plan, never fixed inside this plan's own commits or PR.
This plan authors content only; a defect found in the `course-paths` feature code belongs to
[`ayokoding-learning-path-03-navigation-ui`](../../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/README.md)
or to a new backlog plan — not here.

**Never empty.** If no generalizable learning surfaced, record the explicit escape below:
`No generalizable learnings — <one-line reason>`.

## Entry template

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning — would a durable surface catch this
  automatically next time?
```

## Entries

<!-- Append entries below this line during execution. -->

## Learning: bare plan-identifier worktree branch collides with `<plan-id>/<slug>` phase branches

- **Context**: provisioning this plan's worktree per `plan-execution.md` Step 0 created branch
  `ayokoding-learning-path-04-course-authoring` (the bare plan-identifier, per the documented
  `git worktree add -b <plan-identifier> ...` snippet). Phase 0 committed on that branch (never
  pushed). Starting Phase 1's first course sub-phase per `delivery.md`'s own instruction
  (`git checkout -b ayokoding-learning-path-04-course-authoring/<phase-slug>`) failed:
  `cannot lock ref 'refs/heads/.../evaluating-ai-output-essentials': '.../ayokoding-learning-path-04-course-authoring' exists`.
- **Observation**: git's `refs/heads/` namespace is a filesystem-like tree — a ref cannot be both a
  leaf (`ayokoding-learning-path-04-course-authoring`) and a directory prefix
  (`ayokoding-learning-path-04-course-authoring/<anything>`) at once. The provisioning snippet and the
  phase-branch-naming convention are mutually incompatible as literally written whenever the worktree
  is provisioned with the bare plan-identifier as its own branch name. Fix applied: `git branch -m
ayokoding-learning-path-04-course-authoring/evaluating-ai-output-essentials` — renaming the current
  (unpushed) branch directly into the first phase-1 sub-branch name, which both frees the bare name
  and carries the local Phase 0 commit forward (satisfying "Phase 0's evidence rides the Phase 1 PR").
  Only works because nothing had been pushed yet; a worktree with a pushed bare-named branch would
  need a different resolution (e.g. delete the remote ref too, or pick a provisioning name outside the
  `<plan-id>/*` namespace, e.g. `<plan-id>-base`).
- **Why it might generalize**: every `worktree-to-pr` plan whose delivery.md phase-branch convention
  reuses the plan-identifier as a `/`-prefix will hit this on its very first phase branch. Worth fixing
  at the source — either the worktree provisioning snippet in `plan-execution.md` Step 0 or the
  worktree-setup convention should name the initial branch outside the `<plan-id>/*` namespace (e.g.
  `<plan-id>-base` or provision directly onto a throwaway/detached ref) so it never collides with the
  first real phase branch.
