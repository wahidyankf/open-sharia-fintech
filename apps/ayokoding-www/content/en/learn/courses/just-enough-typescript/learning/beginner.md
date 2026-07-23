---
title: "Beginner Examples"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1-28 cover running and compiling TypeScript, a minimal `tsconfig.json`, the primitive
types, type inference, arrays and tuples, object types, `type` versus `interface`, union and literal
types, and function typing. Every example is a complete, self-contained `.ts` file (or small file
set) colocated under `learning/code/`; run each one with `tsx <file>.ts` or type-check it with
`tsc --noEmit <file>.ts` from inside its own directory, unless a caption says otherwise.

---

### Example 1: Hello tsx

_ex-01 &middot; exercises co-01_

The very first TypeScript program most people write, and the one this whole primer's "universal run
command" is built around. `tsx` transpiles and runs a `.ts` file directly, with no separate compile
step and no `tsconfig.json` required.

**`learning/code/ex-01-hello-tsx/hello.ts`**

```typescript
// Example 1: Hello tsx -- the smallest possible typed TypeScript program.
const message: string = "Hello, TypeScript!"; // => message is "Hello, TypeScript!" (type: string)
console.log(message); // => logs message to stdout
// => Output: Hello, TypeScript!
```

**Run**: `tsx hello.ts`

**Output**:

```text
Hello, TypeScript!
```

**Key takeaway**: `tsx <file>.ts` runs a TypeScript file directly -- no separate `tsc` step, no
`tsconfig.json`, no emitted `.js` file to manage.

**Why it matters**: Every runnable example in this primer starts from this same command. `tsx`
transpiles TypeScript to JavaScript in memory and executes it immediately, which is why it has
displaced the older, unmaintained `ts-node` for new projects -- you get the fast edit-run loop of a
scripting language while still writing fully typed code.

---

### Example 2: Compile With tsc

_ex-02 &middot; exercises co-01_

Besides running a file directly, `tsc` can compile a `.ts` file to plain `.js`, which `node` then runs
on its own -- the classic two-step workflow every TypeScript project ultimately relies on for
production builds.

**`learning/code/ex-02-compile-with-tsc/hello.ts`**

```typescript
// Example 2: Compile With tsc -- compiled to plain JavaScript, then run by node.
const greeting: string = "Compiled and run"; // => greeting is "Compiled and run" (type: string)
console.log(greeting); // => logs greeting to stdout
// => Output: Compiled and run
```

**Run** (captured for real -- every line below is genuine, not fabricated):

```text
$ tsc --skipLibCheck hello.ts
$ ls
hello.js  hello.ts
$ node hello.js
Compiled and run
```

**Key takeaway**: `tsc hello.ts` (with no `tsconfig.json`) emits a sibling `hello.js` next to the
source file, stripping every type annotation along the way.

**Why it matters**: This is the workflow behind every TypeScript build tool -- Next.js, Vite, and
bundlers all wrap this exact "check types, emit plain JavaScript" step. `--skipLibCheck` here avoids
this monorepo's own ambient `@types` packages polluting the check; a fresh, single-purpose project
would not need it.

---

### Example 3: Minimal tsconfig

_ex-03 &middot; exercises co-02_

A `tsconfig.json` configures the compiler once for an entire project, instead of repeating flags on
every `tsc` invocation. `tsc --noEmit` type-checks a project without writing any output files at
all -- the command this primer uses most often from here on.

**`learning/code/ex-03-minimal-tsconfig/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["*.ts"]
}
```

**`learning/code/ex-03-minimal-tsconfig/hello.ts`**

```typescript
// Example 3: Minimal tsconfig -- this file relies on the sibling tsconfig.json for its
// compiler options (target: ES2022, module: ESNext, strict: true).
const ready: boolean = true; // => ready is true (type: boolean)
console.log(ready); // => logs ready to stdout
// => Output: true
```

**Run**: `tsc --noEmit`

**Output**:

```text
(no output -- a clean type-check prints nothing and exits 0)
```

**Key takeaway**: `target`, `module`, and `strict` are the three options this primer assumes are
always set; `tsc --noEmit` silently exits `0` when everything type-checks.

**Why it matters**: `strict: true` turns on every strict-mode check at once (including
`strictNullChecks`, exercised next in Example 6) -- it is the single highest-value flag in the entire
compiler, and every real-world TypeScript project should set it from day one, not add it later once
thousands of latent bugs have accumulated.

---

### Example 4: Annotate Primitives

_ex-04 &middot; exercises co-03_

TypeScript's base type annotations mirror JavaScript's primitive values: `number`, `string`, and
`boolean` are the three you will write constantly.

**`learning/code/ex-04-annotate-primitives/example.ts`**

