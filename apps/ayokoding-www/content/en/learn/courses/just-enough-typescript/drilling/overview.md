---
title: "Overview"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Just Enough TypeScript primer: five fixed
drills that force active recall instead of passive re-reading. Work through them in order --
short-answer recall first, then scenario judgment, then hands-on repetition, then a checklist to
confirm real automaticity, and finally why/why-not prompts that test whether you can explain the
reasoning, not just execute the syntax. Every answer is hidden in a `<details>` block; try each
item yourself before opening it.

## Recall Q&A

Twenty-six short-answer questions, one per concept (`co-01` through `co-26`). Answer from memory,
then check.

**Q1 (co-01 -- running-ts).** Name the two ways to execute a `.ts` file, and which one produces no
separate `.js` output file at all.

<details>
<summary>Answer</summary>

`tsc` compiles the file to a sibling `.js` file, which `node` then runs (Example 2) -- a two-step
workflow. `tsx` transpiles and runs a `.ts` file directly, in memory, with no emitted file at all
(Example 1) -- that's the one with no separate output file.

</details>

**Q2 (co-02 -- minimal-tsconfig).** What does `tsc --noEmit` do differently from a plain `tsc` run,
and what three options does this primer's minimal `tsconfig.json` always set?

<details>
<summary>Answer</summary>

`tsc --noEmit` type-checks the project and reports errors without writing any output files at all.
A plain `tsc` run does the same checking but also emits compiled `.js`. The three always-set
options: `target: ES2022`, `module: ESNext`, and `strict: true`.

</details>

**Q3 (co-03 -- primitive-types).** Name TypeScript's five base annotations this primer covers, and
state what `strict` mode does to `null`/`undefined`'s assignability.

<details>
<summary>Answer</summary>

`string`, `number`, `boolean`, `null`, and `undefined`. Under `strict`, `null` and `undefined` are
NOT automatically part of every type -- a bare `string` rejects `null` outright; only an explicit
union like `string | null` allows it (Example 6).

</details>

**Q4 (co-04 -- type-inference).** If you write `let count = 5` with no annotation, what type does
`count` get inferred as, and when should you add an explicit annotation instead of relying on
inference?

<details>
<summary>Answer</summary>

`number`, widened from the literal `5` (Example 7). Add an explicit annotation where inference
would be too wide or is simply unavailable -- most commonly on function parameters, since
TypeScript can't infer a parameter's type backward from how the function body happens to use it
(Example 20).

</details>

**Q5 (co-05 -- arrays-and-tuples).** What's the difference between `T[]` and a tuple type
`[T, T]`, and what does prefixing an array type with `readonly` prevent?

<details>
<summary>Answer</summary>

`T[]` types a homogeneous list of any length; a tuple fixes both the length and each position's own
type. `readonly T[]` makes every mutating method (`.push()`, `.pop()`, index assignment) a compile
error (Example 10).

</details>

**Q6 (co-06 -- object-types).** What does `prop?:` mean on an object type, and what compiler check
fires when you pass an object literal with a field the type doesn't declare?

<details>
<summary>Answer</summary>

`prop?:` marks the property optional -- callers may omit it entirely (Example 14). Passing an
object literal directly with an undeclared extra field triggers the excess-property check, a
compile error (Example 50, Kata 1).

</details>

**Q7 (co-07 -- type-vs-interface).** Name one thing `interface` supports that a plain `type` alias
in this primer's coverage does not.

<details>
<summary>Answer</summary>

`interface X extends Y` -- declaring an object contract that extends another interface, inheriting
and adding fields (Example 17). `type` describes any type shape (unions, tuples, primitives) but
has no dedicated `extends` keyword form of its own.

</details>

**Q8 (co-08 -- union-types).** What must happen before you can use a union-typed value in a way
specific to only one of its member types?

<details>
<summary>Answer</summary>

Narrowing (co-14) must run first -- a `typeof`, truthiness, `in`, or `instanceof` check that proves
which member type the value actually is in that branch. Without it, the compiler only lets you use
operations valid on every member of the union at once.

</details>

**Q9 (co-09 -- literal-types).** Why does `const c = "on"` give `c` the literal type `"on"` rather
than the wider `string`, while `let c = "on"` would not?

<details>
<summary>Answer</summary>

`const` bindings can never be reassigned, so TypeScript infers the narrowest possible type -- the
literal value itself. `let` allows later reassignment to any other string, so its initializer's
type widens to the general `string` to leave room for that.

</details>

**Q10 (co-10 -- intersection-types).** What does `A & B` require of a value, in contrast to what
`A | B` requires?

<details>
<summary>Answer</summary>

`A & B` requires the value to satisfy every member type at once -- all of `A`'s members and all of
`B`'s members together (Example 52). `A | B` requires only that the value be one specific type from
the set, never all of them simultaneously.

</details>

**Q11 (co-11 -- function-typing).** What does annotating a function's return type as `void`
communicate, and what happens if a body declared `void` contains `return someValue;`?

<details>
<summary>Answer</summary>

`void` communicates that the function returns no usable value, and callers shouldn't rely on its
result. Returning an actual value from a function whose declared return type is `void` is a
compile error (Example 21).

</details>

**Q12 (co-12 -- optional-default-rest-params).** Name the three ways a function parameter can
accept fewer explicit arguments than declared, and how each is written.

<details>
<summary>Answer</summary>

Optional (`x?: T`, may be omitted entirely, Example 22), default (`x: T = value`, uses the default
when omitted, Example 23), and rest (`...xs: T[]`, collects any number of trailing arguments --
including zero -- into a typed array, Example 24).

</details>

**Q13 (co-13 -- arrow-and-function-type-expressions).** What does the type
`(n: number) => string` describe, and what kinds of values satisfy it?

<details>
<summary>Answer</summary>

