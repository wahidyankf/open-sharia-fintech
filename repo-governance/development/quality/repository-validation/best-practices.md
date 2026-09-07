---
description: "Best practices for writing repository validation checks."
when_to_use: "Use when writing a new repository validation check."
---

# Best Practices

## Always Extract Frontmatter First

**Rule:** When checking frontmatter content, ALWAYS extract it first before searching.

```bash
# PASS: CORRECT
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' "$file" | grep "pattern"

# FAIL: WRONG
grep "pattern" "$file"
```

**Why:** Prevents false positives from markdown body content.

## Use Proper Regex Escaping

**Rule:** Escape regex metacharacters in field names and search patterns.

**Metacharacters:** `. * [ ] ^ $ \ + ? { } | ( )`

```bash
# If field name contains special chars, escape them
field_name="some.field.name"
escaped_field=$(echo "$field_name" | sed 's/\./\\./g')

# Then use in grep
awk '...' "$file" | grep "^${escaped_field}:"
```

## Verify File Existence Before Checking Content

**Rule:** Always verify file exists before attempting to read/validate content.

```bash
# PASS: CORRECT
if [ ! -f "$file" ]; then
  echo "ERROR: File not found: $file"
  exit 1
fi

# Then proceed with validation
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' "$file" | grep "#"
```

## Handle Edge Cases

**Rule:** Account for special cases and exceptions.

**Common edge cases:**

- **Files without frontmatter** - Not all markdown files have YAML frontmatter
- **Empty frontmatter** - Frontmatter exists but contains no fields
- **Malformed frontmatter** - Missing opening/closing `---` delimiters
- **Special directories** - `metadata/`, exempted from naming conventions
- **Special files** - `README.md`, `index.md` exempt from naming conventions

```bash
# Check if frontmatter exists
if ! grep -q "^---$" "$file"; then
  echo "WARNING: No frontmatter found in $file"
  # Decide: skip check or report missing frontmatter
fi
```

## Use Consistent Error Reporting

**Rule:** Report violations with consistent format including file path, line number, and context.

**Standard format:**

```
FILE: path/to/file.md
LINE: 42
ISSUE: [VIOLATION_TYPE] Description of the issue
CONTEXT: |
  actual line content here
EXPECTED: What should be present instead
```

**Example:**

```
FILE: .opencode/agents/docs-maker.md
LINE: 5
ISSUE: [FRONTMATTER_COMMENT] YAML comment found in agent frontmatter
CONTEXT: |
  tools: Read, Write # These are the tools
EXPECTED: Clean frontmatter without comments (no # symbols)
```
