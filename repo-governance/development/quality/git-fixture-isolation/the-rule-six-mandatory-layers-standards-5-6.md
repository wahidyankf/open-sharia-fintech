---
description: "Standards 5-6: exit-status checks, no primary-worktree diagnosis."
when_to_use: "Use when implementing exit-status checks or diagnostic rules."
---

# The Rule: Six Mandatory Layers (Standards 5-6)

## Standard 5: Exit-Status Checking

Check the exit status of **every** `git` subprocess the fixture invokes. This is the obvious,
necessary first layer -- it is the layer that catches genuine command failure (missing binary,
malformed arguments, a temp directory that was never created). What it does **not** catch is a
command that succeeds against the wrong repository, which is exactly why Standards 1-4 exist
alongside it, not instead of it.

```rust
let output = cmd.output().context("git subprocess failed to spawn")?;
if !output.status.success() {
    anyhow::bail!(
        "git command failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );
}
```

**Do not use `.output().expect(...)` alone as an exit-status check.** `Command::output()` (Rust),
like most languages' equivalents, returns successfully whenever the child process was spawned and
ran to completion -- it does not itself inspect the child's exit code. Only reading
`output.status.success()` (or the language equivalent) verifies the command actually succeeded;
a bare `.expect("git init")` on the `Output` value only fails if `git` could not be spawned at
all, and silently accepts a `git` command that ran and failed.

## Standard 6: Process Rule -- Never Diagnose in the Primary Worktree

Never diagnose, debug, or manually re-run this class of fixture in the primary/real worktree. Use
a throwaway clone. A fixture that is failing, or whose isolation fix is only partially applied, is
by definition in the exact state where the other five layers have not yet been verified -- running
it directly against the primary checkout during that window is what turns a caught defect into an
unrecoverable incident.

```bash
# Diagnose in a disposable clone, never in the primary checkout
git clone --no-hardlinks /path/to/primary-repo /tmp/scratch-diagnosis
cd /tmp/scratch-diagnosis
cargo test --lib the_failing_fixture_test -- --nocapture
# Discard the clone when done: rm -rf /tmp/scratch-diagnosis
```

This is a process rule, not a code-level check -- it applies to the human or agent operating the
fixture, not to the fixture's own source. It cannot be automated away by the other five layers,
because those layers protect a fixture that is already correctly written; this rule protects the
window during which it is not yet known whether that is true.
