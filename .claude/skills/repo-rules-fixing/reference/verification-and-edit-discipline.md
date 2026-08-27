# Verification and Edit Discipline

## File Operations

Normal file-editing tools are pre-authorized for binding paths (see `CLAUDE.md` §Working with
`.claude/` and `.opencode/`), but authorization does not override path ownership. Use `Write`/`Edit`
only on paths that `repo-config.yml` declares `source` or `vendored`; never hand-edit a generated
mirror or generated delimited region. After changing `.claude/` sources, run
`npm run generate:bindings` and keep every changed mirror in the same commit.

## Post-Fix Verification (MANDATORY)

`sed -i` exits `0` even when its pattern matched nothing in the target file — a silent no-op that
has produced garbled headings in previous iterations of this agent's fixes. Every fix MUST be
grepped for after applying, never trusted from exit code alone:

```bash
sed -i 's/old-pattern/new-pattern/' path/to/file.md
grep -q "new-pattern" path/to/file.md || echo "WARNING: edit did not match — fix NOT applied to path/to/file.md"
```

If verification fails, log the fix as **FAILED (not applied)** and continue to the next finding —
never assume success from a clean sed exit code.

## Python for Multi-Line Agent File Edits (MANDATORY)

`sed` is line-oriented and silently fails on patterns spanning multiple lines (a heading plus its
following paragraph, a whole section). For any multi-line replacement, use Python instead:

```python
import re, pathlib
p = pathlib.Path("path/to/file.md")
text = p.read_text()
new_text = re.sub(r"old multi-line pattern", "new content", text, count=1)
assert new_text != text, "pattern did not match — fix NOT applied"
p.write_text(new_text)
```

Then run the same post-fix `grep` verification as above.

## Confidence Assessment (Re-validation)

Before applying any finding from the audit report: (1) re-read the current state of the target
file — the issue may already be resolved since the report was generated; (2) assess fix
confidence — **HIGH** (issue confirmed, fix is mechanical and unambiguous), **MEDIUM** (issue
likely but target/scope ambiguous — skip, document), **FALSE_POSITIVE** (issue no longer exists,
or was misidentified). Fix HIGH only; see the priority-matrix in `repo-assessing-criticality-confidence`
for how confidence combines with criticality to set fix order.

## Capture Changed Files for Scoped Re-validation

After each batch of fixes: `git diff --name-only HEAD` to list every touched file, and record it
in the fix report so a follow-up `repo-rules-checker` run can scope its re-validation to exactly
what changed rather than re-scanning the whole repo.

## FALSE_POSITIVE Carry-Forward

Persist every skipped FALSE_POSITIVE with a stable key so re-runs don't re-flag it:

```
[category] | [file] | [brief-description]
```

Append to `generated-reports/.known-false-positives.md` under a dated `## Accepted FALSE_POSITIVE
Findings` entry.

## Mode Parameter Handling

See `repo-applying-maker-checker-fixer` skill: **lax** fixes CRITICAL only; **normal** fixes
CRITICAL+HIGH; **strict** (default) fixes CRITICAL+HIGH+MEDIUM; **ocd** fixes all levels.
