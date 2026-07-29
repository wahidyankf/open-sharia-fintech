---
title: "Overview"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Advanced Frontend course: five fixed sections
that force active recall instead of passive re-reading. Work through them in order -- the **Drills
Overview** frames the method, the **Drill List** is the recall Q&A plus applied problems plus
hands-on code katas, **Difficulty Progression** explains how the drills ramp, **Evaluation
Criteria** is the self-check checklist that confirms real automaticity, and **Capstone Integration**
ties every drill back to the capstone steps. Every answer is hidden in a `<details>` block; try each
item yourself before opening it.

## Drills Overview

The drills exist to move a concept from "recognized when read" to "recallable when asked." Three
formats, each attacking a different failure mode:

- **Recall Q&A** -- one short-answer question per concept (`co-01` through `co-37`). Answer from
  memory, then check. If you cannot phrase it, the concept is not yet yours.
- **Applied problems** -- a scenario with the concept unnamed; you name the mechanism that solves it.
  This tests transfer, not recitation.
- **Code katas** -- a genuinely-executed `before` script that misapplies a concept, a diagnosed bug
  from the observed output, a fix from memory, then the `after` script and its output to compare.

The drills deliberately span this topic's cross-cutting big ideas -- `taming-state` (the cache/split
and global-store drills) and `consistency-latency-throughput` (the Core Web Vitals and rendering-
strategy drills) -- so you rehearse the reasoning, not just the vocabulary.

## Drill List

### Recall Q&A

Thirty-seven short-answer questions, one per concept (`co-01` through `co-37`). Answer from memory,
then check.

**Q1 (co-01 -- rendering-csr).** What is in the DOM before the JavaScript bundle runs under CSR, and
why does that matter for crawlers?

<details>
<summary>Answer</summary>

Nothing -- CSR ships an empty shell that the bundle fills. A crawler or no-JS user sees a blank page
until the bundle executes, which is the problem SSR/SSG/streaming (Examples 2-4) exist to solve.

</details>

**Q2 (co-02 -- rendering-ssr).** What does the server return per request under SSR, and what does it
cost versus SSG?

<details>
<summary>Answer</summary>

Fully-formed HTML with content baked in, per request. The cost is server work on every request;
SSG (Example 3) avoids that by baking once at build time.

</details>

**Q3 (co-03 -- rendering-ssg).** When is a page rendered under SSG, and what is the trade-off?

<details>
<summary>Answer</summary>

At build time, to static files identical for every visitor. Cheapest and most cacheable, but content
is fixed until the next build -- stale for time-sensitive data.

</details>

**Q4 (co-04 -- streaming-ssr).** What streams first under streaming SSR, and what problem does that
solve?

<details>
<summary>Answer</summary>

A `<Suspense>` fallback streams first, then the resolved content. It lets the browser paint the shell
before the slowest data is ready, so one slow fetch no longer blocks the whole page's first paint.

</details>

**Q5 (co-05 -- hydration).** What does `hydrateRoot` do that mounting from scratch does not, and what
happens on a server/client mismatch?

<details>
<summary>Answer</summary>

It attaches event handlers to the EXISTING server HTML instead of re-rendering it. A mismatch
(content differing between server and client) warns and recovers by re-rendering the client tree
(Examples 5-6).

</details>

**Q6 (co-06 -- islands-architecture).** In an islands page, which regions ship JavaScript?

<details>
<summary>Answer</summary>

Only the small interactive "islands" ship JS; the rest is static HTML with zero JS. This keeps the
bundle small while still hydrating the interactive widgets (Example 7).

</details>

**Q7 (co-07 -- react-server-components).** Is `'use client'` a render-tree boundary or a module-tree
boundary, and can a client component render a server component?

<details>
<summary>Answer</summary>

A module-dependency-tree boundary (it governs imports). A client component can still render a server
component through its `children` prop (composition, not an import) -- Examples 8-9.

</details>

**Q8 (co-08 -- core-web-vitals).** Name the current Core Web Vitals triad, and which one replaced
FID, and when.

