# 13 · Just Enough TypeScript (Primer, TypeScript †)

**prd row**: Pass 1 · Core Foundations · Primer · TypeScript † · Learn 113 / Drill 213 · Nvim-ready
Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: just enough TypeScript to be productive in
[`14-frontend-essentials`](./14-frontend-essentials.md) / [`47-advanced-frontend`](./47-advanced-frontend.md)
and the TS side of [`15-software-testing`](./15-software-testing.md). Node/TS are Tier-1 OSS (DD-21).

## Why this exists · the big idea

- **The problem before the solution**: JavaScript runs the web but has no types, so whole classes of bug
  only surface at runtime in front of a user — TypeScript moves those failures to compile time.
- **Keep-this-if-you-forget-everything**: a type is a compile-time proof about a runtime shape, checked
  structurally (by shape, not by name) — you pay in annotations and buy caught errors.
- **Big ideas touched**: `correctness-vs-pragmatism` — TS is _gradual_: `any`/`unknown`/`never` let you
  dial rigor up where correctness matters and stay loose where speed does.

## Prerequisites

- **Prior topics**: [topic 1 Just Enough Nvim](./01-just-enough-nvim.md) (to edit/run); prior
  programming maturity from [topic 4 Just Enough Python](./04-just-enough-python.md) helps but is not
  required.
- **Tools & environment**: a macOS/Linux terminal; **Node.js** (`node --version`) + **npm**/pnpm; the
  **`tsc`** compiler and **`tsx`**/ts-node runner; eslint/prettier CLIs.
- **Assumed knowledge**: basic programming concepts (variables, functions, control flow) from any prior
  language; basic terminal use.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28); re-verified 2026-07-14 immediately
> before authoring, resolving that sweep's own escalation note. TS 7.0 GA (2026-07-08) is the confirmed
> stable baseline for this topic.

- 2026-07-12 — verified (CORRECTION, time-sensitive): **TypeScript 7.0 became stable 2026-07-08** — a
  native-Go compiler rewrite ("Project Corsa", ~10-12x faster type-checking; TS 6.0 / 2026-03-23 was the
  last JS-based compiler). **Caveat**: full editor/tooling support for Vue, Svelte, Astro, MDX is NOT yet
  on 7.0 (pending a programmatic API in 7.1) — flag this if the topic teaches broad editor tooling.
  (visualstudiomagazine.com; confirm at devblogs.microsoft.com/typescript)
- 2026-07-12 — verified: **Node 24 ("Krypton") is Active LTS**; Node 22 Maintenance LTS; Node 26 Current
  (LTS Oct 2026). **`tsx` (~4.23.0) is the dominant TS-run tool** for new projects; `ts-node` is stale
  (no major since 2021), not recommended for new work. (nodejs.org / npmjs.com)
- 2026-07-12 — verified (RESOLVED): minimal `tsconfig.json` — `target: ES2022`, `module: ESNext`
  (or `NodeNext`/`Bundler` resolution), `strict: true`. TS 7.0 adopts TS 6.0's new defaults (`strict`
  and `module: esnext` now default; `target` floats to latest stable ES) and turns 6.0's deprecations
  (`moduleResolution: node/classic`, `target: es5`, `baseUrl`, `module: amd/umd/system`) into **hard
  errors**. The recommended minimal config above uses none of the removed options and is fully
  forward-compatible; `strict: true` is now explicit-for-clarity rather than strictly required.
  (typescriptlang.org release-notes 6.0/7.0)
- 2026-07-14 — re-verified (no material changes): **TypeScript is still 7.0.2 GA** (npm registry) — no
  7.0.3 patch or 7.1 beta/RC posted at devblogs.microsoft.com/typescript (latest post remains
  "Announcing TypeScript 7.0", 2026-07-08); the 7.1 programmatic API for Vue/Svelte/Astro/MDX editor
  tooling has **not** landed, so the caveat above still holds. **Node 24 "Krypton" confirmed Active LTS**
  (LTS since 2025-10-28, Maintenance from 2026-10-20; Node 22 "Jod" now in Maintenance since 2025-10-21;
  Node 26 Current, LTS from 2026-10-28) — matches the 2026-07-12 sweep exactly.
  (registry.npmjs.org/typescript; devblogs.microsoft.com/typescript;
  github.com/nodejs/Release/schedule.json)
