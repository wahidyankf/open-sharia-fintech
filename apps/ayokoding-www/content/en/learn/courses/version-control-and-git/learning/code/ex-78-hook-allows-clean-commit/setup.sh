#!/bin/bash
# ex-78-hook-allows-clean-commit: the same hook exits 0 and lets a clean commit through normally (co-27)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >notes.txt
git add notes.txt
git commit -q -m "initial notes"
cat >.git/hooks/pre-commit <<'HOOK'
#!/bin/sh
if git diff --cached | grep -q "TODO"; then
  echo "pre-commit: staged changes contain a TODO marker -- commit blocked"
  exit 1
fi
exit 0
HOOK
chmod +x .git/hooks/pre-commit

echo "finished notes, no markers" >>notes.txt # => this staged diff contains no "TODO"
git add notes.txt

git commit -m "add finished notes" # => co-27: the hook's grep finds nothing,
#    exits 0, and Git proceeds to create the commit
#    exactly as if no hook were installed at all

git log --oneline # => TWO commits now -- the clean one
#    genuinely landed, unlike ex-77's blocked attempt
