---
title: "Directory Purposes — generated-reports/ and Progressive Writing Requirement"
description: What generated-reports/ is for under the intent test, and why checker agents must write progressively.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when deciding whether an artifact belongs in generated-reports/ or local-tmp/.
---

# Directory Purposes — generated-reports/ and Progressive Writing Requirement

## `generated-reports/`

**Use for**: artifacts a human asked for by name and will read themselves.

**Examples**:

- A report the user asked for in their own words — "write me a summary of X"
- A deliverable the user will open and read, rather than one an agent consumes

An artifact fails both tests if a human did not name it, or if it is a step toward the answer rather
than the answer. Checker audit reports, fixer reports, execution verification reports, and todo or
progress tracking are all agent-to-agent working state and belong in `local-tmp/<agent-family>/`,
not here — see [`local-tmp/`](./local-tmp-directory.md).

## Progressive Writing Requirement for Checker Agents

**CRITICAL BEHAVIOURAL REQUIREMENT**: All \*-checker agents MUST write their validation reports PROGRESSIVELY (continuously updating files during execution), NOT buffering findings in memory to write once at the end.

**Why This is Critical:**

Progressive writing ensures reports survive context compaction:

- During long audits, conversation context may be compacted/summarized by the AI assistant
- If agent only writes report at the END, file contents may be lost during compaction
- If file is continuously updated THROUGHOUT execution, findings persist regardless of context compaction
- This is a **behavioural requirement**, not optional

**What Progressive Writing Means:**

**FAIL: Bad Pattern (Buffering - DO NOT DO THIS)**:

```markdown
findings = [] # Collect in memory
for item in items:
result = validate(item)
findings.append(result) # Buffer in memory

# At the very end...

write_report(findings) # Write once after all validation complete
```

**PASS: Good Pattern (Progressive - MUST DO THIS)**:

```markdown
file.write("# Audit Report\n\n") # Create file immediately
file.write("**Status**: In Progress\n\n")

for item in items:
result = validate(item)
file.write(f"## {item}\n")
file.write(f"Result: {result}\n\n") # Write immediately
file.flush() # Ensure written to disk

file.write("**Status**: Complete\n") # Update final status
file.flush()
```

Continued in [Progressive Writing Requirement — Requirements and Implementation Pattern](./progressive-writing-requirements-and-implementation.md).
