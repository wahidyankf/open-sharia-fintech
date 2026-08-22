# Why the Path Rule Is That Shape

[Rule 3](./refutation-clause-execution.md) admits exactly one tracked regular file per path. Each of
its three conditions closes an escape that was live, and all three are the same mistake — **git
tracks an entry name; it does not promise what reading that name returns.**

```bash
git ls-files -s -- <path>    # exactly one line, mode 100644 or 100755, path field == <path>
```

- **Zero lines** means untracked. This repo keeps real secrets in gitignored `.env*` files by
  convention, and an untracked file is not part of the change under review either way.
- **A path field that differs from `<path>`** means `<path>` was a directory: the check passes on
  any directory holding one tracked file, while a read that walks it reaches every ignored file
  underneath. Verified — `git ls-files --error-unmatch <dir>` exits 0 while a recursive grep on
  the same argument prints a gitignored file's contents.
- **Mode `120000`** means a symlink. Git stores the link, not the target, so a symlink committed
  by the PR under review passes every in-repo test and still resolves to anywhere the process can
  read. Verified — `cat` on a tracked symlink printed a file outside the repository.

`cat`, `sed`, `grep`, and `rg` all follow symlinks and none of them consult git. The two `git`
shapes are exempt from that specific failure because they read the blob: on a symlink,
`git show <ref>:<path>` prints the target's path text, never the target's contents.
