# Maker-Checker-Fixer — Tool Requirements

## Checkers

Checkers typically need:

- **Read**: Read files to validate
- **Glob**: Find files by pattern
- **Grep**: Extract content patterns (code blocks, commands, etc.)
- **Write**: Initialize and update report file
- **Bash**: Generate UUID, timestamp, file operations
- **WebFetch**: (Optional) Access official documentation
- **WebSearch**: (Optional) Find authoritative sources

**Bash Tool Critical**: Required for UUID generation and report initialization.

## Fixers

Fixers typically need:

- **Read**: Read audit reports and files to fix
- **Edit**: Apply fixes to docs/ files
- **Bash**: Apply fixes to .claude/ files (sed, awk, heredoc)
- **Write**: Generate fix reports
- **Glob/Grep**: Optional - for pattern matching and validation

**NO Web Tools**: Fixers intentionally lack WebFetch/WebSearch (trust checker's verification).
