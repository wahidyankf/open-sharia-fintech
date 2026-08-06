# Harness binding catalog drift

One-line summary: triage the 2026-07-20 harness-compat audit findings and reconcile the
platform-binding catalog with upstream harness conventions that have since moved.

> De-promoted 2026-07-21 from a full backlog plan (full detail preserved in git history).

## Problem / context

A `repo-harness-compatibility-checker` run at ose-public commit `6aea08047` found several catalog rows
describing upstream harness conventions that have since drifted. The catalog decides which binding
files this repo emits and which instruction surfaces each vendor reads, so a stale row is not
cosmetic — it can mean shipping a binding file a harness no longer reads or omitting one it now
expects. Phase 0 of the same run was clean (**all five deterministic parity invariants PASS** across
`.claude/`, `.opencode/`, `.amazonq/`); this is entirely about external drift. The highest-rated
findings: **Windsurf → Devin Desktop** (HIGH/HIGH — full vendor+product rebrand as of 2026-06-02 with
an already-passed EOL date), **OpenAI Codex CLI** custom-agent declaration (HIGH/MEDIUM — reportedly
moved from `[agents.<name>]` sub-tables to standalone `.codex/agents/*.toml`, while the repo's live
`.codex/config.toml` still uses the old form), **GitHub Copilot** MCP path (MEDIUM/HIGH) and skills
surface (MEDIUM/MEDIUM — reportedly now reads `.claude/skills/`), and **OpenCode** skills prose (LOW,
incomplete not wrong). Note the audit's own summary contradicts its report body in at least one place:
the summary flagged JetBrains Junie as HIGH, but the report records it `FALSE_POSITIVE`.

## Why now

Harness conventions move continuously and each stale row is a latent mis-emit. The audit is already
done and copied to `findings.md` in the folder (the `generated-reports/` original is gitignored and
vanishes on clean), so the evidence exists now but decays as vendors keep changing.

## Prior art / precedents

- **AGENTS.md standard** — the open cross-vendor instruction format the binding catalog resolves each
  harness against. [agents.md](https://agents.md/)
- **Multi-Harness Binding convention** — defines the two-tier binding model and no-shadowing rule the
  catalog implements. [multi-harness-binding](../../../repo-governance/conventions/structure/multi-harness-binding.md)
- **Platform Bindings reference** — the catalog document itself, the primary artifact this triage
  reconciles. [platform-bindings](../../../docs/reference/platform-bindings.md)
- **repo-harness-compatibility-checker** — the agent whose 2026-07-20 run produced the drift findings
  being triaged. [checker agent](../../../.claude/agents/repo-harness-compatibility-checker.md)

## Proposed direction (sketch)

- Triage each Phase 1 finding, deciding per row: update the catalog, update the emitted binding files,
  or record the row as deliberately unchanged with a dated reason.
- Delegate re-verification to `web-researcher` rather than trusting the report's citations — several
  findings are MEDIUM confidence precisely because the checker could not fully settle them.
- Read the report body, not its summary (the summary is known to disagree with it).
- Rows confirmed correct-as-written gain a dated "re-verified" note so the next audit does not
  re-litigate them.

## Rough scope & non-goals

In scope: triage and reconcile the Phase 1 findings; touches `docs/reference/platform-bindings.md` and
possibly the emitters.

Out of scope (for now): Amazon Q → Kiro CLI succession (logged no-drift by request, already in the
catalog); any Phase 0 parity work (already green).

## Risks & open questions

- MEDIUM-confidence findings may not survive independent re-verification — acting on the report
  directly risks chasing a non-issue (the Junie FALSE_POSITIVE is the cautionary example).
- The Codex `config.toml` carries an Nx-tooling provenance caveat — establish who owns that file
  before editing it. (open)
- Any change to emitted output must keep the three-repo binding parity invariants green — re-run the
  checker's Phase 0 before merging.

## What success looks like + promotion signal

Success: every Phase 1 finding is either reconciled into the catalog/emitters or recorded as
deliberately unchanged with a dated reason, and Phase 0 parity stays green. Ready to re-promote to a
`backlog/` plan once the highest-rated rows (Windsurf/Devin, Codex CLI, Copilot) are independently
re-verified so the actual set of required changes is known.
