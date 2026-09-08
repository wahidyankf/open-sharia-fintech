---
description: "Standards 3-4: identity/config hygiene, escape guard."
when_to_use: "Use when implementing identity blanking or an escape guard."
---

# The Rule: Six Mandatory Layers (Standards 3-4)

## Standard 3: Identity/Config Hygiene (`GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM`)

Set `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null` so the developer's real
identity/config never bleeds **into** the fixture, and the fixture's own throwaway identity never
writes **out** to the developer's real global config.

```rust
cmd.env("GIT_CONFIG_GLOBAL", "/dev/null")
   .env("GIT_CONFIG_SYSTEM", "/dev/null");
```

**Why**: Standard 2 confines _local_-scoped config writes to the fixture's own repository. This
layer covers the two directions Standard 2 does not: (a) a fixture that reads config before it has
set its own values could otherwise pick up the developer's real name/email from `~/.gitconfig`,
silently contaminating throwaway commits with real identity; (b) a fixture (or a future refactor
of one) that issues a `--global` write -- intentionally or by a typo dropping `--local` -- would
otherwise land in the developer's actual `~/.gitconfig`, corrupting it for every other repository
on the machine. Blanking both scopes removes both directions at once.

## Standard 4: Pre-Write Escape Guard

Before **any** write command, assert that `git rev-parse --show-toplevel` resolves to the intended
temp directory (canonicalized); panic/fail-loud if it resolves anywhere else. This catches every
escape mechanism -- CWD race, `TMPDIR`-under-repo, a missed `.env()` call in a future refactor, or
any discovery path not enumerated above -- at the source, before a single write happens, rather
than after the real repository has already been corrupted.

```rust
fn assert_repo_root_is(expected: &Path) -> Result<()> {
    let output = Command::new("git")
        .args(["rev-parse", "--show-toplevel"])
        .current_dir(expected)
        .env("GIT_CEILING_DIRECTORIES", expected)
        .env("GIT_DIR", expected.join(".git"))
        // GIT_WORK_TREE is deliberately NOT set here: it would make
        // `--show-toplevel` merely echo the variable, defeating the guard.
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null")
        .output()
        .context("escape guard: failed to invoke git rev-parse")?;

    let resolved = PathBuf::from(String::from_utf8(output.stdout)?.trim());
    let resolved_canonical = resolved
        .canonicalize()
        .context("escape guard: failed to canonicalize resolved repo root")?;
    let expected_canonical = expected
        .canonicalize()
        .context("escape guard: failed to canonicalize expected repo root")?;

    if resolved_canonical != expected_canonical {
        panic!(
            "git fixture escape guard tripped: expected repo root {expected_canonical:?}, \
             git resolved {resolved_canonical:?} -- refusing to run a write command \
             against the wrong repository"
        );
    }
    Ok(())
}
```

Call this guard immediately before every write subcommand (`commit`, `config`, `worktree add`,
`branch`, `checkout -b`, `reset --hard`, etc.) in the fixture's sequence -- not just once at setup.
A fixture that only checks once, before its first write, still leaves every subsequent write
unguarded against a race that develops mid-sequence.