A function type expression: any callable taking one `number` parameter and returning a `string`.
An arrow function, a `function` expression, or a named function reference can all satisfy it, as
long as the parameter and return types line up (Example 26).

</details>

**Q14 (co-14 -- narrowing).** Name four different syntactic checks that TypeScript's control-flow
analysis recognizes as narrowing a union type inside a branch.

<details>
<summary>Answer</summary>

`typeof x === "..."` (Example 29), plain truthiness (`if (x)`, Example 30), the `in` operator
(`"role" in obj`, Example 31), and `instanceof` (`x instanceof Date`, Example 32) -- an equality
check against a literal narrows too (Example 33).

</details>

**Q15 (co-15 -- type-guards-user-defined).** What return-type syntax turns an ordinary
boolean-returning function into a user-defined type guard the compiler trusts at every call site?

<details>
<summary>Answer</summary>

`x is T` as the declared return type (e.g. `function isCat(a: Animal): a is Cat`), in place of a
plain `boolean` (Example 34). An `asserts x is T` return type does the same for a function that
throws instead of returning `false` (Example 35).

</details>

**Q16 (co-16 -- discriminated-unions).** What role does a shared literal "tag" field play in a
discriminated union, and what does a `never`-typed default case in a `switch` over that tag
guarantee?

<details>
<summary>Answer</summary>

The tag field (e.g. `kind`) lets a `switch`/`if` narrow the whole union to exactly one variant per
branch, purely from the tag's literal value (Example 37). A `never`-typed default case guarantees,
at compile time, that every variant has a matching case -- if a new variant is added without one,
assigning the unhandled value to `never` fails to compile (Example 38, Kata 2).

</details>

**Q17 (co-17 -- generics).** What do `extends` and `= DefaultType` do to a generic type parameter
`<T>`, respectively?

<details>
<summary>Answer</summary>

`extends` constrains what shapes `T` may legally be, restricting it to types with certain members
(e.g. `T extends { length: number }`, Example 42, Kata 4). `= DefaultType` supplies a default type
argument used automatically when a caller omits an explicit one (Example 43).

</details>

**Q18 (co-18 -- unknown-any-never).** Rank `any`, `unknown`, and `never` from "opts out of type
checking entirely" to "no value can ever have this type," and state what each actually is.

<details>
<summary>Answer</summary>

`any` opts out of checking entirely -- every operation on it compiles, unchecked (Example 47).
`unknown` is the safe top type: every value is assignable to it, but nothing may be done with it
until it's narrowed (Example 46). `never` is the empty bottom type: it represents a value that can
never exist, such as unreachable code or a function that always throws (Example 48).

</details>

**Q19 (co-19 -- structural-typing).** Does an object need to explicitly declare a relationship
(like `implements SomeInterface`) to satisfy a TypeScript type? Why or why not?

<details>
<summary>Answer</summary>

No. Type compatibility is decided purely by shape -- "structural typing." Any object with the
required members satisfies a type, with no declared relationship needed at all (Example 51).

</details>

**Q20 (co-20 -- type-assertions).** What real runtime risk do `x!` and `x as T` share, that `as
const` does not?

<details>
<summary>Answer</summary>

Both `x!` and `x as T` tell the compiler "trust me, I know more than you do" with zero runtime
check backing that claim -- if the author is wrong, the program misbehaves or crashes with no
compile-time warning (Example 54, Example 55, Kata 5). `as const` carries no such risk: it only
narrows literal inference and adds `readonly`, it never overrides what the compiler can already
prove.

</details>

**Q21 (co-21 -- enums-and-const-assertions).** What two things does `{...} as const` do to an
object literal that plain `{...}` does not, and how does that enable the modern `keyof typeof`
alternative to `enum`?

<details>
<summary>Answer</summary>

`as const` infers every property as its narrowest literal type (instead of the wide primitive) and
makes the whole object deeply `readonly` (Example 56). Combined with `keyof typeof`, this derives a
literal-union type straight from the object's own keys -- an alternative to `enum` that needs no
dedicated keyword (Example 58).

</details>

**Q22 (co-22 -- modules-esm).** What is the one guarantee `import type` makes about the compiled
output that a regular `import` does not?

<details>
<summary>Answer</summary>

`import type` is guaranteed to be erased completely at compile time -- it produces zero runtime
code and has zero side effects (Example 63). A regular `import` may execute the imported module and
keeps a runtime binding to whatever it imports.

</details>

**Q23 (co-23 -- promises-async-await).** What type does a caught error have inside an `async`
function's `catch` block under `strict`, and what must happen before using it?

<details>
<summary>Answer</summary>

`unknown` (Example 67) -- the same `useUnknownInCatchVariables` behavior that applies to every
`catch` under `strict`. It must be narrowed (most commonly `instanceof Error`) before any property
on it may be accessed.

</details>

**Q24 (co-24 -- utility-types).** Name the utility type that makes every property of `T` optional,
and the one that makes every property required (removing optionality).

<details>
<summary>Answer</summary>

`Partial<T>` makes every property optional (Example 70). `Required<T>` makes every property
required, stripping away any `?` (Example 73).

</details>

**Q25 (co-25 -- keyof-and-index-signatures).** For `type Point = { x: number; y: number }`, what
does `keyof Point` evaluate to, and what does an index signature `{ [key: string]: number }` allow
that a fixed object type does not?

<details>
<summary>Answer</summary>

`keyof Point` is exactly `"x" | "y"` -- the union of the type's own property names (Example 59). An
index signature allows an open-ended, arbitrary set of string keys, rather than a fixed, enumerated
list, each mapping to the declared value type (Example 60).

</details>

**Q26 (co-26 -- tooling-eslint-prettier).** What is the division of labor between `eslint` and
`prettier`, and how do you invoke each to check without modifying files?

<details>
<summary>Answer</summary>

