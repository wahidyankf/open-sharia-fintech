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
- **A pinned `HEAD`** is the fourth condition, on the shape rather than the path: the check
  reads the current tree, so the read must too. Left free, `<ref>` lets a clause pass the check
  against a file that is safe today and print that same file as it existed at any earlier commit —
  a secret committed and later scrubbed is still readable at `HEAD~1`. Verified —
  `git show HEAD~1:config.yml` printed a value the working tree no longer contains.

- **Mode `120000`** means a symlink. Git stores the link, not the target, so a symlink committed
  by the PR under review passes every in-repo test and still resolves to anywhere the process can
  read. Verified — `cat` on a tracked symlink printed a file outside the repository.

- **One check per path.** `cat` and `grep` accept `<path>...`, and a batched check cannot reject
  what it silently omits. Verified — `git ls-files -s -- tracked.txt ignored.txt` printed one line,
  mode `100644`, exit 0, satisfying the singular check word for word, while
  `cat tracked.txt ignored.txt` printed both files.
- **`test ! -L` then `test -f`.** `git ls-files` reports the **index**, not the disk. An unstaged
  type change leaves a symlink where the index still records a regular file. Verified — after
  swapping a tracked file for a symlink and staging nothing, `git ls-files -s` still printed
  `100644` while `cat` printed a file from outside the repository. Run it immediately before the
  read: it is standing in for the read.

`cat`, `sed`, `grep`, and `rg` all follow symlinks and none of them consult git. The `git show`
shape is exempt from that specific failure because it reads the blob: on a symlink,
`git show HEAD:<path>` prints the target's path text, never the target's contents.
