# Developing AI Agents — Tool Usage Documentation

Agents should document which tools they use and why, helping users understand capabilities and maintainers understand dependencies.

## Tool Documentation Pattern

Add "Tools Usage" section (optional but recommended) listing each tool with its purpose:

```markdown
## Tools Usage

- **Read**: Read files to validate/create/fix
- **Glob**: Find files by pattern in directories
- **Grep**: Extract content patterns (code blocks, commands, etc.)
- **Write**: Create/update files and reports
- **Bash**: Generate UUIDs, timestamps, file operations
- **Edit**: Apply fixes to existing files
- **WebFetch**: Access official documentation URLs
- **WebSearch**: Find authoritative sources, verify claims
```

## When to Document Tools

**Recommended for**:

- Agents with 4+ tools (helps users understand capabilities)
- Agents where tool selection isn't obvious
- Agents with unusual tool combinations
- Reference documentation for complex agents

**Optional for**:

- Simple agents with 2-3 obvious tools
- Agents following standard patterns

## Tool Documentation Examples

**Checker Agents** (Read, Glob, Grep, Write, Bash, WebFetch, WebSearch):

```markdown
## Tools Usage

- **Read**: Read documentation files to validate
- **Glob**: Find markdown files in directories
- **Grep**: Extract code blocks, commands, version numbers
- **Write**: Generate audit reports to `local-tmp/<agent-family>/`
- **Bash**: Generate UUIDs, timestamps for reports
- **WebFetch**: Access official documentation URLs
- **WebSearch**: Find versions, verify tools, fallback for 403s
```

**Fixer Agents** (Read, Edit, Bash, Write):

```markdown
## Tools Usage

- **Read**: Read audit reports and files to fix
- **Edit**: Apply fixes to governed source or vendored paths; never generated mirrors
- **Bash**: Run shell commands, bulk sed substitutions across many files, timestamp/UUID generation
- **Write**: Generate fix reports to `local-tmp/<agent-family>/`
```

**Maker Agents** (Read, Write, Glob, Grep, Bash):

```markdown
## Tools Usage

- **Read**: Read existing files for context
- **Write**: Create documentation and canonical agent or skill sources
- **Glob**: Find related files for cross-references
- **Grep**: Extract patterns for consistency
- **Bash**: Run shell commands, bulk text substitutions, directory creation
```

## Placement

Add "Tools Usage" section:

- After "Core Responsibility" or main description
- Before detailed workflow sections
- Near top for quick reference
