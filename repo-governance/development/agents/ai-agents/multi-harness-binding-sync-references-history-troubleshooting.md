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

**Script**: `scripts/sync-agent-configs.sh` (or `.js`)

**Commands**:

- `npm run generate:bindings` - Full sync (agents + skills)
- `npm run sync:agents` - Agents only
- `npm run sync:skills` - agent skills only (no-op — secondary harness reads natively from `.claude/skills/`)
- `npm run validate:sync` - Verify semantic equivalence

**Conversion Logic**:

- **Agents**: Primary format → secondary format (tool arrays → permission object, model mapping; boolean flags output is deprecated/legacy)
- **Agent skills**: No mirror — secondary harness reads `.claude/skills/` natively (no copy or conversion)
- **Validation**: Confirms both directories are semantically equivalent

## Documentation References

- **[CLAUDE.md](../../../../CLAUDE.md)** (PRIMARY) - primary platform binding configuration
- **[AGENTS.md](../../../../AGENTS.md)** (SECONDARY) - secondary platform configuration with auto-generated warning
- **[Primary binding agent catalog](../../../../.claude/agents/README.md)** (PRIMARY) - Agent catalog
- **[Secondary binding agent catalog](../../../../.claude/agents/README.md)** (SECONDARY) - `.opencode/agents/` contains auto-synced agent files; `.claude/agents/README.md` is the authoritative catalog for both bindings
- **[Primary binding skills catalog](../../../../.claude/skills/README.md)** (PRIMARY) - agent skills catalog
- **[Secondary binding skills catalog](../../../../.claude/skills/README.md)** (SECONDARY) - secondary skills catalog with warning

## Migration History

- **2026-01-12**: Initial secondary platform binding migration
- **2026-01-16**: Dual-binding setup established, `.claude/` created as source of truth

## Best Practices

1. **Always edit `.claude/` first** - Never edit `.opencode/` directly (changes will be overwritten)
2. **Run sync after changes** - Ensure `.opencode/` stays synchronized
3. **Test both platforms** - Verify agents work in all supported platforms after major changes
4. **Document sync status** - Keep README files updated in both directories
5. **Security policy** - Only use skills from trusted sources (all platforms)

## Troubleshooting

**Problem**: `.opencode/` agents out of sync with `.claude/`
**Solution**: Run `npm run generate:bindings` to regenerate

**Problem**: Conversion errors during sync
**Solution**: Check agent frontmatter format in `.claude/agents/`, fix YAML syntax, re-sync

**Problem**: agent skills missing in one directory
**Solution**: Verify skills exist in `.claude/skills/`, run `npm run sync:skills`

---

**Appendix Added**: 2026-01-16
**See Also**: [Repository Governance Architecture](../../../repository-governance-architecture.md)
