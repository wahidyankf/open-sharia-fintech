# Tutorial Structure Template

All tutorials follow this seven-section structure.

## 1. Frontmatter (YAML)

```yaml
title: Tutorial Title (verb-noun format)
description: Brief description (1-2 sentences)
type: tutorial
coverage: beginner|intermediate|advanced|quick-start|initial-setup|cookbook|by-example
category: Category name
tags: [tag1, tag2, tag3]
prerequisites: [prerequisite1, prerequisite2]
created: YYYY-MM-DD
```

**Required fields**: title, description, type, coverage, category, created. **Optional fields**:
tags, prerequisites.

## 2. Introduction Section

**Purpose**: set expectations and motivate learning.

```markdown
## Introduction

Brief paragraph explaining:

- What you'll learn
- Why it's useful
- Expected outcome

**In this tutorial, you will learn:**

- Specific skill 1
- Specific skill 2
- Specific skill 3
```

## 3. Prerequisites Section

**Purpose**: ensure readers have required knowledge.

```markdown
## Prerequisites

Before starting, ensure you have:

- Prerequisite 1 with link to relevant tutorial/doc
- Prerequisite 2 with verification command if applicable
- Prerequisite 3 with version requirements
```

## 4. Tutorial Steps

**Purpose**: guide users through the learning process. Use H2 (`##`) for main steps in
verb-noun format, H3 (`###`) for substeps. Include code examples with syntax highlighting, show
expected outputs, and explain WHY things work, not just HOW.

```markdown
## Step 1: Action Verb + Specific Task

Brief explanation of what you'll do in this step.

### 1.1 Substep Name

Detailed instructions with code examples, command outputs, screenshots (if needed), and
explanatory text.

**Example:**
\`\`\`bash
command --flag value
\`\`\`

**Expected output:**
\`\`\`
output text
\`\`\`

**Explanation**: Why this works and what it does.

## Step 2: Next Action

Continue the pattern...
```

## 5. Validation Section

**Purpose**: help users verify successful completion.

```markdown
## Verify Your Work

Check that everything works as expected:

1. **Verification step 1**
   \`\`\`bash
   verification-command
   \`\`\`
   Expected result: Description

2. **Verification step 2**
   Similar format...
```

## 6. Next Steps Section

**Purpose**: guide continued learning.

```markdown
## Next Steps

Now that you've completed this tutorial, you can:

- **Next tutorial**: [Tutorial Title](./relative-path.md) - Brief description
- **Related how-to**: [Guide Title](./relative-path.md) - When to use this
- **Deep dive**: [Explanation Title](./relative-path.md) - Understand the concepts
```

## 7. Troubleshooting Section (Optional)

**Purpose**: address common issues.

```markdown
## Troubleshooting

### Issue: Common Problem Description

**Symptom**: What the user sees

**Cause**: Why it happens

**Solution**:
\`\`\`bash
fix-command
\`\`\`
```