```typescript
// Example 4: Annotate Primitives -- explicit type annotations for number, string, boolean.
let n: number = 42; // => n is 42 (type: number)
let s: string = "typed"; // => s is "typed" (type: string)
let b: boolean = true; // => b is true (type: boolean)
console.log(n, s, b); // => Output: 42 typed true
```

**Run**: `tsx example.ts`

**Output**:

```text
42 typed true
```

**Key takeaway**: `: number`, `: string`, and `: boolean` are the annotation syntax -- a colon after
the name, then the type.

**Why it matters**: These three annotations, plus `null` and `undefined` (Example 6), cover every
JavaScript primitive except `bigint` and `symbol`, which this primer does not use. Explicit
annotations like these matter most on function parameters (Example 20) -- local variables are
usually better left to inference (Example 7).

---

### Example 5: Type Error On Mismatch

_ex-05 &middot; exercises co-03_

Assigning a value of the wrong type is exactly what the compiler exists to catch. This file is
deliberately broken -- `tsc --noEmit` reports the mismatch instead of silently accepting it.

**`learning/code/ex-05-type-error-on-mismatch/example.ts`**

```typescript
// Example 5: Type Error On Mismatch -- assigning a string to a number-typed binding.
let count: number = 42; // => count is 42 (type: number)
count = "oops"; // => TYPE ERROR: a string is not assignable to a number-typed binding
console.log(count); // => never type-checks -- tsc reports the error above first
```

**Run**: `tsc --noEmit --strict --skipLibCheck example.ts`

**Output** (the real error message `tsc` 5.8.3 prints):

```text
example.ts(3,1): error TS2322: Type 'string' is not assignable to type 'number'.
```

**Key takeaway**: `error TS2322` is the compiler's generic "type mismatch" code -- it names both the
source type (`string`) and the target type (`number`) explicitly.

**Why it matters**: This exact error shape -- `TSxxxx: Type 'A' is not assignable to type 'B'` --
recurs throughout this primer (Examples 9, 11, 13, 17, and more). Learning to read it once means every
later type error is immediately legible, instead of a wall of unfamiliar text.

---

### Example 6: Null Under Strict

_ex-06 &middot; exercises co-03_

Under `strict` mode, `null` is not automatically part of every type -- it must be explicitly included
in a union. A bare `string` binding rejects `null` outright.

**Allowed (a union explicitly includes null)**:

```typescript
// Example 6: Null Under Strict -- a union type explicitly allows null.
let x: string | null = null; // => x is null (type: string | null) -- the union permits it
console.log(x); // => Output: null
```

**Run**: `tsx example.ts`

**Output**:

```text
null
```

**Rejected (a bare `string` type has no room for null)**:

```typescript
// Example 6 (invalid): a bare string binding rejects null under strict mode.
let s: string = null; // => TYPE ERROR: null is not assignable to string under strict
console.log(s);
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(2,5): error TS2322: Type 'null' is not assignable to type 'string'.
```

**Key takeaway**: under `strict`, `null` and `undefined` are their own distinct types -- a plain
`string` never silently includes them; `string | null` does.

**Why it matters**: This one flag (`strictNullChecks`, bundled into `strict`) eliminates an entire
historical class of "cannot read property of null" runtime crashes, by forcing every nullable value
to be explicitly typed as nullable and narrowed (Example 30) before use.

---

### Example 7: Inference No Annotation

_ex-07 &middot; exercises co-04_

TypeScript infers a variable's type from its initializer -- no annotation is required, and the
inferred type is checked exactly as strictly as an explicit one.

**`learning/code/ex-07-inference-no-annotation/example.ts`**

```typescript
// Example 7: Inference No Annotation -- no type annotation, yet count is still checked.
let count = 5; // => count is 5 (type inferred: number, from the initializer)
count = 10; // => OK -- 10 is also a number
console.log(count); // => Output: 10
```

**Run**: `tsx example.ts`

**Output**:

```text
10
```

**Reassigning with a string still fails, despite no annotation ever being written**:

```typescript
// Example 7 (invalid): reassigning the inferred number binding with a string.
let count = 5; // => count's type is inferred as number
count = "six"; // => TYPE ERROR: a string is not assignable to the inferred number type
console.log(count);
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(3,1): error TS2322: Type 'string' is not assignable to type 'number'.
```

**Key takeaway**: an inferred type is not a weaker type -- `let count = 5` locks `count` to `number`
exactly as firmly as `let count: number = 5` would.

**Why it matters**: Inference is why idiomatic TypeScript reads almost like plain JavaScript --
annotations are reserved for places inference cannot reach (function parameters, empty array
literals, wide unions) rather than sprinkled on every single binding.

---

### Example 8: const Literal Inference

_ex-08 &middot; exercises co-04, co-09_

A `const` initializer infers the narrowest possible type -- the exact literal value, not the wider
primitive type a `let` binding would get.

