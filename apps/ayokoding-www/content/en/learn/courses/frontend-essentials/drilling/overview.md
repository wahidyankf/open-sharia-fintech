---
title: "Overview"
date: 2026-07-15T00:00:00+07:00
draft: false
weight: 1
---

This page is the active-recall companion to the Frontend Essentials learning track: four fixed
drills that force retrieval instead of passive re-reading. Work through them in order --
short-answer recall first, then scenario judgment, then hands-on implementation, then a checklist to
confirm real automaticity. Every answer is hidden in a `<details>` block; try each item yourself
before opening it. Every kata below is fully self-contained HTML/CSS/JS -- no live third-party host,
no bundler, no dev server -- so recognizing an answer isn't enough; you have to actually reconstruct
the reasoning by opening the file yourself.

## Recall Q&A

Twenty-eight short-answer questions, one per concept (`co-01` through `co-28`). Answer from memory,
then check.

**Q1 (co-01 -- html-document-structure).** Name the three things a valid HTML5 page needs at minimum,
and what the `viewport` meta tag actually controls.

<details>
<summary>Answer</summary>

`<!doctype html>`, a `head` with `charset` and `title`, and a `body`. The `viewport` meta tag tells a
mobile browser how to scale the page to the device's screen width, instead of rendering it at a
fixed desktop-width default and shrinking everything down.

</details>

**Q2 (co-02 -- html-semantics).** Why does `<nav>` communicate more to a screen reader than a `<div
class="nav">` styled identically?

<details>
<summary>Answer</summary>

`<nav>` is a real landmark element -- it's exposed in the accessibility tree with the `navigation`
role automatically, letting assistive tech jump straight to it. A `<div class="nav">` carries no
semantic meaning at all; a screen reader sees a generic, unnamed container regardless of its class
name or visual styling.

</details>

**Q3 (co-03 -- text-and-links).** An `<img>` fails to load. What must be present on that element for
a user to still know what it was, and why can't a filename alone serve that purpose?

<details>
<summary>Answer</summary>

A descriptive `alt` attribute. Filenames are often auto-generated, cryptic, or purely technical
(`IMG_4821.jpg`) and are never read aloud by assistive tech in place of `alt` text -- only `alt`
is guaranteed to convey the image's meaning when the image itself is unavailable.

</details>

**Q4 (co-04 -- css-selectors).** Write a single selector that targets every `input` of type `email`
while it has keyboard focus, and name the two selector features it combines.

<details>
<summary>Answer</summary>

`input[type=email]:focus` -- it combines an attribute selector (`[type=email]`) with a pseudo-class
selector (`:focus`). Both narrow the same base element type down to a more specific condition.

</details>

**Q5 (co-05 -- css-specificity-cascade).** An element has both a class rule and an id rule setting
different colors. Which wins, and would the answer change if the class rule appeared later in the
stylesheet?

<details>
<summary>Answer</summary>

The id rule wins regardless of source order -- an id selector carries higher specificity than a
class selector, and specificity is compared before source order ever becomes a tiebreaker. Source
order only decides the winner when two rules have EQUAL specificity.

</details>

**Q6 (co-06 -- css-custom-properties).** Two unrelated CSS rules both use `var(--brand)`. If
`--brand` is redefined inside a `.dark` scope, what happens to elements inside that scope versus
elements outside it?

<details>
<summary>Answer</summary>

Elements inside `.dark` recompute `var(--brand)` to the new, scoped value; elements outside `.dark`
keep resolving to whatever `--brand` is defined as in their own ancestor chain (typically `:root`'s
value). Custom properties cascade and are resolved per-element, not once globally.

</details>

**Q7 (co-07 -- box-model).** An element has `width: 100px`, `padding: 10px`, and `border: 2px solid`.
Under the default box model, what is its actual rendered (`offsetWidth`) width, and how does
`box-sizing: border-box` change that?

<details>
<summary>Answer</summary>

Under the default `content-box` model, `offsetWidth` is 124px (100 content + 20 padding + 4 border).
Switching to `box-sizing: border-box` folds padding and border INTO the declared width, so
`offsetWidth` becomes exactly 100px -- the declared width now means the full rendered box, not just
the content area.

