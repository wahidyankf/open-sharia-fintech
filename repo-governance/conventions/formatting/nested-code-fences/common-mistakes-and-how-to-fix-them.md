---
title: "Common Mistakes and How to Fix Them"
description: Three common nested-fence mistakes — extra closing fences, wrong fence depth, and mismatched fence pairs — each with a broken example and its fix.
when_to_use: Use when a nested code fence example is rendering incorrectly and you need to diagnose which mistake caused it.
category: explanation
subcategory: conventions
tags:
  - markdown
  - code-fences
  - nesting
  - syntax
  - documentation
created: 2025-12-23
---

# Common Mistakes and How to Fix Them

## Mistake 1: Extra Closing Fence

**Broken**:

`````markdown
````markdown
### Example

```javascript
code here
```
````

```← ORPHANED! Breaks rendering

```
`````

**Fixed**:

`````markdown
````markdown
### Example

```javascript
code here
```
````
`````

**Fix**: Remove the orphaned closing fence after the proper 4-backtick closure.

## Mistake 2: Wrong Fence Depth

**Broken** (using 3 backticks for outer fence):

`````markdown
````markdown
### Example

```javascript
code here
```
````
`````

```

```

``````

**Problem**: Parser can't distinguish outer from inner fences. Rendering is unpredictable.

**Fixed** (using 4 backticks for outer fence):

`````markdown
````markdown
### Example

```javascript
code here
```
``````

``````

## Mistake 3: Mismatched Fence Pairs

**Broken**:

`````markdown
`````markdown
### Example

`````javascript
code here
````   ← WRONG! Closes with 4 backticks (should be 3)
````   ← WRONG! Extra 4-backtick fence
``````

```

```

**Fixed**:

`````markdown
````markdown
### Example

```javascript
code here
```
````
`````

**Fix**: Each fence pair must use same depth (3-3 or 4-4, not 3-4).
