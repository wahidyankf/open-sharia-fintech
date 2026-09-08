---
description: "Checks 4-5: broken link detection, file naming convention."
when_to_use: "Use when implementing or debugging the link or naming checks."
---

# Standard Validation Checks (4-5)

## 4. Broken Link Detection

**Purpose:** Verify markdown links point to existing files.

**Pattern:**

```bash
# Extract link target from markdown
link_target=$(echo "$link" | sed 's/.*(\(.*\))/\1/')

# Resolve relative path
resolved_path=$(dirname "$file")/"$link_target"

# Check if file exists
if [ -f "$resolved_path" ]; then
  echo "VALID"
else
  echo "INVALID - broken link: $link_target"
fi
```

**Key details:**

- Extract target from `[text](target)` format using sed
- Resolve relative paths from file's directory (not working directory)
- Use `-f` test for file existence (not `-e` which matches directories too)
- Handle absolute paths differently (start with `/`)
- Normalize paths (e.g., `./file.md` vs `file.md`)

**Example:**

```bash
# Validate link from repo-governance/conventions/formatting/linking.md
file="repo-governance/conventions/formatting/linking.md"
link="[Indentation](../../conventions/formatting/indentation.md)"

# Extract target
link_target=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
# Result: ./indentation.md

# Resolve path
resolved_path=$(dirname "$file")/"$link_target"
# Result: repo-governance/conventions/./indentation.md

# Check existence
if [ -f "$resolved_path" ]; then
  echo "Link valid: $link_target"
else
  echo "Broken link: $link_target (resolved to: $resolved_path)"
fi
```

## 5. File Naming Convention Check

**Purpose:** Verify files use lowercase kebab-case basenames with a standard extension (see [File Naming Convention](../../../conventions/structure/file-naming.md)).

**Pattern:**

```bash
# Extract basename without extension
basename=$(basename "$file" .md)

# Check: lowercase letters, digits, hyphens only (no underscores, no uppercase, no spaces)
if [[ "$basename" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "VALID"
else
  echo "INVALID - not kebab-case: $basename"
fi
```

**Key details:**

- Allowed characters in basename: `a-z`, `0-9`, `-`
- No underscores, no uppercase, no spaces, no leading/trailing hyphens
- Handle special cases: `README.md`, `docs/metadata/`, date-prefixed files (`YYYY-MM-DD-*`)
- Directory hierarchy encodes category — no prefix required on filenames; a leading `NN-` ordinal is
  permitted only per [Ordinal Filename Prefixes](../../../conventions/structure/ordinal-filename-prefixes.md)
