# Let the agent converter preserve frontmatter fields it does not own

One-line summary: the Claude→OpenCode agent converter emits a fixed field set, so any OpenCode-only
frontmatter key on a mirrored agent is silently dropped the first time that agent gains a `.claude/`
source.

> Surfaced 2026-08-17 during `optimize-gov` PR review.

## Problem / context

`ose-private` carried `.opencode/agents/ci-monitor-subagent.md` as a hand-maintained file with no
`.claude/` counterpart. It declared `mode: subagent`, which is how OpenCode distinguishes a subagent
from an ordinary agent. Two archived plans (`2026-05-25__multi-harness-compatibility`,
`2026-06-07__plan-domain-parity`) record it as hand-maintained and explicitly to be preserved.

Authoring a `.claude/` counterpart to close the agent-inventory gap forced the mirror to be
regenerated, because `validate_agent_equivalence` requires every `.claude/` source to have a
YAML-equivalent `.opencode/` file. Measured before/after on the regenerated mirror:

```diff
-mode: subagent
+model: zai-coding-plan/glm-5.2
+permission:
+  bash: allow
+  read: allow
+color: warning
```

The instruction body survived unchanged. Only the field that made it a subagent was lost.

The converter (`apps/rhino-cli/src/application/agents/converter.rs`) writes description, model,
permission, color, steps, and skills, in that order, with no passthrough for unrecognized keys. So
this is not specific to `mode` or to this agent: any OpenCode-side key a harness may add in future
is dropped the moment the agent acquires a Claude source, and no gate reports it — the equivalence
check compares against what the converter _would_ emit, so a regenerated file always agrees with
itself.

## Why now

The loss has already landed once, in `ose-private` PR #50, as a deliberate and recorded trade: the
agent inventories now match at 56 each and `mode: subagent` is gone. That is a real behavioural
change to live `/monitor-ci` tooling, taken because the alternative was a permanent standing finding
on Phase 0 Invariant 4. It should not stay a silent trade.

Against urgency: only one agent is affected, and OpenCode's behaviour without `mode` may be
acceptable in practice — nobody has observed a `/monitor-ci` failure.

## Prior art / precedents

- **`2026-06-07__plan-domain-parity`** — established the hand-maintained-outside-the-managed-block
  pattern for exactly this file, in `.codex/config.toml`.
- **`.amazonq` emitter** (`bindings.rs`) — already models the opposite discipline: it tracks which
  definitions it manages and removes only stale ones it owns.
- **Prettier / `.prettierignore` precedent in this repo** — generated files are excluded from
  formatters that would otherwise clobber byte-equality; the same "do not touch what you do not own"
  instinct.

## Proposed direction (sketch)

1. Give the converter a passthrough: carry unrecognized source-side keys into the emitted mirror
   rather than dropping them.
2. Or, model an explicit exemption list of harness-native files the generator must not rewrite.
3. Either way, make the equivalence validator able to tell "matches the converter" from "matches the
   converter _and_ retains its harness-native keys".

## Rough scope & non-goals

In scope: the converter, the sync validator's equivalence check, and restoring `mode: subagent` on
the one affected agent.

**Out of scope (for now)**: broader Claude↔OpenCode schema translation; the Amazon Q and Cursor
tiers, which have no observed native-only keys.

## Risks & open questions

- Does OpenCode actually degrade without `mode: subagent`, or does it infer subagent status from
  directory placement? Unverified — this determines whether the landed change is harmless or a real
  regression.
- `apps/rhino-cli/**` is the parity boundary across ose-public and ose-private, so a converter change
  is a coordinated multi-repo change with a manifest regen.
- A blanket passthrough could let genuinely stale keys survive regeneration, which is the behaviour
  the generator exists to prevent.

## What success looks like + promotion signal

`mode: subagent` is back on the mirrored agent and survives a `generate:bindings` run, or the field
is confirmed unnecessary and that finding is written down. Promotion signal: someone confirms
OpenCode's actual behaviour for an agent lacking `mode` — that answer decides whether this is a bug
fix or a documentation note.
