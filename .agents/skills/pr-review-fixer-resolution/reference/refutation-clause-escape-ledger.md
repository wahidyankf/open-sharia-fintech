# The Refutation-Clause Escape Ledger

Each entry is a hole found in the refutation-clause rule by a PR review, and what closed it. It is
kept apart from [the invariants](./refutation-clause-invariants.md) because it grows and they do
not: a new escape appends here without touching the reasoning it exists to test.

1. A verb allowlist accepted `git --output=`, which writes. Closed by matching whole shapes **and**
   forbidding a placeholder value beginning with `-` — shape-matching alone leaves `--output=`
   arriving as the `<path>`, and the shape still matches.
2. `sed -n '1e cmd'` ran a shell under the very flag that was supposed to make it read-only.
3. A placeholder value beginning with `-` arrived as a flag. Closed by forbidding a leading dash.
4. A directory pathspec passed the tracked-path check while `grep -r` walked gitignored files.
5. A tracked symlink passed the same check and resolved outside the repository.
6. `<ref>` was free, so `git show HEAD~1:<path>` read a secret the working tree no longer held.
7. `<M>` was never constrained, and `<pattern>` was never quoted.
8. A batched `cat <path>...` passed a check written in the singular: one tracked path produced one
   line of output, and an untracked path beside it contributed none. Closed by one check per path.
9. `git log --oneline` printed commit subjects from a path's entire history, which a check on that
   path never examined. Closed by removing the shape.
10. `<pattern>` admitted backreferences, which `grep` matches by backtracking: a six-group pattern
    took 44 seconds against a 12-byte file, growing fourfold per byte added.
11. A clause's own output carried attacker-authored file content back into the fixer's context,
    where nothing classified it as untrusted.

Entries 1-7 were each closed by naming the thing just abused. Entry 8 onward were closed by an
invariant that already covered them, which is the argument for keeping the invariants short.
