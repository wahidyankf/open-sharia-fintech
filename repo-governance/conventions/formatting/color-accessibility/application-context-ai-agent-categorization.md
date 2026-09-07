---
description: "Defines the colored-square emoji scheme used to categorize AI agents by role in agent index files."
when_to_use: "Use when assigning or reviewing a colored-square emoji for an agent definition in an agents README index."
---

# Application Contexts: AI Agent Color Categorization

**Context**: Agents are visually categorized by role using colored square emojis in the agent definition index file (e.g., the platform binding's `agents/README.md`).

## Agent Color Assignment

| Emoji | Color  | Hex Code | Role                                                                | Examples                                                                            |
| ----- | ------ | -------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 🟦    | Blue   | #0173B2  | **Writers/Creators** - Agents that create or write new content      | docs-maker, docs-tutorial-maker, agent-maker, plan-maker                            |
| 🟩    | Green  | #029E73  | **Checkers/Validators** - Agents that validate or check consistency | docs-checker, docs-link-checker, docs-tutorial-checker, plan-checker, rules-checker |
| 🟨    | Yellow | #F1C40F  | **Fixers** - Agents that apply validated fixes to existing content  | docs-file-manager, repo-workflow-fixer                                              |
| 🟪    | Purple | #CC78BC  | **Implementors/Executors** - Agents that execute or implement plans | plan-execution-checker, deployers                                                   |

## Implementation in Agent Index Files

**Best Practice Example**:

```markdown
### 🟦 docs-maker.md

Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.

### 🟩 docs-checker.md

Expert documentation validator focusing on factual correctness and consistency. Use when verifying documentation accuracy and detecting contradictions.

### 🟨 docs-file-manager.md

Expert at managing files and directories in docs/ (rename, move, delete). Use when reorganizing documentation structure while maintaining conventions.

### 🟪 plan-execution-checker.md

Expert at validating completed plan implementations against requirements and quality standards. Use for independent post-execution validation.
```

## Color Accessibility for Agent Categorization

**Critical requirement**: Agents are identified by **multiple visual cues**, not color alone:

1. **Color** (🟦 blue emoji) - Supplementary visual marker
2. **Shape** (square emoji vs. other shapes) - Visual differentiation
3. **Text label** (agent name like "docs-maker") - Primary identifier
4. **Context** (placement in README, description) - Semantic meaning

**Users with color blindness can identify agents by**: - Agent name (primary identifier) - File name (secondary identifier) - Role suffix (writer, checker, fixer, implementor) - Description text - Position in document

The colored square emoji is **supplementary enhancement** only, not the primary identification method.