<details>
<summary>Answer</summary>

LCP, INP, CLS. INP replaced FID as a stable Core Web Vital on March 12, 2024 -- any older FID material
is stale (Example 13).

</details>

**Q9 (co-09 -- lcp).** What does LCP measure, what is the "good" threshold, and what does the
reported element tell you?

<details>
<summary>Answer</summary>

LCP measures loading -- the largest contentful paint. Good is at or below 2.5 s at the 75th
percentile. The reported element is the one to optimize (Example 10).

</details>

**Q10 (co-10 -- inp).** What does INP measure, what is the "good" threshold, and why did it replace
FID?

<details>
<summary>Answer</summary>

INP measures responsiveness -- the worst input-to-paint latency across interactions. Good is at or
below 200 ms. FID measured only the first interaction's delay, missing jank on later clicks
(Example 11).

</details>

**Q11 (co-11 -- cls).** What does CLS measure, what is the "good" threshold, and the usual fix?

<details>
<summary>Answer</summary>

CLS measures visual stability (content jumping). Good is at or below 0.1. The usual fix is reserving
width/height (or aspect-ratio) up front so late content drops into an existing box (Example 12, 63).

</details>

**Q12 (co-12 -- critical-rendering-path).** Why is CSS render-blocking, and what does that imply for
first paint?

<details>
<summary>Answer</summary>

The render tree needs both the DOM and the CSSOM, so the browser will not paint until the CSSOM is
built. A large blocking stylesheet delays first paint by its full download+parse time (Example 14);
inlining critical CSS helps (Example 15).

</details>

**Q13 (co-13 -- code-splitting).** What do `React.lazy` + `<Suspense>` do, and where must `lazy` be
called?

<details>
<summary>Answer</summary>

They defer a component into a chunk loaded on first render, behind a Suspense fallback. `lazy` must
be called at the top level, never inside a condition (Examples 16-17).

</details>

**Q14 (co-14 -- tree-shaking).** What is tree shaking, and what makes it possible?

<details>
<summary>Answer</summary>

Dead-code elimination: an export nothing imports is dropped from the bundle. It works because ES
module imports/exports are statically analyzable at build time (Example 18).

</details>

**Q15 (co-15 -- client-vs-server-state).** Why keep client UI state and the server cache separate,
and what are invalidation and optimistic updates for?

<details>
<summary>Answer</summary>

They update on different schedules; conflating them causes redundant refetches and lost UI state.
Invalidation marks a query stale so observers refetch; optimistic updates show the expected result
now and roll back on failure (Examples 31-34).

</details>

**Q16 (co-16 -- when-redux).** When should you reach for a Redux-style global store?

<details>
<summary>Answer</summary>

Only for state that is large, frequently updated, AND shared across many components -- not for every
piece of state. Most state is better local or in a server cache (Example 35).

</details>

**Q17 (co-17 -- rules-of-hooks).** State the two Rules of Hooks.

<details>
<summary>Answer</summary>

(1) Only call Hooks at the top level (not in loops, conditions, nested functions, or after an early
return); (2) only call them from React function components or custom Hooks (Examples 19-20).

</details>

**Q18 (co-18 -- useeffect-semantics).** When do effects run relative to paint, when does cleanup run,
and what gates a re-run?

<details>
<summary>Answer</summary>

Effects run after paint. Cleanup runs with the OLD values before the next setup runs with NEW values
(and on unmount). A re-run is gated by the dependency array, compared with `Object.is`
(Examples 21-23).

</details>

**Q19 (co-19 -- usememo-usecallback).** What do `useMemo` and `useCallback` cache, and when should
you actually use them?

<details>
<summary>Answer</summary>

`useMemo` caches a value; `useCallback` caches a function reference -- both recomputed/recreated only
on dep change. Use them as targeted optimizations (especially for memoized children), not by default
(Examples 24-25, 36).

</details>

**Q20 (co-20 -- reconciliation-keys).** Why do list items need stable keys, and what breaks with
random keys?

