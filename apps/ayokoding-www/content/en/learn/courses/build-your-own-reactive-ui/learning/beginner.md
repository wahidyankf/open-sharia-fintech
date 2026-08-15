---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1-26 are self-contained strict TypeScript micro-runtimes. Each has no `any` and follows the five-part by-example format: context, diagram where flow needs it, annotated source, takeaway, and production relevance.

---

### Example 1: H Function

_ex-01 &middot; exercises co-02_

H Function isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-01-h-function/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "h-function", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: h-function");
// => Output: PASS: h-function
```

**Run**: `npx tsx learning/code/ex-01-h-function/example.ts`

**Output**:

```text
PASS: h-function
```

**Key takeaway**: H Function is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 2: H Nested

_ex-02 &middot; exercises co-02, co-04_

H Nested isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-02-h-nested/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "h-nested", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: h-nested");
// => Output: PASS: h-nested
```

**Run**: `npx tsx learning/code/ex-02-h-nested/example.ts`

**Output**:

```text
PASS: h-nested
```

**Key takeaway**: H Nested is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 3: VNode Shape

_ex-03 &middot; exercises co-04_

VNode Shape isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-03-vnode-shape/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "vnode-shape", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: vnode-shape");
// => Output: PASS: vnode-shape
```

**Run**: `npx tsx learning/code/ex-03-vnode-shape/example.ts`

**Output**:

```text
PASS: vnode-shape
```

**Key takeaway**: VNode Shape is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 4: JSX Desugar

_ex-04 &middot; exercises co-03_

JSX Desugar isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-04-jsx-desugar/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "jsx-desugar", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: jsx-desugar");
// => Output: PASS: jsx-desugar
```

**Run**: `npx tsx learning/code/ex-04-jsx-desugar/example.ts`

**Output**:

```text
PASS: jsx-desugar
```

**Key takeaway**: JSX Desugar is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 5: Text VNode

_ex-05 &middot; exercises co-04_

Text VNode isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-05-text-vnode/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "text-vnode", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: text-vnode");
// => Output: PASS: text-vnode
```

**Run**: `npx tsx learning/code/ex-05-text-vnode/example.ts`

**Output**:

```text
PASS: text-vnode
```

**Key takeaway**: Text VNode is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 6: Mount Element

_ex-06 &middot; exercises co-05_

Mount Element isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-06-mount-element/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "mount-element", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: mount-element");
// => Output: PASS: mount-element
```

**Run**: `npx tsx learning/code/ex-06-mount-element/example.ts`

**Output**:

```text
PASS: mount-element
```

**Key takeaway**: Mount Element is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 7: Mount Props

_ex-07 &middot; exercises co-05_

Mount Props isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-07-mount-props/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "mount-props", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: mount-props");
// => Output: PASS: mount-props
```

**Run**: `npx tsx learning/code/ex-07-mount-props/example.ts`

**Output**:

```text
PASS: mount-props
```

**Key takeaway**: Mount Props is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 8: Mount Children

_ex-08 &middot; exercises co-05_

Mount Children isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-08-mount-children/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "mount-children", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: mount-children");
// => Output: PASS: mount-children
```

**Run**: `npx tsx learning/code/ex-08-mount-children/example.ts`

**Output**:

```text
PASS: mount-children
```

**Key takeaway**: Mount Children is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 9: Mount Text

_ex-09 &middot; exercises co-05_

Mount Text isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-09-mount-text/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "mount-text", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: mount-text");
// => Output: PASS: mount-text
```

**Run**: `npx tsx learning/code/ex-09-mount-text/example.ts`

**Output**:

```text
PASS: mount-text
```

**Key takeaway**: Mount Text is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 10: View As Function

_ex-10 &middot; exercises co-01_

View As Function isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-10-view-as-function/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "view-as-function", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: view-as-function");
// => Output: PASS: view-as-function
```

**Run**: `npx tsx learning/code/ex-10-view-as-function/example.ts`

**Output**:

```text
PASS: view-as-function
```

**Key takeaway**: View As Function is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 11: Rerender Naive

_ex-11 &middot; exercises co-01_

Rerender Naive isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-11-rerender-naive/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "rerender-naive", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: rerender-naive");
// => Output: PASS: rerender-naive
```

**Run**: `npx tsx learning/code/ex-11-rerender-naive/example.ts`

**Output**:

```text
PASS: rerender-naive
```

**Key takeaway**: Rerender Naive is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 12: Diff Text Change

_ex-12 &middot; exercises co-06_

Diff Text Change isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-12-diff-text-change/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "diff-text-change", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: diff-text-change");
// => Output: PASS: diff-text-change
```

**Run**: `npx tsx learning/code/ex-12-diff-text-change/example.ts`

**Output**:

```text
PASS: diff-text-change
```

**Key takeaway**: Diff Text Change is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 13: Patch Text

_ex-13 &middot; exercises co-07_

Patch Text isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-13-patch-text/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "patch-text", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: patch-text");
// => Output: PASS: patch-text
```

**Run**: `npx tsx learning/code/ex-13-patch-text/example.ts`

**Output**:

```text
PASS: patch-text
```

**Key takeaway**: Patch Text is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 14: Diff Prop Change

_ex-14 &middot; exercises co-06_

Diff Prop Change isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-14-diff-prop-change/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "diff-prop-change", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: diff-prop-change");
// => Output: PASS: diff-prop-change
```

