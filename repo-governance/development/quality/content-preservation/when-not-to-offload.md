---
description: "Cases where offloading is the wrong move."
when_to_use: "Use when unsure whether a section actually needs offloading."
---

# When NOT to Offload

**Keep content in the original file when:**

1. **Agent-specific implementation details** - How THIS agent applies a convention
2. **Agent-unique workflows** - Process specific to this agent's task
3. **Agent decision logic** - Internal reasoning not applicable elsewhere
4. **Minimal content** - Section is already 3-5 lines
5. **Context-dependent** - Content only makes sense in this specific context

**Example of content to keep:**

```markdown
## File Naming Convention

You MUST follow the [File Naming Convention](../../conventions/structure/file-naming.md).

When creating documentation files:

1. Read the target directory path
2. Choose a lowercase kebab-case basename describing the content
3. Let the directory hierarchy encode the category
```

**Why keep:** This is agent-specific application (how docs-maker uses the convention), not the convention itself.