</details>

**Q8 (co-08 -- normal-flow-display).** An element is set to `display: none`. What does
`element.offsetParent` report, and how does that differ from an element merely styled
`visibility: hidden`?

<details>
<summary>Answer</summary>

`offsetParent` reports `null` -- the element is removed from layout entirely, occupying no space and
participating in no flow calculations. `visibility: hidden` is different: the element still occupies
its layout space and still has a non-null `offsetParent`; it's only invisible, not removed.

</details>

**Q9 (co-09 -- flexbox).** In a flex row, one child has `flex-grow: 1` and its two siblings have
`flex-grow: 0` (the default). What happens to the container's leftover free space?

<details>
<summary>Answer</summary>

The one child with `flex-grow: 1` absorbs ALL of the leftover free space along the main axis; the
`flex-grow: 0` siblings stay at their natural (or explicitly set) size and grow no further.

</details>

**Q10 (co-10 -- grid).** What's the difference between `grid-template-columns` and
`grid-template-areas` as ways of placing children into a grid?

<details>
<summary>Answer</summary>

`grid-template-columns` (paired with `grid-template-rows`) defines the SIZE of each track (e.g.
`1fr 1fr` for two equal columns); `grid-template-areas` names REGIONS of the grid as a text map, and
children opt into a named region via `grid-area`. The two are usually combined -- tracks define the
geometry, areas give each region a readable name.

</details>

**Q11 (co-11 -- responsive-media-queries).** A layout uses `@media (max-width: 600px)` to stack two
columns into one. What triggers that rule to apply, and does it require any JavaScript?

<details>
<summary>Answer</summary>

The rule applies purely from CSS, whenever the browser's viewport width is at most 600px --
re-evaluated live as the viewport is resized. No JavaScript is involved; media queries are a
declarative CSS mechanism the rendering engine itself evaluates.

</details>

**Q12 (co-12 -- dom-selection).** `document.querySelectorAll('li')` is called once, then two more
`li` elements are appended to the page. Does the returned collection grow to include them?

<details>
<summary>Answer</summary>

No -- `querySelectorAll` returns a static `NodeList`, a snapshot taken at call time. Elements added
to the DOM afterward are not reflected in that already-returned collection; a fresh
`querySelectorAll` call would be needed to see them.

</details>

**Q13 (co-13 -- dom-manipulation).** Name three distinct DOM APIs used to mutate rendered content,
and what each one changes.

<details>
<summary>Answer</summary>

`textContent` replaces an element's text; `createElement` + `append` builds and inserts a brand-new
node; `classList` (`add`/`remove`/`toggle`) changes which CSS classes -- and therefore which styles
-- apply, without touching the element's structure or text at all.

</details>

**Q14 (co-14 -- event-handling).** What object does an event handler receive as its argument, and
name one property on it that identifies which element the event actually happened on.

<details>
<summary>Answer</summary>

The handler receives an `Event` object (or a more specific subtype, like `MouseEvent`); its
`target` property identifies the exact element the event originated from -- distinct from `this` /
`currentTarget`, which identifies the element the LISTENER is attached to.

</details>

**Q15 (co-15 -- event-propagation).** A `click` listener sits on a `ul`; the user clicks one of its
`li` children. Does the `ul`'s listener fire, and what's this pattern called?

<details>
<summary>Answer</summary>

Yes -- the click event bubbles up the ancestor chain from the `li` to the `ul` (and beyond), so a
single listener on the parent fires for a click on any descendant. This pattern is called event
delegation, and it means one listener can handle many current AND future children without
individually binding each one.

</details>

**Q16 (co-16 -- default-action-control).** What's the difference between calling `preventDefault()`
and calling `stopPropagation()` inside the same click handler?

<details>
<summary>Answer</summary>

`preventDefault()` suppresses the browser's own built-in behavior for that event (like following a
link's `href` or submitting a form) but does NOT stop the event from continuing to bubble.
`stopPropagation()` does the opposite -- it halts the event from reaching any ancestor listeners, but
does nothing to the browser's default action. They control two independent things.

</details>

