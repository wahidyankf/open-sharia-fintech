---
description: "Lists the indicators that signal a code block should be split into multiple blocks, why it matters, and the split solution pattern."
when_to_use: "Read when reviewing a single code block that mixes languages, alternatives, or excessive comparison comments, to decide whether it must be split."
---

# Multiple Code Blocks Pattern: When to Split Code Blocks

**CRITICAL RULE**: When a single code block contains multiple distinct concepts, approaches, or language implementations, split into separate code blocks with markdown text between them. This prevents comment overload and maintains syntax highlighting.

**Indicators for splitting**:

1. **Commented-out code for alternative implementations** - `/* ... */` or `// ...` showing different approaches
2. **Code in different languages** - Java + C, Java + SQL, Go + Assembly
3. **Multiple library approaches** - ASM vs ByteBuddy, JNI vs Panama Foreign Function API
4. **Excessive comments explaining alternatives/trade-offs** - >30% comment lines explaining options rather than showing state
5. **Multiple distinct patterns in one example** - Strategy + Observer + Decorator combined

**Why this matters**:

- **Syntax highlighting breaks** when mixing languages or commented-out alternatives
- **Density measurement becomes meaningless** when comments explain alternatives instead of annotating code
- **Code isn't runnable** when showing multiple incompatible approaches in one block
- **Scannability suffers** when readers must mentally parse which code is active

**Solution**: Split into multiple code blocks with explanatory text between:

````markdown
**Approach A: Low-Level Library**

```java
import lib.A;
ClassA client = new ClassA();  // => Creates client instance
client.configure(config);      // => Applies configuration
```

**Trade-offs**: Provides fine-grained control but requires manual setup.

**Approach B: High-Level Library**

```java
import lib.B;
ClassB client = ClassB.create();  // => Auto-configured client
Response res = client.get(url);   // => Executes GET request
```

**Trade-offs**: Automatic configuration but limited customization.
````

This maintains 1.0-2.25 density PER BLOCK while separating WHAT (code annotations) from WHY (explanatory text).