<details>
<summary>Answer</summary>

Keys give items stable identity so React reuses the DOM node (and its state) on reorder. Random keys
recreate every node and lose per-item state (input drafts, focus) (Examples 26-27).

</details>

**Q21 (co-21 -- virtual-dom).** What does the virtual-DOM diff emit, and why?

<details>
<summary>Answer</summary>

Only the delta (changed props/text) between two trees, so the expensive real DOM is touched as little
as possible (Example 37).

</details>

**Q22 (co-22 -- signals-fine-grained).** What re-runs when a signal changes, and how is that different
from React?

<details>
<summary>Answer</summary>

Only the effects that read the signal (fine-grained); the parent component does NOT re-render. In
React a state change re-runs the whole component (Examples 40-42).

</details>

**Q23 (co-23 -- wcag-accessibility).** What do semantic landmark elements give you for free, and what
are live regions for?

<details>
<summary>Answer</summary>

Landmarks (`header`/`nav`/`main`/...) map to ARIA roles automatically, feeding the accessibility
tree. Live regions (`aria-live`) announce dynamic updates without moving focus (Examples 43, 47).

</details>

**Q24 (co-24 -- focus-management).** Name two strategies for keyboard navigation in a composite
widget, and what a focus trap does.

<details>
<summary>Answer</summary>

Roving tabindex and `aria-activedescendant`. A focus trap cycles Tab within a dialog so focus cannot
escape to the background page (Examples 45-46).

</details>

**Q25 (co-25 -- controlled-vs-uncontrolled).** What makes an input controlled vs uncontrolled, and
what is forbidden?

<details>
<summary>Answer</summary>

Controlled: state owns the `value`. Uncontrolled: the DOM owns it, read via a ref. An input cannot
switch modes mid-life (Examples 28-30).

</details>

**Q26 (co-26 -- accessible-forms).** Which three attributes wire an error to its input, and what does
an error summary do?

<details>
<summary>Answer</summary>

`required`/`aria-required`, `aria-invalid`, and `aria-describedby` (pointing at the error text). An
error summary collects every error and receives focus, announcing them in order (Examples 48-49).

</details>

**Q27 (co-27 -- performance-budget).** What does a performance budget turn bundle size into, and what
follows a budget failure?

<details>
<summary>Answer</summary>

A CI gate: exceeding the limit fails the check (non-zero exit), blocking the regression. Bundle
analysis then names the oversized dependency (Examples 55-56).

</details>

**Q28 (co-28 -- http-caching-swr).** What does `stale-while-revalidate` do?

<details>
<summary>Answer</summary>

It lets a cache serve a STALE response immediately while revalidating in the background, so the user
gets an instant response and the next request is fresh (Example 53; RFC 5861).

</details>

**Q29 (co-29 -- css-at-scale).** How do CSS Modules and Tailwind each solve CSS's global-namespace
problem, and what decides a specificity conflict?

<details>
<summary>Answer</summary>

CSS Modules rewrite local class names to unique global ones; Tailwind composes single-purpose
utilities. A conflict is decided by the ID--CLASS--TYPE specificity model, then source order
(Examples 50-52).

</details>

**Q30 (co-30 -- data-fetching-patterns).** Why is a request waterfall slow, and what triggers a
Suspense fallback (and what does not)?

<details>
<summary>Answer</summary>

A waterfall serializes dependent fetches, so total latency is the SUM. A Suspense fallback triggers on
`use(promise)` (or lazy code / a framework integration) -- NOT on a `useEffect` fetch
(Examples 57-60).

</details>

**Q31 (co-31 -- image-optimization).** Name three image optimizations and what each controls.

<details>
<summary>Answer</summary>

Responsive `srcset`/`sizes` (right-sized bytes), lazy loading (defer off-screen bytes), and reserved
dimensions (prevent CLS) (Examples 61-63).

</details>

**Q32 (co-32 -- edge-rendering).** What is the edge runtime, and what is its main constraint?