`eslint` flags likely bugs and code smells -- linting. `prettier` enforces a canonical formatting
style -- spacing, quotes, line breaks. `eslint <file>` reports without fixing (`--fix` applies
fixes); `prettier --check <file>` reports formatting violations without writing changes (`--write`
applies them, Examples 77-78).

</details>

## Applied problems

Eleven scenarios. Each describes a task without naming the construct -- decide which TypeScript
feature or idiom solves it, then check.

**AP1.** You pass a config object literal directly to a function expecting a narrower object type,
and `tsc` rejects it for one extra field the literal has. You store the exact same object shape in
a variable first, then pass that variable instead -- and it compiles clean, with no other change.
What's going on?

<details>
<summary>Answer</summary>

The excess-property check only fires against an object literal written directly at the call site --
there, an extra field can only be a mistake, since the literal exists nowhere else to be
intentionally wider. Once the value is stored in a variable first, TypeScript falls back to its
general, more permissive structural-typing rule: any object with at least the required members
satisfies the type, extra members and all (Kata 1).

</details>

**AP2.** Two coworkers debug the same `catch (err) { ... err.message ... }` block, on the exact same
TypeScript version and `strict` tsconfig. One's code compiles cleanly; yours doesn't. What's the
likely difference in how `err` -- or an intermediate step -- ended up typed?

<details>
<summary>Answer</summary>

Under `strict`, a caught error's default type is `unknown`, which requires narrowing (e.g.
`instanceof Error`) before `.message` compiles (Kata 3). The coworker's version likely narrows `err`
first, or their tsconfig doesn't actually have `strict`/`useUnknownInCatchVariables` on, which
silently falls back to the old, unsafe `any` typing for caught errors.

</details>

**AP3.** You write `if (isReady(x)) { x.doSomething(); }`, where `isReady` is declared
`function isReady(x: unknown): boolean`. Inside the `if`, `x` is still typed `unknown`, and
`.doSomething()` fails to compile -- even though the boolean genuinely proves `x` is ready at
runtime. What single change to `isReady`'s signature fixes it, with zero change to its body?

<details>
<summary>Answer</summary>

Change the declared return type from `boolean` to a type predicate: `x is Ready` (Example 34).
Narrowing does not automatically cross a function-call boundary -- a plain `boolean` return tells
the compiler nothing about what became true when it's `true`. A type predicate is the explicit
contract that lets the caller's branch narrow, exactly what a plain boolean can never express on
its own.

</details>

**AP4.** A `switch` over a discriminated union's tag field used to compile cleanly. A teammate added
a new tagged variant to the union elsewhere in the codebase, and now the exact same `switch` fails
to compile, with an error mentioning `never`. What broke, and what's the fix?

<details>
<summary>Answer</summary>

The `switch`'s `default` case narrows the unhandled remainder of the union to `never` and assigns it
to a `never`-typed binding -- that only compiles when every variant is truly handled above it. The
new variant isn't handled by any existing `case`, so inside `default` the value is still that new
variant's type, not `never`, and the assignment fails (Kata 2). The fix is adding a `case` for the
new variant.

</details>

**AP5.** A generic helper reads `.length` off its type parameter `T` inside the function body, and
the function itself fails to compile -- with no caller in sight yet. What's missing from `T`'s
declaration?

<details>
<summary>Answer</summary>

A constraint: `<T extends { length: number }>` instead of a bare `<T>` (Kata 4). An unconstrained
`T` could be instantiated with any type at any call site, so the compiler has no grounds to assume
it has a `.length` -- or any property -- unless the signature says so explicitly.

</details>

**AP6.** A generic `getValue(obj, key)` helper constrains `key`'s type to `K extends keyof T`. A
call site passes a hardcoded, misspelled key string, and it fails to compile with an error listing
the exact valid key names. What made that typo catchable at compile time instead of surfacing as
`undefined` at runtime?

<details>
<summary>Answer</summary>

`keyof T` evaluates to the literal union of `T`'s actual property names (e.g. `"id" | "name"`), and
constraining `key`'s type parameter to that union means only those exact strings are valid
arguments -- a misspelled string simply isn't a member of the union, so `tsc` rejects it before the
program ever runs (Kata 6).

</details>

**AP7.** A module imports a class using `import type { ApiError } from "./errors"`, purely to use
`ApiError` as a type annotation elsewhere in the file. Later, someone adds
`throw new ApiError(...)` to the same file, using that same import, and it fails to compile with an
error about "cannot be used as a value." What's the fix?

<details>
<summary>Answer</summary>

Change `import type { ApiError }` to a regular `import { ApiError }`. `import type` is a promise,
enforced by the compiler, that the import produces zero runtime code -- so referencing the imported
name in a value position (`new ApiError(...)`) is a hard compile error, not a runtime surprise
(Kata 7).

</details>

**AP8.** `const [n, s] = await Promise.all([fetchNumber(), fetchString()]);` correctly types `n` as
`number` and `s` as `string`. If you instead give the array literal passed to `Promise.all` an
explicit `: Promise<number | string>[]` annotation before the call, what happens to `n` and `s`'s
types, and why?

<details>
<summary>Answer</summary>

Both `n` and `s` become `number | string`, losing their per-position precision (Example 68). Without
the explicit annotation, TypeScript infers each array element as its own distinct promise type and
`Promise.all` preserves that as a tuple, position by position. Force-widening the array to a single
homogeneous `Promise<number | string>[]` type throws that positional information away before
`Promise.all` ever sees it -- the wider annotation is a real loss, not a harmless simplification.

</details>

**AP9.** A numeric enum's members were deliberately started at `1`, not the default `0` (e.g. so `0`
can mean "unset" elsewhere in the codebase). Later code does `EnumName[0]`, expecting the first
member's name back, and gets a surprising result at runtime -- with zero compile error. What value
does it actually get, and why didn't `tsc` catch it?

<details>
<summary>Answer</summary>