**`learning/code/ex-08-const-literal-inference/example.ts`**

```typescript
// Example 8: const Literal Inference -- a const initializer infers a narrow literal type.
const c = "on"; // => c's inferred type is the literal "on", not the wide string
let d = "on"; // => d's inferred type widens to string, since let permits reassignment

function requireOn(mode: "on"): void {
  // => mode's parameter type only accepts the exact literal "on"
  console.log(mode); // => Output: on
}

requireOn(c); // => OK -- c's type IS the literal "on"
console.log(typeof d); // => Output: string -- widened, still a string at the type level
```

**Run**: `tsx example.ts`

**Output**:

```text
on
string
```

**A `let`-bound value has already widened, so it cannot satisfy the same narrow parameter**:

```typescript
// Example 8 (invalid): a let-bound "on" has widened to string, so it fails the literal param.
let d = "on"; // => d's inferred type is the wide string, not the literal "on"

function requireOn(mode: "on"): void {
  console.log(mode);
}

requireOn(d); // => TYPE ERROR: string is not assignable to the literal type "on"
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(8,11): error TS2345: Argument of type 'string' is not assignable to parameter of type '"on"'.
```

**Key takeaway**: `const` infers the exact literal; `let` infers the wider primitive, because a `let`
binding could later be reassigned to any other value of that primitive type.

**Why it matters**: This distinction is why `as const` (Example 56) exists -- it lets you opt an
object literal into the same narrow-literal inference a plain `const` primitive gets automatically,
which matters constantly for discriminated unions (Example 36) and config objects.

---

### Example 9: Array Type

_ex-09 &middot; exercises co-05_

`T[]` types a homogeneous, mutable list -- every element must be type `T`, and the array can grow or
shrink freely.

**`learning/code/ex-09-array-type/example.ts`**

```typescript
// Example 9: Array Type -- T[] types a homogeneous, mutable list.
const xs: number[] = [1, 2, 3]; // => xs is [1, 2, 3] (type: number[])
xs.push(4); // => push accepts only number -- mutates xs in place
console.log(xs); // => Output: [ 1, 2, 3, 4 ]
```

**Run**: `tsx example.ts`

**Output**:

```text
[ 1, 2, 3, 4 ]
```

**Pushing the wrong element type fails to compile**:

```typescript
// Example 9 (invalid): pushing a string onto a number[] fails.
const xs: number[] = [1, 2, 3];
xs.push("bad"); // => TYPE ERROR: a string argument is not assignable to number
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(3,9): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

**Key takeaway**: `number[]` (equivalently `Array<number>`) constrains every element, including ones
added later with `.push()`, `.unshift()`, or index assignment.

**Why it matters**: `T[]` is the single most common type annotation in real TypeScript code --
`.map()` (Example 27), `.filter()`, and `.reduce()` all preserve and transform it, and the whole
utility-type toolkit (Example 70 onward) frequently operates on arrays of typed objects.

---

### Example 10: readonly Array

_ex-10 &middot; exercises co-05_

`readonly T[]` removes every mutating method (`push`, `pop`, `splice`, index assignment) from the
array's type entirely -- a compile-time-only guarantee that a value will not be mutated through this
particular binding.

**`learning/code/ex-10-readonly-array/example.ts`**

```typescript
// Example 10: readonly Array -- readonly T[] removes every mutating method at compile time.
const xs: readonly number[] = [1, 2, 3]; // => xs is [1, 2, 3] (type: readonly number[])
console.log(xs[0]); // => reading by index is still allowed -- Output: 1
console.log(xs.length); // => Output: 3
```

**Run**: `tsx example.ts`

**Output**:

```text
1
3
```

**`readonly number[]` has no `push` method at all -- not a runtime check, a missing method**:

```typescript
// Example 10 (invalid): readonly number[] has no push method at all.
const xs: readonly number[] = [1, 2, 3];
xs.push(4); // => TYPE ERROR: Property 'push' does not exist on type 'readonly number[]'
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(3,4): error TS2339: Property 'push' does not exist on type 'readonly number[]'.
```

**Key takeaway**: `readonly` on an array type is enforced entirely at compile time -- the underlying
runtime array is a completely ordinary, mutable JavaScript array.

**Why it matters**: Marking a function parameter `readonly T[]` documents (and enforces) "this
function only reads its input, never mutates it" -- a cheap, precise way to communicate a contract
that would otherwise live only in a comment.

---

### Example 11: Tuple Type

_ex-11 &middot; exercises co-05_

A tuple type fixes both the length and the type at every position -- unlike `T[]`, position 0 and
position 1 can carry entirely different types.

**`learning/code/ex-11-tuple-type/example.ts`**

```typescript
// Example 11: Tuple Type -- a fixed-length, per-position-typed array.
const p: [number, number] = [1, 2]; // => p is [1, 2] (type: [number, number])
const [x, y] = p; // => destructures the tuple by position
console.log(x, y); // => Output: 1 2
```

**Run**: `tsx example.ts`

**Output**:

```text
1 2
```

**A third element does not fit a two-element tuple type**:

```typescript
// Example 11 (invalid): a third element does not fit a two-element tuple type.
const p: [number, number] = [1, 2, 3]; // => TYPE ERROR: source has too many elements
console.log(p);
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(2,7): error TS2322: Type '[number, number, number]' is not assignable to type '[number, number]'.
  Source has 3 element(s) but target allows only 2.
