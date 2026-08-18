---
title: "YAML and Code Block Indentation"
description: The required 2-space YAML frontmatter indentation and the language-specific idiomatic indentation rules for code blocks embedded in markdown.
when_to_use: Use when indenting YAML frontmatter or writing a code block inside a markdown file.
category: explanation
subcategory: conventions
tags:
  - indentation
  - formatting
  - markdown
created: 2025-12-12
---

# YAML and Code Block Indentation

## YAML Frontmatter Indentation

All YAML frontmatter blocks MUST use **2 spaces per indentation level** (standard YAML requirement):

```yaml
PASS: CORRECT - Frontmatter uses 2 spaces:
---
title: "Document Title"
description: Brief description
category: explanation
tags:
  - primary-topic # 2 spaces before dash
  - secondary-topic # 2 spaces before dash
created: 2025-12-12
---
```

**Why spaces in frontmatter?**

- **YAML specification**: YAML standard uses spaces for indentation
- **Tool compatibility**: All YAML parsers expect consistent space indentation
- **Critical for ALL nested frontmatter fields**: This applies to `tags`, any list fields, and any nested objects

**After frontmatter**: All markdown content (including bullets) continues using standard markdown formatting (space indentation).

## Code Block Indentation

Code blocks within documentation MUST use **language-specific idiomatic indentation**:

- **JavaScript/TypeScript**: 2 spaces per indent level (aligns with project Prettier configuration)
- **Python**: 4 spaces per indent level (PEP 8 standard)
- **YAML**: 2 spaces per indent level (YAML specification)
- **JSON**: 2 spaces per indent level (project standard)
- **CSS**: 2 spaces per indent level
- **Bash/Shell**: 2 spaces per indent level (common practice)
- **Go**: Tabs (Go language standard - ONLY exception where tabs are correct)

**CRITICAL**: Using TAB characters in code blocks (except Go) creates code that cannot be copied and pasted correctly. Always use the language's idiomatic indentation.

**Example**:

````markdown
- Research on authentication patterns #auth
  - Key findings about OAuth 2.0
    - Implementation in JavaScript:

```javascript
function authenticate(user) {
  if (user.isValid) {
    return generateToken(user); // 2 spaces (JavaScript standard)
  }
  return null;
}
```

    - Implementation in Python:

```python
def authenticate(user):
    if user.is_valid:
        return generate_token(user)  # 4 spaces (Python standard)
    return None
```

    - Implementation in Go (uses tabs):

```go
func Authenticate(user User) Token {
 if user.IsValid {
  return generateToken(user) // Tab indentation (Go standard)
 }
 return nil
}
```
````

**Rationale**: Code blocks represent actual source code and must follow their language's conventions, not the markdown formatting rules. This ensures code examples are syntactically correct and can be copied directly into editors or files without modification.
