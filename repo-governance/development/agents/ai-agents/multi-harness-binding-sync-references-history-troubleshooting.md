---
title: "Multi-Harness Binding Operation — Sync Automation, References, History, Practices, and Troubleshooting"
description: "Covers sync automation, documentation references, migration history, best practices, and troubleshooting for multi-harness binding operations."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when an agent or Skill change needs to propagate across the multi-harness bindings, or when troubleshooting a sync failure.
---

# Multi-Harness Binding Operation — Sync Automation, References, History, Practices, and Troubleshooting

## Sync Automation

**Generator**: `rhino-cli harness bindings generate` (Rust). No `scripts/sync-agent-configs.sh` /
`.js` exists in this repository.

**Commands**:

- `npm run generate:bindings` - Full sync, every generated-tier harness
- `npm run sync:agents` - Agents only
- `npm run sync:skills` - `.claude/skills/`-native harnesses only (no-op); does NOT touch the
  `.agents/skills/` real-file mirror
- `npm run validate:sync` - `.opencode/agents/` and `.agents/skills/`; does **not** cover
  `.codex/agents/`
- `npm run harness:bindings-validation` - every generated-tier binding including `.codex/`; this is
  what the pre-push gate runs

**Conversion Logic**:

- **Agents**: Primary format → secondary format (tool arrays → permission object, model mapping)
- **Agent skills**: one harness reads `.claude/skills/` natively; the other gets a real-file
  byte-copy mirror at `.agents/skills/`
- **Validation**: three mirror trees now, not two — `.opencode/agents/`, `.codex/agents/` (plus
  `.codex/config.toml`), and `.agents/skills/`. `harness:bindings-validation` checks all three;
  `validate:sync` checks only the first and third.

## Documentation References

- **[CLAUDE.md](../../../../CLAUDE.md)** - the coding agent's shim, `class: source` (hand-authored)
- **[AGENTS.md](../../../../AGENTS.md)** - vendor-neutral root file read by `.opencode/` and
  `.codex/`, `class: source` for both (hand-authored, no auto-generated warning)
- **[Agent catalog](../../../../.claude/agents/README.md)** - authoritative for every binding;
  `.opencode/agents/` and `.codex/agents/` carry no catalog of their own
- **[Agent skills catalog](../../../../.claude/skills/README.md)** - authoritative source catalog;
  **[secondary mirror](../../../../.agents/skills/README.md)** is Codex's generated real-file copy

## Migration History

- **2026-01-12**: Initial secondary platform binding migration
- **2026-01-16**: Dual-binding setup established, `.claude/` created as source of truth

## Best Practices

1. **Always edit `.claude/` first** - Never edit a `class: generated` file under `.opencode/` or
   `.codex/` directly (changes will be overwritten). Exception: a path an entry's `ownership:` list
   declares `vendored` — e.g. `.opencode/opencode.json`, `.codex/config.toml`'s undelimited
   region — is hand-maintained by design and MUST be edited directly.
2. **Run sync after changes** - Ensure every generated-tier binding stays synchronized
3. **Test every platform** - Verify agents work in all supported platforms after major changes
4. **Document sync status** - Keep canonical README indexes current, then regenerate every
   registry-declared mirror
5. **Security policy** - Only use skills from trusted sources (all platforms)

## Troubleshooting

**Problem**: `.opencode/` agents out of sync with `.claude/`
**Solution**: Run `npm run generate:bindings` to regenerate

**Problem**: Conversion errors during sync
**Solution**: Check agent frontmatter format in `.claude/agents/`, fix YAML syntax, re-sync

**Problem**: agent skills missing in one directory
**Solution**: Verify skills exist in `.claude/skills/`, then run `npm run generate:bindings` (not
`npm run sync:skills` — that command only touches the no-op secondary-harness path and never
writes the other secondary harness's `.agents/skills/` mirror)

---

**Appendix Added**: 2026-01-16
**See Also**: [Repository Governance Architecture](../../../repository-governance-architecture.md)
