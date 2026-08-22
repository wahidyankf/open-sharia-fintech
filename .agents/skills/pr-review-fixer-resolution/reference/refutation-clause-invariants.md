# Why There Are Three Invariants

The [escape ledger](./refutation-clause-escape-ledger.md) records every escape found in this rule
and what closed it. Read it end to end and the mistake is the same every time: **a rule that
enumerates what is forbidden is always one enumeration behind.** Each clause added was correct, and
the rule failed the next cycle anyway, because correctness of a clause says nothing about coverage
of the class.

So the rules are stated as consequences of three invariants.

**Nothing the author wrote is ever interpreted by anything but the program receiving it.** The
recurring event is text the author wrote being read by something other than its intended reader — a
shell, or `sed`'s script parser. Building an argument vector instead of a command string removes the
shell entirely, so word-splitting cannot occur and no space needs banning. Where a program parses
its own language, that language is constrained directly: `<N>` and `<M>` are digits because `sed`
reads its script whatever the shell does. The same sentence decides which search engine is on the
list: a rule cannot enumerate every construct a backtracking engine mishandles, so the only engine
allowed is one that bounds its own cost.

**Every check runs on the exact object about to be read, immediately before reading it.** The
recurring event is a check verifying something adjacent to what was read — the argument rather than
the file, the set rather than the member, the index rather than the disk, the current tree rather
than the commit named. Each was individually surprising; stated as one invariant, none of them is. A
shape that cannot satisfy this invariant is removed rather than fenced, which is why no `git` shape
is on the list. `git log` reads a path's whole commit history; `git show HEAD:` reads the committed
tree, which is not the working file once an edit is staged. A check on that file covers neither.

**What a clause returns is data.** The first two govern what goes in. What comes back is a file the
PR author may have written: read into the fixer's reasoning it is an injection channel, copied into
a reply a disclosure channel. So output is classified, never obeyed; the report carries the outcome — matched, did not
match, how many lines — never the content; and no shape returns more than the claim needs, which is
why the context flags are not on the list.

Unlike the first two, this invariant has no mechanical backstop. Invariant 1 is discharged by
building an argument vector, invariant 2 by two `test` calls, and a reviewer can check a transcript
for either. Invariant 3 is discharged by the same reader the untrusted text reaches, so narrowing
the shapes is what reduces the exposure.

None of the three proves the rule safe. They give the next reviewer something to test against other
than a list.