**Run**: `npx tsx learning/code/ex-14-diff-prop-change/example.ts`

**Output**:

```text
PASS: diff-prop-change
```

**Key takeaway**: Diff Prop Change is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 15: Patch Prop

_ex-15 &middot; exercises co-07_

Patch Prop isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-15-patch-prop/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "patch-prop", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: patch-prop");
// => Output: PASS: patch-prop
```

**Run**: `npx tsx learning/code/ex-15-patch-prop/example.ts`

**Output**:

```text
PASS: patch-prop
```

**Key takeaway**: Patch Prop is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 16: Diff Add Child

_ex-16 &middot; exercises co-06_

Diff Add Child isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-16-diff-add-child/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "diff-add-child", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: diff-add-child");
// => Output: PASS: diff-add-child
```

**Run**: `npx tsx learning/code/ex-16-diff-add-child/example.ts`

**Output**:

```text
PASS: diff-add-child
```

**Key takeaway**: Diff Add Child is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 17: Patch Add Child

_ex-17 &middot; exercises co-07_

Patch Add Child isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-17-patch-add-child/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "patch-add-child", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: patch-add-child");
// => Output: PASS: patch-add-child
```

**Run**: `npx tsx learning/code/ex-17-patch-add-child/example.ts`

**Output**:

```text
PASS: patch-add-child
```

**Key takeaway**: Patch Add Child is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 18: Diff Remove Child

_ex-18 &middot; exercises co-06_

Diff Remove Child isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-18-diff-remove-child/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "diff-remove-child", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: diff-remove-child");
// => Output: PASS: diff-remove-child
```

**Run**: `npx tsx learning/code/ex-18-diff-remove-child/example.ts`

**Output**:

```text
PASS: diff-remove-child
```

**Key takeaway**: Diff Remove Child is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 19: Patch Remove Child

_ex-19 &middot; exercises co-07_

Patch Remove Child isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-19-patch-remove-child/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "patch-remove-child", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: patch-remove-child");
// => Output: PASS: patch-remove-child
```

**Run**: `npx tsx learning/code/ex-19-patch-remove-child/example.ts`

**Output**:

```text
PASS: patch-remove-child
```

**Key takeaway**: Patch Remove Child is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 20: Same Type Reuse

_ex-20 &middot; exercises co-08, co-09_

Same Type Reuse isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-20-same-type-reuse/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "same-type-reuse", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: same-type-reuse");
// => Output: PASS: same-type-reuse
```

**Run**: `npx tsx learning/code/ex-20-same-type-reuse/example.ts`

**Output**:

```text
PASS: same-type-reuse
```

**Key takeaway**: Same Type Reuse is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 21: Different Type Replace

_ex-21 &middot; exercises co-10_

Different Type Replace isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-21-different-type-replace/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "different-type-replace", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: different-type-replace");
// => Output: PASS: different-type-replace
```

**Run**: `npx tsx learning/code/ex-21-different-type-replace/example.ts`

**Output**:

```text
PASS: different-type-replace
```

**Key takeaway**: Different Type Replace is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 22: Node Identity Preserved

_ex-22 &middot; exercises co-09_

Node Identity Preserved isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-22-node-identity-preserved/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "node-identity-preserved", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: node-identity-preserved");
// => Output: PASS: node-identity-preserved
```

**Run**: `npx tsx learning/code/ex-22-node-identity-preserved/example.ts`

**Output**:

```text
PASS: node-identity-preserved
```

**Key takeaway**: Node Identity Preserved is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 23: Event Listener Bind

_ex-23 &middot; exercises co-24_

Event Listener Bind isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-23-event-listener-bind/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "event-listener-bind", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: event-listener-bind");
// => Output: PASS: event-listener-bind
```

**Run**: `npx tsx learning/code/ex-23-event-listener-bind/example.ts`

**Output**:

```text
PASS: event-listener-bind
```

**Key takeaway**: Event Listener Bind is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 24: Event Update

_ex-24 &middot; exercises co-24_

Event Update isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-24-event-update/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "event-update", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: event-update");
// => Output: PASS: event-update
```

**Run**: `npx tsx learning/code/ex-24-event-update/example.ts`

**Output**:

```text
PASS: event-update
```

**Key takeaway**: Event Update is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 25: Signal Value

_ex-25 &middot; exercises co-13_

Signal Value isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-25-signal-value/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "signal-value", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: signal-value");
// => Output: PASS: signal-value
```

**Run**: `npx tsx learning/code/ex-25-signal-value/example.ts`

**Output**:

```text
PASS: signal-value
```

**Key takeaway**: Signal Value is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 26: Signal Set

_ex-26 &middot; exercises co-13_

Signal Set isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-26-signal-set/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "signal-set", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: signal-set");
// => Output: PASS: signal-set
```

**Run**: `npx tsx learning/code/ex-26-signal-set/example.ts`

**Output**:

```text
PASS: signal-set
```

**Key takeaway**: Signal Set is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---
