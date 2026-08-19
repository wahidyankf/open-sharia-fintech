# Technical Documentation — Harness Mirror and Test-Isolation Defects

## WS-H1 — the phantom `README` agent

### Evidence

`opencode agent list`, run at the worktree root with OpenCode 1.18.7, returns 7 built-in agents and
94 repository agents. `.opencode/agents/` holds 94 files: 93 generated agent mirrors plus
`README.md`, the annotated index the binding emitter writes there. OpenCode globs the directory and
treats each `.md` as a definition, so the index becomes an agent named `README`.

### Why it exists

The emitter writes the index into the payload directory because that is where the
[README completeness](../../../repo-governance/conventions/structure/governance-readme-completeness.md)
gate expects a directory's index to live. Two rules meet: "every directory carries an annotated
index" and "this directory is globbed by a third-party tool". Nothing currently reconciles them.

### Fix design

The reconciliation must be explicit rather than a special case for one filename:

1. Declare, per harness in `repo-config.yml`, whether its agent directory is **globbed** by the
   vendor tool. Codex is not — it reads `.codex/agents/*.toml`, so a `.md` index there is inert.
2. For a globbed directory, the index moves one level up (`.opencode/README.md`) and links into the
   directory, or the directory's index requirement is discharged by the parent.
3. `harness bindings validate` gains a check: no tracked file inside a globbed agent directory may
   lack agent frontmatter.

Option 2's choice between the two shapes is a decision for execution, taken against whatever the
README-completeness validator will accept without weakening it.

## WS-H2 — smoke tests share one process working directory

### Evidence

`apps/rhino-cli/src/commands/harness_generate_bindings.rs` carries `run(...)` smoke tests that
resolve the git root from the process CWD. Adding two more made `harness_unknown_name_is_error` fail
under the default parallel runner and pass under `--test-threads=1`.

### Why it exists

`run(...)` takes no root argument; it discovers one. That is correct for the binary, whose CWD is
the user's shell, and wrong for a test, whose CWD is shared with every other test in the binary.

### Fix design

Give the command an explicit root parameter and have the binary's entry point pass the discovered
one. Tests then pass a fixture path. This is the same shape as
`rhino_cli::application::repo_config::load(&root)`, which every other call site already uses.

The two removed tests are restored as part of the fix — their absence is the visible cost of the
defect, so their return is the proof it is fixed.

## WS-H3 — 47 dangling anchors

### Evidence

Recorded during `update-harness-support` Phase 6: 47 dangling anchors across 22 files under
`.claude/skills/`. Several point at split-pattern parents that no longer carry the heading the anchor
names — the anchor survived a progressive-disclosure split that moved its target into a child file.

### Why it was invisible

`docs/links.rs` exempted skill files from link validation. The exemption is legitimate in intent —
skill bodies carry references the validator cannot resolve — but it was total, so a genuinely broken
anchor inside a skill was indistinguishable from an unresolvable one.

### Fix design

Repair, not re-exemption. For each of the 47, resolve the intended target and repoint the anchor;
where the target no longer exists in any form, remove the reference and say what replaced it. Then
consider narrowing the exemption so this class cannot hide again — a question this plan raises but
does not presume the answer to.

## Cross-repository obligation

WS-H1 and WS-H2 touch `apps/rhino-cli/**`, which is inside the parity boundary recorded in
`apps/rhino-cli/parity-manifest.sha256`. Changes must land in `ose-public` and `ose-private` as a
paired merge, with the manifest regenerated on both sides after staging. WS-H3 is `ose-public`
content and carries no parity obligation.
