---
description: The 4-backtick-outer/3-backtick-inner depth rule with no orphaned fences, plus three complete worked examples of correctly nested fences.
when_to_use: Use when writing a markdown example that itself contains a code block, and you need the correct fence depth pattern.
---

# Fence Depth Rules and Complete Nesting Examples

## The Solution: Fence Depth Rules

### Rule 1: Outer Fence Uses 4 Backticks

When showing markdown examples that contain code blocks, the outer fence MUST use **4 backticks**:

````markdown
```markdown
### Example Content

This is markdown content being documented.
```
````

### Rule 2: Inner Fence Uses 3 Backticks

Code blocks within the markdown example use **3 backticks**:

`````markdown
````markdown
### Example: Code Block

```javascript
const x = 5;
```
````
`````

### Rule 3: No Orphaned Fences

**Every opening fence MUST have exactly one matching closing fence.** No extra fences allowed.

**Validation**: Count backtick groups in your content:

- Opening 4-backtick fence: ```````` (start of outer)
- Opening 3-backtick fence: ``` (start of inner)
- Closing 3-backtick fence: ``` (end of inner)
- Closing 4-backtick fence: ```````` (end of outer)

**Correct pairing**:

- 4-backtick open → 4-backtick close (outer pair)
- 3-backtick open → 3-backtick close (inner pair)

## Complete Nesting Examples

### Example 1: Single Code Block in Markdown

**Correct** (showing how to write markdown with a code block):

`````markdown
````markdown
### Example 1: Hello World

**Code**:

```javascript
console.log("Hello, World!");
```

**Key Takeaway**: This prints a greeting to the console.
````
`````

**Structure breakdown**:

1. ```(4 backticks) - Opens outer fence

   ```

2. `### Example 1:` - Markdown heading being documented

3. ```(3 backticks) - Opens inner fence for code block

   ```

4. `console.log(...)` - Code content

5. ```(3 backticks) - Closes inner fence

   ```

6. `**Key Takeaway**:` - More markdown content being documented

7. ```(4 backticks) - Closes outer fence

   ```

### Example 2: Multiple Code Blocks

**Correct** (multiple code blocks within documented markdown):

`````markdown
````markdown
### Example 2: Variables

**Code**:

```javascript
const name = "Alice";
const age = 30;
```

**Explanation**: This declares two variables.

**Advanced**:

```javascript
const person = { name, age };
```
````
`````

**Structure breakdown**:

1. ```(4 backticks) - Opens outer fence

   ```

2. First ``` pair - First code block (3 backticks open/close)
3. `**Explanation**:` - Markdown content
4. Second ``` pair - Second code block (3 backticks open/close)

5. ```(4 backticks) - Closes outer fence

   ```

### Example 3: Nested Markdown Without Code

**Correct** (documenting markdown structure without code blocks):

````markdown
```markdown
## Tutorial Structure

### Learning Objectives

By the end of this tutorial, you'll understand:

- Concept A
- Concept B
- Concept C

### Prerequisites

You should have basic knowledge of...
```
````

**Note**: Even without inner code blocks, use 4 backticks for outer fence when documenting markdown structure.
