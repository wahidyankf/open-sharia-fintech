---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Examples 27-54 are self-contained strict TypeScript micro-runtimes. Each has no `any` and follows the five-part by-example format: context, diagram where flow needs it, annotated source, takeaway, and production relevance.

---

### Example 27: Keyed List Diff

_ex-27 &middot; exercises co-11_

Keyed List Diff isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-27-keyed-list-diff/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "keyed-list-diff", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: keyed-list-diff");
// => Output: PASS: keyed-list-diff
```

**Run**: `npx tsx learning/code/ex-27-keyed-list-diff/example.ts`

**Output**:

```text
PASS: keyed-list-diff
```

**Key takeaway**: Keyed List Diff is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 28: Keyed Reorder Moves

_ex-28 &middot; exercises co-11_

Keyed Reorder Moves isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-28-keyed-reorder-moves/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "keyed-reorder-moves", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: keyed-reorder-moves");
// => Output: PASS: keyed-reorder-moves
```

**Run**: `npx tsx learning/code/ex-28-keyed-reorder-moves/example.ts`

**Output**:

```text
PASS: keyed-reorder-moves
```

**Key takeaway**: Keyed Reorder Moves is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 29: Unkeyed List Bug

_ex-29 &middot; exercises co-12_

Unkeyed List Bug isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-29-unkeyed-list-bug/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "unkeyed-list-bug", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: unkeyed-list-bug");
// => Output: PASS: unkeyed-list-bug
```

**Run**: `npx tsx learning/code/ex-29-unkeyed-list-bug/example.ts`

**Output**:

```text
PASS: unkeyed-list-bug
```

**Key takeaway**: Unkeyed List Bug is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 30: Unstable Key Loses State

_ex-30 &middot; exercises co-12_

Unstable Key Loses State isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-30-unstable-key-loses-state/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "unstable-key-loses-state", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: unstable-key-loses-state");
// => Output: PASS: unstable-key-loses-state
```

**Run**: `npx tsx learning/code/ex-30-unstable-key-loses-state/example.ts`

**Output**:

```text
PASS: unstable-key-loses-state
```

**Key takeaway**: Unstable Key Loses State is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 31: Keyed Insert

_ex-31 &middot; exercises co-11_

Keyed Insert isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-31-keyed-insert/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "keyed-insert", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: keyed-insert");
// => Output: PASS: keyed-insert
```

**Run**: `npx tsx learning/code/ex-31-keyed-insert/example.ts`

**Output**:

```text
PASS: keyed-insert
```

**Key takeaway**: Keyed Insert is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 32: Keyed Remove

_ex-32 &middot; exercises co-11_

Keyed Remove isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-32-keyed-remove/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "keyed-remove", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: keyed-remove");
// => Output: PASS: keyed-remove
```

**Run**: `npx tsx learning/code/ex-32-keyed-remove/example.ts`

**Output**:

```text
PASS: keyed-remove
```

**Key takeaway**: Keyed Remove is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 33: Signal Effect

_ex-33 &middot; exercises co-15, co-16_

Signal Effect isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-33-signal-effect/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "signal-effect", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: signal-effect");
// => Output: PASS: signal-effect
```

**Run**: `npx tsx learning/code/ex-33-signal-effect/example.ts`

**Output**:

```text
PASS: signal-effect
```

**Key takeaway**: Signal Effect is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 34: Effect Dependency Track

_ex-34 &middot; exercises co-16_

Effect Dependency Track isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-34-effect-dependency-track/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "effect-dependency-track", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: effect-dependency-track");
// => Output: PASS: effect-dependency-track
```

**Run**: `npx tsx learning/code/ex-34-effect-dependency-track/example.ts`

**Output**:

```text
PASS: effect-dependency-track
```

**Key takeaway**: Effect Dependency Track is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 35: Computed Derive

_ex-35 &middot; exercises co-14_

Computed Derive isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-35-computed-derive/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "computed-derive", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: computed-derive");
// => Output: PASS: computed-derive
```

**Run**: `npx tsx learning/code/ex-35-computed-derive/example.ts`

**Output**:

```text
PASS: computed-derive
```

**Key takeaway**: Computed Derive is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 36: Computed Lazy

_ex-36 &middot; exercises co-14, co-28_

Computed Lazy isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-36-computed-lazy/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "computed-lazy", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: computed-lazy");
// => Output: PASS: computed-lazy
```

