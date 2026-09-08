---
description: The required markdown link syntax and key rules, worked examples by file location, correct-vs-incorrect link examples, and external link formatting.
when_to_use: Use when writing a link in documentation and you need the exact syntax or a worked example for your file's location.
---

# Link Syntax, Examples, and Correct Usage

## Link Syntax Standard

### Required Format

Use standard markdown link syntax with relative paths:

```markdown
`Display Text`
```

### Key Rules

1. **Always include the `.md` extension**

   ```markdown
   PASS: [Initial Setup](./tutorials/initial-setup.md)
   FAIL: [Initial Setup](./tutorials/initial-setup)
   ```

2. **Use relative paths from the current file's location**
   - Same directory: `./file.md`
   - Parent directory: `../file.md`
   - Subdirectory: `./subdirectory/file.md`
   - Multiple levels up: `../../path/to/file.md`
   - **Important**: The number of `../` depends on your file's nesting depth (see [Nested Directory Linking](./nested-directory-linking.md#nested-directory-linking))

3. **Use descriptive link text instead of filename identifiers**
   - PASS: `[File Naming Convention](../structure/file-naming.md)`
   - FAIL: `[file-naming](../structure/file-naming.md)`

4. **Avoid wiki-link syntax**
   - FAIL: `[[filename]]`
   - FAIL: `[[filename|Display Text]]`
   - Reason: GitHub does not render `[[...]]` as links.

## Examples by Location

### Linking from Root README (`docs/README.md`)

```markdown
<!-- Link to category index files -->

[Tutorials](./README.md)
[How-To Guides](./README.md)
[Reference](./README.md)
[Explanation](./README.md)

<!-- Link to nested files -->

[File Naming Convention](../structure/file-naming.md)
[Conventions Index](../README.md)
```

### Linking from Category Index (`docs/tutorials/README.md`)

```markdown
<!-- Link to sibling files in same directory -->

[Initial Setup](./initial-setup.md)
[First Deployment](./first-deployment.md)

<!-- Link to parent directory -->

[Documentation Home](./README.md)

<!-- Link to other categories -->

[How-To Guides](./README.md)
[API Reference](./README.md)
```

### Linking from Nested Files (`repo-governance/conventions/README.md`)

```markdown
<!-- Link to sibling files in same directory -->

[File Naming Convention](../structure/file-naming.md)
[Linking Convention](./linking.md)

<!-- Link to parent directory -->

[Explanation Index](../../docs/explanation/README.md)

<!-- Link to root -->

[Documentation Home](./README.md)

<!-- Link to other categories -->

[Tutorials](./README.md)
```

## Correct vs. Incorrect Examples

### PASS: Correct Examples

```markdown
<!-- Descriptive text with relative path and .md extension -->

[Understanding the Diátaxis Framework](../structure/diataxis-framework.md)
[Monorepo Structure](../../../docs/reference/monorepo-structure.md)
[AI Agents Convention](../../development/agents/ai-agents.md)

<!-- Links with context -->

See the [file naming convention](../structure/file-naming.md) for details.
For more information, refer to our [automation principle](../../principles/software-engineering/automation-over-manual.md).
```

### FAIL: Incorrect Examples

```markdown
<!-- Wiki-link syntax (GitHub does not render these) -->

[[diataxis-framework]]
[[diataxis-framework|Diátaxis Framework]]

<!-- Missing .md extension -->

[Diátaxis Framework](./diataxis-framework)

<!-- Absolute paths -->

[Conventions](../README.md)

<!-- Using filename as link text -->

[file-naming.md](../structure/file-naming.md)

<!-- Wrong number of ../ for nesting depth -->
<!-- From repo-governance/conventions/formatting/linking.md (3 levels deep) -->

[Documentation Home](./README.md) <!-- Should be ../../../README.md -->
[Tutorials](./README.md) <!-- Only 1 ../ instead of 3 -->

<!-- From repo-governance/conventions/README.md (2 levels deep) -->

[Documentation Home](./README.md) <!-- Too many ../ (3 instead of 2) -->
```

## External Links

For links to external resources:

```markdown
<!-- Standard markdown links -->

[Diátaxis Framework](https://diataxis.fr/)
[GitHub](https://github.com/wahidyankf/ose-public)
```