`undefined` -- there is no enum member whose numeric value is `0`, so the reverse-mapping lookup
finds nothing (Kata 8). `tsc` doesn't catch it because a numeric enum's reverse-mapping indexer is
typed to accept any `number`, not just the specific numbers the enum's own members happen to use --
the index expression itself is perfectly well-typed, it's just semantically wrong for this
particular enum's numbering.

</details>

**AP10.** `const user = findUser(id)!;` compiles cleanly and works for most `id`s during testing. In
production, one specific `id` causes a runtime crash reading a property off `user`. `tsc --noEmit`
reported zero errors before shipping. What guarantee did the `!` actually make, and what didn't it
check?

<details>
<summary>Answer</summary>

`!` made no runtime guarantee at all -- it only silenced the compiler's `T | null` warning, on the
author's unchecked word that the result would never actually be `null` (Kata 5). It performs zero
runtime check, so when `findUser` genuinely does return `null` for that one `id`, nothing catches
it: the crash surfaces later, at `user.name`, not at the assertion itself.

</details>

**AP11.** A function's parameter is typed `{ id: number }`, intended to accept exactly a minimal
identifier shape. A caller passes a full `User` object (with a dozen extra fields) stored in a
variable, and it compiles without complaint. Is this a type-system bug, or working as designed --
and what's the underlying rule?

<details>
<summary>Answer</summary>

Working as designed. TypeScript's structural typing only requires a value to have **at least** the
declared members -- extra members are always allowed once the value comes from a variable, not a
literal written directly at the call site (Example 49). This is the same rule that makes Kata 1's
fix legitimate rather than a loophole: only a bare literal gets the stricter excess-property check.

</details>

## Code katas

Eight hands-on repetition drills. Each is a before/after `.ts` file (or small file set) colocated
under `drilling/code/`. Every "before" file is real, actually-checked-and-run TypeScript that
misapplies the concept being drilled -- run it yourself (`tsc --noEmit --strict --skipLibCheck` and
`tsx`, the same 5.8.3/4.21.0 toolchain used throughout `learning/`), diagnose the failure from the
observed compiler or runtime behavior, fix it from memory, then compare your fix against the "after"
file and the model solution before checking your work against the actually-executed output shown.

### Kata 1 -- excess-property check: literal vs. variable

**Task.** `printPoint` accepts a `Point2D` (`{ x, y }`). Passing an object literal with an extra `z`
field directly should fail the excess-property check. The version below does exactly that -- it
never compiles.

**Before** (`drilling/code/kata-01-excess-property-literal-vs-variable/before/kata.ts`)

```typescript
// Kata 1 (before): an object literal with an extra field fails excess-property checking.
type Point2D = { x: number; y: number };

function printPoint(p: Point2D): void {
  console.log(`(${p.x}, ${p.y})`);
}

printPoint({ x: 1, y: 2, z: 3 });
```

**Observed (buggy) output** (captured by actually running `tsc --noEmit --strict --skipLibCheck
kata.ts` -- it fails to compile):

```text
kata.ts(8,26): error TS2353: Object literal may only specify known properties, and 'z' does not exist in type 'Point2D'.
```

**After** (`drilling/code/kata-01-excess-property-literal-vs-variable/after/kata.ts`)

```typescript
// Kata 1 (after): storing the literal in a variable first sidesteps the excess-property check.
type Point2D = { x: number; y: number };

function printPoint(p: Point2D): void {
  console.log(`(${p.x}, ${p.y})`);
}

const point3D = { x: 1, y: 2, z: 3 };
printPoint(point3D);
```

<details>
<summary>Model solution</summary>

```typescript
type Point2D = { x: number; y: number };

function printPoint(p: Point2D): void {
  console.log(`(${p.x}, ${p.y})`);
}

// THE FIX: bind the literal to a variable BEFORE passing it -- point3D's inferred
// type (x, y, z) is checked structurally against Point2D, and structural typing
// only requires x and y to be present -- extra members through a variable are fine.
const point3D = { x: 1, y: 2, z: 3 };
printPoint(point3D); // => Output: (1, 2)
```

**Root cause**: the excess-property check is a narrow, deliberate exception to TypeScript's
otherwise permissive structural typing -- it exists specifically for object literals written
directly at a call site, because there's no legitimate reason such a literal would carry a field
the target type doesn't declare, so an extra field there is almost always a typo. Once the same
shape is stored in a variable first, the general structural rule applies again: any value with at
least the required members satisfies the type.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
(1, 2)
```

</details>

### Kata 2 -- missing never-exhaustiveness after a new variant

**Task.** `area` computes a `Shape`'s area via a `switch` on `kind`, with a `never`-typed `default`
case enforcing exhaustiveness. A `"triangle"` variant was added to the `Shape` union, but the
`switch` was never updated -- it no longer compiles.

**Before** (`drilling/code/kata-02-missing-never-exhaustiveness/before/kata.ts`)

```typescript
// Kata 2 (before): a NEW "triangle" variant was added, but the switch was never updated --
// the never-typed exhaustiveness check catches the gap at compile time.
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2;
    case "square":
      return shape.s * shape.s;
    default: {
      const _exhaustive: never = shape;
      return _exhaustive;
    }
  }
}

console.log(area({ kind: "triangle", base: 4, height: 3 }));
```

**Observed (buggy) output** (captured by actually running `tsc --noEmit --strict --skipLibCheck
kata.ts` -- it fails to compile):

```text
kata.ts(15,13): error TS2322: Type '{ kind: "triangle"; base: number; height: number; }' is not assignable to type 'never'.
```

**After** (`drilling/code/kata-02-missing-never-exhaustiveness/after/kata.ts`)

```typescript
// Kata 2 (after): a "triangle" case handles the new variant -- the switch is exhaustive again.
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2;
    case "square":
      return shape.s * shape.s;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default: {
      const _exhaustive: never = shape;
      return _exhaustive;
    }
  }
}

