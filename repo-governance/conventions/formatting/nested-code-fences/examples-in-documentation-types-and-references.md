---
description: Worked nested-fence examples for tutorials, how-to guides, and reference docs, plus links to the CommonMark and GitHub Flavored Markdown fence specifications.
when_to_use: Use when writing a nested-fence example in a tutorial, how-to guide, or reference document and want a template to follow.
---

# Examples in Documentation Types and References

## Examples in Documentation Types

### Tutorial Example

Showing code block structure in a tutorial:

`````markdown
````markdown
### Step 3: Create Your First Function

**Code**:

```javascript
function greet(name) {
  return `Hello, ${name}!`;
}
```

**Explanation**: This function takes a name parameter and returns a greeting string.
````
`````

### How-To Guide Example

Documenting a code pattern:

`````markdown
````markdown
## Solution: Error Handling Pattern

**Implementation**:

```typescript
try {
  const result = await fetchData();
  return result;
} catch (error) {
  console.error("Fetch failed:", error);
  throw error;
}
```

**When to use**: Use this pattern for async operations that might fail.
````
`````

### Reference Example

Showing API documentation format:

`````markdown
````markdown
### Method: `calculate()`

**Syntax**:

```javascript
calculate(value: number): number
```

**Parameters**:

- `value` - The input number to calculate

**Returns**: The calculated result
````
`````

## References

**Markdown Specifications**:

- [CommonMark Spec - Fenced Code Blocks](https://spec.commonmark.org/0.30/#fenced-code-blocks) - Official syntax specification
- [GitHub Flavored Markdown](https://github.github.com/gfm/#fenced-code-blocks) - GitHub's markdown implementation

**Related Standards**:

- [Content Quality Principles](../../writing/quality.md) — Universal content standards
- [Conventions Index](../README.md) — All documentation conventions
