---
description: "The PostToolUse hook that formats/lints markdown after Edit/Write, and its jq requirement."
when_to_use: "Use when the markdown auto-format hook is not firing."
---

# Coding Agent Hook Integration

## PostToolUse Hook

Automatically runs after Edit/Write/MultiEdit operations on markdown files.

**Location**: `.claude/hooks/format-lint-markdown.sh`

**Configuration**: `.claude/settings.json`

**Actions**:

1. Runs Prettier to format the file
2. Runs markdownlint-cli2 to fix violations

**Requirements**: `jq` must be installed for JSON parsing

**Install jq**:

```bash
# Linux
sudo apt-get install jq

# macOS
brew install jq
```
