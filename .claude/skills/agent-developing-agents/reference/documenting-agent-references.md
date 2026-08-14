# Developing AI Agents — Documenting Agent References

All agents SHOULD include a "Reference Documentation" section near the end (before any appendices) with standardized subsections.

## Section Template

```markdown
## Reference Documentation

**Project Guidance**:

- [AGENTS.md](../../../CLAUDE.md) - Primary guidance for OpenCode
- [Agent-specific convention](path/to/convention.md) - Domain-specific standards

**Related Agents**:

- `maker-agent` - Creates content for this domain
- `checker-agent` - Validates content (upstream dependency)
- `fixer-agent` - Fixes issues found by checker
- `related-domain-agent` - Related functionality

**Related Conventions**:

- [Primary Convention](path/to/convention.md) - Main standards this agent implements
- [Secondary Convention](path/to/convention.md) - Additional relevant standards

**Skills**:

- `primary-skill` - Main Skill for domain knowledge
- `wow-assessing-criticality-confidence` - Criticality assessment (if applicable)
- `wow-generating-validation-reports` - Report generation (if applicable)
```

## Subsection Details

### Project Guidance

**Purpose**: Link to primary project instructions and domain conventions.

**Always Include**:

- AGENTS.md.\*primary guidance for all agents)

**Conditionally Include**:

- Domain-specific conventions (e.g., README Quality Convention for readme-agents)
- Framework-specific guidance (e.g., Next.js guide for ayokoding-web-agents)
- Special standards relevant to agent's scope

**Pattern**:

```markdown
**Project Guidance**:

- [AGENTS.md](../../../CLAUDE.md) - Primary guidance
- [Specific Convention](path/to/convention.md) - Domain standards
```

### Related Agents

**Purpose**: Help users understand agent workflow relationships.

**Include**:

- **Upstream agents**: Agents this agent depends on (e.g., checker for fixer)
- **Downstream agents**: Agents that depend on this one (e.g., fixer for checker)
- **Parallel agents**: Agents in same family/domain (e.g., other checkers)
- **Complementary agents**: Agents with related functionality

**Organize by Relationship**:

```markdown
**Related Agents**:

- `upstream-agent` - Description of relationship
- `downstream-agent` - Description of relationship
- `parallel-agent` - Description of functionality
```

**Examples by Agent Type**:

**Maker Agents**:

```markdown
- `checker-agent` - Validates content created by this maker
- `related-maker` - Creates content in related domain
```

**Checker Agents**:

```markdown
- `maker-agent` - Creates content this checker validates
- `fixer-agent` - Fixes issues found by this checker
- `related-checker` - Validates related aspects
```

**Fixer Agents**:

```markdown
- `checker-agent` - Generates audit reports this fixer processes
- `maker-agent` - Updates content after fixes applied
```

### Related Conventions

**Purpose**: Link to conventions the agent implements.

**Include**:

- Primary convention agent implements
- Secondary conventions relevant to agent's scope
- Development practices agent follows (e.g., AI Agents Convention)
- Standards agent enforces (for checkers)

**Pattern**:

```markdown
**Related Conventions**:

- [Primary Convention](path/to/convention.md) - Main standards
- [Secondary Convention](path/to/convention.md) - Additional standards
- [Development Practice](path/to/practice.md) - Implementation guidance
```

**Checkers Should List**:

- Conventions they validate against
- Quality standards they enforce

**Makers Should List**:

- Conventions they follow when creating content
- Formatting standards they apply

### Skills

**Purpose**: Skills the agent uses for domain knowledge and patterns.

**Include**:

- All Skills listed in agent's `skills:` frontmatter field
- Skills should be listed without path (just skill name)
- Brief description of what each Skill provides

**Pattern**:

```markdown
**Skills**:

- `domain-skill` - Domain-specific knowledge
- `wow-skill` - Cross-cutting pattern or workflow
- `agent-skill` - Agent development guidance
```

**Note**: Skills section duplicates frontmatter `skills:` field for documentation visibility.