console.log(area({ kind: "triangle", base: 4, height: 3 }));
```

<details>
<summary>Model solution</summary>

```typescript
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2;
    case "square":
      return shape.s * shape.s;
    // THE FIX: a matching case for the new "triangle" variant -- once every
    // variant has a case above it, shape narrows all the way to never below.
    case "triangle":
      return (shape.base * shape.height) / 2; // => 4 * 3 / 2 = 6
    default: {
      const _exhaustive: never = shape; // => now compiles: nothing reaches here unhandled
      return _exhaustive;
    }
  }
}

console.log(area({ kind: "triangle", base: 4, height: 3 })); // => Output: 6
```

**Root cause**: the `never`-typed `default` case is a deliberate compile-time tripwire -- it only
type-checks when the `switch` above it has genuinely eliminated every union member, leaving nothing
but `never` behind. Adding a union variant without a matching `case` means that variant's own type
(not `never`) reaches `default`, and assigning it to a `never`-typed binding fails -- exactly the
signal that a real code path was left unhandled.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
6
```

</details>

### Kata 3 -- unknown caught error, used before narrowing

**Task.** `run` catches whatever `risky` throws and logs its `.message`. Under `strict`, a caught
error's type defaults to `unknown` -- reading `.message` off it directly, with no narrowing, fails
to compile.

**Before** (`drilling/code/kata-03-unknown-caught-error/before/kata.ts`)

```typescript
// Kata 3 (before): a caught error's type is unknown under strict -- .message fails to compile.
function risky(): void {
  throw new Error("network timeout");
}

function run(): void {
  try {
    risky();
  } catch (err) {
    console.log(err.message);
  }
}

run();
```

**Observed (buggy) output** (captured by actually running `tsc --noEmit --strict --skipLibCheck
kata.ts` -- it fails to compile):

```text
kata.ts(10,17): error TS18046: 'err' is of type 'unknown'.
```

**After** (`drilling/code/kata-03-unknown-caught-error/after/kata.ts`)

```typescript
// Kata 3 (after): narrow err with instanceof Error before reading .message.
function risky(): void {
  throw new Error("network timeout");
}

function run(): void {
  try {
    risky();
  } catch (err) {
    if (err instanceof Error) {
      console.log(err.message);
    }
  }
}

run();
```

<details>
<summary>Model solution</summary>

```typescript
function risky(): void {
  throw new Error("network timeout");
}

function run(): void {
  try {
    risky();
  } catch (err) {
    // THE FIX: instanceof Error narrows err's type from unknown to Error inside this branch.
    if (err instanceof Error) {
      console.log(err.message); // => .message is safe now -- Output: network timeout
    }
  }
}

run();
```

**Root cause**: JavaScript's `throw` can throw any value at all, not just an `Error`, so `strict`
types a caught error as `unknown` -- honest about "this could be anything" -- rather than assuming
the common case and risking a crash on the uncommon one. `unknown` compiles nothing until it's
narrowed; `instanceof Error` is the narrowing check that proves, in this branch, `err` genuinely has
a `.message`.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
network timeout
```

</details>

### Kata 4 -- generic function with no constraint

**Task.** `longest` should return whichever of its two same-typed arguments has the greater
`.length`. The version below leaves `T` completely unconstrained, so the compiler has no proof `T`
has a `.length` at all -- it never compiles.

**Before** (`drilling/code/kata-04-generic-missing-constraint/before/kata.ts`)

```typescript
// Kata 4 (before): T has no constraint, so the compiler can't prove it has a .length at all.
function longest<T>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

console.log(longest("hi", "hello"));
```

**Observed (buggy) output** (captured by actually running `tsc --noEmit --strict --skipLibCheck
kata.ts` -- it fails to compile, once per access):

```text
kata.ts(3,12): error TS2339: Property 'length' does not exist on type 'T'.
kata.ts(3,24): error TS2339: Property 'length' does not exist on type 'T'.
```

**After** (`drilling/code/kata-04-generic-missing-constraint/after/kata.ts`)

```typescript
// Kata 4 (after): extends { length: number } proves T has .length before the body reads it.
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

console.log(longest("hi", "hello"));
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: extends { length: number } is the caller-visible contract -- only types
// that genuinely have a .length are legal type arguments for T.
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b; // => .length now compiles -- the constraint proves it exists
}

console.log(longest("hi", "hello")); // => "hello".length (5) >= "hi".length (2) -- Output: hello
```

**Root cause**: an unconstrained `T` could be instantiated with any type at any call site -- a
`number`, a `boolean`, anything -- so the compiler has zero grounds to assume it has a `.length`
property unless the signature says so. `extends { length: number }` narrows the set of legal type
arguments to exactly the ones that do, and in exchange, the function body is allowed to rely on that
property existing.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
hello
```

</details>

### Kata 5 -- non-null assertion hides a real null

**Task.** `findUser` genuinely returns `null` for an unknown id. The version below asserts the
result is never null with `!`, which compiles cleanly -- and then crashes at runtime for exactly the
id that doesn't exist.

**Before** (`drilling/code/kata-05-non-null-assertion-runtime-null/before/kata.ts`)

```typescript
// Kata 5 (before): `!` asserts findUser's result is never null -- but for id 2, it genuinely is.
function findUser(id: number): { name: string } | null {
  return id === 1 ? { name: "Ada" } : null;
}

const user = findUser(2)!; // => compiles clean -- the assertion silences the type checker
console.log(user.name); // => runtime crash: user is actually null here
```

**Observed (buggy) output** (`tsc --noEmit --strict --skipLibCheck kata.ts` reports ZERO errors --
the bug only surfaces when actually run with `tsx kata.ts`):