- 2026-07-14 — re-verified (minor delta): **`tsx` bumped 4.23.0 → 4.23.1** (patch release) — still the
  recommended TS-run tool over stale `ts-node`. **This repo's pinned `typescript` devDependency is
  5.8.3 and `tsx` is 4.21.0** (root `package.json`) — noticeably behind the 7.0.2/4.23.1 upstream-latest
  cited above; worked examples in this topic are authored and verified against the **actually-installed
  5.8.3/4.21.0 toolchain** (a dependency bump is out of scope for this content-only pass; see
  Dependency Bump Stability & Safety Policy), using only syntax and tsconfig options that are valid on
  both 5.8.3 and forward-compatible with 7.0 (no removed/deprecated options used). `tsconfig.json` hard
  errors on TS 7.0 reconfirmed verbatim; two TS 7.0 defaults not previously logged, both minor/non-
  blocking for the minimal config taught here: `types: []` (auto-discovery removed — list `@types/*`
  packages explicitly if needed) and `rootDir` now defaults to `./` (larger layouts may need
  `rootDir: "./src"`). Utility Types Handbook page spot-checked, unchanged (shows a 2026-07-13 update,
  no removals/renames). **eslint 10.7.0 / prettier 3.9.5** both current upstream and CLI-invoked as
  described (co-26); eslint's flat config (default filename `eslint.config.js`, `.mjs`/`.cjs` also
  valid) remains default since v9 (legacy `.eslintrc` deprecated) — ex-77 ships a real flat
  `eslint.config.mjs` (shown in full, not just invoked from the CLI); ex-78 (prettier) runs
  `prettier --check`/`--write` directly with no config file, relying on prettier's built-in defaults —
  both are described accurately, so no correction needed.
  (npmjs.com/package/tsx; devblogs.microsoft.com/typescript/announcing-typescript-7-0;
  typescriptlang.org/docs/handbook/utility-types.html; eslint.org)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: the TypeScript Handbook + release notes (typescriptlang.org),
> Microsoft TS devblog, npm, and nodejs/Release. **Zero factual errors found**; all 26 concepts verified.

