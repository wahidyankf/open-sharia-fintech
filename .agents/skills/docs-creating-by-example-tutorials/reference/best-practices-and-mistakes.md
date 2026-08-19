# By-Example Tutorials — Best Practices and Common Mistakes

## Example Creation Workflow

1. **Identify concept**: What specific feature/pattern to demonstrate?
2. **Write working code**: Ensure it compiles and runs
3. **Make self-contained**: Remove external dependencies
4. **Add annotations**: 1.0-2.25 comments per code line
5. **Verify output**: Run code, document actual output
6. **Add diagram** (if complex): Use accessible colors
7. **Write takeaway**: 1-2 sentence lesson summary
8. **Measure density**: Count annotations per code line

## Annotation Guidelines

**DO**:

- Document WHAT happens at each step
- Show variable values after operations
- Indicate types when useful
- Explain side effects
- Use consistent `// =>` or `# =>` notation

**DON'T**:

- Repeat obvious information ("assigns 10 to x" when code shows `x = 10`)
- Write paragraphs (keep annotations concise)
- Skip intermediate values in complex operations
- Use inconsistent notation styles

## Quality Checklist

Before publishing by-example tutorial:

- [ ] 75-85 examples total
- [ ] 95% language coverage achieved
- [ ] Each example follows five-part structure
- [ ] Annotation density 1.0-2.25 per example
- [ ] All examples are self-contained and runnable
- [ ] Multiple code blocks used for comparisons
- [ ] Diagrams use accessible color palette
- [ ] Examples progress from beginner → intermediate → advanced
- [ ] Key takeaways summarize lessons clearly

## Mistake 1: File-level annotation density instead of per-example

**Wrong**: Measuring annotations across entire file

**Right**: Measure each example independently. One example with 0.5 density and another with 2.0 density both fail (first too low, second acceptable). Target 1.0-2.25 for EACH example.

## Mistake 2: Combining different approaches in single code block

```java
// WRONG! Mixed mutable and immutable in one block
String str = "Hello";
str = str + " World";
StringBuilder sb = new StringBuilder("Hello");
sb.append(" World");
```

**Right**: Use multiple code blocks with text between explaining differences.

## Mistake 3: Examples requiring external setup

```java
// WRONG! Requires database setup
Connection conn = DriverManager.getConnection("jdbc:...");
// Users can't run this without database
```

**Right**: Use in-memory data structures or mock objects for self-containment.

## Mistake 4: Missing intermediate values

```java
// WRONG! Complex operation with no intermediate annotations
int result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .reduce(0, Integer::sum);  // => result is 56
```

**Right**: Annotate each stage showing intermediate values.

## Mistake 5: Paragraph annotations

```java
// WRONG! Too verbose
int x = 10;  // This line declares a variable named x and assigns it the integer value 10. Variables in Java must have a type, and here the type is int which represents 32-bit signed integers ranging from -2,147,483,648 to 2,147,483,647.
```

**Right**: Concise annotations scaling with code complexity.