```text
$ tsc --noEmit --strict --skipLibCheck kata.ts
(no output -- the assertion makes this compile clean, with no warning at all)

$ tsx kata.ts
.../kata-05-non-null-assertion-runtime-null/before/kata.ts:7
console.log(user.name); // => runtime crash: user is actually null here
                 ^

TypeError: Cannot read properties of null (reading 'name')
    at <anonymous> (.../kata-05-non-null-assertion-runtime-null/before/kata.ts:7:18)
    ... (remaining Node.js/tsx internal stack frames omitted)
Node.js v24.16.0
```

**After** (`drilling/code/kata-05-non-null-assertion-runtime-null/after/kata.ts`)

```typescript
// Kata 5 (after): a real null check replaces the assertion -- no crash, no lie to the compiler.
function findUser(id: number): { name: string } | null {
  return id === 1 ? { name: "Ada" } : null;
}

const user = findUser(2);
if (user !== null) {
  console.log(user.name);
} else {
  console.log("user not found");
}
```

<details>
<summary>Model solution</summary>

```typescript
function findUser(id: number): { name: string } | null {
  return id === 1 ? { name: "Ada" } : null;
}

// THE FIX: no `!` -- keep the real `{ name: string } | null` type and narrow it with a check.
const user = findUser(2);
if (user !== null) {
  console.log(user.name);
} else {
  console.log("user not found"); // => id 2 doesn't exist -- this branch runs
}
```

**Root cause**: `!` performs zero runtime check -- it only silences the compiler's `T | null`
warning, on the author's unchecked word that the value will never actually be `null`. When
`findUser` genuinely does return `null`, nothing catches that at the assertion; the crash surfaces
later, at `user.name`, with no compile-time trace connecting it back to the assertion that hid it. A
real `if (user !== null)` check narrows the type AND verifies it at runtime, in one step.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
user not found
```

</details>

### Kata 6 -- keyof-constrained getter catches a typo

**Task.** `getValue<T, K extends keyof T>` should only accept a `key` argument that is actually one
of `T`'s own property names. The version below passes a misspelled key string -- it never compiles,
instead of returning `undefined` at runtime the way a plain `obj[key]` lookup would.

**Before** (`drilling/code/kata-06-keyof-generic-getter-typo/before/kata.ts`)

```typescript
// Kata 6 (before): a typo'd key string doesn't satisfy keyof T -- tsc catches it at the call site.
function getValue<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Ada" };
console.log(getValue(user, "naem"));
```

**Observed (buggy) output** (captured by actually running `tsc --noEmit --strict --skipLibCheck
kata.ts` -- it fails to compile):

```text
kata.ts(7,28): error TS2345: Argument of type '"naem"' is not assignable to parameter of type '"id" | "name"'.
```

**After** (`drilling/code/kata-06-keyof-generic-getter-typo/after/kata.ts`)

```typescript
// Kata 6 (after): "name" is a real key of user, so it satisfies keyof T.
function getValue<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Ada" };
console.log(getValue(user, "name"));
```

<details>
<summary>Model solution</summary>

```typescript
function getValue<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Ada" };
// THE FIX: "name" (spelled correctly) IS a member of keyof typeof user ("id" | "name").
console.log(getValue(user, "name")); // => Output: Ada
```

**Root cause**: `keyof T` evaluates to the literal union of `T`'s own property names --
`"id" | "name"` here -- and constraining `key`'s type parameter `K` to that union means only those
exact strings are legal arguments. A misspelled string is simply not a member of the union, so
`tsc` rejects the call before the program ever runs, instead of the typo silently returning
`undefined` the way an untyped (or plain `string`-keyed) lookup would.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
Ada
```

</details>

### Kata 7 -- import type used as a runtime value

**Task.** `main.ts` imports the `ApiError` class purely to use it as a type -- with `import type`.
Later, the same file also tries to construct one with `new ApiError(...)`. Because `import type` is
guaranteed to erase at compile time, using the imported name as a runtime value fails to compile.

**Before** (`drilling/code/kata-07-import-type-runtime-value/before/`)

```typescript
// types.ts -- ApiError is a class, so it exists as BOTH a type and a runtime value.
export class ApiError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
  ) {
    super(message);
  }
}
```

```typescript
// main.ts (before): `import type` erases ApiError from the compiled output --
// using it as a runtime value (`new ApiError(...)`) fails to compile.
import type { ApiError } from "./types";

function fail(): never {
  throw new ApiError(404, "not found");
}

fail();
```

**Observed (buggy) output** (captured by actually running `tsc --noEmit` from this kata's directory
-- it fails to compile):

```text
main.ts(6,13): error TS1361: 'ApiError' cannot be used as a value because it was imported using 'import type'.
```

**After** (`drilling/code/kata-07-import-type-runtime-value/after/`)

```typescript
// main.ts (after): a regular (runtime) import -- ApiError survives into the compiled output.
import { ApiError } from "./types";

function fail(): never {
  throw new ApiError(404, "not found");
}

try {
  fail();
} catch (err) {
  if (err instanceof ApiError) {
    console.log(`${err.statusCode}: ${err.message}`);
  }
}
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: import { ApiError } (a regular import), not import type { ApiError }.
// ApiError now genuinely exists at runtime, so `new ApiError(...)` compiles.
import { ApiError } from "./types";

function fail(): never {
  throw new ApiError(404, "not found");
}

try {
  fail();
} catch (err) {
  if (err instanceof ApiError) {
    console.log(`${err.statusCode}: ${err.message}`); // => Output: 404: not found
  }
}
```

**Root cause**: `import type` is a promise, enforced by the compiler, that an import produces zero
runtime code -- useful for tooling (Babel, esbuild, swc) that transpiles one file at a time and
can't always tell on its own whether an import is type-only. Referencing that same name in a value
position (`new ApiError(...)`) breaks the promise, so `tsc` rejects it with a specific, named error
(`TS1361`) rather than letting it become a silent `undefined is not a constructor` at bundle time.

**Run**: `tsc --noEmit && tsx main.ts`

**Output**:

```text
404: not found
```

</details>

### Kata 8 -- enum reverse-mapping off-by-one