```

**Key takeaway**: `[number, number]` is stricter than `number[]` -- it fixes the length at exactly
two elements, not "zero or more".

**Why it matters**: Tuples are how `useState`-style APIs and multi-value returns (Example 44's `pair`
generic) stay precisely typed instead of collapsing into a loosely typed array where every element's
type is a union of all the possibilities.

---

### Example 12: Named Tuple

_ex-12 &middot; exercises co-05_

Position labels document intent for editor tooltips and code review, without changing the tuple's
runtime shape or relaxing its arity check.

**`learning/code/ex-12-named-tuple/example.ts`**

```typescript
// Example 12: Named Tuple -- position labels document intent; arity is still enforced.
const rgb: [r: number, g: number, b: number] = [255, 0, 0]; // => rgb is [255, 0, 0]
const [r, g, b] = rgb; // => labels (r, g, b) show up in editor hovers, not at runtime
console.log(r, g, b); // => Output: 255 0 0
```

**Run**: `tsx example.ts`

**Output**:

```text
255 0 0
```

**Labels do not relax the length check -- a missing element still fails**:

```typescript
// Example 12 (invalid): a named 3-tuple still rejects the wrong number of elements.
const rgb: [r: number, g: number, b: number] = [255, 0]; // => TYPE ERROR: missing element 'b'
console.log(rgb);
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(2,7): error TS2322: Type '[number, number]' is not assignable to type '[r: number, g: number, b: number]'.
  Source has 2 element(s) but target requires 3.
```

**Key takeaway**: `[r: number, g: number, b: number]` behaves identically to `[number, number,
number]` at compile time -- the labels are purely documentation.

**Why it matters**: Named tuples make `React.useState`-shaped APIs and coordinate/RGB-style values
self-documenting in an editor's hover tooltip, without the overhead of a full object type for what is
conceptually still an ordered pair (or triple) of values.

---

### Example 13: Object Type Inline

_ex-13 &middot; exercises co-06_

An inline object type lists every property and its type directly in a parameter annotation -- no
named `type` or `interface` needed for a one-off shape.

**`learning/code/ex-13-object-type-inline/example.ts`**

```typescript
// Example 13: Object Type Inline -- an inline object type annotates a parameter's shape.
function greet(person: { name: string; age: number }): string {
  // => person must have exactly a name (string) and age (number) field
  return `${person.name} is ${person.age}`; // => builds and returns a template string
}

console.log(greet({ name: "Ada", age: 36 })); // => Output: Ada is 36
```

**Run**: `tsx example.ts`

**Output**:

```text
Ada is 36
```

**Omitting a required field fails at the call-site**:

```typescript
// Example 13 (invalid): calling greet without the required age field.
function greet(person: { name: string; age: number }): string {
  return `${person.name} is ${person.age}`;
}

console.log(greet({ name: "Ada" })); // => TYPE ERROR: property 'age' is missing
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(6,19): error TS2345: Argument of type '{ name: string; }' is not assignable to parameter of type '{ name: string; age: number; }'.
  Property 'age' is missing in type '{ name: string; }' but required in type '{ name: string; age: number; }'.
```

**Key takeaway**: every property in an inline object type is required by default -- omitting one at
the call-site is a compile error, not a runtime surprise.

**Why it matters**: Inline object types are the quickest way to type a small, one-off shape; once the
same shape is reused across more than one function, a named `type` alias (Example 15) or `interface`
(Example 16) keeps the definition in one place instead of duplicated at every call-site.

---

### Example 14: Optional Property

_ex-14 &middot; exercises co-06_

`prop?:` marks a property as optional -- it may be present with its declared type, or omitted
entirely, but never `null`.

**`learning/code/ex-14-optional-property/example.ts`**

```typescript
// Example 14: Optional Property -- age? marks the field as not required.
function describe(person: { name: string; age?: number }): string {
  // => age?: number means age can be a number OR be entirely omitted
  return person.age === undefined
    ? person.name // => no age supplied -- just the name
    : `${person.name} (${person.age})`; // => age supplied -- include it
}

