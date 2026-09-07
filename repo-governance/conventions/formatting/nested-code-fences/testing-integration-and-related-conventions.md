---
description: The process for testing nested fence rendering before committing, and how this convention integrates with related formatting conventions.
when_to_use: Use when you need to verify a nested-fence example renders correctly or find related conventions that apply.
---

# Testing, Integration, and Related Conventions

## Testing Your Nested Fences

**Process**:

1. **Write the nested structure** following depth rules
2. **Preview the file** in GitHub preview or markdown editor
3. **Verify formatting** - Check bold, italic, headings render correctly
4. **Count fence pairs** - Every opening fence has one closing fence
5. **Check for literals** - No markdown syntax showing as plain text

**Tools**:

- **GitHub Preview**: View file on GitHub web interface
- **VS Code**: Use markdown preview (Cmd/Ctrl + Shift + V)
- **nx dev**: For Next.js sites, test with local dev server

## Integration with Other Conventions

This convention works with:

- **[Content Quality Principles](../../writing/quality.md)**: Proper code block formatting is part of content quality
- **[Indentation Convention](../indentation.md)**: Code blocks use language-specific indentation
- **[Tutorial Convention](../../tutorials/general.md)**: Tutorials often demonstrate markdown syntax

## Related Conventions

**Formatting Standards**:

- [Content Quality Principles](../../writing/quality.md) — Code block formatting standards
- [Indentation Convention](../indentation.md) — Code block indentation rules
- [Mathematical Notation Convention](../mathematical-notation.md) — LaTeX in markdown (no nesting needed)

**Context-Specific**:

- [Tutorial Convention](../../tutorials/general.md) — Teaching markdown syntax in tutorials
- [README Quality Convention](../../writing/readme-quality.md) — Code examples in README files