**Task.** `Priority` deliberately starts numbering at `1`, not the default `0`. The version below
looks up `Priority[0]`, expecting the first member's name back -- and gets a silent, wrong answer,
with zero compile error at all.

**Before** (`drilling/code/kata-08-enum-reverse-mapping-off-by-one/before/kata.ts`)

```typescript
// Kata 8 (before): Priority starts at 1, not the default 0 -- Priority[0] has no matching member.
enum Priority {
  Low = 1,
  Medium,
  High,
}

console.log(Priority[0]);
```

**Observed (buggy) output** (`tsc --noEmit --strict --skipLibCheck kata.ts` reports ZERO errors --
the bug only surfaces when actually run with `tsx kata.ts`):

```text
$ tsc --noEmit --strict --skipLibCheck kata.ts
(no output -- Priority[0] is well-typed, just semantically wrong for THIS enum's numbering)

$ tsx kata.ts
undefined
```

**After** (`drilling/code/kata-08-enum-reverse-mapping-off-by-one/after/kata.ts`)

```typescript
// Kata 8 (after): look up Priority.Low itself instead of guessing its underlying numeric value.
enum Priority {
  Low = 1,
  Medium,
  High,
}

console.log(Priority[Priority.Low]);
```

<details>
<summary>Model solution</summary>

```typescript
enum Priority {
  Low = 1, // => Priority.Low is 1, NOT the default 0 -- deliberately, so 0 can mean "unset" elsewhere
  Medium, // => Priority.Medium is 2
  High, // => Priority.High is 3
}

// THE FIX: reverse-map through Priority.Low itself (guaranteed correct) instead of
// hardcoding the numeric literal 0, which has no member at all in this enum.
console.log(Priority[Priority.Low]); // => Output: Low
```

**Root cause**: a numeric enum's reverse-mapping indexer (`Priority[n]`) is typed to accept any
`number`, not just the specific numbers this particular enum's members actually use -- so
`Priority[0]` is perfectly well-typed, it just has no member to find at runtime and silently
resolves to `undefined`. Indexing through the enum member itself (`Priority[Priority.Low]`) is
immune to this: it can never drift out of sync with whatever numbering the enum actually uses.

**Run**: `tsc --noEmit --strict --skipLibCheck kata.ts && tsx kata.ts`

**Output**:

```text
Low
```

</details>

## Self-check checklist

Confirm each item without checking the manual first. If you hesitate, that concept needs another
pass.

- [ ] I can name the two ways to run a `.ts` file (`tsc` + `node`, or `tsx` directly) and say which
      one produces no emitted `.js` file. (co-01)
- [ ] I can write a minimal `tsconfig.json` (`target`, `module`, `strict`) and explain what
      `tsc --noEmit` checks without emitting. (co-02)
- [ ] I can name all five primitive annotations this primer covers and explain what `strict` does
      to `null`/`undefined`. (co-03)
- [ ] I can predict a `let` variable's inferred type from its initializer, and say when an explicit
      annotation is still worth adding. (co-04)
- [ ] I can write both an array type and a tuple type, and explain what `readonly T[]` blocks.
      (co-05)
- [ ] I can write an object type with an optional property and explain what triggers an
      excess-property-check error. (co-06)
- [ ] I can write both a `type` alias and an `interface` for the same object shape, and name one
      thing only `interface` can do. (co-07)
- [ ] I can write a union type and explain why it must be narrowed before type-specific use.
      (co-08)
- [ ] I can explain why `const c = "on"` infers the literal type `"on"`, not the wide `string`.
      (co-09)
- [ ] I can write an intersection type and explain how it differs from a union in what it requires.
      (co-10)
- [ ] I can annotate a function's parameters and return type, and explain what `void` communicates
      to a caller. (co-11)
- [ ] I can write a function using an optional parameter, a default parameter, and a rest
      parameter, all three. (co-12)
- [ ] I can write a function type expression (`(n: number) => string`) and use it to type a
      variable. (co-13)
- [ ] I can name at least four different checks (`typeof`, truthiness, `in`, `instanceof`) that
      narrow a union inside a branch. (co-14)
- [ ] I can write a user-defined type guard using the `x is T` return-type syntax. (co-15)
- [ ] I can model a discriminated union with a tag field and add a `never`-typed exhaustiveness
      check to a `switch` over it. (co-16)
- [ ] I can write a generic function with an `extends` constraint and explain what problem the
      constraint solves. (co-17)
- [ ] I can explain the difference between `any`, `unknown`, and `never` in one sentence each.
      (co-18)
- [ ] I can explain why an object satisfies a type purely by shape, with no declared relationship
      required. (co-19)
- [ ] I can name three type-assertion forms (`as T`, `!`, `as const`) and explain the runtime risk
      each one carries. (co-20)
- [ ] I can write a numeric `enum` and its modern `as const` + `keyof typeof` alternative. (co-21)
- [ ] I can explain the one guarantee `import type` makes about the compiled output that a regular
      `import` doesn't. (co-22)
- [ ] I can write an `async` function that awaits a typed `Promise`, and explain what type a caught
      error has under `strict`. (co-23)
- [ ] I can name at least four built-in utility types (`Partial`, `Pick`, `Omit`, `Record`,
      `Readonly`, `Required`, `ReturnType`) and what each derives. (co-24)
- [ ] I can compute `keyof T` for a concrete object type by hand, and explain what an index
      signature allows that a fixed shape doesn't. (co-25)
- [ ] I can state the division of labor between `eslint` and `prettier`, and the check-only flag
      for each. (co-26)
- [ ] I can explain, in one sentence, why TypeScript is deliberately gradual -- letting
      `any`/`unknown`/`never` dial rigor up or down rather than forcing "provably right" before
      anything runs. (`correctness-vs-pragmatism`)

## Elaborative interrogation & self-explanation

Six why/why-not prompts. Answer each in your own words before opening the model explanation.

