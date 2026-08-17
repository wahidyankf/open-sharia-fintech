# A ref-advancing fetch desynchronized a checkout, and git reported the drift as 265 staged changes

One-line summary: `git fetch origin main:main` fast-forwarded a **checked-out** branch's ref by 9
commits without touching the index or working tree, so `git status` presented the entire 9-commit
delta as a pending mass revert — 265 staged files, −16,550 lines — which then broke a push, and which
two separate agent sessions correctly-but-wrongly read as "another actor's in-flight work" and
deferred to.

> Surfaced 2026-08-05 while investigating why the sibling `beaver-nest` repository showed 265
> uncommitted files. Filed as a brief rather than fixed inline: the tree recovery is one thing, but
> the class — a ref that moves without its checkout, and the deferral behavior it triggers — needs its
> own scoped decision.

## Problem / context

`git status` in the `beaver-nest` working tree reported **265 staged files**: 106 deletions, 30
additions, 128 modifications, **−16,550 lines**. It read exactly like a large in-flight session's
work. It was nobody's work at all.

On **2026-08-04 at 09:12**, something ran `git fetch origin main:main`. That refspec form writes the
destination branch ref directly. Git normally refuses when the destination is the currently
checked-out branch, but `--update-head-ok` overrides that guard — and the local `main` ref
fast-forwarded **9 commits**, from `be67af9f0` to `cd2ec0e4d`. HEAD jumped forward. The index and the
working tree stayed exactly where the last real checkout had left them, at their **2026-08-03 ~20:56**
state. Git then did the only thing it can do: it diffed a 2026-08-03 index against a 2026-08-04 HEAD
and reported the whole 9-commit span as pending changes — which, read in the normal direction, looks
like a staged **revert** of everything that landed in between.

The reflog signature is how anyone would recognize a recurrence (hashes real, commit subject elided):

```text
cd2ec0e4d main@{0}: fetch origin main:main: fast-forward
be67af9f0 main@{1}:
be67af9f0 main@{2}: commit: <subject elided>
```

The tell is the combination: a `commit:` entry the checkout itself made, a **blank-message** bare ref
move, then a `fetch <remote> <src>:<dst>: fast-forward` — and **no `checkout:` or `merge:` entry
anywhere across the 9-commit span**. A branch that advanced without its working tree leaves exactly
this gap.

Four independent observations confirmed the staged set was a revert rather than authorship:

- The staged diff restored `next.config.ts` and `src/app/**` while deleting `index.html` and
  `App.tsx` — the precise inverse of the commit `feat(beaver-nest-fe): migrate workspace to vite`.
- `vite.config.ts` was present in HEAD but absent from both the disk and the index.
- Files that `git ls-files --others` reported as **untracked** were simultaneously **staged-deleted**
  in the index while still sitting on disk.
- The index tree was 43 files away from the last commit that checkout had actually made, and 306 files
  away from HEAD. It had never advanced.

Two F# files whose content genuinely differed turned out to be strictly _earlier_ drafts —
pre-formatter line wrapping, a missing `open`, an older API call — not newer work.

Three consequences actually bit:

- **A docs-only commit could not be pushed.** Pre-push `md links validate` failed on a stale README
  pointing at a spec file that had since been moved, and `nx affected -t test:quick` selected 9
  projects and failed 4 — every failure sourced from the stale tree, none from the commit being
  pushed. This compounds
  [nx-affected-cross-worktree-contamination](./nx-affected-cross-worktree-contamination.md), which
  covers `nx affected` including uncommitted working-directory state.
- **An agent deferred its own work — twice, across two sessions.** Reading `git status`, it correctly
  concluded "another session holds 265 staged files" and stood down. The repo's File-Touch Discipline
  rule ("anything not on your ledger is another actor's in-flight work — leave it untouched") gives
  exactly the wrong answer when the foreign-looking changes are a ref-advance artifact rather than a
  real actor. Deferring to a phantom blocks real work indefinitely.