**Q17 (co-17 -- event-loop).** `console.log("A")`, then `Promise.resolve().then(() => console.log("B"))`,
then `setTimeout(() => console.log("C"), 0)`, then `console.log("D")` all run in that order. In what
order do "A", "B", "C", "D" actually print?

<details>
<summary>Answer</summary>

A, D, B, C. The synchronous code (`A`, `D`) runs first, in order. Once the call stack is empty, all
queued MICROtasks (the `Promise.then` callback, `B`) run before the event loop even looks at the
macrotask queue that `setTimeout` schedules into (`C`) -- microtasks always drain fully before the
next macrotask, even a `setTimeout(fn, 0)`.

</details>

**Q18 (co-18 -- ui-as-function-of-state).** In the render-from-state pattern this topic teaches, what
is the ONE thing allowed to directly change the DOM, and what is everything else allowed to change
instead?

<details>
<summary>Answer</summary>

Only the render function is allowed to directly touch the DOM. Everything else (event handlers, data
loaders, business logic) is only allowed to change STATE and then call render again -- the DOM is
always a pure, derived reflection of the current state, never mutated ad hoc from scattered places.

</details>

**Q19 (co-19 -- component-props).** A `Greeting(props)` function is called twice with different
`props.name` values. What determines the two calls' output, and can the component itself change
what `props` it received?

<details>
<summary>Answer</summary>

The output is entirely determined by the `props` argument each call receives -- same shape of
function, different input, different output, exactly like any pure function. The component cannot
change the `props` object it was handed; props flow one way, parent to child, and reassigning a
local copy inside the child never reaches back up to the parent's own data.

</details>

**Q20 (co-20 -- component-state).** What two things does a minimal interactive component need beyond
a plain render function, to behave like a counter that increments on click?

<details>
<summary>Answer</summary>

Some mutable state living OUTSIDE the render function (so it survives across re-renders, e.g. a
closed-over variable) and an event handler that updates that state and then calls render again --
render alone, with no state and no handler, can only ever produce the same static output every time.

</details>

**Q21 (co-21 -- list-rendering).** An array of five items is mapped to five `li` elements. What does
"keying" a rendered list mean, and what problem does it solve on a re-render?

<details>
<summary>Answer</summary>

Keying means giving each rendered item a stable identifier (e.g. an id-derived DOM `id`, or in
framework contexts a `key` prop) tied to the underlying data item, not its array index. On a
re-render, that stable identity lets the renderer recognize "this is the same logical item, just
possibly reordered or updated" instead of treating every re-render as a full tear-down and rebuild.

</details>

**Q22 (co-22 -- forms-controlled-input).** What makes a text input "controlled," and what are the two
halves of the round trip that keep it that way?

<details>
<summary>Answer</summary>

A controlled input's displayed `value` comes FROM state (state -> input, on every render), and its
`input` event WRITES that new value back into state (input -> state, on every keystroke) --
state and the on-screen value never drift apart, because both directions of the round trip are
wired explicitly.

</details>

**Q23 (co-23 -- form-validation).** Name three attributes/methods from the Constraint Validation API
covered in this topic, and what each one is responsible for.

<details>
<summary>Answer</summary>

`required` marks a field as mandatory; `pattern` supplies a regex the value must match;
`checkValidity()` runs all of an input's active constraints and returns whether it currently passes;
`setCustomValidity(message)` lets code report a custom failure reason beyond what the built-in
constraints alone can express.

</details>

**Q24 (co-24 -- accessible-forms).** An input has no visible label text next to it, only a
placeholder. Why does that fail accessibility, and what's the fix?

<details>
<summary>Answer</summary>