**E1.** Why does TypeScript perform the excess-property check only against an object literal passed
directly, and not against the same shape stored in a variable first (Kata 1)?

<details>
<summary>Model explanation</summary>

TypeScript's underlying compatibility rule is structural (co-19): a value satisfies a type once it
has at least the required members, and extra members are normally harmless -- that flexibility is
the entire point of structural typing. But an object literal written directly at a call site is a
special case: there's no other legitimate reason it would carry an extra field, since the literal
exists nowhere else to be intentionally wider -- the extra field is almost certainly a typo or a
copy-paste leftover. The excess-property check is a narrow, deliberate carve-out from otherwise
permissive structural typing, aimed specifically at that one situation. Once the value is stored in
a variable first (Kata 1's fix), the general rule applies again, because now there IS a legitimate
reason the variable's type might be wider than what this one call site needs -- it might be reused
elsewhere for its full shape. This is `correctness-vs-pragmatism` in miniature: TypeScript accepts
the false-negative risk (a genuinely wrong extra field, hidden behind a variable) in exchange for
not rejecting every legitimately wider object that happens to pass through a variable first.

</details>

**E2.** Why does a generic type parameter `<T>` start out with none of an object's properties
assumed, forcing an explicit `extends` constraint (Kata 4) before the function body can read
anything off it?

<details>
<summary>Model explanation</summary>

An unconstrained `T` can be instantiated with literally any type at every call site -- a `number`,
a `boolean`, a class instance, anything at all -- so the compiler has zero grounds to assume `T` has
a `.length` (or any other property) unless the signature explicitly says so. If TypeScript let a
generic function body freely access arbitrary properties on an unconstrained `T`, it would be
silently assuming every possible caller's type happens to have that shape, which defeats the entire
purpose of generics: expressing "this works for many types, but only the ones that actually satisfy
this contract." `extends { length: number }` (Example 42, Kata 4) is that caller-visible contract,
made explicit -- only types that genuinely have a `.length` are legal type arguments, and in
exchange the function body earns the right to rely on that property existing.

</details>

**E3.** Why does a caught error's type default to `unknown`, not `any` or a bare `Error`, under
`strict` (Kata 3)?

<details>
<summary>Model explanation</summary>

JavaScript's `throw` statement can throw literally any value at all -- a string, a number,
`undefined`, or a genuine `Error` instance -- so a caught error's actual runtime type is never
guaranteed to be `Error`, and typing it as `Error` outright would be a claim the compiler can't
actually verify. `any` would compile, but it would also silently permit calling `.message` (or
anything else) on a value that might not have it, defeating the entire point of typing the catch
parameter at all. `unknown` is the deliberately conservative middle ground: honest about "this could
genuinely be anything," while still forcing a narrowing check (Kata 3's `instanceof Error`) before
any member access compiles -- `correctness-vs-pragmatism` resolved firmly on the side of correctness
for exactly this one, historically bug-prone spot.

</details>

**E4.** Why does `import type` need to exist as its own explicit keyword, rather than TypeScript
silently detecting "this import is only ever used as a type" and erasing it automatically (Kata 7)?

<details>
<summary>Model explanation</summary>

TypeScript's own compiler can often infer whether an import is type-only just from how it's used
within a single file, and does erase plain type-only imports automatically in the common case --
but `import type` exists for the cases where that inference can't be trusted silently, particularly
under transpile-per-file tooling (Babel, esbuild, swc) that only ever sees one file at a time and
has no way to cross-reference the imported module to check whether a name is a type or a value.
Making the erasure syntax-visible also documents intent for a human reader: `import type` is a
promise, checked by the compiler, that this specific import produces zero runtime code -- which is
exactly why reusing the same name in a runtime position (`new ApiError(...)`, Kata 7's bug) is a
hard, named compile error (`TS1361`) rather than a silent `undefined is not a constructor` surprise
much later, at bundle time.

</details>

**E5.** Why does the non-null assertion operator (`!`) exist at all, given that Kata 5 shows it can
hide a real runtime `null` and cause the exact crash it looks like it should prevent?

<details>
<summary>Model explanation</summary>

`!` exists because TypeScript's static analysis is sometimes provably less precise than what the
author actually knows -- for example, a value narrowed by a check that happened in a different
function, or guaranteed non-null by an invariant the type system has no way to express at all (like
"this array is never empty because the line right above just pushed to it"). In those genuine cases,
`!` is a deliberate, visible escape hatch: a single character admitting "the compiler can't prove
this here, but I can." The cost, which is Kata 5's entire point, is that `!` performs zero runtime
check -- if the author's belief turns out to be wrong, `!` doesn't fail loudly at the assertion
itself; it fails later, less clearly, wherever the now-mistyped value actually gets used. This is
`correctness-vs-pragmatism` at its sharpest: TypeScript trusts the author's stated intent over its
own analysis, on the explicit, unenforced condition that the author accepts the entire risk of being
wrong.

</details>

**E6.** Why does TypeScript's structural type system decide compatibility purely by an object's
shape, with no `implements` keyword or declared relationship required, unlike nominally-typed
languages?

<details>
<summary>Model explanation</summary>

TypeScript was designed to type an enormous existing body of untyped JavaScript, where objects are
built ad hoc -- object literals, factory functions, JSON responses parsed straight off the wire --
code that never declared any formal "this object implements that interface" relationship, because
JavaScript itself has no such concept at all. A nominal type system would require retrofitting every
one of those objects with an explicit declaration before any of them could be typed, which would
make adopting TypeScript for real-world JavaScript nearly impossible in practice. Structural typing
sidesteps that entirely: if a value has the required members, it satisfies the type, full stop --
exactly what lets Example 51's object satisfy an interface with no `implements` clause anywhere, and
exactly what makes Kata 1's "store it in a variable first" workaround a legitimate consequence of the
design, not a loophole in it.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