- **The obvious one-line fix was unsafe.** Real uncommitted work — 8 files, +218/−37, including a
  141-line file present on no remote — sat in the same tree, so `git reset --hard` would have
  destroyed it.

Two adjacent findings from the same investigation confirm the checkout was unattended rather than
merely unlucky: `stag-beaver-nest-be` and `stag-beaver-nest-fe` were both 9 commits behind
`origin/main`, so staging served pre-migration code; and the entire workstream reached `main` with no
PR at all (that repository holds only two PRs, both from an earlier day), against its own
`worktree-to-pr` default.

## Why now

The repository's concurrency model assumes many actors share one machine, one object store, and one
set of worktrees — and it hands agents a single primitive, `git status`, to tell their own work from
everyone else's. This incident shows that primitive returning a confident, well-formed, entirely false
answer, and shows the standing File-Touch Discipline response to that answer (defer, touch nothing)
converting a recoverable desynchronization into an indefinite work stoppage. The failure is silent by
construction: nothing errors, nothing warns, and the longer the checkout sits, the larger and more
convincing the phantom changeset grows. It cost two agent sessions and one blocked push before anyone
looked at the reflog.

## Prior art / precedents

- **`nx affected` cross-worktree contamination** — the closest sibling: an unrelated dirty tree
  failing an innocent push's pre-push gate. Same victim (a docs-only push), different upstream cause
  (there, concurrent WIP; here, a phantom changeset). The two compound, and a fix for either would
  have softened this incident.
  [nx-affected-cross-worktree-contamination](./nx-affected-cross-worktree-contamination.md)
- **File-Touch Discipline** — the ledger rule whose "in the tree but not on your ledger → another
  actor's work, leave it untouched and unstaged" clause produced the wrong call twice here. The rule
  is right for its intended case and has no notion of this one.
  [file-touch-discipline](../../../repo-governance/development/practice/file-touch-discipline.md)
- **Bare-Repo Base-Worktree Landing Method** — already carries a **topology-keyed** terminal reconcile:
  `git fetch origin main:main` where the repository is bare, `git fetch` then
  `git merge --ff-only origin/main` where a work tree exists. The rule to prevent this incident
  therefore already exists in this repo; what the doc does not yet state is the consequence of
  misapplying the key. It justifies the bare form as carrying "the same safety property `--ff-only`
  provides" — true on the non-fast-forward-refusal axis, and silent on the index/worktree axis that
  actually failed here.
  [bare-repo-landing-method](../../../repo-governance/development/workflow/bare-repo-landing-method.md)
- **Same-machine assumption** — the standing convention that concurrent agents share disk, git
  objects, and worktrees, and that this sharing is exactly what makes `git status` unreliable as a
  record of one's own work. This incident is a new failure mode under that assumption: unreliable in a
  direction the convention does not anticipate.
  [agent-workflow-orchestration](../../../repo-governance/development/agents/agent-workflow-orchestration.md)
- **No Destructive Git Operations** — the reason `git reset --hard` was correctly not reached for,
  and the reason recovery needed a plan rather than a one-liner given the 8 files of real
  uncommitted work in the same tree.
  [no-destructive-git-operations](../../../repo-governance/development/workflow/no-destructive-git-operations.md)
- **`git-fetch(1)`'s `--update-head-ok` documentation** — git's own manual states that fetch refuses
  to update the head corresponding to the current branch, and that this flag disables the check,
  explicitly warning it can leave the index and working tree inconsistent with HEAD. The behavior is
  documented; the operational consequence in a shared multi-agent checkout is not.

## Proposed direction (sketch)

Four angles, none of them yet the pick:

- **Never advance a checked-out branch by ref-write.** Where a work tree exists, the safe form is
  `git fetch` followed by `git merge --ff-only` (or `git pull --ff-only`), which fails loudly against
  a dirty or diverged tree instead of silently desynchronizing it. The repo's landing method already
  says this; the open question is whether it needs to say it as a _prohibition_ with the failure mode
  attached, rather than as a table row keyed on topology.