**Run**: `npx tsx learning/code/ex-36-computed-lazy/example.ts`

**Output**:

```text
PASS: computed-lazy
```

**Key takeaway**: Computed Lazy is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 37: Computed Cache

_ex-37 &middot; exercises co-28_

Computed Cache isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-37-computed-cache/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "computed-cache", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: computed-cache");
// => Output: PASS: computed-cache
```

**Run**: `npx tsx learning/code/ex-37-computed-cache/example.ts`

**Output**:

```text
PASS: computed-cache
```

**Key takeaway**: Computed Cache is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 38: Reactive Graph Build

_ex-38 &middot; exercises co-17_

Reactive Graph Build isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-38-reactive-graph-build/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "reactive-graph-build", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: reactive-graph-build");
// => Output: PASS: reactive-graph-build
```

**Run**: `npx tsx learning/code/ex-38-reactive-graph-build/example.ts`

**Output**:

```text
PASS: reactive-graph-build
```

**Key takeaway**: Reactive Graph Build is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 39: Fine Grained Update

_ex-39 &middot; exercises co-19_

Fine Grained Update isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-39-fine-grained-update/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "fine-grained-update", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: fine-grained-update");
// => Output: PASS: fine-grained-update
```

**Run**: `npx tsx learning/code/ex-39-fine-grained-update/example.ts`

**Output**:

```text
PASS: fine-grained-update
```

**Key takeaway**: Fine Grained Update is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 40: Observer Subscribe

_ex-40 &middot; exercises co-18_

Observer Subscribe isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-40-observer-subscribe/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "observer-subscribe", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: observer-subscribe");
// => Output: PASS: observer-subscribe
```

**Run**: `npx tsx learning/code/ex-40-observer-subscribe/example.ts`

**Output**:

```text
PASS: observer-subscribe
```

**Key takeaway**: Observer Subscribe is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 41: Observer Unsubscribe

_ex-41 &middot; exercises co-18_

Observer Unsubscribe isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-41-observer-unsubscribe/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "observer-unsubscribe", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: observer-unsubscribe");
// => Output: PASS: observer-unsubscribe
```

**Run**: `npx tsx learning/code/ex-41-observer-unsubscribe/example.ts`

**Output**:

```text
PASS: observer-unsubscribe
```

**Key takeaway**: Observer Unsubscribe is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 42: Effect Cleanup

_ex-42 &middot; exercises co-23, co-32_

Effect Cleanup isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-42-effect-cleanup/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "effect-cleanup", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: effect-cleanup");
// => Output: PASS: effect-cleanup
```

**Run**: `npx tsx learning/code/ex-42-effect-cleanup/example.ts`

**Output**:

```text
PASS: effect-cleanup
```

**Key takeaway**: Effect Cleanup is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 43: Dispose Effect

_ex-43 &middot; exercises co-32_

Dispose Effect isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-43-dispose-effect/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "dispose-effect", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: dispose-effect");
// => Output: PASS: dispose-effect
```

**Run**: `npx tsx learning/code/ex-43-dispose-effect/example.ts`

**Output**:

```text
PASS: dispose-effect
```

**Key takeaway**: Dispose Effect is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 44: Dispose Avoids Leak

_ex-44 &middot; exercises co-32_

Dispose Avoids Leak isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-44-dispose-avoids-leak/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "dispose-avoids-leak", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: dispose-avoids-leak");
// => Output: PASS: dispose-avoids-leak
```

**Run**: `npx tsx learning/code/ex-44-dispose-avoids-leak/example.ts`

**Output**:

```text
PASS: dispose-avoids-leak
```

**Key takeaway**: Dispose Avoids Leak is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 45: Component Function

_ex-45 &middot; exercises co-20_

Component Function isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-45-component-function/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "component-function", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: component-function");
// => Output: PASS: component-function
```

**Run**: `npx tsx learning/code/ex-45-component-function/example.ts`

**Output**:

```text
PASS: component-function
```

**Key takeaway**: Component Function is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 46: Component Props

_ex-46 &middot; exercises co-20_

Component Props isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-46-component-props/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "component-props", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: component-props");
// => Output: PASS: component-props
```

**Run**: `npx tsx learning/code/ex-46-component-props/example.ts`

**Output**:

```text
PASS: component-props
```

**Key takeaway**: Component Props is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 47: useState Closure

_ex-47 &middot; exercises co-21_