<details>
<summary>Answer</summary>

A V8 isolate running your function at the CDN edge (selected with `runtime: 'edge'`), close to the
user. Its constraint is a Web-API subset -- Node-only modules (`node:fs`, `Buffer`) are unavailable
(Examples 64-65).

</details>

**Q33 (co-33 -- typescript-frontend).** How does a discriminated union plus a never-assertion improve
correctness?

<details>
<summary>Answer</summary>

The union makes impossible states unrepresentable (each branch's payload exists only in that branch);
a never-assertion in a switch's default makes a missing case a COMPILE error (Examples 66-69).

</details>

**Q34 (co-34 -- pwa-service-worker).** What three PWA capabilities make a site resilient and
installable?

<details>
<summary>Answer</summary>

A pre-cached app shell (instant repeat visits), a web manifest (installability), and an offline
fallback page (usable when down) (Examples 70-72).

</details>

**Q35 (co-35 -- i18n).** Why use `Intl` and logical CSS properties for i18n?

<details>
<summary>Answer</summary>

`Intl` formats numbers/dates correctly per locale without hand-built code; logical properties
(`margin-inline-start`) flip with `dir`, so one stylesheet serves LTR and RTL (Examples 73-75).

</details>

**Q36 (co-36 -- testing-behaviour).** Why query by role/text rather than by class, and what is a
Playwright smoke for?

<details>
<summary>Answer</summary>

Role/text queries mirror how a user perceives the UI and survive refactors; class queries break on
implementation churn. A Playwright smoke drives the critical path in a real browser, verifying the
assembled system (Examples 76-78).

</details>

**Q37 (co-37 -- error-boundary).** What does an error boundary catch, and what does it NOT catch?

<details>
<summary>Answer</summary>

It catches RENDER errors in its subtree and shows a fallback instead of crashing the app. It does NOT
catch errors in event handlers or async code (Example 79).

</details>

### Applied problems

Eight scenarios. Each describes a task without naming the construct -- decide which mechanism solves
it, then check.

**AP1.** A product list reorders when the user sorts, and the checkbox a user just toggled silently
un-toggles because state followed the wrong row.

<details>
<summary>Answer</summary>

Stable keys (co-20; Examples 26-27). Use a stable id as the key, not the array index, so per-item
state follows the item on reorder.

</details>

**AP2.** An effect that logs the current filter keeps logging the initial value forever.

<details>
<summary>Answer</summary>

A stale closure from a missing dependency (co-18; Example 23, Kata 2). Add `filter` to the dependency
array so the effect re-runs with the fresh value.

</details>

**AP3.** An "add to cart" shows the item instantly, but when the server rejects it the item stays in
the cart.

<details>
<summary>Answer</summary>

A missing optimistic-rollback (co-15; Example 34, Kata 3). Snapshot the prior state before applying
optimistically, and restore it on failure.

</details>

**AP4.** A late-loading hero image shoves the headline down when it arrives, and Lighthouse reports a
poor CLS.

<details>
<summary>Answer</summary>

Reserve the image's dimensions (co-11/co-31; Example 12, 63, Kata 4). Set width/height (or
aspect-ratio) so the box exists before the image loads.

</details>

**AP5.** A page feels slow; the dev added a Suspense boundary around an effect-fetching component but
no fallback ever shows.

<details>
<summary>Answer</summary>

Suspense does not detect a `useEffect` fetch (co-30; Example 60). Switch to `use(promise)` or a
framework loader so the boundary actually fires, or keep a hand-rolled loading state.

</details>

**AP6.** A teammate added a new `"timeout"` status to the state union and the UI silently renders
blank for it.

<details>
<summary>Answer</summary>

A non-exhaustive switch (co-33; Example 67, Kata 6). Add a never-assertion in the default branch so a
new, unhandled variant is a compile error instead of a silent blank.

</details>

**AP7.** A user in Germany sees prices as "1,234.56" with a comma decimal, which reads as two
numbers.

<details>
<summary>Answer</summary>