- **A cheap staleness detector an agent can run before trusting `git status`.** The signatures are
  mechanical: a large staged set whose diff is the _inverse_ of recent `HEAD` commits, or an index
  tree far from HEAD but close to an older commit (here: 306 files from HEAD, 43 from the checkout's
  own last commit). Either is computable in a few plumbing commands, and either is decisive.
- **Teach File-Touch Discipline to distinguish "foreign in-flight work" from "ref-advance artifact"
  before deferring.** Deferral is the right default only when a real actor exists; against a phantom
  it is an indefinite block. The rule may need a precondition rather than a rewrite.
- **Audit whether tooling can issue this command into a checked-out branch.** Verified for
  `ose-public`: no hook, script, GitHub Actions workflow, or agent definition issues
  `fetch <src>:<dst>` into a local branch — the only refspec fetches in `.github/workflows/` write
  into `refs/remotes/*`, and the `main:main` form appears solely in governance prose. The exposure
  here is therefore a **human or agent following the bare-repo branch of a topology-keyed rule in a
  repository that has a work tree**, not an automated caller. Whether that holds in the other three
  repos is untested.

## Rough scope & non-goals

In scope: deciding whether the topology-keyed reconcile rule needs a stated prohibition and failure
mode for the has-a-work-tree case; specifying a detector an agent can run cheaply before trusting
`git status`; deciding whether File-Touch Discipline's deferral clause needs a
"verify-the-actor-exists" precondition; verifying the tooling audit above across both parity repos.

Out of scope: recovering the specific `beaver-nest` tree (an operational task with its own care
requirements, given the 8 files of real uncommitted work); rewriting the bare-repo landing method's
bare-topology guidance, which remains correct for bare repositories; building a git wrapper or
enforcing anything at the git-plumbing level; the `stag-beaver-nest-*` staleness and the missing-PR
observation, which are symptoms of the unattended checkout and belong to that repo's own hygiene.

## Risks & open questions

- **Which tool or human ran the fetch.** Unknown. The reflog records the command and the timestamp
  but not the caller, and no ose-public tooling issues this form. Without an answer, any fix targets a
  hypothesis about who to constrain. (open)
- **Whether a detector can distinguish this from a legitimate large refactor without false
  positives.** A genuine 265-file refactor and a phantom 265-file revert differ in direction, not in
  size — the inverse-of-recent-HEAD-commits test is the discriminator, but its false-positive rate
  against real revert commits and real large-scale renames is untested. A detector that cries wolf
  gets ignored, which is worse than none. (open)
- **Whether the same pattern exists in the other three repos.** Unverified. Two of the four are bare
  and legitimately use this exact command, which makes the boundary between correct and catastrophic
  usage exactly one topology check wide. (open)
- **Whether relaxing File-Touch Discipline's deferral clause reopens the hazard it was written to
  close.** The clause exists because agents have clobbered concurrent work; any "verify first"
  precondition must not become a licence to touch genuinely foreign files when verification is
  inconclusive. (open)
- **How long the checkout had been drifting before anyone noticed.** The ref moved 2026-08-04 09:12
  and the discovery came 2026-08-05, but nothing establishes that the fetch was the first such event
  rather than the most recent. (open)

## What success looks like + promotion signal

Success: an agent that opens a checkout showing a large unexplained staged set runs one bounded check
and gets a decisive verdict — "this is a ref-advance artifact, reconcile it" versus "this is another
actor's work, defer" — instead of defaulting to indefinite deferral; and the has-a-work-tree reconcile
path states its failure mode loudly enough that following the wrong branch of the topology key is hard
rather than silent.

Promotion signal: promote once two things hold — the tooling audit above is repeated across all four
repos with a per-repo verdict, and the inverse-of-recent-HEAD detector is trialled against at least
one real large revert commit and one real large refactor commit to establish it separates them. Those
two results turn every open question above from a hypothesis into a scoped fix. A second occurrence in
any of the four repos before then escalates promotion immediately.
