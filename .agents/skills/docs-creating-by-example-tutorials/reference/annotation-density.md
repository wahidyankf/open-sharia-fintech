# By-Example Tutorials — Annotation Density Standards

## The 1.0-2.25 Rule

**CRITICAL**: Target 1.0-2.25 comment lines per code line **PER EXAMPLE**

**Measurement**: Each code block is measured independently

- **Minimum**: 1.0 (examples below this need enhancement)
- **Optimal**: 1.0-2.25 (target range for educational value)
- **Upper bound**: 2.5 (examples exceeding this need reduction)

**Density Calculation Formula**:

```
density = (number of comment lines) ÷ (number of code lines)
```

**Example**:

- 15 comment lines ÷ 7 code lines = 2.14 density ✅ (optimal)
- NOT: 7 code lines ÷ 15 comments = 0.47 ❌ (inverted formula)

## Annotation Pattern

Use `// =>` or `# =>` notation to document:

- **Values**: Show variable values after assignment
- **States**: Show object/data structure states after modification
- **Outputs**: Show console/print output
- **Side effects**: Show file changes, network calls, database updates
- **Intermediate steps**: Show values during complex operations

**Examples**:

```java
// Simple line (1 annotation)
int x = 10;                      // => x is 10 (type: int)

// Complex line (2 annotations)
String result = transform(x);    // => Calls transform with 10
                                 // => result is "10-transformed" (type: String)

// Output line (1 annotation)
System.out.println(result);      // => Output: 10-transformed
```

```python
# Simple operation (1 annotation)
numbers = [1, 2, 3, 4, 5]       # => numbers is [1, 2, 3, 4, 5] (type: list)

# Complex operation (2 annotations)
squared = [n**2 for n in numbers]  # => List comprehension squares each number
                                    # => squared is [1, 4, 9, 16, 25]

# Output (1 annotation)
print(squared)                  # => Output: [1, 4, 9, 16, 25]
```

## Quality Over Quantity

**Focus on**:

- Concise explanations that scale with code complexity
- Simple operations get brief annotations
- Complex operations get detailed breakdowns
- Avoid repetitive patterns across similar code