- **Version + toolchain** — TypeScript **7.0.2** (GA 2026-07-08, native-Go rewrite ~11.9× faster than TS
  6.0, [devblog](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/); Apache-2.0);
  Node **24 "Krypton"** Active LTS / 22 Maintenance / 26 Current per
  [nodejs/Release](https://github.com/nodejs/Release); `tsx` **4.23.0** dominant, `ts-node` no major since
  2021 ([npm](https://www.npmjs.com/package/tsx)). TS 7.0 hardens 6.0's deprecations to errors (caveat
  resolved above).
- **Type system (co-06/07/10/14/16/17/18/19)** — structural typing, excess-property checks (object
  literal vs via-variable), `typeof`/truthiness/`in`/`instanceof` narrowing, discriminated unions +
  `never` exhaustiveness, generics + constraints/defaults, intersection types, `type` vs `interface`,
  `unknown`/`any`/`never` — all verbatim from the [Handbook](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
  (the Handbook's own `const _exhaustiveCheck: never` and `keyof Point → "x"|"y"` examples match ex-38/ex-59).
- **Utility types + operators (co-21/22/23/24/25)** — `Partial`/`Required`/`Readonly`/`Pick`/`Omit`/
  `Record`/`ReturnType` ([Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)),
  `keyof`, `as const` (3.4), numeric enum reverse-mapping, `import type` runtime-erasure (3.8), catch
  var `unknown` under `strict` (`useUnknownInCatchVariables`, 4.4), `Promise.all` tuple preservation — all
  confirmed against release notes / Handbook.
- **Scope note** — `satisfies` (TS 4.9) is intentionally out of scope for this "just enough" primer (no
  false claim is made about it); it pairs with `as const` (co-21) and is a candidate for a future pass.
- **Read more** — _Programming TypeScript_ (Cherny, O'Reilly 2019); _Effective TypeScript_ 2nd ed.
  (Vanderkam, O'Reilly 2024, "updated for TS 5"); TypeScript Handbook
  ([typescriptlang.org](https://www.typescriptlang.org/docs/handbook/intro.html), continuously updated) —
  all author/edition/year/URL confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · running-ts** — TypeScript is authored in `.ts`, type-checked/compiled by `tsc`, and run
  directly with `tsx` (or emitted to `.js` and run by `node`).
- **co-02 · minimal-tsconfig** — a `tsconfig.json` (`target: ES2022`, `module: ESNext`, `strict: true`)
  configures the compiler; `tsc --noEmit` type-checks without producing output.
- **co-03 · primitive-types** — the base annotations are `string`, `number`, `boolean`, `null`,
  `undefined`, and `strict` mode makes `null`/`undefined` non-assignable unless explicitly allowed.
- **co-04 · type-inference** — TypeScript infers a variable's type from its initializer, so annotations
  are needed only where inference is too wide or absent.
- **co-05 · arrays-and-tuples** — `T[]` (and `readonly T[]`) type homogeneous lists; a tuple type fixes
  the length and per-position types, optionally with position labels.
- **co-06 · object-types** — an object type lists each property and its type; `prop?:` marks a property
  optional, and passing an object-literal with extra fields triggers an excess-property check.
- **co-07 · type-vs-interface** — `type` aliases any type shape while `interface` declares an object
  contract that can be extended/implemented; both describe object shapes.
- **co-08 · union-types** — `A | B` is a value that is one of several types, requiring narrowing before
  type-specific use.
- **co-09 · literal-types** — a specific string/number value can itself be a type (`"up"`, `42`), and
  `const` bindings infer the narrow literal rather than the wide primitive.
- **co-10 · intersection-types** — `A & B` combines members, so a value must satisfy every constituent
  type at once.
- **co-11 · function-typing** — parameters and return types are annotated (`(a: number): number`), and
  `void` marks a function that returns no usable value.
- **co-12 · optional-default-rest-params** — parameters can be optional (`x?`), have defaults
  (`x = 1`), or collect the tail as a typed rest array (`...xs: number[]`).
- **co-13 · arrow-and-function-type-expressions** — arrow functions carry the same parameter/return
  annotations, and a function type expression `(n: number) => string` types a callback or variable.
- **co-14 · narrowing** — control-flow analysis narrows a union inside a branch via `typeof`,
  truthiness, `in`, `instanceof`, or equality checks.
- **co-15 · type-guards-user-defined** — a predicate `x is T` (or an `asserts x is T` assertion
  function) teaches the compiler to narrow at the call-site.
- **co-16 · discriminated-unions** — a shared literal tag field lets a `switch`/`if` narrow each variant
  and a `never` default enforce exhaustiveness.
- **co-17 · generics** — type parameters (`<T>`) make functions/types reusable across types, with
  `extends` constraints and defaults refining what `T` may be.
- **co-18 · unknown-any-never** — `any` opts out of checking, `unknown` is the safe top type requiring
  narrowing before use, and `never` is the empty bottom type (unreachable / always-throws).
- **co-19 · structural-typing** — type compatibility is decided by shape, not name, so any object with
  the required members satisfies a type without declaring a relationship.
- **co-20 · type-assertions** — `as T`, the non-null `!`, and `as const` override the compiler's
  inference where the author knows more than the checker (at runtime risk).
- **co-21 · enums-and-const-assertions** — `enum` defines a named set of constants, and a
  `{...} as const` object plus `keyof typeof` is the modern literal-union alternative.
- **co-22 · modules-esm** — `import`/`export` (ESM) share bindings across files; `import type` erases at
  runtime and a barrel `index.ts` re-exports a group.
- **co-23 · promises-async-await** — `Promise<T>` types an async result; `async`/`await` unwraps it and
  a rejected promise surfaces as a caught `unknown` error to narrow.
- **co-24 · utility-types** — built-ins like `Partial`, `Required`, `Readonly`, `Pick`, `Omit`,
  `Record`, and `ReturnType` derive new types from existing ones.
- **co-25 · keyof-and-index-signatures** — `keyof T` is the union of a type's keys, `T[K]` indexes a
  property type, an index signature types open-ended keys, and mapped types transform every property.
- **co-26 · tooling-eslint-prettier** — `eslint` flags code smells and `prettier` enforces formatting,
  both run from the CLI as part of the edit-run loop.

## Worked examples

Colocated under `just-enough-typescript/learning/code/`; each is runnable via `tsx <file>` (or
type-checked with `tsc --noEmit`), uses idiomatic typed TypeScript throughout (DD-20/DD-30), and cites
the `co-NN` it exercises. Contiguous `ex-01..ex-82`.

### Beginner

- **ex-01 · hello-tsx** — write `hello.ts` that logs a typed string, run `tsx hello.ts` — verify the
  string prints. (co-01)
- **ex-02 · compile-with-tsc** — run `tsc hello.ts` — verify a sibling `hello.js` is emitted and runs
  under `node`. (co-01)
- **ex-03 · minimal-tsconfig** — create a `tsconfig.json` (`target: ES2022`, `module: ESNext`,
  `strict: true`), run `tsc --noEmit` — verify it type-checks clean. (co-02)
- **ex-04 · annotate-primitives** — declare `let n: number`, `let s: string`, `let b: boolean` — verify
  `tsc` accepts matching assignments. (co-03)
- **ex-05 · type-error-on-mismatch** — assign a string to a `number`-typed variable, run `tsc --noEmit`
  — verify it reports the type error. (co-03)
- **ex-06 · null-under-strict** — type `let x: string | null = null` — verify the union allows `null`
  while a bare `string` variable rejects it under `strict`. (co-03)
- **ex-07 · inference-no-annotation** — write `let count = 5` with no annotation — verify `count` is
  inferred `number` and reassigning a string errors. (co-04)
- **ex-08 · const-literal-inference** — write `const c = "on"` — verify `c`'s type is the literal `"on"`,
  not the wide `string`. (co-04, co-09)
- **ex-09 · array-type** — declare `const xs: number[] = [1, 2, 3]` — verify pushing a string errors.
  (co-05)
- **ex-10 · readonly-array** — declare `const xs: readonly number[]` — verify `xs.push(4)` is a compile
  error. (co-05)
- **ex-11 · tuple-type** — declare `const p: [number, number] = [1, 2]` — verify a third element errors.
  (co-05)
- **ex-12 · named-tuple** — declare `const rgb: [r: number, g: number, b: number]` — verify the labels
  appear and arity is enforced. (co-05)
- **ex-13 · object-type-inline** — annotate a parameter as `{ name: string; age: number }` — verify a
  missing field errors at the call-site. (co-06)
- **ex-14 · optional-property** — give an object type `age?: number` — verify omitting `age`
  type-checks. (co-06)
- **ex-15 · type-alias** — declare `type Point = { x: number; y: number }` — verify a matching literal
  satisfies it. (co-07)
- **ex-16 · interface-declaration** — declare `interface User { id: number; name: string }` — verify a
  conforming object satisfies it. (co-07)
- **ex-17 · interface-extends** — declare `interface Admin extends User { role: string }` — verify an
  `Admin` requires all three fields. (co-07)
- **ex-18 · union-type** — declare `type Id = number | string` — verify both a number and a string
  assign to it. (co-08)
- **ex-19 · literal-union** — declare `type Dir = "up" | "down" | "left" | "right"` — verify assigning
  `"north"` errors. (co-09, co-08)
- **ex-20 · function-typed** — write `function add(a: number, b: number): number` — verify a non-number
  argument errors. (co-11)
- **ex-21 · void-return** — annotate a logging function `: void` — verify returning a value errors.
  (co-11)
- **ex-22 · optional-param** — write `greet(name: string, title?: string)` — verify calling with one
  argument type-checks. (co-12)
- **ex-23 · default-param** — write `pow(base: number, exp: number = 2)` — verify omitting `exp` uses
  the default. (co-12)
- **ex-24 · rest-params** — write `sum(...nums: number[]): number` — verify variadic calls type-check
  and a string argument errors. (co-12)
- **ex-25 · arrow-function-typed** — write `const double = (n: number): number => n * 2` — verify it
  returns a number. (co-13)
- **ex-26 · function-type-expression** — type a variable as `(n: number) => string` — verify a
  mismatching arrow assignment errors. (co-13)
- **ex-27 · typed-callback-param** — pass a callback to `Array.prototype.map` — verify the element
  parameter is inferred as the array's element type. (co-13, co-04)
- **ex-28 · run-typed-script-tsx** — run a small multi-function typed script end to end via `tsx` —
  verify the expected console output. (co-01)

### Intermediate

- **ex-29 · narrow-with-typeof** — in a `number | string` function, branch on
  `typeof x === "string"` — verify each branch sees the narrowed type. (co-14)
- **ex-30 · narrow-truthiness** — narrow `string | undefined` with `if (x)` — verify inside the branch
  `x` is `string`. (co-14)
- **ex-31 · narrow-in-operator** — narrow an object union with `"role" in obj` — verify the branch is
  typed to the matching variant. (co-14)
- **ex-32 · narrow-instanceof** — narrow with `x instanceof Date` — verify the branch is typed as
  `Date`. (co-14)
- **ex-33 · narrow-equality** — narrow a literal union with `===` — verify the branch narrows to the
  matched literal. (co-14, co-09)
- **ex-34 · user-defined-type-guard** — write `function isCat(a: Animal): a is Cat` — verify callers
  narrow after calling it. (co-15)
- **ex-35 · assertion-function** — write `function assertString(x: unknown): asserts x is string` —
  verify code after the call treats `x` as `string`. (co-15, co-18)
- **ex-36 · discriminated-union-shape** — model
  `type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number }` — verify each variant
  type-checks. (co-16)
- **ex-37 · discriminated-switch** — `switch` on `kind` to compute area — verify each branch may access
  only its own fields. (co-16, co-14)
- **ex-38 · exhaustiveness-never** — add `default: const _exhaustive: never = shape` — verify adding a
  new variant without handling it errors. (co-16, co-18)
- **ex-39 · state-machine-union** — model
  `type State = { status: "loading" } | { status: "success"; data: string } | { status: "error"; msg: string }`
  — verify accessing `data` on the loading variant errors. (co-16)
- **ex-40 · generic-identity** — write `function identity<T>(x: T): T` — verify the return type matches
  the argument type. (co-17)
- **ex-41 · generic-array-first** — write `first<T>(xs: T[]): T | undefined` — verify calling it on a
  `number[]` returns `number | undefined`. (co-17)
- **ex-42 · generic-constraint** — write `longest<T extends { length: number }>(a: T, b: T): T` — verify
  a `number` argument (no `length`) errors. (co-17)
- **ex-43 · generic-default-param** — write `<T = string>` as a default type parameter — verify omitting
  the type argument uses the default. (co-17)
- **ex-44 · generic-two-params** — write `pair<A, B>(a: A, b: B): [A, B]` — verify the tuple element
  types are preserved. (co-17, co-05)
- **ex-45 · generic-interface** — declare `interface Box<T> { value: T }` — verify `Box<number>`
  requires a numeric `value`. (co-17, co-07)
- **ex-46 · unknown-requires-narrowing** — assign a value to `unknown` then use it — verify calling a
  method errors until the value is narrowed. (co-18)
- **ex-47 · any-escapes-checking** — assign a value to `any` and call arbitrary members — verify no
  compile error, contrasting with `unknown`. (co-18)
- **ex-48 · never-from-throw** — write a function that always throws — verify its inferred return type is
  `never`. (co-18)
- **ex-49 · structural-compatibility** — assign an object with extra fields (via a variable) to a
  narrower type — verify shape-based compatibility. (co-19)
- **ex-50 · excess-property-check** — pass an object literal with an extra field directly — verify the
  excess-property error fires. (co-19, co-06)
- **ex-51 · structural-interface-match** — let an object satisfy an interface without `implements` —
  verify it type-checks purely by shape. (co-19, co-07)
- **ex-52 · intersection-type** — declare `type Staff = Person & Employee` — verify a `Staff` value
  requires all fields of both. (co-10)
- **ex-53 · intersection-config-merge** — merge two option object types with `&` — verify the combined
  object requires both member sets. (co-10, co-06)
- **ex-54 · as-assertion** — narrow an `unknown` parsed JSON value with `as User` — verify it compiles
  (noting the unchecked runtime risk). (co-20, co-18)
- **ex-55 · non-null-assertion** — apply `x!` to a `T | null` value — verify the `null` is asserted
  away. (co-20)
- **ex-56 · const-assertion** — write `const cfg = { mode: "dark" } as const` — verify `mode`'s type is
  the literal `"dark"` and the object is `readonly`. (co-21, co-09)
- **ex-57 · numeric-enum** — declare `enum Color { Red, Green, Blue }` — verify `Color.Red === 0` and
  reverse mapping works. (co-21)
- **ex-58 · const-object-union** — replace an enum with an `as const` object plus `keyof typeof` — verify
  the derived literal-union type. (co-21, co-25)
- **ex-59 · keyof-operator** — declare `type K = keyof Point` — verify `K` is `"x" | "y"`. (co-25)
- **ex-60 · index-signature** — declare `type Dict = { [k: string]: number }` — verify arbitrary string
  keys hold numbers and a string value errors. (co-25, co-06)

### Advanced

- **ex-61 · esm-named-export-import** — export a function from one module and import it into another, run
  via `tsx` — verify it executes. (co-22)
- **ex-62 · esm-default-export** — default-export a value and import it — verify the default binding
  resolves. (co-22)
- **ex-63 · type-only-import** — use `import type { User }` — verify the type imports with no runtime
  emit. (co-22, co-07)
- **ex-64 · re-export-barrel** — write an `index.ts` re-exporting sibling modules — verify a single
  import path resolves them all. (co-22)
- **ex-65 · typed-promise** — write `function fetchN(): Promise<number>` — verify `.then` receives a
  `number`. (co-23)
- **ex-66 · async-await-typed** — write an `async` function awaiting that promise — verify the awaited
  value is `number`. (co-23)
- **ex-67 · async-error-typed** — model an async flow that rejects, caught in `try/catch` with an
  `unknown` error — verify narrowing the caught error before use. (co-23, co-18)
- **ex-68 · promise-all-tuple** — call `Promise.all([p1, p2])` over differently-typed promises — verify
  the resolved tuple types are preserved. (co-23, co-05)
- **ex-69 · async-discriminated-state** — an async fetch producing loading→success/error discriminated
  states — verify each state is narrowed at the call-site. (co-23, co-16)
- **ex-70 · utility-partial** — apply `Partial<User>` — verify every field becomes optional. (co-24)
- **ex-71 · utility-pick-omit** — apply `Pick<User, "id">` and `Omit<User, "id">` — verify the resulting
  shapes. (co-24)
- **ex-72 · utility-record** — apply `Record<string, number>` — verify it behaves like a string index
  signature. (co-24, co-25)
- **ex-73 · utility-readonly-required** — apply `Readonly<T>` (blocks assignment) and `Required<T>`
  (removes optionality) — verify both effects. (co-24)
- **ex-74 · utility-returntype** — apply `ReturnType<typeof fn>` — verify it extracts the function's
  return type. (co-24, co-17)
- **ex-75 · mapped-type** — write a mapped type `{ [K in keyof T]: ... }` — verify it transforms every
  property. (co-25, co-24)
- **ex-76 · generic-constrained-getter** — write `get<T, K extends keyof T>(o: T, k: K): T[K]` — verify
  the return type is the indexed property's type. (co-17, co-25)
- **ex-77 · eslint-clean** — run `eslint` on a file with an unused variable — verify it flags, then fix
  to clean. (co-26)
- **ex-78 · prettier-format** — run `prettier --check` then `prettier --write` — verify formatting is
  applied. (co-26)
- **ex-79 · tsc-noemit-catches-error** — introduce a type error, run `tsc --noEmit` — verify it fails,
  then fix to pass. (co-01, co-02)
- **ex-80 · typed-argv-parsing** — a `tsx` script reading `process.argv` typed as `string[]` — verify it
  echoes a passed argument. (co-01, co-05)
- **ex-81 · end-to-end-typed-fetch** — an async function fetching and parsing JSON into a typed shape via
  a user-defined type guard — verify a valid payload narrows and an invalid one is rejected. (co-23,
  co-15, co-16)
- **ex-82 · full-typed-module** — assemble a module with a discriminated-union state, a generic utility,
  an async flow, and ESM imports, type-checked with `tsc --noEmit` — verify a clean compile and the
  expected `tsx` output. (co-16, co-17, co-23, co-22)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: write one small (~80–150-line) typed TypeScript CLI/module that uses a discriminated union
  for state, a generic utility, and an `async`/`await` data flow — run from the terminal with `tsx`,
  type-checked clean with `tsc --noEmit`.
- **Concepts exercised**: [ ] `tsconfig` + `tsx` run [ ] union + narrowing [ ] a generic function
  [ ] discriminated union state (loading/error/success) [ ] `async`/`await` + typed Promise [ ] ESM
  imports.
- **Ordered steps**:
  1. `.../learning/capstone/code/` — `tsconfig.json` + `src/state.ts` (discriminated union) + a generic
     `src/util.ts`. Verify `npx tsc --noEmit` passes.
  2. `src/main.ts` — an async flow producing loading→success/error states, narrowed at the call-site.
     Verify `npx tsx src/main.ts` prints the expected transitions.
  3. Add a deliberate type error, show `tsc` catching it, then fix. Verify clean type-check.
- **Acceptance criteria**: `tsc --noEmit` clean; `tsx src/main.ts` runs and prints expected output;
  eslint/prettier clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Programming TypeScript** — Boris Cherny (2019). Comprehensive tour of the type system for engineers coming from JavaScript.
- **Effective TypeScript** — Dan Vanderkam (2nd ed., 2024). Item-based best-practices applying the "Effective X" format to TypeScript.

**Papers & articles**

- **TypeScript Handbook** — Microsoft TypeScript team (continuously updated). Authoritative official reference. <https://www.typescriptlang.org/docs/handbook/intro.html>

---

← Previous: [12 · Networking Essentials](./12-networking-essentials.md) · Next: [14 · Frontend Essentials](./14-frontend-essentials.md) →