A placeholder is not an accessible name -- it disappears the moment the user starts typing, and many
assistive technologies don't reliably announce it as a label at all. The fix is a real `<label
for="...">` (or `aria-label`/`aria-labelledby`) tied to the input's `id`, giving it a persistent,
programmatically-associated accessible name.

</details>

**Q25 (co-25 -- aria-roles-semantics).** A `<div>` is given `role="button"` and a click handler. What
does the `role` attribute alone accomplish, and what does it NOT accomplish?

<details>
<summary>Answer</summary>

`role="button"` exposes the button semantic to the accessibility tree, so assistive tech announces
it as a button. It does NOT make the element keyboard-focusable or keyboard-operable on its own --
those require an explicit `tabindex="0"` and manual Enter/Space key handling, none of which a real
`<button>` element would need in the first place.

</details>

**Q26 (co-26 -- keyboard-navigation).** A dialog opens and traps focus inside it. What should happen
when the user presses Tab on the last focusable element inside the dialog?

<details>
<summary>Answer</summary>

Focus should cycle back to the FIRST focusable element inside the dialog, not escape to whatever
comes next in the underlying page's tab order. A focus trap deliberately makes the dialog's
focusable elements the entire tab cycle for as long as it's open.

</details>

**Q27 (co-27 -- discriminated-union-states).** A `TaskListState` type has four tagged variants:
`loading`, `error`, `empty`, `loaded`. What does "exhaustive" mean when a `switch` handles this type,
and what tool catches a missed case?

<details>
<summary>Answer</summary>

Exhaustive means every possible tag/variant has its own explicit `case`, with no variant left
unhandled. A `switch`'s `default` branch typed as `never` is what catches a missed case: if a new
variant is later added to the union but no new `case` is written for it, TypeScript's `tsc` reports
a type error at the `never`-typed default, since that branch is no longer provably unreachable.

</details>

**Q28 (co-28 -- typing-props-state).** A component's props interface declares `label: string`, but a
caller passes `label={42}`. At what point is this mismatch caught, and what would catch it if the
props interface didn't exist?

<details>
<summary>Answer</summary>

`tsc` catches it at compile time, before the component ever renders -- a type error against the
declared `label: string` shape. Without a typed props interface, nothing catches it until runtime
(if ever) -- the component would simply receive a number where it expected a string and behave
however that mismatch happens to play out, silently or not.

</details>

## Applied problems

Ten scenarios spanning beginner through advanced material. Each describes a realistic engineering
situation without naming the specific technique -- decide what applies and why, then check your
reasoning against the worked solution.

**AP1.** A teammate's page passes an automated HTML validator but a screen-reader user still reports
"I can't tell what's the navigation and what's the main content." What's the most likely root cause?

<details>
<summary>Worked solution</summary>

The page probably uses generic `div`s styled to LOOK like a nav bar and a main content area, instead
of real semantic landmarks (`<nav>`, `<main>`). An HTML validator only checks that markup is
well-formed, not that it's semantically meaningful -- passing validation says nothing about whether
assistive tech can identify the page's structure (co-02).

</details>

**AP2.** Two CSS rules both target the same button: one written as `.btn { color: blue; }` earlier in
the file, another as `.primary-btn { color: red; }` later, and the button has both classes. Which
color renders, and why might a teammate be surprised by the answer?

<details>
<summary>Worked solution</summary>

Red renders -- both selectors are single-class selectors of EQUAL specificity, so the tiebreaker is
source order, and `.primary-btn` appears later. A teammate expecting the more "specific-sounding"
class name (`primary-btn`) to always win might be surprised that specificity is measured
structurally (selector type/count), not by how semantically specific a class name reads (co-05).

</details>

**AP3.** A design system wants one place to change an entire app's accent color, including inside a
dark-mode variant that overrides just that one value. What CSS mechanism fits, and why not just
find-and-replace every hardcoded color?

<details>
<summary>Worked solution</summary>

CSS custom properties (`--accent` at `:root`, referenced everywhere via `var(--accent)`, then
re-declared inside a `.dark` scope). Find-and-replace is brittle and fully static -- it can't express
"this value is different depending on which scope/mode is active," while a custom property resolves
per-element through the cascade, live, with zero JavaScript (co-06, co-11).

</details>

**AP4.** A card component's declared `width: 200px` renders WIDER than expected once padding and a
border are added, breaking a grid layout that assumed exact 200px cards. What's the fix, without
changing the declared width value at all?

<details>
<summary>Worked solution</summary>

Add `box-sizing: border-box` to the card. Under the default `content-box` model, padding and border
ADD to the declared width, growing the rendered box beyond 200px. `border-box` fixes exactly that by
folding padding and border back inside the declared width, so `offsetWidth` stays exactly 200px
(co-07).

</details>

**AP5.** A three-column layout needs to become a single stacked column on narrow screens, with zero
JavaScript and no separate mobile-only markup. What CSS feature combination handles this cleanly?

<details>
<summary>Worked solution</summary>

A flex or grid container for the desktop layout, combined with a `@media (max-width: ...)` rule that
switches `flex-direction`/`grid-template-columns` to a single-column arrangement below the
breakpoint. The SAME markup serves every viewport width; only the CSS layout mechanism responds
(co-09 or co-10, plus co-11).

</details>

**AP6.** A dynamically-rendered list re-renders every 2 seconds from fresh server data, and a
developer complains that a text input INSIDE one of the list items keeps losing focus and its typed
text on every refresh, even though that item's other data hasn't changed. What's the most likely
missing piece?

<details>
<summary>Worked solution</summary>

The list is probably not stably keyed -- without a key tied to each item's own identity, a naive
re-render can tear down and rebuild every node from scratch on each pass, destroying focus and
in-progress input state even for items whose underlying data is unchanged. Stable keys let the
renderer recognize "same logical item" and preserve its live DOM node instead (co-21).

</details>

**AP7.** A form's `Add` button is a `<div role="button" tabindex="0">` with a `click` listener only.
QA reports it works fine with a mouse but does nothing when a keyboard-only user presses Enter on
it while it's focused. What's missing, and is this a framework bug?

<details>
<summary>Worked solution</summary>

Not a framework bug -- `role="button"` and `tabindex="0"` only expose the role and make the element
focusable; they do NOT wire up the actual Enter/Space keyboard activation a real `<button>` gets for
free. The fix is either to add explicit `keydown` handling for Enter/Space, or -- far simpler and
more robust -- replace the `div` with a real `<button>` element (co-25, co-26).

</details>

**AP8.** A component fetches data on mount and needs to show a spinner, an error message, an
empty-state message, or the actual list -- and a bug report says two of those UI states have both
rendered on screen simultaneously after a slow request. What class of bug is this, and what pattern
prevents it structurally?

<details>
<summary>Worked solution</summary>

This is a classic symptom of tracking loading/error/data as SEPARATE independent boolean/nullable
flags (`isLoading`, `error`, `data`) that can drift into an invalid combination (e.g. both
`isLoading: true` and `data: [...]` set at once). A discriminated union with exactly one active `tag`
at a time (`{status: "loading"} | {status: "error", message} | ...`) makes that invalid combination
structurally unrepresentable -- there is no state value where two branches could both be true
(co-27).

</details>

**AP9.** A teammate insists a component's `props` object can be safely mutated inside the component
"since JavaScript passes everything by reference anyway." Is this reasoning sound for a props object
containing only primitive fields (strings, numbers, booleans)?

<details>
<summary>Worked solution</summary>

The premise about reference semantics is correct for the props OBJECT itself, but reassigning one of
its primitive-valued fields inside the child only changes the child's own local binding -- it does
not write back into the parent's original object, since primitives are copied by value at the moment
they're read out of the object. The one-way flow is real regardless of whether the field is a
primitive or a nested object; mutating a NESTED object field would actually reach the parent, which
is exactly why passing primitives (or making deliberate copies) is the safer default (co-19).

</details>

**AP10.** A `switch` over a four-variant discriminated union has three cases handled and a `default:
break;` that silently does nothing for the fourth. Six months later, a fifth variant is added to the
union elsewhere in the codebase. What happens, and how would changing that `default` case to be
typed `never` have caught the gap immediately?

<details>
<summary>Worked solution</summary>

With a bare `default: break;`, the fifth variant silently falls into the same do-nothing branch as
the original unhandled fourth -- no error, no warning, just a UI that quietly does the wrong thing
for two variants instead of one. A `default` branch that assigns the switched value to a
`never`-typed variable instead makes the compiler prove every variant is exhausted: adding a fifth
variant without a matching new `case` breaks that proof, and `tsc` reports a type error at the
`never` assignment the moment the new variant exists -- turning a silent runtime gap into an
immediate compile-time failure (co-27, co-28).

</details>

## Code katas

Six hands-on drills, spanning beginner tools through advanced component work. Each is a
self-contained, runnable HTML/CSS/JS task with a scenario distinct from the learning track's 80
worked examples -- no live third-party host is ever required for this topic's material, since every
worked example and every kata here is fully self-contained HTML/CSS/JS opened directly from disk, per
DD-30: attempt the task yourself first, then compare against the reference approach and the
genuinely captured output shown.

### Kata 1 -- Fix a heading hierarchy that skips a level

**Task.** A page has `<h1>Dashboard</h1>` followed directly by `<h3>Recent orders</h3>` (skipping
`h2`). Without changing any visible text or styling, fix the heading levels so the outline is
correctly nested.

**Reference approach**: change the skipped-level heading to `<h2>`, preserving every other heading's
relative depth beneath it.

```html
<h1>Dashboard</h1>
<h2>Recent orders</h2>
<!-- was <h3>, which skipped a level with nothing at h2 in between -->
```

**Key takeaway**: A correct document outline requires each heading level to appear in order with no
gaps -- `h1` to `h3` with no `h2` anywhere is an invalid outline even though it renders visually fine,
since visual size can be restyled with CSS independent of the semantic level (co-03).

### Kata 2 -- Write a `computeSpecificity()` sketch for two rules, without a browser

**Task.** Given the two selectors `#nav a.active` and `nav a.active.current`, reason out (without
opening a browser) which one wins if both set a conflicting `color`, and why.