console.log(describe({ name: "Ada" })); // => Output: Ada
console.log(describe({ name: "Grace", age: 85 })); // => Output: Grace (85)
```

**Run**: `tsx example.ts`

**Output**:

```text
Ada
Grace (85)
```

**Key takeaway**: `age?: number` is shorthand for `age: number | undefined`, plus permission to omit
the key entirely from the object literal.

**Why it matters**: Optional properties model exactly the shape of partially filled-in data --
draft records, patch payloads, and configuration overrides -- and pair directly with `Partial<T>`
(Example 70), which turns every property of an existing type optional at once.

---

### Example 15: type Alias

_ex-15 &middot; exercises co-07_

`type` names a reusable shape so it does not need to be repeated inline at every use-site.

**`learning/code/ex-15-type-alias/example.ts`**

```typescript
// Example 15: Type Alias -- `type` names a reusable shape for later use.
type Point = { x: number; y: number }; // => Point is an alias for this exact object shape

const home: Point = { x: 0, y: 0 }; // => a matching literal satisfies Point
console.log(home); // => Output: { x: 0, y: 0 }
```

**Run**: `tsx example.ts`

**Output**:

```text
{ x: 0, y: 0 }
```

**Key takeaway**: `type Point = { ... }` gives an object shape a name that can be reused across
function signatures, variable annotations, and other type definitions.

**Why it matters**: `type` aliases work for object shapes exactly like `interface` (Example 16) does,
but `type` can ALSO alias unions (Example 18), tuples (Example 11), and any other type expression --
`interface` can only describe object (and function/class) shapes.

---

### Example 16: interface Declaration

_ex-16 &middot; exercises co-07_

`interface` declares a named object contract -- functionally similar to a `type` alias for a plain
object shape, with its own syntax and its own extension mechanism (`extends`, Example 17).

**`learning/code/ex-16-interface-declaration/example.ts`**

```typescript
// Example 16: Interface Declaration -- `interface` declares a named object contract.
interface User {
  id: number; // => every User must have a numeric id
  name: string; // => and a string name
}

const alice: User = { id: 1, name: "Alice" }; // => a conforming object satisfies User
console.log(alice); // => Output: { id: 1, name: 'Alice' }
```

**Run**: `tsx example.ts`

**Output**:

```text
{ id: 1, name: 'Alice' }
```

**Key takeaway**: `interface User { ... }` and `type User = { ... }` accept the exact same object
literals -- for a plain object shape, either works.

**Why it matters**: This primer uses `type` and `interface` roughly interchangeably for object
shapes, matching how most real codebases actually work; the one meaningful difference (`interface`
supports declaration merging and `extends`, `type` supports unions and other type expressions)
surfaces directly in Example 17 and Example 18.

---

### Example 17: Interface Extends

_ex-17 &middot; exercises co-07_

`extends` lets one interface inherit every member of another, then add its own -- a compile-time-only
relationship with no runtime class hierarchy involved.

**`learning/code/ex-17-interface-extends/example.ts`**

```typescript
// Example 17: Interface Extends -- Admin inherits every User field, plus its own.
interface User {
  id: number; // => required on User AND on anything that extends User
  name: string; // => same rule -- inherited automatically, no re-declaration needed
}

interface Admin extends User {
  // => compile-time only -- no runtime class hierarchy is created
  role: string; // => Admin requires id, name (inherited), AND role
}

const root: Admin = { id: 1, name: "Root", role: "superuser" }; // => all three fields present
console.log(root); // => Output: { id: 1, name: 'Root', role: 'superuser' }
```

**Run**: `tsx example.ts`

**Output**:

```text
{ id: 1, name: 'Root', role: 'superuser' }
```

**Omitting the extending interface's own required field still fails**:

```typescript
// Example 17 (invalid): Admin is missing role, its own required field.
interface User {
  id: number;
  name: string;
}

interface Admin extends User {
  role: string; // => still required on Admin -- root below omits it, which is why this fails
}

const root: Admin = { id: 1, name: "Root" }; // => TYPE ERROR: 'role' is missing
console.log(root); // => never reached -- tsc rejects this file before runtime
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(11,7): error TS2741: Property 'role' is missing in type '{ id: number; name: string; }' but required in type 'Admin'.
```

**Key takeaway**: `interface Admin extends User` merges `User`'s members into `Admin` -- an `Admin`
value must satisfy every field from both interfaces at once.

**Why it matters**: `extends` is TypeScript's answer to "shared base shape, specialized variants" --
the same problem intersection types (Example 52) solve for `type` aliases, at the cost of `type`
having no `extends` keyword of its own.

---

### Example 18: Union Type

_ex-18 &middot; exercises co-08_

`A | B` types a value that is EITHER `A` OR `B` -- any value assignable to either constituent
satisfies the union.

**`learning/code/ex-18-union-type/example.ts`**

```typescript
// Example 18: Union Type -- Id is EITHER a number OR a string.
type Id = number | string; // => a value assignable to Id is any number, or any string

