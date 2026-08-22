# Why There Are Two Invariants

Seven escapes have been found in this rule, on seven different PR-review cycles. Each was closed by
constraining the part just exploited:

1. A verb allowlist accepted `git --output=`, which writes. Closed by matching whole shapes.
2. `sed -n '1e cmd'` ran a shell under the very flag that was supposed to make it read-only.
3. A placeholder value beginning with `-` arrived as a flag. Closed by forbidding a leading dash.
4. A directory pathspec passed the tracked-path check while `grep -r` walked gitignored files.
5. A tracked symlink passed the same check and resolved outside the repository.
6. `<ref>` was free, so `git show HEAD~1:<path>` read a secret the working tree no longer held.
7. `<M>` was never constrained, and `<pattern>` was never quoted.

Read the list end to end and the shape of the mistake is the same every time: **a rule that
enumerates what is forbidden is always one enumeration behind.** Six of the seven were closed by
adding a clause naming the thing that had just been abused, and each of those clauses was correct.
The rule still failed the next cycle, because correctness of a clause says nothing about coverage
of the class.

So the rules are now stated as consequences of two invariants.

**Nothing the author wrote is ever interpreted by anything but the program receiving it.** Escapes
1, 2, 3 and 7 are all the same event: text the author wrote was read by something other than its
intended reader — a shell, or `sed`'s script parser. Building an argument vector instead of a
command string removes the shell entirely, so word-splitting cannot occur and no space needs
banning. Where a program parses its own language, that language is constrained directly, which is
why `<N>` and `<M>` are digits: `sed` reads its script whatever the shell does or does not do.

**Every check runs on the exact object about to be read, immediately before reading it.** Escapes
4, 5, 6 and the batched-path case are all the same event: the check verified something adjacent to
what was read — the argument rather than the file, the set rather than the member, the index rather
than the disk, the current tree rather than the commit named. Each was individually surprising.
Stated as one invariant, none of them is.

Neither invariant proves the rule safe. They give the next reviewer something to test against
other than a list, which is the difference between a rule that can be reasoned about and a rule
that can only be patched.
