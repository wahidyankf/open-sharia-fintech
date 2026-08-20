# 🪞 Harness Mirror and Test-Isolation Defects

## Context

Three defects surfaced while executing the `update-harness-support` plan (archived under
[`plans/done/`](../../done/README.md)), which reduced the supported harness set to Claude Code,
OpenCode, and Codex CLI and mechanized how the bindings stay in sync.

None was fixed inline. All three touch `apps/rhino-cli` or the `.claude/skills/` content tree, so the
[Code-Routing Downstream Rule](../../../repo-governance/development/quality/knowledge-capture/the-code-routing-downstream-rule.md)
makes a separate plan mandatory — each carries its own TDD cycle, companion Gherkin, and a
parity-manifest obligation across the sibling repositories.

What they share is a shape worth naming: **a tree was treated as uniform when it is not**. A mirror
directory holds one file that is not an agent; a test binary holds tests that are not independent; a
link checker exempted a tree by literal prefix rather than by what the tree is.

## Workstreams

| ID    | Workstream                                                        | Status    |
| ----- | ----------------------------------------------------------------- | --------- |
| WS-H1 | OpenCode loads `.opencode/agents/README.md` as an agent           | Specified |
| WS-H2 | `harness_generate_bindings` smoke tests share a process-wide CWD  | Specified |
| WS-H3 | 47 dangling anchors in `.claude/skills/`, invisible until Phase 6 | Specified |

### WS-H1 — the mirror's own README is loaded as an agent

`opencode agent list` run at the worktree root returns 7 built-in agents plus **94** repository
agents, and one of them is named `README`. OpenCode treats every `.md` file under
`.opencode/agents/` as an agent definition; the binding emitter writes an annotated index into that
same directory.

Nothing invokes the phantom agent, so no behaviour is currently wrong. The defect is that the
repository publishes a junk entry into every OpenCode user's agent picker, and that the emitter's
layout — index file inside the payload directory — is what causes it. The same shape would apply to
any future harness that globs a binding directory.

### WS-H2 — two smoke tests could not be added because the suite is not isolated

`apps/rhino-cli/src/commands/harness_generate_bindings.rs` carries `run(...)` smoke tests that
resolve the git root from the **process** working directory. Because every test in a binary shares
one process, they are only as isolated as the whole binary. Adding two more made
`harness_unknown_name_is_error` fail under parallel execution and pass in isolation.

The two new tests were removed rather than left as a flake source — the honest short-term call, but
it means the suite currently constrains what can be tested. The fix is to give each test an explicit
root rather than reading the ambient one.

### WS-H3 — 47 dangling anchors were hidden by a prefix-keyed exemption

`apps/rhino-cli/src/application/docs/links.rs` exempted skill files from link validation, keyed on
the literal string `.claude/skills/`. When Phase 6 created a byte-identical mirror at
`.agents/skills/`, the same bytes were reported as broken in one tree and fine in the other.

That inconsistency was fixed at root cause during Phase 6 (the exemption is now a property of skill
trees as a class). **The links themselves were not fixed.** 47 anchors across 22 skill files are
genuinely dangling in the `.claude/skills/` sources — several point at split-pattern parents that no
longer carry the heading. They were invisible for as long as the exemption existed.

## Scope

**Repositories**: `ose-public` and `ose-private` for WS-H1 and WS-H2 — both touch the `rhino-cli`
parity boundary and must land as a paired merge. WS-H3 is `ose-public` content only.

**Trees in scope**: `apps/rhino-cli/src/application/agents/`, `apps/rhino-cli/src/commands/`,
`apps/rhino-cli/tests/`, `specs/apps/rhino/behavior/rhino-cli/gherkin/`, and `.claude/skills/`.

**Out of scope**: changing which harnesses are supported; the `.agents/skills/` mirror layout, which
Codex reads as a skill root and which carries no equivalent defect; the vendored plugin skill
directories, which this repository cannot regenerate.

## Approach Summary

WS-H1 and WS-H2 are behaviour changes in `rhino-cli` and carry companion Gherkin per
[Feature Change Completeness](../../../repo-governance/development/quality/feature-change-completeness.md).
WS-H3 is content repair whose gate is the existing link validator with the exemption narrowed for
the duration of the fix — a repair with no test to write, but a measurable before/after count.

WS-H2 should land before any workstream that adds tests to the same binary, or the new tests inherit
the flake.

## Documents

- [brd.md](./brd.md) — why a phantom agent and a non-isolated suite are worth paying to fix.
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — the observed evidence and the fix design for each workstream.
- [delivery.md](./delivery.md) — the phase-by-phase execution checklist.