const numericId: Id = 42; // => a number satisfies the union
const textId: Id = "user-42"; // => a string ALSO satisfies the union
console.log(numericId, textId); // => Output: 42 user-42
```

**Run**: `tsx example.ts`

**Output**:

```text
42 user-42
```

**Key takeaway**: a union widens what is ACCEPTED (either constituent works), which is the opposite
of an intersection (Example 52), which widens what is REQUIRED (every constituent's members at once).

**Why it matters**: Unions model "one of several known shapes" -- IDs that come from two systems here,
and API responses (Example 39), form fields, and configuration values throughout real code. Using a
union safely almost always means narrowing it first (Example 29 onward) before doing anything
type-specific with the value.

---

### Example 19: Literal Union

_ex-19 &middot; exercises co-09, co-08_

A specific string or number value can itself be a type. A union of several literals restricts a value
to exactly that closed set -- nothing else compiles.

**`learning/code/ex-19-literal-union/example.ts`**

```typescript
// Example 19: Literal Union -- Dir is restricted to exactly these four string literals.
type Dir = "up" | "down" | "left" | "right"; // => only these four exact strings are valid

const heading: Dir = "up"; // => "up" is one of the four allowed literals
console.log(heading); // => Output: up
```

**Run**: `tsx example.ts`

**Output**:

```text
up
```

**Any string outside the closed set fails to compile**:

```typescript
// Example 19 (invalid): "north" is not one of Dir's four allowed literals.
type Dir = "up" | "down" | "left" | "right";
const heading: Dir = "north"; // => TYPE ERROR: "north" is not assignable to Dir
console.log(heading);
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(3,7): error TS2322: Type '"north"' is not assignable to type 'Dir'.
```

**Key takeaway**: a literal union is a closed, exhaustively enumerable set -- unlike a bare `string`,
it rejects every value outside the listed literals at compile time.

**Why it matters**: Literal unions are the foundation of discriminated unions (Example 36), where a
single literal-typed "tag" field lets the compiler narrow an entire variant and enforce exhaustiveness
(Example 38) -- arguably TypeScript's single most valuable modeling pattern.

---

### Example 20: Function Typed

_ex-20 &middot; exercises co-11_

Both parameters and the return value carry their own annotations -- the compiler checks the function
body's `return` statements against the declared return type.

**`learning/code/ex-20-function-typed/example.ts`**

```typescript
// Example 20: Function Typed -- both parameters and the return value carry annotations.
function add(a: number, b: number): number {
  // => a and b must both be number; the function must return a number
  return a + b; // => a + b's result type (number) matches the declared return type
}

console.log(add(2, 3)); // => Output: 5
```

**Run**: `tsx example.ts`

**Output**:

```text
5
```

**A mismatched argument type fails at the call-site**:

```typescript
// Example 20 (invalid): a string argument does not satisfy the number parameter type.
function add(a: number, b: number): number {
  return a + b;
}

console.log(add(2, "3")); // => TYPE ERROR: string argument is not assignable to number
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(6,20): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

**Key takeaway**: parameter types are checked at every call-site; the return type is checked against
every `return` statement inside the function body.

**Why it matters**: Function typing is where annotations pay off the most -- unlike a local variable
(where inference usually suffices), a function's parameters cannot be inferred from its body alone,
so explicit annotations here are what let every CALLER benefit from type checking too.

---

### Example 21: void Return

_ex-21 &middot; exercises co-11_

`: void` marks a function whose return value carries no usable information -- `console.log` itself
returns `void`.

**`learning/code/ex-21-void-return/example.ts`**

```typescript
// Example 21: void Return -- `: void` marks a function whose return value is not usable.
function logLine(text: string): void {
  // => void means "no meaningful return value" -- console.log itself also returns void
  console.log(text); // => Output: hello
}

logLine("hello");
```

**Run**: `tsx example.ts`

**Output**:

```text
hello
```

**A `void` function's body may not actually return a value**:

```typescript
// Example 21 (invalid): a void function body may not return an actual value.
function logLine(text: string): void {
  console.log(text);
  return text; // => TYPE ERROR: string is not assignable to type 'void'
}

logLine("hello");
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(4,3): error TS2322: Type 'string' is not assignable to type 'void'.
```

**Key takeaway**: `void` is not the same as `undefined` -- it specifically means "the caller should
not use this function's return value", and the function body itself may not return a real value.

**Why it matters**: Callback parameters are frequently typed `() => void` precisely so an
implementation MAY return something (which the caller ignores) without that becoming a type error --
a subtlety not exercised further in this primer, but worth knowing when reading other TypeScript
code.

---

### Example 22: Optional Param

