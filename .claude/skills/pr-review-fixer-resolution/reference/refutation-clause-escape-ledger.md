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
    took 44 seconds against a 12-byte file. Closed by banning them, which closed too little — see 12.
11. A clause's own output carried attacker-authored file content back into the fixer's context,
    where nothing classified it as untrusted.
12. Nested bounded intervals — `\(a\{1,n\}\)\{1,n\}b`, ordinary BRE carrying no backreference and
    needing no `-P` — reached 19 seconds against a 500-byte file, growing roughly cubically. It
    walked straight through entry 10's ban. Closed by removing `grep`: `rg` matches with finite
    automata, so the guarantee comes from the engine rather than from a list.
13. `git show HEAD:<path>` read the committed tree while rule 3 checked the index and the disk. A
    secret redacted in the working tree was still returned from `HEAD`. Closed by removing the
    shape — `HEAD` is not the current state once the fixer has staged an edit, which is exactly
    when clauses run.

Entries 1-7 were each closed by naming the thing just abused. Entry 8 onward were closed by an
invariant that already covered them, or by deleting a component that could not satisfy one. That is
the argument for keeping the invariants short and the allowlist shorter.