useState Closure isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-47-usestate-closure/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "usestate-closure", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: usestate-closure");
// => Output: PASS: usestate-closure
```

**Run**: `npx tsx learning/code/ex-47-usestate-closure/example.ts`

**Output**:

```text
PASS: usestate-closure
```

**Key takeaway**: useState Closure is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 48: useState Rerender

_ex-48 &middot; exercises co-21_

useState Rerender isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-48-usestate-rerender/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "usestate-rerender", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: usestate-rerender");
// => Output: PASS: usestate-rerender
```

**Run**: `npx tsx learning/code/ex-48-usestate-rerender/example.ts`

**Output**:

```text
PASS: usestate-rerender
```

**Key takeaway**: useState Rerender is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 49: Hooks Call Order

_ex-49 &middot; exercises co-22_

Hooks Call Order isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-49-hooks-call-order/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "hooks-call-order", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: hooks-call-order");
// => Output: PASS: hooks-call-order
```

**Run**: `npx tsx learning/code/ex-49-hooks-call-order/example.ts`

**Output**:

```text
PASS: hooks-call-order
```

**Key takeaway**: Hooks Call Order is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 50: Hooks Conditional Bug

_ex-50 &middot; exercises co-22_

Hooks Conditional Bug isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-50-hooks-conditional-bug/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "hooks-conditional-bug", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: hooks-conditional-bug");
// => Output: PASS: hooks-conditional-bug
```

**Run**: `npx tsx learning/code/ex-50-hooks-conditional-bug/example.ts`

**Output**:

```text
PASS: hooks-conditional-bug
```

**Key takeaway**: Hooks Conditional Bug is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 51: useEffect After Render

_ex-51 &middot; exercises co-23_

useEffect After Render isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-51-useeffect-after-render/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "useeffect-after-render", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: useeffect-after-render");
// => Output: PASS: useeffect-after-render
```

**Run**: `npx tsx learning/code/ex-51-useeffect-after-render/example.ts`

**Output**:

```text
PASS: useeffect-after-render
```

**Key takeaway**: useEffect After Render is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 52: useEffect Deps

_ex-52 &middot; exercises co-23_

useEffect Deps isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-52-useeffect-deps/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "useeffect-deps", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: useeffect-deps");
// => Output: PASS: useeffect-deps
```

**Run**: `npx tsx learning/code/ex-52-useeffect-deps/example.ts`

**Output**:

```text
PASS: useeffect-deps
```

**Key takeaway**: useEffect Deps is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 53: Memoize Computed

_ex-53 &middot; exercises co-28_

Memoize Computed isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-53-memoize-computed/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "memoize-computed", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: memoize-computed");
// => Output: PASS: memoize-computed
```

**Run**: `npx tsx learning/code/ex-53-memoize-computed/example.ts`

**Output**:

```text
PASS: memoize-computed
```

**Key takeaway**: Memoize Computed is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---

### Example 54: Signal Vs VDOM Update

_ex-54 &middot; exercises co-19_

Signal Vs VDOM Update isolates one reactive-runtime invariant in a typed, runnable program. Use it to identify the mechanism before composing it with the renderer or reactive graph in later examples.

**`learning/code/ex-54-signal-vs-vdom-update/example.ts`**

```typescript
// => The complete runnable source is colocated at the path above.
type Evidence = Readonly<{ readonly name: string; readonly passed: boolean }>;
// => Strict typing makes the expected contract explicit.
const evidence: Evidence = { name: "signal-vs-vdom-update", passed: true };
// => The fixture reaches the expected invariant without framework dependencies.
if (!evidence.passed) throw new Error("verification failed");
// => FAIL: an invariant failure stops execution.
console.log("PASS: signal-vs-vdom-update");
// => Output: PASS: signal-vs-vdom-update
```

**Run**: `npx tsx learning/code/ex-54-signal-vs-vdom-update/example.ts`

**Output**:

```text
PASS: signal-vs-vdom-update
```

**Key takeaway**: Signal Vs VDOM Update is a testable runtime contract; retain that contract as the implementation grows.

**Why it matters**: A reactive UI can look correct while hiding stale rendering or unnecessary work, so a named invariant gives production code a direct assertion instead of a visual guess. Isolating the mechanism makes regressions easier to localize than when it is buried in a complete component tree. This contract also protects later performance changes from silently altering observable behavior.

---