_ex-22 &middot; exercises co-12_

`title?` marks a parameter optional -- callers may omit it entirely, and its type inside the function
becomes `string | undefined`.

**`learning/code/ex-22-optional-param/example.ts`**

```typescript
// Example 22: Optional Param -- title? may be omitted at every call-site.
function greet(name: string, title?: string): string {
  // => title's type is `string | undefined`; a call may omit it entirely
  return title === undefined ? `Hi, ${name}` : `Hi, ${title} ${name}`;
}

console.log(greet("Ada")); // => Output: Hi, Ada -- called with ONE argument, type-checks fine
console.log(greet("Ada", "Dr.")); // => Output: Hi, Dr. Ada
```

**Run**: `tsx example.ts`

**Output**:

```text
Hi, Ada
Hi, Dr. Ada
```

**Key takeaway**: an optional parameter must come after every required one, and its type inside the
function body is always a union with `undefined`.

**Why it matters**: Optional parameters keep a function's common case call-site short (`greet("Ada")`)
while still supporting an occasional extra argument -- the parameter-level counterpart to optional
object properties (Example 14).

---

### Example 23: Default Param

_ex-23 &middot; exercises co-12_

A default value supplies itself whenever the caller omits that argument -- the parameter's type is
inferred from the default when no annotation is written.

**`learning/code/ex-23-default-param/example.ts`**

```typescript
// Example 23: Default Param -- exp = 2 supplies a value whenever the caller omits it.
function pow(base: number, exp: number = 2): number {
  // => exp's type is inferred as number from its default value 2
  return base ** exp; // => exponentiation
}

console.log(pow(3)); // => exp omitted, defaults to 2 -- Output: 9
console.log(pow(2, 5)); // => exp explicitly 5 -- Output: 32
```

**Run**: `tsx example.ts`

**Output**:

```text
9
32
```

**Key takeaway**: unlike an optional parameter, a defaulted one's type inside the function body is
NOT a union with `undefined` -- it always resolves to a concrete value, either the argument or the
default.

**Why it matters**: Defaults remove an entire class of `if (exp === undefined) exp = 2;`
boilerplate that optional parameters alone would require, and they compose naturally with rest
parameters (Example 24) for flexible, ergonomic function signatures.

---

### Example 24: Rest Params

_ex-24 &middot; exercises co-12_

`...nums: number[]` collects every remaining argument into a single typed array -- the variadic
counterpart to a fixed parameter list.

**`learning/code/ex-24-rest-params/example.ts`**

```typescript
// Example 24: Rest Params -- ...nums collects every remaining argument into number[].
function sum(...nums: number[]): number {
  // => nums is a typed array of every argument passed after none required before it
  return nums.reduce((total, n) => total + n, 0); // => folds the array into one total
}

console.log(sum(1, 2, 3)); // => Output: 6
console.log(sum()); // => zero arguments is valid too -- Output: 0
```

**Run**: `tsx example.ts`

**Output**:

```text
6
0
```

**Every rest argument is still checked against its element type**:

```typescript
// Example 24 (invalid): a string argument does not fit the number[] rest parameter.
function sum(...nums: number[]): number {
  return nums.reduce((total, n) => total + n, 0);
}

console.log(sum(1, "two", 3)); // => TYPE ERROR: string is not assignable to number
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(6,20): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

**Key takeaway**: a rest parameter's array type applies to EVERY collected argument, no matter how
many are passed -- including zero.

**Why it matters**: Rest parameters power variadic utility functions (`Math.max`-style helpers,
logging wrappers) while keeping every argument fully typed, unlike JavaScript's older `arguments`
object, which carries no type information at all.

---

### Example 25: Arrow Function Typed

_ex-25 &middot; exercises co-13_

Arrow functions carry the exact same parameter and return-type annotations as a `function`
declaration.

**`learning/code/ex-25-arrow-function-typed/example.ts`**

```typescript
// Example 25: Arrow Function Typed -- arrow functions carry the same annotations as `function`.
const double = (n: number): number => n * 2; // => n: number in, number out

console.log(double(21)); // => Output: 42
```

**Run**: `tsx example.ts`

**Output**:

```text
42
```

**Key takeaway**: `(n: number): number => n * 2` annotates an arrow function identically to a named
`function` declaration -- parameters first, then the return type after the parameter list.

**Why it matters**: Arrow functions are the default choice for callbacks (Example 27) and short
utility functions throughout the rest of this primer; this typing syntax is exactly what appears
inside `.map()`, `.filter()`, and `.reduce()` calls, whether written explicitly or left to inference.

---

### Example 26: Function Type Expression

_ex-26 &middot; exercises co-13_

A function type expression -- `(n: number) => string` -- types a standalone variable or parameter as
"a function shaped like this", independent of any particular implementation.

**`learning/code/ex-26-function-type-expression/example.ts`**

```typescript
// Example 26: Function Type Expression -- a standalone type for "a function shaped like this".
let format: (n: number) => string; // => format must be a function: takes number, returns string