Use `Intl.NumberFormat` with the user's locale (co-35; Example 73). de-DE correctly renders
"1.234,56"; never hand-build separators.

</details>

**AP8.** Three sequential awaits make a dashboard take 300ms to load when each call is only ~100ms.

<details>
<summary>Answer</summary>

A request waterfall (co-30; Examples 57-58). Parallelize the independent fetches with `Promise.all`
so the total is the MAX, not the sum.

</details>

### Code katas

Six hands-on repetition drills against small, self-contained, genuinely-executed TypeScript files --
pure standard library, no dependency. Each is a `before`/`after` `example.ts` colocated under
`drilling/code/`. Run the `before` script, diagnose the bug from the observed output, fix it from
memory, then compare against the `after` script and the shown output.

#### Kata 1 -- unstable list key (co-20)

The `before` version keys a list by the array INDEX, so a per-item draft attaches to a slot, not an
item -- on reorder the draft lands on the wrong row.

**Before** (`drilling/code/kata-01-unstable-list-key/before/example.ts`)

```typescript
// Kata 1 (before): a list rendered with INDEX keys loses per-item state on reorder.
interface Item {
  id: string;
  label: string;
}

function renderByKey(items: Item[], drafts: Map<string, string>): string[] {
  // THE BUG: key = String(index) -> the draft is tied to the slot, not the item
  return items.map((item, index) => {
    const key = String(index);
    return `${item.label}="${drafts.get(key) ?? ""}"`;
  });
}

const drafts = new Map<string, string>([["0", "typed-in-first"]]);
const before: Item[] = [
  { id: "a", label: "A" },
  { id: "b", label: "B" },
  { id: "c", label: "C" },
];
const reordered: Item[] = [
  { id: "b", label: "B" },
  { id: "a", label: "A" },
  { id: "c", label: "C" },
];

console.log("before reorder:", renderByKey(before, drafts));
console.log("after reorder: ", renderByKey(reordered, drafts));
```

**Observed (buggy) output**:

```text
before reorder: [ 'A="typed-in-first"', 'B=""', 'C=""' ]
after reorder:  [ 'B="typed-in-first"', 'A=""', 'C=""' ]
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: key = item.id -> the draft follows the ITEM when it moves.
function renderByKey(items: Item[], drafts: Map<string, string>): string[] {
  return items.map((item) => {
    const key = item.id; // stable identity key
    return `${item.label}="${drafts.get(key) ?? ""}"`;
  });
}
// drafts keyed by [["a", "typed-in-first"]] instead of [["0", ...]]
```

**Root cause**: an index key ties per-item state to a position (co-20; Examples 26-27). On reorder the
position's contents change but the key stays, so the draft lands on whichever item now occupies that
slot. A stable id key makes the draft follow the item.

**Run**: `npx tsx after/example.ts`

**Output**:

```text
before reorder: [ 'A="typed-in-first"', 'B=""', 'C=""' ]
after reorder:  [ 'B=""', 'A="typed-in-first"', 'C=""' ]
```

</details>

#### Kata 2 -- useEffect stale dependency (co-18)

The `before` version has an empty dependency array, so the effect closes over the FIRST render's
filter forever.

**Observed (buggy) output**:

```text
effect logged (BUG: only first render): [ 'a' ]
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: deps = [filter] -> the effect re-runs when filter changes.
prevDeps = runEffect(() => loggedFilters.push(filter), prevDeps, [filter]);
```

**Root cause**: an empty deps array means mount-only (co-18; Example 23, Kata 2). The effect captured
the initial `filter` and never re-ran, so it logs a stale value. Listing `filter` in the deps makes it
re-run with the current value.

**Run**: `npx tsx after/example.ts`

**Output**:

```text
effect logged (FIX: every change): [ 'a', 'ab', 'abc' ]
```

</details>

#### Kata 3 -- no optimistic rollback (co-15)

The `before` version applies the optimistic add but keeps no snapshot, so a failed mutation cannot
restore the prior state -- the row stays (a lie).