**Reference approach**: count each selector's ids, classes/attributes/pseudo-classes, and elements.

```text
#nav a.active        -> 1 id, 1 class, 1 element   -> (1, 1, 1)
nav a.active.current -> 0 ids, 2 classes, 2 elements -> (0, 2, 2)
```

**Key takeaway**: `#nav a.active` wins -- specificity compares id-count first, and one id already
outranks any number of classes or elements; the second selector's extra class and element count
never even enter the comparison (co-05).

### Kata 3 -- Build a `render(state)` function for a traffic light, from scratch

**Task.** Without looking at Example 43, write a pure `render(root: HTMLElement, color: "red" |
"yellow" | "green")` function that rebuilds a single `div` inside `root` with a background color
matching `color`.

**Reference approach**:

```javascript
function render(root, color) {
  root.innerHTML = "";
  const light = document.createElement("div");
  light.style.width = "40px";
  light.style.height = "40px";
  light.style.borderRadius = "50%";
  light.style.background = color;
  root.append(light);
}
```

**Key takeaway**: The entire "UI as a function of state" idea is captured in this one small
function's shape -- clear what was there before, derive fresh output purely from the input argument,
never read or write any outside state (co-18).

### Kata 4 -- Add keyboard support to a custom disclosure toggle

**Task.** Starting from a `<div role="button" tabindex="0">` that already toggles a panel's
visibility on `click`, add the missing keyboard handling so Enter and Space also activate it.

