---
description: "Checks 1-3: frontmatter comments, missing fields, wrong field values."
when_to_use: "Use when implementing or debugging one of the first three standard checks."
---

# Standard Validation Checks (1-3)

## 1. Frontmatter Comment Detection

**Purpose:** Detect `#` symbols in YAML frontmatter (where they indicate comments, which are forbidden in certain contexts like agent frontmatter).

**Pattern:**

```bash
# Extract frontmatter and search for # symbols
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' "$file" | grep "#"

# If no output → No comments (VALID)
# If output → Comments found (INVALID)
```

**Why it works:** AWK extracts only the YAML block, grep finds any `#` in that isolated content.

**Common pitfall:** Searching entire file flags legitimate markdown headings.

## 2. Missing Frontmatter Field Check

**Purpose:** Verify required frontmatter fields exist (e.g., `name`, `description`, `tools`).

**Pattern:**

```bash
# Extract frontmatter and check for field
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' "$file" | \
  grep "^${field_name}:"

# If no output → Field missing (INVALID)
# If output → Field present (VALID)
```

**Key details:**

- Use `^${field_name}:` to match field at start of line (prevents false positives from values containing the field name)
- Escape field name if it contains regex metacharacters
- Consider case sensitivity (YAML is case-sensitive)

**Example:**

```bash
# Check if 'model' field exists
field_name="model"
awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' .opencode/agents/docs-maker.md | \
  grep "^model:"
```

## 3. Wrong Field Value Check

**Purpose:** Verify frontmatter field has expected value (e.g., `model: sonnet`, `color: blue`).

**Pattern:**

```bash
# Extract field value
actual_value=$(awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' "$file" | \
  grep "^${field_name}:" | cut -d: -f2- | tr -d ' ')

# Compare with expected
if [ "$actual_value" = "$expected_value" ]; then
  echo "VALID"
else
  echo "INVALID - wrong value: got '$actual_value', expected '$expected_value'"
fi
```

**Key details:**

- `cut -d: -f2-` extracts everything after first `:` (the value)
- `tr -d ' '` removes leading/trailing spaces
- Use exact string comparison (`=`) for field values
- Handle quoted values appropriately

**Example:**

```bash
# Check if model field is 'sonnet'
field_name="model"
expected_value="sonnet"
actual_value=$(awk 'BEGIN{p=0} /^---$/{if(p==0){p=1;next}else{exit}} p==1' .opencode/agents/docs-maker.md | \
  grep "^model:" | cut -d: -f2- | tr -d ' ')

if [ "$actual_value" = "$expected_value" ]; then
  echo "Model field is correct: $actual_value"
else
  echo "Model field mismatch: got '$actual_value', expected '$expected_value'"
fi
```
