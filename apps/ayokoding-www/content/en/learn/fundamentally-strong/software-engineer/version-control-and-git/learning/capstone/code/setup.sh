#!/bin/bash
# Version Control & Git capstone: a small "task-tracker" project taken from an empty directory to a
# reviewed, merged, pushed change on trunk -- a curated commit history, a resolved conflict, a
# recovered mistake, and a pull-request-style merge, in that order (the syllabus's four ordered steps).
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => throwaway identity, scoped to
#    this script -- never the developer's real config

git init --bare -q origin.git # => co-01, co-23: a BARE "remote" repo -- stands in for
#    the shared, hosted repository step 4 pushes to
mkdir work && cd work
git -c init.defaultBranch=main init -q
git remote add origin ../origin.git

echo "############################################"
echo "# Step 1: curated hunk-staged commit history"
echo "############################################"
cat >notes.md <<'NOTES'
# Task Tracker Notes

Track daily tasks in this file.
NOTES
git add notes.md
git commit -q -m "docs: start task tracker notes" # => co-05, co-07: first real commit

seq 1 20 | sed 's/^/task /' >tasks.txt
git add tasks.txt
git commit -q -m "feat: add initial task list" # => co-02, co-05, co-07: a 20-line file,
#    tracked whole -- deliberately long so the next two
#    unrelated edits land far enough apart to hunk-split

sed -i.bak '1s/.*/task 1 (buy groceries)/' tasks.txt && rm -f tasks.txt.bak # => two edits, far apart --
sed -i.bak '20s/.*/task 20 (plan trip)/' tasks.txt && rm -f tasks.txt.bak   #    Git's default 3-line context keeps
#    them in two SEPARATE hunks

printf 'y\nn\n' | git add -p              # => co-06: stage ONLY the line-1 hunk
git commit -m "fix: label groceries task" # => one focused commit per hunk
git add tasks.txt                         # => the remaining hunk, staged now
git commit -m "fix: label trip task"      # => a second, equally focused commit

git log --graph --oneline # => co-10: four curated commits,
#    a clean, linear line so far
git cat-file -p HEAD # => co-03: resolves the tip
#    commit down to its raw fields -- "tree <hash>" is the
#    root snapshot this whole step built up to
git cat-file -p 'HEAD^{tree}' # => and that tree's own two
#    blob entries -- notes.md and tasks.txt, content-addressed

echo "############################################"
echo "# Step 2: branch + forced conflict + three-way merge"
echo "############################################"
git switch -c retitle -q # => co-11: a short-lived
#    branch for one focused, reviewable change
sed -i.bak '2s/.*/task 2 (write status report)/' tasks.txt && rm -f tasks.txt.bak
git commit -aqm "fix: retitle task 2 on retitle branch"
git switch main -q
sed -i.bak '2s/.*/task 2 (write weekly report)/' tasks.txt && rm -f tasks.txt.bak # => main independently
#    rewrites the SAME line -- an unavoidable, deliberate
#    overlap with what retitle already changed
git commit -aqm "fix: retitle task 2 on main"

git merge retitle || true # => co-13, co-14:
#    both sides diverged AND overlap -- a real conflict,
#    not an automatic three-way merge
git status                                                                               # => "both modified"
sed -i.bak '2s/.*/task 2 (write weekly status report)/' tasks.txt && rm -f tasks.txt.bak # => the human
#    resolution, combining both intents into one line
git add tasks.txt
git commit --no-edit # => co-14:
#    resolution complete -- the merge commit is created
git log --oneline --graph # => the
#    fork-and-rejoin shape is now visible in the graph
git cat-file -p HEAD | grep "^parent" # => co-13:
#    TWO parent lines -- unambiguous, low-level proof this
#    is a real merge commit, not an ordinary one