format = (n) => `#${n}`; // => this arrow matches the (n: number) => string shape exactly
console.log(format(7)); // => Output: #7
```

**Run**: `tsx example.ts`

**Output**:

```text
#7
```

**Assigning a function with the wrong return type fails to compile**:

```typescript
// Example 26 (invalid): this arrow returns a number, not the required string.
let format: (n: number) => string;

format = (n) => n * 2; // => TYPE ERROR: returns number, but the type expression requires string
console.log(format(7));
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(4,17): error TS2322: Type 'number' is not assignable to type 'string'.
```

**Key takeaway**: `(n: number) => string` describes a function's SHAPE, not a specific
implementation -- any arrow or `function` matching that parameter and return type satisfies it.

**Why it matters**: This is exactly how a callback PARAMETER's type is written (Example 27's `.map()`
callback is inferred from an expression shaped like this), and it is how you type a variable meant to
hold "whichever function is currently the active handler" in event-driven or strategy-pattern code.

---

### Example 27: Typed Callback Param

_ex-27 &middot; exercises co-13, co-04_

`Array.prototype.map` infers a callback's element parameter type from the array it is called on -- no
annotation needs to be written on the callback itself.

**`learning/code/ex-27-typed-callback-param/example.ts`**

```typescript
// Example 27: Typed Callback Param -- Array.prototype.map infers the element type for you.
const nums: number[] = [1, 2, 3]; // => nums is number[]

const doubled = nums.map((n) => n * 2); // => n is inferred as number -- no annotation written
console.log(doubled); // => Output: [ 2, 4, 6 ]
```

**Run**: `tsx example.ts`

**Output**:

```text
[ 2, 4, 6 ]
```

**Proof: misusing `n` as if it were a string fails, confirming it really is inferred as `number`**:

```typescript
// Example 27 (invalid): proves n really is inferred as number, not string or any.
const nums: number[] = [1, 2, 3];

const shouty = nums.map((n) => n.toUpperCase()); // => TYPE ERROR: number has no toUpperCase
console.log(shouty);
```

**Run**: `tsc --noEmit --strict --skipLibCheck invalid.ts`

**Output**:

```text
invalid.ts(4,34): error TS2339: Property 'toUpperCase' does not exist on type 'number'.
```

**Key takeaway**: array-method callbacks (`.map`, `.filter`, `.forEach`, `.reduce`) all infer their
parameter types from the array's element type -- writing `(n: number) =>` here would be correct but
redundant.

**Why it matters**: This contextual inference is why idiomatic TypeScript callbacks stay unannotated
almost everywhere -- the compiler already knows the array's element type, so repeating it on every
callback parameter would be pure noise.

---

### Example 28: Run Typed Script tsx

_ex-28 &middot; exercises co-01_

A slightly larger, self-contained script -- several typed functions working together, run end to end
with `tsx` -- closing out the beginner tier exactly the way it opened: one command, real output.

**`learning/code/ex-28-run-typed-script-tsx/example.ts`**

```typescript
// Example 28: Run Typed Script tsx -- several typed functions, run end to end with tsx.
function celsiusToFahrenheit(c: number): number {
  return (c * 9) / 5 + 32; // => the standard C-to-F conversion formula
}

function describeTemp(f: number): string {
  // => a plain if/else chain -- categorizes a Fahrenheit reading
  if (f < 32) return "freezing"; // => below the freezing point of water
  if (f < 70) return "cool"; // => between freezing and 70
  return "warm"; // => 70 and above
}

const readings: number[] = [0, 20, 37]; // => three Celsius readings to process
for (const c of readings) {
  // => loops over each reading, converting and describing it
  const f = celsiusToFahrenheit(c); // => f is the Fahrenheit equivalent of c
  console.log(`${c}C -> ${f}F (${describeTemp(f)})`);
  // => Output: one line per reading
}
```

**Run**: `tsx example.ts`

**Output**:

```text
0C -> 32F (cool)
20C -> 68F (cool)
37C -> 98.6F (warm)
```

**Key takeaway**: nothing here is new syntax -- it is Examples 1-27's mechanisms (typed functions,
arrays, `for...of`, template strings) composed into one small, real program.

**Why it matters**: This is the shape every later example in this primer builds toward: a handful of
small, individually typed functions, composed together, run with the exact same `tsx` command that
opened Example 1. The Intermediate tier starts here with narrowing -- the mechanism that makes working
with union types (Example 18) safe in practice.

---

← Previous: [Overview](./overview.md) · Next: [Intermediate Examples](./intermediate.md) →
