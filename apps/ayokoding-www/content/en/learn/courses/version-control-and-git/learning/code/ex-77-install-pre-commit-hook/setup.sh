#!/bin/bash
# ex-77-install-pre-commit-hook: a pre-commit hook can block a commit outright with a nonzero exit (co-27)
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
# pre-commit: block any commit whose staged diff introduces a TODO marker
if git diff --cached | grep -q "TODO"; then
  echo "pre-commit: staged changes contain a TODO marker -- commit blocked"
  exit 1
fi
exit 0
HOOK
chmod +x .git/hooks/pre-commit # => co-27: hooks live in .git/hooks/, are
#    plain executable scripts, and run automatically at
#    the lifecycle point their filename names -- no
#    plugin system, no config file, just an executable

echo "TODO: fix this later" >>notes.txt
git add notes.txt

git commit -m "add a todo" || true # => Git runs pre-commit BEFORE creating the
#    commit object -- the hook's grep finds "TODO", exits
#    1, and Git aborts the commit entirely

git log --oneline # => still only ONE commit -- the blocked
#    attempt never became history at all
