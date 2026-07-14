# 6 · Version Control & Git (By Example, Git †)

**prd row**: Pass 1 · Core Foundations · By Example · Git † · Learn 106 / Drill 206 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: Git as the working engineer's memory and collaboration substrate — building an
object-model intuition (commits/trees/blobs/refs), everyday CLI fluency, branching with merge and
rebase, and a pull-request / trunk-based flow. `†`: everything is driven from the `git` command line,
no GUI. The build-your-own-Git pass that reconstructs the content-addressed object store from scratch
lives at [`90-build-your-own-git`](./90-build-your-own-git.md).

## Why this exists · the big idea

- **The problem before the solution**: before version control, coordinating change meant zipped
  folders, `final_v2_REALLY_final` filenames, and silently overwriting a colleague's work with no way
  back — there was no shared, trustworthy record of who changed what and why.
- **Keep-this-if-you-forget-everything**: a commit is an immutable snapshot of the whole tree,
  identified by the hash of its content, and a branch is just a movable pointer to one commit — once
  that clicks, merge, rebase, reset, and reflog stop being magic and become graph operations.
- **Big ideas touched**: `coupling-vs-cohesion` (a branch-and-PR flow keeps changes that belong
  together in one reviewable commit and unrelated work apart), `correctness-vs-pragmatism` (rebase
  buys a clean linear history but rewrites shared state — the disciplined compromise is rebase local
  work, merge shared work).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md) and
  [topic 5 Just Enough Bash](./05-just-enough-bash.md).
- **Tools & environment**: a macOS/Linux terminal; **Git** at a recent stable release; a GitHub (or
  equivalent) account for the remote/PR flow; Neovim/VSCode with Git integration for diffs and blame
  (DD-17).