**Observed (buggy) output**:

```text
after a FAILED add (BUG: row left behind): [ 'buy milk', 'fly kite' ]
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: snapshot the prior state; restore it on failure.
const snapshot = [...list];
list = [...list, label]; // optimistic
if (fails) list = snapshot; // rollback
```

**Root cause**: optimism without a rollback is unsafe (co-15; Example 34, Kata 3). Without a snapshot
there is nothing to restore, so a rejected mutation leaves the user with a row the server never
accepted.

**Run**: `npx tsx after/example.ts`

**Output**:

```text
after a FAILED add (FIX: rolled back): [ 'buy milk' ]
```

</details>

#### Kata 4 -- CLS with no reserved space (co-11)

The `before` version renders an image with no reserved height, so when it loads it shoves content
down -- a poor CLS.

**Observed (buggy) output**:

```text
layout shift (px, BUG: huge): 300
CLS verdict: poor
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: reserve the box (reservedHeight = intrinsicHeight) so the layout is stable.
const fixedImage: ImageBox = { reservedHeight: 300, intrinsicHeight: 300 };
```

**Root cause**: the browser cannot know an image's size until it downloads (co-11; Examples 12, 63,
Kata 4). Without a reserved box the image arrives into a 0-height hole and shifts everything below.
Reserving dimensions makes the shift zero.

**Run**: `npx tsx after/example.ts`

**Output**:

```text
layout shift (px, FIX: zero): 0
CLS verdict: good
```

</details>

#### Kata 5 -- controlled input mode switch (co-25)

The `before` version clears the field by setting `value = undefined`, which flips the input from
controlled to uncontrolled mid-life.

**Observed (buggy) output**:

```text
modes: controlled -> uncontrolled
warnings: [ 'Warning: changing controlled to uncontrolled. Inputs should not switch modes.' ]
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: clear with "" (not undefined) so value is always a string -> always controlled.
const modes = [inputMode("hi"), inputMode("")];
```

**Root cause**: an input cannot switch modes over its lifetime (co-25; Example 30, Kata 5). Setting
`value` to `undefined` removes the controlled `value` prop, making the input uncontrolled. Clearing
with `""` keeps it controlled throughout.

**Run**: `npx tsx after/example.ts`

**Output**:

```text
modes: controlled -> controlled
warnings: []
```

</details>

#### Kata 6 -- non-exhaustive switch (co-33)

The `before` version handles three of four state variants; the unhandled `"stale"` falls through to a
silent empty-string default.

**Observed (buggy) output**:

```text
render stale (BUG: empty): ""
```

<details>
<summary>Model solution</summary>

```typescript
// THE FIX: add the "stale" case AND a never-assertion so a future missing case is a compile error.
case "stale":
  return "Stale -- refetching";
default: {
  const exhaustive: never = state; // exhaustiveness check
  return exhaustive;
}
```

**Root cause**: a switch without exhaustive handling silently misrenders an unhandled variant
(co-33; Example 67, Kata 6). The never-assertion turns a forgotten case into a compile error, so the
bug is caught before it ships.

**Run**: `npx tsx after/example.ts`

**Output**:

```text
render stale (FIX: handled): Stale -- refetching
```

</details>

## Difficulty Progression

The drills ramp in three tiers, matching the course's own Beginner/Intermediate/Advanced structure:

- **Recall first** (the Q&A) -- pure retrieval, no application. If recall fails, re-read the cited
  example before moving on. These map 1:1 to `co-01` through `co-37` in concept order.
- **Applied second** (the problems) -- the concept is unnamed; you must recognize the mechanism from
  a real-world symptom. This tests transfer: the same idea phrased as a bug report rather than a
  definition.
- **Katas last** (the code) -- a genuinely-executed buggy script whose OUTPUT is the evidence. You
  diagnose from the output, fix from memory, then compare. This is the closest to real debugging.

Work top-to-bottom within each tier and do not open a `<details>` block until you have committed to an
answer. A drill you can only answer with the block open is a drill to revisit tomorrow.