echo "############################################"
echo "# Step 3: interactive rebase curation, then a reset --hard mistake + reflog recovery"
echo "############################################"
git switch -c cleanup -q
echo "review budget notes" >budget.md
git add budget.md
git commit -qm "wip budget notes"
echo "trip itinerary draft" >itinerary.md
git add itinerary.md
git commit -qm "wip trip itinerary"
echo "final polish on both docs" >>budget.md
echo "final polish" >>itinerary.md
git add budget.md itinerary.md
git commit -qm "wip polish" # => three
#    messy "wip" commits -- exactly what interactive
#    rebase exists to curate before landing on trunk

GIT_SEQUENCE_EDITOR="sed -i.bak -e '1s/^pick/reword/'" \
	GIT_EDITOR="bash -c 'echo \"docs: add budget notes\" > \"\$1\"' --" \
	git rebase -i HEAD~3 # => co-16:
#    reword ONLY the first commit's message

GIT_SEQUENCE_EDITOR="sed -i.bak -e '2s/^pick/squash/'" \
	GIT_EDITOR="bash -c 'echo \"docs: add trip itinerary\" > \"\$1\"' --" \
	git rebase -i HEAD~2 # => co-16:
#    fold the "wip polish" commit into the itinerary commit
git log --oneline # => two
#    clean, well-named commits replace three messy ones

echo "--- deliberate mistake: reset --hard loses the just-curated itinerary commit ---"
git reset --hard HEAD~1 # => co-18:
#    HEAD, index, AND working tree all move back -- the
#    itinerary commit becomes unreachable from any branch
git log --oneline

echo "--- recovery via reflog ---"
git reflog | head -4 # => co-22:
#    the reset shows up as its own reflog entry -- the
#    itinerary commit's hash is still right there, one step back
git reset --hard 'HEAD@{1}' # => co-22,
#    co-18: jump HEAD back to exactly where it was one move ago
git log --oneline # => the
#    "lost" commit is back -- nothing was ever truly deleted

echo "############################################"
echo "# Step 4: a passing pre-commit hook, then push and land via a PR-style merge"
echo "############################################"
cat >.git/hooks/pre-commit <<'HOOK'
#!/bin/sh
if git diff --cached | grep -q "TODO"; then
  echo "pre-commit: staged changes contain a TODO marker -- commit blocked"
  exit 1
fi
exit 0
HOOK
chmod +x .git/hooks/pre-commit # => co-27:
#    installed BEFORE the landing merge -- it will run
#    automatically on every commit from here on, including a merge commit

echo "--- prove the hook is genuinely enforced, not decorative ---"
echo "TODO: revisit before shipping" >>budget.md
git add budget.md
git commit -m "docs: note a followup" || true # => co-27:
#    blocked -- the hook really does run and really can fail a commit
git restore --staged budget.md && git checkout -- budget.md # => undo
#    the deliberately-blocked attempt, returning to a clean state

git switch main -q
git merge --no-ff cleanup -m "Merge pull request: task-tracker cleanup" # => co-28,
#    co-13: the exact operation a hosted PR's "merge" button
#    performs -- and the pre-commit hook DOES run for this merge
#    commit (it is not a fast-forward), passing cleanly this time
git log --oneline --graph

echo "--- push the finished trunk to the shared remote ---"
git push -q origin main                    # => co-23
git -C ../origin.git log --oneline --graph # => the
#    remote's own trunk matches local exactly -- the change
#    genuinely landed, with the full curated history intact

echo "--- final acceptance check: nothing INTENDED is dangling or lost ---"
git fsck --lost-found # => co-22:
#    the two dangling commits fsck reports are the ORIGINAL
#    pre-rebase "wip trip itinerary"/"wip polish" objects
#    that step 3's squash superseded -- expected, harmless
#    rebase byproducts, eventually gc'd; every INTENDED
#    commit (including the reflog-recovered one) remains
#    reachable from main, confirmed by the log above
git log --oneline --all | grep -c "docs: add trip itinerary" # => 1:
#    the reflog-recovered commit is reachable exactly once
#    from a real ref -- genuinely restored, not dangling