**Reference approach**:

```javascript
toggleButton.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault(); // stop Space from also scrolling the page
    toggleButton.click(); // reuse the existing click handler's logic
  }
});
```

**Key takeaway**: `role="button"` and `tabindex="0"` get you exposed semantics and focusability for
free, but keyboard ACTIVATION is never automatic for a non-native element -- it must be wired by
hand, one more reason a real `<button>` (which needs none of this) is usually the simpler choice
(co-25, co-26).

### Kata 5 -- Model a three-variant fetch state as a discriminated union

**Task.** Without reusing Example 65-67's exact shape, design your own `FetchState<T>` discriminated
union covering `idle`, `pending`, and `done` (holding a `T` payload), and write the exhaustive
`switch` with a `never`-typed default.

**Reference approach**:

```typescript
type FetchState<T> = { kind: "idle" } | { kind: "pending" } | { kind: "done"; value: T };

function describe<T>(state: FetchState<T>): string {
  switch (state.kind) {
    case "idle":
      return "not started";
    case "pending":
      return "in flight";
    case "done":
      return `got: ${JSON.stringify(state.value)}`;
    default: {
      const exhaustive: never = state;
      return exhaustive;
    }
  }
}
```

**Key takeaway**: The exhaustiveness technique (a `never`-typed `default`) is completely general --
it applies to any tagged union with any variant names or field shapes, not just the specific
`loading`/`error`/`empty`/`loaded` union this topic's worked examples happened to use (co-27, co-28).