## Evaluation Criteria

Confirm each item without checking the manual first. If you hesitate, that concept needs another
pass.

- [ ] I can name the four rendering strategies and the defining cost of CSR (co-01..co-04).
- [ ] I can explain what `hydrateRoot` does and what a mismatch warning means (co-05).
- [ ] I can explain why islands ship less JS than CSR (co-06).
- [ ] I can state whether `'use client'` is a render-tree or module-tree boundary (co-07).
- [ ] I can name the LCP/INP/CLS triad and that INP replaced FID (co-08).
- [ ] I can state the good thresholds for LCP, INP, and CLS (co-09..co-11).
- [ ] I can explain why CSS is render-blocking for first paint (co-12).
- [ ] I can split code with `React.lazy` + `<Suspense>` and per route (co-13).
- [ ] I can explain what tree shaking drops and why (co-14).
- [ ] I can keep client UI state separate from the server cache, with invalidation and rollback (co-15).
- [ ] I can state when a Redux-style store is justified (co-16).
- [ ] I can state both Rules of Hooks (co-17).
- [ ] I can describe effect timing, cleanup, and dependency gating (co-18).
- [ ] I can use `useMemo`/`useCallback` as targeted optimizations (co-19).
- [ ] I can explain why stable keys matter and what random keys break (co-20).
- [ ] I can describe what the virtual-DOM diff emits (co-21).
- [ ] I can contrast signal fine-grained updates with a React re-render (co-22).
- [ ] I can name landmark roles and what live regions do (co-23).
- [ ] I can implement roving tabindex and a focus trap (co-24).
- [ ] I can distinguish controlled from uncontrolled and state the no-switch rule (co-25).
- [ ] I can wire an error to an input accessibly and build an error summary (co-26).
- [ ] I can enforce a performance budget as a CI gate (co-27).
- [ ] I can explain `stale-while-revalidate` (co-28).
- [ ] I can contrast CSS Modules, Tailwind, and the specificity model (co-29).
- [ ] I can avoid a fetch waterfall and state what triggers Suspense (co-30).
- [ ] I can apply `srcset`, lazy loading, and reserved dimensions to images (co-31).
- [ ] I can opt into the edge runtime and name its constraint (co-32).
- [ ] I can model state as a discriminated union and enforce exhaustive narrowing (co-33).
- [ ] I can build an app shell, installability, and an offline fallback (co-34).
- [ ] I can format with `Intl`, externalize messages, and handle RTL (co-35).
- [ ] I can query by behaviour, write a `user-event` flow, and a Playwright smoke (co-36).
- [ ] I can catch a render error with an error boundary, and name what it does NOT catch (co-37).

## Capstone Integration

Every drill maps to a capstone step, so the recall rehearsed here is the recall the capstone depends
on:

- **Capstone Step 1 (SSR + baseline)** rehearses co-04 (streaming SSR) and co-30 (paginated fetch).
  Drill Q4, Q30, and AP8 are the retrieval that step leans on.
- **Capstone Step 2 (perf work + CWV)** rehearses co-08, co-11, and co-27. Drill Q8-Q12, Q27, and
  Kata 4 are the retrieval; the capstone's `measureCwv`/`rate` are exactly Example 13's bands.
- **Capstone Step 3 (cache + optimistic + derived)** rehearses co-15 and co-19. Drill Q15, Q19, AP3,
  and Kata 3 are the retrieval; the capstone's `optimisticAdd` is Example 34 and `selectFiltered` is
  Example 36.
- **Capstone Step 4 (ARIA widget + tests)** rehearses co-23, co-24, and co-36. Drill Q23, Q24, Q36,
  and Kata 1 are the retrieval; the combobox + arrow-key nav are Examples 44-45, and the tests are
  Examples 76-78.

If a capstone step feels shaky, return to its mapped drills before re-attempting it -- the capstone is
the integration test of exactly these concepts.

---

&larr; Previous: [Capstone](../learning/capstone/overview.md)
