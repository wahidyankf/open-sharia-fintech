---
description: "Specifies the remaining required and optional parts of a cookbook recipe: how-it-works explanation, common pitfalls, related recipes, and learn-more links."
when_to_use: "Read when drafting the explanation, pitfalls, and cross-reference sections of a cookbook recipe."
---

# Recipe Structure Standards: How It Works, Common Pitfalls, and Related Recipes

## 4. How It Works

**Format**: 2-4 paragraphs explaining the solution approach.

**Example**:

```markdown
### How It Works

This solution uses Go's standard library `encoding/csv` package which handles most edge cases automatically. The key insight is treating the first row as headers and mapping subsequent rows to key-value pairs.

The `TrimLeadingSpace` option handles inconsistent formatting without manual preprocessing. By reading one row at a time, this approach works efficiently even with large CSV files.

The error handling covers three cases: file not found, malformed headers, and malformed data rows. Each error is returned immediately rather than collecting errors, following Go's fail-fast philosophy.
```

**Requirements**:

- Explain the approach, not the syntax
- Highlight key insights or patterns
- Mention why this approach works well
- Keep concise (don't duplicate code comments)

## 5. Common Pitfalls

**Format**: Bulleted list of mistakes to avoid.

**Example**:

```markdown
### Common Pitfalls

- **Not checking header length**: If a row has more columns than headers, indexing fails. Always validate `i < len(headers)`.
- **Forgetting to close file**: Without `defer file.Close()`, files stay open until program exits.
- **Assuming consistent encoding**: CSV files may use different encodings (UTF-8, Latin-1). Use `golang.org/x/text/encoding` for non-UTF-8 files.
- **Not handling quoted fields**: Fields containing commas must be quoted. The standard `csv.Reader` handles this, but custom parsers often don't.
```

**Requirements**:

- 3-5 common mistakes
- Each with brief explanation
- Actionable (what to do instead)
- Based on real production errors

## 6. Related Recipes

**Format**: Bulleted list linking to related recipes.

**Example**:

```markdown
### Related Recipes

- **Write CSV with Custom Headers** - Reverse operation, writing data to CSV
- **Parse JSON with Schema Validation** - Similar problem for JSON instead of CSV
- **Handle Large Files with Streaming** - Memory-efficient approach for huge CSV files
```

**Requirements**:

- 2-4 related recipes
- Brief description of relationship
- Links when recipes exist
- Helps readers discover related solutions

## 7. Learn More (Optional)

**Format**: Links to related learning content in by-concept or by-example.

**Example**:

```markdown
### Learn More

- **By-Concept: File I/O** - Comprehensive coverage of file operations and error handling patterns
- **By-Example: Example 23** - More CSV parsing examples with different formats
```

**Requirements**:

- Optional (include when helpful)
- Links to comprehensive learning paths
- Helps readers deepen understanding beyond immediate problem