### Kata 6 -- Type a component's props and catch a mismatched caller

**Task.** Write a `Badge` props interface with `label: string` and `count: number`, then write one
correct call and one call passing `count` as a string literal, and predict `tsc`'s output for the
bad call before running it.

**Reference approach**:

```typescript
interface BadgeProps {
  label: string;
  count: number;
}

function Badge(props: BadgeProps): string {
  return `${props.label}: ${props.count}`;
}

Badge({ label: "Open", count: 3 }); // fine
Badge({ label: "Open", count: "3" }); // predict the tsc error before running
```

**Output** (genuinely captured, via `tsc --noEmit --strict --skipLibCheck`):

```text
error TS2322: Type 'string' is not assignable to type 'number'.
```

**Key takeaway**: A typed props interface turns a caller's shape mistake into a compile-time
`TS2322` the moment it's written, in an editor or in CI -- with no props interface at all, the same
mistake (a string where a number was expected) would only surface however the component happens to
misbehave at runtime, if it's ever even noticed (co-28).

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can name the minimum pieces a valid HTML5 document needs and what the viewport meta tag
      controls. (co-01)
- [ ] I can explain why a semantic landmark element communicates more than a visually identical
      `div`. (co-02)
- [ ] I can explain why `alt` text matters even when a filename looks descriptive. (co-03)
- [ ] I can combine an attribute selector and a pseudo-class into one selector, from memory. (co-04)
- [ ] I can explain why an id selector beats a class selector regardless of source order. (co-05)
- [ ] I can explain how a custom property redefined inside a nested scope changes what descendants
      resolve to. (co-06)
- [ ] I can compute an element's rendered width under both the default and `border-box` box models.
      (co-07)
- [ ] I can explain the difference between `display: none` and `visibility: hidden` in terms of
      layout participation. (co-08)
- [ ] I can explain what `flex-grow: 1` does to a flex child's share of leftover space. (co-09)
- [ ] I can explain the difference between `grid-template-columns` and `grid-template-areas`.
      (co-10)
- [ ] I can write a media query that changes a layout below a given viewport width, with zero
      JavaScript. (co-11)
- [ ] I can explain why `querySelectorAll`'s returned NodeList does not grow when new matching
      elements are added later. (co-12)
- [ ] I can name three DOM APIs that mutate rendered content and what each one changes. (co-13)
- [ ] I can explain the difference between an event's `target` and the element a listener is
      attached to. (co-14)
- [ ] I can explain event bubbling and why it enables delegation. (co-15)
- [ ] I can explain the difference between `preventDefault()` and `stopPropagation()`. (co-16)
- [ ] I can order `console.log` calls, a `Promise.then`, and a `setTimeout(fn, 0)` correctly by when
      each actually runs. (co-17)
- [ ] I can state, in one sentence, what "UI as a function of state" means and what it forbids.
      (co-18)
- [ ] I can explain why reassigning a prop inside a child component never changes the parent's own
      data. (co-19)
- [ ] I can name the two ingredients a minimal interactive (stateful) component needs beyond a plain
      render function. (co-20)
- [ ] I can explain what "keying" a rendered list means and the problem it solves on re-render.
      (co-21)
- [ ] I can explain both directions of a controlled input's round trip between state and the DOM.
      (co-22)
- [ ] I can name at least three pieces of the Constraint Validation API and what each is responsible
      for. (co-23)
- [ ] I can explain why a placeholder alone is not an accessible label. (co-24)
- [ ] I can explain what `role="button"` accomplishes and what it does NOT accomplish on its own.
      (co-25)
- [ ] I can explain what should happen when Tab is pressed on the last focusable element inside a
      focus trap. (co-26)
- [ ] I can explain what "exhaustive" means for a switch over a discriminated union and name the
      tool that catches a missed case. (co-27)
- [ ] I can explain when a typed-props mismatch is caught with a props interface present, versus
      without one. (co-28)

---

&larr; Previous: [Capstone](../learning/capstone/overview.md)
