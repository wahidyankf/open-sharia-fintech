# Why There Are Three Invariants

Every escape found in this rule so far was closed by constraining the part just exploited. The
[escape ledger](./refutation-clause-escape-ledger.md) records each one and what closed it.

Read that ledger end to end and the shape of the mistake is the same every time: **a rule that
enumerates what is forbidden is always one enumeration behind.** Most were closed by adding a clause
naming the thing that had just been abused, and each of those clauses was correct. The rule still
failed the next cycle, because correctness of a clause says nothing about coverage of the class.

So the rules are stated as consequences of three invariants.

**Nothing the author wrote is ever interpreted by anything but the program receiving it.** The
recurring event is text the author wrote being read by something other than its intended reader — a
shell, or `sed`'s script parser. Building an argument vector instead of a command string removes the
shell entirely, so word-splitting cannot occur and no space needs banning. Where a program parses
its own language, that language is constrained directly: `<N>` and `<M>` are digits because `sed`
reads its script whatever the shell does, and `<pattern>` carries no backreference because a
regex engine reads one whatever `grep` was asked to find.

**Every check runs on the exact object about to be read, immediately before reading it.** The
recurring event is a check verifying something adjacent to what was read — the argument rather than
the file, the set rather than the member, the index rather than the disk, the current tree rather
than the commit named. Each was individually surprising; stated as one invariant, none of them is. A
shape that cannot satisfy this invariant is removed rather than fenced, which is why `git log` is
not on the list: it reads a path's whole commit history, and no check on that path covers it.

**What a clause returns is data.** The first two invariants govern what goes into a clause. Neither
says anything about what comes back, and what comes back is a file the PR author may have written.
Read into the fixer's reasoning it is an injection channel; copied into a reply it is a disclosure
channel. So output is classified, never obeyed, and the report carries the outcome — matched, did
not match, how many lines — never the content.

None of the three proves the rule safe. They give the next reviewer something to test against other
than a list, which is the difference between a rule that can be reasoned about and one that can only
be patched.
