---
title: "Stage 1: Maker (Comprehensive Content Management)"
description: "The maker stage - creates or updates content and dependencies."
category: explanation
subcategory: development
tags:
  - maker-checker-fixer
  - workflow
  - content-quality
  - agent-patterns
  - validation
  - automation
created: 2025-12-14
when_to_use: "Use when a request calls for the maker stage."
---

# Stage 1: Maker (Comprehensive Content Management)

**Role**: Creates NEW content and updates EXISTING content with all dependencies

**Characteristics**:

- **User-driven operation** - Responds to user requests for content creation/modification
- **Comprehensive scope** - Creates target content AND updates all related files
- **Cascading changes** - Adjusts indices, cross-references, and dependencies
- **Proactive management** - Anticipates what needs updating beyond the immediate request

**Tool Pattern**: `Write`, `Edit` (content modification tools)

**Color**: 🟦 Blue (Writer agents) or 🟨 Yellow (repo-rules-maker uses bash)

**Examples**:

| Agent                               | Creates/Updates                                    | Also Manages                                      | Tools Used            |
| ----------------------------------- | -------------------------------------------------- | ------------------------------------------------- | --------------------- |
| repo-rules-maker                    | Convention docs, AGENTS.md sections, agent prompts | Cross-references, indices, related documentation  | Bash (not Edit/Write) |
| apps-ayokoding-www-general-maker    | General Next.js learning content, blog posts       | Navigation files, overview pages, indices         | Write, Edit           |
| apps-ayokoding-www-by-example-maker | By-example tutorials with annotated code           | 75-90 examples, diagrams, educational annotations | Write, Edit           |
| docs-tutorial-maker                 | Tutorial content with narrative flow               | Learning objectives, diagrams, code examples      | Write, Edit           |
| apps-ose-www-content-maker          | Platform update posts, about pages                 | Navigation, asset references                      | Write, Edit           |
| readme-maker                        | README sections with engaging content              | Links to detailed docs, cross-references          | Write, Edit           |

**Note**: `repo-rules-maker` is a special case that uses bash commands (cat, sed, awk) instead of Edit/Write tools for file operations.

**Key Responsibilities**:

- PASS: Create new content from scratch
- PASS: Update existing content when requested
- PASS: Adjust ALL dependencies (indices, cross-refs, navigation)
- PASS: Follow all conventions during creation
- PASS: Provide complete, production-ready content

**When to Use**: User wants to **create or update content** (not validate or fix)

**Example Workflow**:

```markdown
User: "Add a new tutorial to ayokoding-www about TypeScript generics"

Maker Agent (apps-ayokoding-www-general-maker):

1. Creates content/en/learn/swe/programming-languages/typescript/generics.md
2. Creates content/id/belajar/swe/programming-languages/typescript/generics.md (bilingual)
3. Updates content/en/learn/swe/programming-languages/typescript/\_index.md (navigation)
4. Updates content/id/belajar/swe/programming-languages/typescript/\_index.md (navigation)
5. Ensures overview.md/ikhtisar.md links are correct
6. Follows weight ordering convention (level-based)
7. Uses accessible colors in diagrams
8. Validates all internal links
9. Delivers complete, ready-to-publish content
```