- **Assumed knowledge**: navigating a filesystem and running CLI tools (topic 05); reading a small
  script well enough to understand a commit hook (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: Git's core CLI (`add`/`commit`/`branch`/`merge`/`rebase`/`log`/`reflog`) and
  object model (blob/tree/commit/tag, hash-addressed storage) are stable and correctly left
  version-unpinned. Git's SHA-1 → SHA-256 object-format transition is still opt-in/experimental —
  describe the store as hash-addressed without asserting the default hash is already SHA-256.
- 2026-07-12 — verified: "trunk-based development" and the pull-request review flow described here
  match current mainstream practice; there is no version claim to pin.
- 2026-07-14 — corrected (post-authoring `apps-ayokoding-www-facts-checker` sweep): the reflog concept
  entry (co-22, `learning/overview.md`) originally claimed the reflog "by default expires unreachable
  entries after 90 days." Verified against [git-gc](https://git-scm.com/docs/git-gc) that Git has two
  separate defaults: `gc.reflogExpire` = 90 days for entries still **reachable** from a branch tip, but
  `gc.reflogExpireUnreachable` = **30 days** for entries made unreachable (exactly the `reset --hard`
  recovery scenario the passage describes). Content corrected to state both defaults accurately.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: `git-scm.com/docs` (official command reference) and the Pro
> Git book (`git-scm.com/book`). All 29 concepts + all sampled worked-example command/flag/output claims
> verified.

- **Version + object model (co-01/03, ex-13..16)** — current stable **Git 2.55.0** (2026-06-29,
  [Downloads](https://git-scm.com/downloads); body text correctly leaves it unpinned). Blob/tree/commit
  - hash-addressed store per [Pro Git "Git Objects"](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects);
    SHA-1 default, SHA-256 opt-in (`extensions.objectFormat=sha256`) per
    [hash-function-transition](https://git-scm.com/docs/hash-function-transition) — confirms the
    hash-addressed-without-asserting-SHA-256 framing. `git cat-file -p`/`-t` verbatim from
    [git-cat-file](https://git-scm.com/docs/git-cat-file).
- **Staging, commit, diff, log (co-05..10)** — [git-add](https://git-scm.com/docs/git-add) (`-p` patch,
  `s` split-hunk), [git-commit](https://git-scm.com/docs/git-commit) (`-a`/`-m`/`--amend`),
  [git-diff](https://git-scm.com/docs/git-diff) (working-vs-index, `--staged`, two-commit),
  [git-log](https://git-scm.com/docs/git-log) (`--oneline`/`--graph`/`--pretty`/`-N`/`-- path`) — all verbatim.
- **Branch, merge, rebase, reset, revert, restore, stash (co-11..21)** —
  [git-branch](https://git-scm.com/docs/git-branch)/[git-switch](https://git-scm.com/docs/git-switch)
  (`-c`); [git-merge](https://git-scm.com/docs/git-merge) + [Pro Git Basic Branching](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
  (`Fast-forward`, `--no-ff`, `--abort`, `both modified:`, conflict markers);
  [git-rebase](https://git-scm.com/docs/git-rebase) (replay → new hashes, `-i` reword/squash/fixup/drop);
  [git-reset](https://git-scm.com/docs/git-reset) (**`--mixed` default**, soft/mixed/hard scope);
  [git-revert](https://git-scm.com/docs/git-revert) (`-m 1` mainline);
  [git-restore](https://git-scm.com/docs/git-restore) (`--staged`/`--source`);
  [git-stash](https://git-scm.com/docs/git-stash) (`pop`/`apply`/`push -m`/`list`) — all verbatim.
- **Reflog, remotes, tags, ignore, hooks, cherry-pick (co-22..29)** —
  [git-reflog](https://git-scm.com/docs/git-reflog) (`HEAD@{2}`) + [git-fsck](https://git-scm.com/docs/git-fsck)
  (`--lost-found`); [git-fetch](https://git-scm.com/docs/git-fetch)/[git-push](https://git-scm.com/docs/git-push)
  (non-fast-forward `rejected`)/[git-pull](https://git-scm.com/docs/git-pull) (`--rebase`);
  [git-tag](https://git-scm.com/docs/git-tag) (annotated=tag object, lightweight=ref);
  [gitignore](https://git-scm.com/docs/gitignore) + `git add -f`; [githooks](https://git-scm.com/docs/githooks)
  (`pre-commit` non-zero aborts); [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick) (`--continue`);
  trunk flow per [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/) — all verified.
- **Lineage** — Git 2005, Linux-kernel/BitKeeper breakdown, Torvalds, per
  [Pro Git "A Short History of Git"](https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git).
- **Read more corrections** — the enumerated "seven rules" convention is **Chris Beams' 2014**
  [cbea.ms/git-commit](https://cbea.ms/git-commit/), not Tim Pope's 2008 article (now cited for its own
  subject/body-and-wrapping content); the "Git Internals" narrative chapters are in the Pro Git book, not
  at `git-scm.com/docs` (citation descriptions corrected accordingly).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · repository-init-and-clone** — `git init` creates the `.git/` directory that turns a folder
  into a repository, and `git clone` copies an existing repository plus its full history.
- **co-02 · three-states-model** — every tracked file lives in one of three areas: the working tree
  (what you edit), the staging area / index (what the next commit will contain), and committed history.
- **co-03 · object-model** — Git stores content as four hash-addressed object types — blob (file
  content), tree (directory), commit (snapshot + metadata), and tag — each identified by the hash of
  its content.
- **co-04 · refs-branches-head** — a branch or tag is just a named pointer to a commit, and `HEAD` is a
  pointer to the current branch (or a detached commit) that decides what "current" means.
- **co-05 · staging-and-status** — `git add` moves changes from the working tree into the index, and
  `git status` reports which files are untracked, modified-but-unstaged, or staged.
- **co-06 · hunk-staging** — `git add -p` stages selected hunks (or split sub-hunks) so one physical
  edit can become several focused commits.
- **co-07 · committing-and-messages** — `git commit` records the staged snapshot as a new commit with a
  subject line and optional body following the imperative-mood convention.
- **co-08 · amending-commits** — `git commit --amend` rewrites the most recent commit (message and/or
  contents), producing a new hash that replaces the previous tip.
- **co-09 · diffing** — `git diff` compares states: working-tree-vs-index, index-vs-HEAD
  (`--staged`), or any two commits/branches.
- **co-10 · history-inspection** — `git log` (with `--oneline`/`--graph`/`--pretty`), `git show`, and
  `git cat-file` reveal the commit graph and the raw objects behind it.
- **co-11 · branching** — `git branch`/`git switch`/`git checkout` create, list, rename, delete, and
  move between branches, each a cheap movable pointer.
- **co-12 · fast-forward-merge** — when the target branch has not diverged, `git merge` simply advances
  the branch pointer with no new commit.
- **co-13 · three-way-merge** — when both branches have new commits, `git merge` creates a merge commit
  with two parents that combines the divergent trees.
- **co-14 · conflict-resolution** — overlapping edits produce conflict markers that must be resolved,
  re-staged, and committed (or the merge/rebase aborted).
- **co-15 · rebase** — `git rebase` replays a branch's commits onto a new base, producing new commit
  hashes and a linear history.
- **co-16 · interactive-rebase** — `git rebase -i` curates local history by reordering, squashing,
  rewording, editing, or dropping commits.
- **co-17 · rebase-vs-merge-policy** — rebase rewrites commit identity, so the discipline is "rebase
  local work, merge shared work — never rebase history others have pulled."
- **co-18 · reset-modes** — `git reset` moves `HEAD` and optionally the index (`--mixed`, default) and
  working tree (`--hard`), or leaves both (`--soft`).
- **co-19 · revert** — `git revert` records a new inverse commit that undoes an earlier one without
  rewriting history — the safe, additive undo.
- **co-20 · restore-files** — `git restore` (with `--staged`/`--source`) recovers file contents from
  the index or any commit into the working tree.
- **co-21 · stash** — `git stash` shelves uncommitted changes onto a stack so the working tree is clean,
  then `pop`/`apply` restores them later.
- **co-22 · reflog** — `git reflog` records every movement of `HEAD`, making "lost" commits and deleted
  branches recoverable after resets and rebases.
- **co-23 · remotes-fetch-push-pull** — `git remote`, `git fetch`, `git push`, and `git pull` connect a
  local repository to remote copies and synchronize commits between them.
- **co-24 · tracking-branches** — an upstream (tracking) relationship links a local branch to a
  remote-tracking ref so `push`/`pull` know the default target.
- **co-25 · tagging** — `git tag` marks a commit with a lightweight or annotated (object-backed) name,
  typically for releases.
- **co-26 · gitignore** — `.gitignore` patterns keep generated/secret files untracked, while `git add
-f` can override an ignore rule.
- **co-27 · commit-hooks** — executable scripts in `.git/hooks/` (e.g. `pre-commit`) run at lifecycle
  points and can block a commit that fails a check.
- **co-28 · pull-request-trunk-flow** — short-lived branches are integrated to trunk through review
  (pull request) and frequent merges, the backbone of trunk-based development.
- **co-29 · cherry-pick** — `git cherry-pick` applies the change introduced by an individual commit onto
  the current branch as a new commit.

## Tensions & trade-offs — when NOT to reach for this

- **Rebase vs merge is not free**: rebasing rewrites commit identity, so rebasing a branch others have
  already pulled forces everyone to reconcile — the clean linear history is worth it locally and a
  liability once shared.
- **History rewriting has a blast radius**: `reset --hard`, force-push, and history-rewriting filters
  can destroy work; the reflog rescues you locally but not a force-pushed remote. When in doubt prefer
  additive operations (`revert`) over destructive ones.
- **Git is not a large-binary store**: it snapshots whole file content, so large binaries bloat every
  clone forever. Reach for LFS or an artifact store instead — this is a "when not to put it in Git"
  boundary, not a tuning knob.

## Lineage — why it beat the alternative

- Centralized version control (CVS, then Subversion) put history on one server: every commit needed
  the network, branching was expensive, and the server was a single point of failure. Git (2005, built
  for Linux-kernel development) inverted this — every clone is a full repository with the entire
  history, commits are local and cheap, and content-addressed storage makes integrity and
  de-duplication fall out for free. Distributed, near-free branching is precisely what made the
  pull-request and trunk-based workflows practical. This topic hands its object-model intuition to
  [`90-build-your-own-git`](./90-build-your-own-git.md), which rebuilds the content-addressed store,
  and its collaboration flow to [`55-cicd-and-release-engineering`](./55-cicd-and-release-engineering.md),
  which automates the path from commit to production.

## Worked examples

All colocated under `version-control-and-git/learning/code/`; each is a real repo you build and inspect
from the `git` CLI (DD-20/DD-30), and each cites the `co-NN` it exercises. Contiguous `ex-01..ex-82`.

### Beginner

- **ex-01 · init-repository** — run `git init` in an empty directory — verify `.git/` exists and `git
status` reports "No commits yet". (co-01)
- **ex-02 · check-status-clean** — run `git status` in a fresh repo — verify it names the current branch
  and reports "nothing to commit". (co-05)
- **ex-03 · create-untracked-file** — create `file.txt`, run `git status` — verify the file appears
  under "Untracked files". (co-05)
- **ex-04 · stage-a-file** — run `git add file.txt` — verify `git status` moves it from the working tree
  into "Changes to be committed". (co-05, co-02)
- **ex-05 · first-commit** — run `git commit -m "add file"` — verify `git log --oneline` shows exactly
  one commit. (co-07)
- **ex-06 · commit-shows-snapshot** — run `git show HEAD` — verify it prints the commit metadata and the
  added file's diff. (co-07, co-10)
- **ex-07 · stage-all-changes** — modify two tracked files, run `git add -A` — verify both appear staged
  in `git status`. (co-05)
- **ex-08 · unstage-file** — after staging, run `git restore --staged file.txt` — verify it returns to
  unstaged in `git status`. (co-20, co-05)
- **ex-09 · diff-working-tree** — modify a tracked file, run `git diff` — verify the unstaged change
  appears. (co-09)
- **ex-10 · diff-staged** — stage a change, run `git diff --staged` — verify the staged change appears
  while plain `git diff` is empty. (co-09, co-02)
- **ex-11 · view-log-oneline** — after several commits run `git log --oneline` — verify one line per
  commit with abbreviated hashes. (co-10)
- **ex-12 · view-log-graph** — run `git log --graph --oneline --all` — verify an ASCII commit graph
  renders. (co-10)
- **ex-13 · inspect-blob-cat-file** — run `git cat-file -p HEAD:file.txt` — verify it prints the file's
  committed contents. (co-03, co-10)
- **ex-14 · inspect-commit-object** — run `git cat-file -p HEAD` — verify it shows the tree hash,
  parent, author, and message. (co-03)
- **ex-15 · inspect-tree-object** — run `git cat-file -p HEAD^{tree}` — verify it lists blob/tree
  entries with modes and names. (co-03)
- **ex-16 · object-type** — run `git cat-file -t HEAD` — verify it prints "commit". (co-03)
- **ex-17 · amend-last-commit** — run `git commit --amend -m "new msg"` — verify `git log` shows the
  updated message and a new hash. (co-08)
- **ex-18 · amend-add-forgotten-file** — stage a forgotten file, run `git commit --amend --no-edit` —
  verify `git show --stat` lists it in HEAD's tree. (co-08)
- **ex-19 · gitignore-basics** — add `*.log` to `.gitignore`, create `x.log` — verify `git status` does
  not list `x.log`. (co-26)
- **ex-20 · force-add-ignored** — run `git add -f x.log` — verify the ignored file stages despite
  `.gitignore`. (co-26)
- **ex-21 · create-branch** — run `git branch feature` — verify `git branch` lists `feature` beside the
  current branch. (co-11)
- **ex-22 · switch-branch** — run `git switch feature` — verify `git status` reports "On branch
  feature". (co-11)
- **ex-23 · create-and-switch** — run `git switch -c hotfix` — verify a new branch is created and
  checked out in one step. (co-11)
- **ex-24 · head-tracks-branch** — after switching, compare `git rev-parse HEAD` and `git rev-parse
hotfix` — verify the two hashes are identical. (co-04)
- **ex-25 · list-refs** — run `git show-ref` (or `git branch -v`) — verify each branch name maps to a
  commit hash. (co-04)
- **ex-26 · delete-merged-branch** — run `git branch -d feature` after merging — verify `git branch` no
  longer lists it. (co-11)
- **ex-27 · rename-branch** — run `git branch -m old new` — verify `git branch` shows the new name. (co-11)
- **ex-28 · tag-lightweight** — run `git tag v1` on HEAD — verify `git tag` lists `v1` and `git rev-parse
v1` matches HEAD. (co-25)

### Intermediate

- **ex-29 · stage-hunks-interactively** — run `git add -p` and accept one hunk — verify only that hunk
  is staged and the rest stays unstaged in `git diff`. (co-06)
- **ex-30 · split-a-hunk** — in `git add -p` press `s` to split, stage one part — verify `git diff
--staged` contains only the chosen sub-hunk. (co-06)
- **ex-31 · commit-with-body** — create a commit with a subject + body — verify `git log --format=%B -1`
  prints both. (co-07)
- **ex-32 · diff-two-commits** — run `git diff HEAD~2 HEAD` — verify the combined change across the last
  two commits appears. (co-09, co-10)
- **ex-33 · diff-branches** — run `git diff main..feature` — verify only feature's divergent changes
  appear. (co-09)
- **ex-34 · log-limit-and-format** — run `git log -3 --pretty=format:"%h %s"` — verify exactly three
  commits print in the custom format. (co-10)
- **ex-35 · log-by-path** — run `git log -- file.txt` — verify only commits touching `file.txt` appear.
  (co-10)
- **ex-36 · fast-forward-merge** — commit only on `feature`, then `git merge feature` from `main` —
  verify `main` advances with no merge commit and `git log` stays linear. (co-12)
- **ex-37 · no-ff-merge** — run `git merge --no-ff feature` — verify a merge commit is created even
  though fast-forward was possible. (co-13)
- **ex-38 · three-way-merge-clean** — diverge both branches on different files, `git merge feature` —
  verify `git cat-file -p HEAD` shows two parent lines. (co-13)
- **ex-39 · create-merge-conflict** — edit the same line on both branches, `git merge feature` — verify
  Git reports a conflict and `git status` lists the file as "both modified". (co-14)
- **ex-40 · resolve-conflict** — remove the conflict markers, `git add`, `git commit` — verify the merge
  completes and `git log --graph` shows it. (co-14)
- **ex-41 · abort-merge** — during a conflict run `git merge --abort` — verify the working tree returns
  to its pre-merge state (`git status` clean). (co-14)
- **ex-42 · inspect-conflict-diff** — during a conflict run `git diff` — verify it shows the combined
  conflict diff with both sides. (co-14)
- **ex-43 · rebase-onto-main** — on `feature` run `git rebase main` — verify the commits replay atop
  main with new hashes and a linear `git log`. (co-15)
- **ex-44 · rebase-conflict-continue** — hit a rebase conflict, resolve, `git add`, `git rebase
--continue` — verify the rebase finishes. (co-15, co-14)
- **ex-45 · rebase-abort** — during a rebase conflict run `git rebase --abort` — verify the branch
  returns to its pre-rebase tip. (co-15)
- **ex-46 · interactive-rebase-squash** — run `git rebase -i HEAD~3`, mark two commits `squash` — verify
  `git log --oneline` shows them combined into one. (co-16)
- **ex-47 · interactive-rebase-reword** — `git rebase -i` with `reword` — verify the target commit's
  message changes while the others stay. (co-16)
- **ex-48 · interactive-rebase-reorder** — reorder the lines in `git rebase -i` — verify `git log` shows
  the new commit order. (co-16)
- **ex-49 · interactive-rebase-drop** — mark a commit `drop` — verify that commit no longer appears in
  `git log`. (co-16)
- **ex-50 · compare-merge-vs-rebase-history** — integrate one branch by merge and an equivalent by
  rebase, then `git log --graph` each — verify one has a merge commit and the other is linear. (co-17)
- **ex-51 · reset-soft** — run `git reset --soft HEAD~1` — verify HEAD moves back one commit but the
  changes remain staged (`git status`). (co-18)
- **ex-52 · reset-mixed** — run `git reset HEAD~1` (mixed default) — verify HEAD moves back and the
  changes become unstaged but still present. (co-18)
- **ex-53 · reset-hard** — run `git reset --hard HEAD~1` — verify HEAD moves back and the working tree
  matches (the change is gone). (co-18)
- **ex-54 · unstage-with-reset** — after staging, run `git reset HEAD file.txt` — verify the file
  becomes unstaged. (co-18, co-05)
- **ex-55 · revert-commit** — run `git revert HEAD` — verify a new inverse commit appears and the change
  is undone while history is preserved. (co-19)
- **ex-56 · restore-file-from-head** — modify a file then run `git restore file.txt` — verify the
  working-tree file reverts to HEAD's version. (co-20)
- **ex-57 · restore-file-from-commit** — run `git restore --source=HEAD~2 file.txt` — verify the file's
  content matches that older commit. (co-20)
- **ex-58 · stash-changes** — with a dirty tree run `git stash` — verify `git status` is clean and `git
stash list` shows one entry. (co-21)
- **ex-59 · stash-pop** — run `git stash pop` — verify the changes return and the stash entry is
  removed. (co-21)
- **ex-60 · stash-named-and-list** — run `git stash push -m "wip"` then `git stash list` — verify the
  labeled entry appears. (co-21)

### Advanced

- **ex-61 · reflog-inspect** — run `git reflog` after several moves — verify it lists HEAD positions as
  `HEAD@{n}` entries. (co-22)
- **ex-62 · recover-after-hard-reset** — do `git reset --hard HEAD~2`, then `git reset --hard HEAD@{1}`
  from the reflog — verify the "lost" commits are restored in `git log`. (co-22, co-18)
- **ex-63 · recover-deleted-branch** — delete a branch, find its tip in `git reflog`, run `git branch
recovered <hash>` — verify the branch and its commits reappear. (co-22, co-11)
- **ex-64 · add-remote** — run `git remote add origin <path>` — verify `git remote -v` lists origin's
  fetch/push URLs. (co-23)
- **ex-65 · clone-repository** — run `git clone <src> dest` — verify `dest/.git` exists and `git -C dest
log` shows the source history. (co-01, co-23)
- **ex-66 · push-to-remote** — run `git push origin main` to a bare remote — verify `git -C remote.git
log` shows the pushed commit. (co-23)
- **ex-67 · set-upstream-tracking** — run `git push -u origin feature` — verify `git branch -vv` shows
  the `origin/feature` tracking ref. (co-24)
- **ex-68 · fetch-updates** — after remote changes run `git fetch` — verify `git log origin/main`
  advances while local `main` does not. (co-23, co-24)
- **ex-69 · pull-fast-forward** — run `git pull` when behind — verify the local branch fast-forwards to
  match `origin`. (co-23, co-12)
- **ex-70 · pull-rebase** — with local and remote commits run `git pull --rebase` — verify local commits
  replay atop the fetched ones (linear `git log`). (co-24, co-15)
- **ex-71 · push-rejected-non-fast-forward** — attempt `git push` after the remote advanced — verify Git
  rejects it with a non-fast-forward error. (co-23)
- **ex-72 · checkout-remote-tracking-branch** — run `git switch feature` for a remote-only branch —
  verify a local tracking branch is created from `origin/feature`. (co-24)
- **ex-73 · annotated-tag** — run `git tag -a v1.0 -m "release"` — verify `git cat-file -t v1.0` prints
  "tag" and `git show v1.0` shows the tagger. (co-25)
- **ex-74 · push-tags** — run `git push origin --tags` — verify the tag appears in the remote (`git -C
remote.git tag`). (co-25, co-23)
- **ex-75 · cherry-pick-commit** — run `git cherry-pick <hash>` onto another branch — verify the single
  commit's change is applied with a new hash. (co-29)
- **ex-76 · cherry-pick-conflict** — resolve a cherry-pick conflict, run `git cherry-pick --continue` —
  verify it completes. (co-29, co-14)
- **ex-77 · install-pre-commit-hook** — add an executable `.git/hooks/pre-commit` that greps for "TODO",
  then commit content containing TODO — verify the commit is blocked with the hook's message. (co-27)
- **ex-78 · hook-allows-clean-commit** — commit clean content with the same hook installed — verify the
  commit succeeds. (co-27)
- **ex-79 · pr-branch-flow** — create a feature branch, push it, and land it to trunk with `git merge
--no-ff` — verify trunk contains the change and shows a merge commit. (co-28, co-13)
- **ex-80 · trunk-based-short-branch** — commit a small change on a short-lived branch, fast-forward it
  to `main`, delete the branch — verify `main` advanced and the branch is gone. (co-28, co-12, co-11)
- **ex-81 · revert-a-merge** — run `git revert -m 1 <merge-hash>` — verify the merge's changes are
  undone by a new commit while history stays intact. (co-19, co-13)
- **ex-82 · verify-history-intact-after-recovery** — after a reset+reflog recovery, run `git log --graph
--all` and `git fsck --lost-found` — verify no intended commits are dangling or lost. (co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a small project from empty directory to a reviewed, merged change on trunk — a
  curated commit history, a resolved conflict, a recovered mistake, and a pull-request merge — proving
  Git fluency end to end.
- **Concepts exercised**: [ ] object-model inspection (`cat-file`/`log --graph`) [ ] commits staged in
  hunks with good messages [ ] a branch + three-way merge with a resolved conflict [ ] an interactive
  rebase [ ] a `reflog` recovery [ ] a PR/trunk-based merge to a remote.
- **Ordered steps**:
  1. `.../learning/capstone/code/` — init the repo and build a three-to-four-commit history staged in
     hunks. Verify `git log --graph` shows the intended graph and `git cat-file -p` resolves a commit
     to its tree and blobs.
  2. Branch, force a conflict against trunk, and resolve it with a merge. Verify the merge commit has
     two parents and the resulting tree is correct.
  3. On a second branch, curate history with an interactive rebase, then recover a deliberate
     `reset --hard` via `reflog`. Verify the "lost" commit is restored.
  4. Push to a remote and land the change through a pull request onto trunk with a passing pre-commit
     hook. Verify trunk contains the change and the history is intact.
- **Acceptance criteria**: the object graph matches intent; the conflict resolves correctly; the rebase
  produces the curated history; the reflog recovery restores the commit; the PR merges to trunk.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Pro Git** — Scott Chacon, Ben Straub (2nd ed.). Canonical free book on Git: data model, branching,
  workflows, internals. <https://git-scm.com/book/en/v2>

**Papers & articles**

- **Git Reference Documentation** — The Git Project. Official command reference (porcelain + plumbing
  commands). The narrative "Git Internals" object-storage chapters live in the Pro Git book above.
  <https://git-scm.com/docs>
- **"A Note About Git Commit Messages"** — Tim Pope (2008). Early, widely cited article on
  subject/body separation, imperative mood, and 50/72 wrapping. <https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>
- **"How to Write a Git Commit Message"** — Chris Beams (2014). Source of the enumerated
  "seven rules" commit-message convention. <https://cbea.ms/git-commit/>

---

← Previous: [5 · Just Enough Bash](./05-just-enough-bash.md) · Next: [7 · Data Structures & Algorithms Essentials](./07-data-structures-and-algorithms-essentials.md) →
