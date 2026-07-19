# 14 · Frontend Essentials (By Example, TypeScript †)

**prd row**: Pass 1 · Core Foundations · By Example · TypeScript † · Learn 114 / Drill 214 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the **usable slice** — the platform (HTML/CSS/DOM), the component model, accessible forms,
and TS-for-UI, with applied component testing. Performance, SSR, and state-at-scale go to
[`47-advanced-frontend`](./47-advanced-frontend.md) (DD-11). WCAG AA intro here (Accessibility First).

## Why this exists · the big idea

- **The problem before the solution**: UIs are stateful and users are unpredictable; hand-mutating the
  DOM on every event becomes an untraceable tangle of who-changed-what.
- **Keep-this-if-you-forget-everything**: the UI is a _function of state_ — you change state and let the
  render derive the DOM, never poke the DOM directly; data flows one way.
- **Big ideas touched**: `taming-state` — unidirectional data flow makes UI state a single source of truth
  instead of scattered mutations; `abstraction-and-its-cost` — the component model buys reuse and charges
  a render/reconciliation layer between you and the DOM.

## Prerequisites

- **Prior topics**: [topic 13 Just Enough TypeScript](./13-just-enough-typescript.md) (all UI code is
  typed TS); applied testing cross-refs [topic 15 Software Testing](./15-software-testing.md).
- **Tools & environment**: a macOS/Linux terminal; **Node.js** + npm/pnpm; a pinned CVE-clean UI
  framework + build tool; **Vitest** + Testing-Library for component tests; a modern **web browser**.
- **Assumed knowledge**: TypeScript basics (types, unions, async) from topic 13; willingness to learn
  HTML/CSS (introduced here, no prior web experience assumed).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring.

- 2026-07-12 — verified (CORRECTION): cite **WCAG 2.2 AA** as the current W3C baseline (not 2.1) and the
  direction all three regimes are moving toward — but as of 2026 EN 301 549's harmonized standard is still
  **WCAG-2.1-based** (v4.1.1 with 2.2 only "expected 2026") and Section 508's binding standard is still
  **WCAG 2.0**; do not claim 2.2 is already legally adopted. Confirm at w3.org/WAI/WCAG22.
  (w3.org primary; access-board.gov; digital-strategy.ec.europa.eu)
- 2026-07-12 — verified: **Vitest 4.1.10** (5.0 in beta). `@testing-library/react` current **v16.3.2**
  (v16+ needs `@testing-library/dom` as explicit peer dep). UI framework/build tool deliberately unnamed
  in the syllabus — pin CVE-clean versions when the maker picks them. (vitest.dev / github releases)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: MDN Web Docs, WHATWG DOM/HTML Living Standards, W3C WAI-ARIA
> APG + WCAG, and registries. All CSS/DOM/events/forms/ARIA claims verified; 2 corrections applied.

- **Versions + a11y baseline** — Vitest **4.1.10**, `@testing-library/react` **v16.3.2** (bumped from
  stale v16.3.0; `@testing-library/dom` peer dep since v16). **WCAG 2.2 AA** is the current
  [W3C Recommendation](https://www.w3.org/TR/WCAG22/) (2023-10-05, errata republish 2024-12-12) — but the
  regulatory-adoption claim was **corrected**: Section 508 still binds **WCAG 2.0**
  ([Access Board](https://www.access-board.gov/ict/)), EN 301 549 harmonized standard still
  **WCAG 2.1** ([EU digital strategy](https://digital-strategy.ec.europa.eu/en/policies/latest-changes-accessibility-standard)).
- **CSS (co-05..11)** — specificity + source-order cascade, `box-sizing: border-box`, `display`
  block/inline/inline-block/none (`offsetParent` null when `display:none`), custom properties `var()`,
  flexbox main/cross axis + `flex-grow`, grid tracks — all verbatim from MDN
  ([Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity),
  [box-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing),
  [flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)).
- **DOM + events (co-12..17)** — `querySelectorAll` returns a **static (not live) NodeList** of real DOM
  elements ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll) — co-12
  wording corrected from "live nodes"); registration-order listener dispatch, bubbling/delegation,
  `preventDefault`/`stopPropagation` separation, microtasks-before-macrotasks — confirmed via MDN +
  [WHATWG DOM](https://dom.spec.whatwg.org/#dom-eventtarget-addeventlistener).
- **Forms + a11y (co-22..26)** — Constraint Validation API (`checkValidity`/`setCustomValidity`),
  `label[for]` focus, `aria-describedby`, landmark roles, `role="button"` needs manual keyboard handling +
  `tabindex`, `aria-live="polite"`, focus-trap + roving-tabindex, ≥4.5:1 AA contrast, single `h1` — all
  verbatim from MDN + [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) + [WCAG 2.2 SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- **Read more** — _Don't Make Me Think, Revisited_ (Krug, 3rd ed. 2014); _CSS: The Definitive Guide_
  (Meyer/Weyl, 5th ed. 2023); _Inclusive Components_ (Pickering, 2021); HTML Living Standard (WHATWG,
  versionless since 2011, [html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/)); WCAG 2.2 (W3C, 2023) — all author/edition/year/URL confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · html-document-structure** — a valid page is `<!doctype html>` plus `head` (charset, viewport,
  title) and `body`; the metadata decides encoding and mobile scaling.
- **co-02 · html-semantics** — semantic landmarks (`header`/`nav`/`main`/`article`/`section`/`footer`)
  convey structure and meaning that generic `div`s cannot, feeding the accessibility tree.
- **co-03 · text-and-links** — headings, paragraphs, lists, anchors, and images-with-alt form the readable,
  navigable, accessible content of a page.
- **co-04 · css-selectors** — element, class, id, attribute, descendant, and pseudo-class selectors decide
  which elements a rule targets.
- **co-05 · css-specificity-cascade** — when rules conflict, specificity and then source order decide the
  winner, and inheritance passes some properties down the tree.
- **co-06 · css-custom-properties** — custom properties (`--name`) hold reusable values resolved through
  `var()` and the cascade, enabling theming from one place.
- **co-07 · box-model** — every element is a content box wrapped in padding, border, and margin;
  `box-sizing: border-box` folds padding and border into the declared width.
- **co-08 · normal-flow-display** — `display` (block / inline / inline-block / none) governs how an element
  participates in normal document flow and layout.
- **co-09 · flexbox** — a flex container distributes and aligns children along a main and cross axis with
  `justify-content`, `align-items`, and `flex-grow`.
- **co-10 · grid** — CSS grid places children into explicit rows and columns of a two-dimensional track
  layout with gaps and named areas.
- **co-11 · responsive-media-queries** — media queries and fluid sizing adapt the layout to the viewport so
  one document serves phone through desktop.
- **co-12 · dom-selection** — `document.querySelector`/`querySelectorAll` locate the actual, currently
  rendered DOM elements (a static snapshot `NodeList`, not an auto-updating collection).
- **co-13 · dom-manipulation** — `textContent`, `createElement`, `append`, `remove`, and `classList` mutate
  the rendered tree imperatively.
- **co-14 · event-handling** — `addEventListener` binds a handler that receives an event object when the
  user interacts with an element.
- **co-15 · event-propagation** — events bubble up the ancestor chain, so one listener on a parent can
  handle events from many descendants (delegation).
- **co-16 · default-action-control** — `preventDefault` suppresses the browser's built-in behavior and
  `stopPropagation` halts bubbling.
- **co-17 · event-loop** — the browser runs a task/microtask loop; `setTimeout` and `Promise` schedule work
  after the current synchronous frame, with microtasks first.
- **co-18 · ui-as-function-of-state** — render derives the DOM from a single state value; you change state
  and re-render rather than poking the DOM ad hoc, so data flows one way.
- **co-19 · component-props** — a component is a function of its props that returns markup; props flow one
  way, parent to child.
- **co-20 · component-state** — local state plus a re-render on change models an interactive component.
- **co-21 · list-rendering** — mapping an array to DOM nodes renders a list, keyed for stable identity
  across updates.
- **co-22 · forms-controlled-input** — a controlled input mirrors state: its value comes from state and its
  input event writes the change back.
- **co-23 · form-validation** — the Constraint Validation API (`required`, `pattern`, `checkValidity`,
  `setCustomValidity`) reports invalid inputs.
- **co-24 · accessible-forms** — every input has an associated `label`, and error messages are wired to it
  via `aria-describedby` so assistive tech announces them.
- **co-25 · aria-roles-semantics** — roles and `aria-*` attributes expose widget semantics and state to
  assistive technology, meeting the WCAG 2.2 AA baseline.
- **co-26 · keyboard-navigation** — focus order, `tabindex`, and key handlers make every control operable
  without a mouse.
- **co-27 · discriminated-union-states** — a tagged union models loading / error / empty / loaded UI states
  so every case is handled exhaustively.
- **co-28 · typing-props-state** — TypeScript types on props and state catch shape mismatches before the
  component ever renders.

## Worked examples

Colocated under `frontend-essentials/learning/code/`; each is a runnable HTML/CSS/JS snippet opened in a
browser or driven with a small DOM harness (DD-20/DD-30), and each cites the `co-NN` it exercises.
Contiguous `ex-01..ex-80`.

### Beginner

- **ex-01 · minimal-html-document** — write a valid HTML5 document with doctype, `head` charset/viewport,
  and a titled `body` — verify it renders and the tab shows the title. (co-01)
- **ex-02 · semantic-page-landmarks** — mark up a page with `header`/`nav`/`main`/`footer` — verify the
  accessibility tree exposes the four landmark roles. (co-02)
- **ex-03 · headings-and-paragraphs** — build an `h1`→`h3` outline with paragraphs — verify exactly one
  `h1` and a correctly nested document outline. (co-03)
- **ex-04 · lists-and-links** — an unordered list of anchor links — verify each `a` has an `href` and its
  visible link text. (co-03)
- **ex-05 · image-with-alt** — add an `img` with descriptive `alt` — verify the alt text surfaces when the
  image fails to load. (co-03)
- **ex-06 · class-selector-style** — style a `.btn` class red — verify `getComputedStyle(el).color` reports
  the applied color. (co-04)
- **ex-07 · id-and-descendant-selector** — target `#nav a` — verify only links inside `#nav` receive the
  rule. (co-04)
- **ex-08 · attribute-and-pseudo-selector** — style `input[type=email]:focus` — verify the focused email
  input gets the border and others do not. (co-04)
- **ex-09 · specificity-conflict** — give one element a class rule and an id rule with different colors —
  verify the id rule wins. (co-05)
- **ex-10 · cascade-source-order** — two equal-specificity color rules — verify the later declaration
  applies. (co-05)
- **ex-11 · custom-property-reuse** — define `--brand` on `:root` and use `var(--brand)` in two rules —
  verify both resolve to the same computed color. (co-06)
- **ex-12 · box-model-padding-border-margin** — style a box with padding, border, and margin — verify
  `offsetWidth` equals content + padding + border. (co-07)
- **ex-13 · box-sizing-border-box** — switch the box to `box-sizing: border-box` — verify the rendered width
  equals the declared width. (co-07)
- **ex-14 · block-vs-inline** — contrast a block `div` and an inline `span` — verify the block spans full
  width while the span wraps only its content. (co-08)
- **ex-15 · inline-block-sizing** — set `display: inline-block` with a width/height — verify the element
  sits inline yet honors its declared size. (co-08)
- **ex-16 · display-none-removes-layout** — toggle `display: none` on an element — verify its `offsetParent`
  becomes `null` (removed from layout). (co-08)
- **ex-17 · select-single-node** — call `document.querySelector('.title')` — verify it returns the matching
  element. (co-12)
- **ex-18 · select-all-nodes** — call `document.querySelectorAll('li')` — verify the NodeList length equals
  the list item count. (co-12)
- **ex-19 · set-textcontent** — set an element's `textContent` — verify the rendered text updates. (co-13)
- **ex-20 · toggle-classlist** — call `el.classList.toggle('active')` twice — verify the class is added then
  removed. (co-13)
- **ex-21 · create-and-append-node** — `createElement('li')` then `append` it — verify the list grows by one
  item. (co-13)
- **ex-22 · remove-node** — call `el.remove()` — verify `querySelector` no longer finds it. (co-13)
- **ex-23 · click-handler-counter** — `addEventListener('click', …)` incrementing a counter — verify the
  displayed count rises with each click. (co-14)
- **ex-24 · input-event-mirror** — on `input`, copy the value into a `span` — verify the span mirrors typed
  text live. (co-14)
- **ex-25 · event-object-target** — read `event.target` in a handler — verify it identifies the clicked
  element. (co-14)
- **ex-26 · multiple-listeners-order** — attach two `click` listeners to one element — verify both fire in
  registration order. (co-14)
- **ex-27 · flex-row-distribution** — a flex row with `justify-content: space-between` — verify the
  children's bounding rects spread to the edges. (co-09)
- **ex-28 · flex-align-center** — center children with `align-items: center` — verify vertical centering via
  their bounding rectangles. (co-09)

### Intermediate

- **ex-29 · flex-grow-absorbs-space** — set `flex-grow: 1` on one child — verify it absorbs the remaining
  free space. (co-09)
- **ex-30 · grid-two-column** — `grid-template-columns: 1fr 1fr` — verify two children land in separate
  columns. (co-10)
- **ex-31 · grid-named-areas** — lay out with `grid-template-areas` — verify each element occupies its named
  region. (co-10)
- **ex-32 · grid-gap** — set `gap` on a grid — verify the measured spacing between tracks. (co-10)
- **ex-33 · responsive-breakpoint** — a media query that stacks columns below 600px — verify the layout
  changes when the viewport shrinks. (co-11)
- **ex-34 · responsive-fluid-image** — an image with `max-width: 100%` — verify it never overflows its
  container at any width. (co-11)
- **ex-35 · custom-property-theming** — override `--brand` inside a `.dark` scope — verify descendants
  recompute their color under the new value. (co-06, co-11)
- **ex-36 · event-bubbling** — click a child and observe a parent listener — verify the parent handler sees
  the event. (co-15)
- **ex-37 · event-delegation-list** — one listener on `ul` handling clicks on any `li` — verify clicking any
  item fires it with the correct `target`. (co-15, co-14)
- **ex-38 · prevent-default-link** — call `preventDefault()` on an anchor click — verify navigation does not
  occur. (co-16)
- **ex-39 · stop-propagation** — call `stopPropagation()` on a child — verify the parent listener does not
  fire. (co-16, co-15)
- **ex-40 · settimeout-defers-work** — schedule a DOM update via `setTimeout(fn, 0)` — verify it runs after
  the surrounding synchronous code. (co-17)
- **ex-41 · microtask-before-timeout** — log the order of `Promise.then` vs `setTimeout` — verify the
  microtask runs before the timeout. (co-17)
- **ex-42 · debounce-input** — debounce an input handler with `setTimeout` — verify only the final value is
  processed after rapid typing. (co-17, co-14)
- **ex-43 · render-from-state** — a `render(state)` function that rebuilds the DOM — verify the rendered DOM
  matches the state object. (co-18)
- **ex-44 · state-change-triggers-render** — mutate state then call `render` — verify only the derived DOM
  changes. (co-18)
- **ex-45 · counter-component** — a vanilla counter component (state + render) — verify clicking increments
  the rendered number. (co-20, co-18)
- **ex-46 · props-driven-component** — a `Greeting(props)` returning markup — verify different props yield
  different output. (co-19)
- **ex-47 · one-way-data-flow** — a parent passes data down to a child render — verify the child reflects
  parent state and cannot write back up. (co-19, co-18)
- **ex-48 · render-list-from-array** — map an array to `li` nodes — verify the rendered count equals the
  array length. (co-21)
- **ex-49 · keyed-list-update** — re-render a list with one changed item, preserving keys — verify only the
  changed node updates. (co-21, co-18)
- **ex-50 · controlled-text-input** — bind an input's value to state and write back on `input` — verify
  state and the input stay in sync. (co-22)
- **ex-51 · controlled-checkbox** — a controlled checkbox reflecting boolean state — verify toggling updates
  both state and the `checked` property. (co-22)
- **ex-52 · controlled-select** — a controlled `select` driven by state — verify choosing an option updates
  state. (co-22)
- **ex-53 · required-field-validation** — mark an input `required` and call `checkValidity()` — verify an
  empty field reports invalid. (co-23)
- **ex-54 · pattern-validation** — add a `pattern` attribute — verify non-matching input fails validity.
  (co-23)
- **ex-55 · custom-validity-message** — call `setCustomValidity(...)` on mismatch — verify the reported
  validation message. (co-23)
- **ex-56 · label-input-association** — associate a `label[for]` with an input `id` — verify clicking the
  label focuses the input. (co-24)
- **ex-57 · aria-describedby-error** — link an error message via `aria-describedby` — verify the accessible
  description includes the error text. (co-24, co-25)
- **ex-58 · form-submit-handler** — handle `submit`, `preventDefault`, and read the field values — verify
  the collected data matches the inputs. (co-22, co-16)
- **ex-59 · aria-role-button** — give a `div` `role="button"` — verify the accessibility tree exposes the
  button role. (co-25)
- **ex-60 · aria-live-region** — an `aria-live="polite"` region updated on change — verify the region's
  content updates. (co-25)

### Advanced

- **ex-61 · keyboard-tab-order** — a form whose `tabindex` yields a logical order — verify pressing Tab
  moves focus in sequence. (co-26)
- **ex-62 · keyboard-activate-custom-button** — handle Enter/Space on a `role="button"` div — verify
  keyboard activation fires the action. (co-26, co-25)
- **ex-63 · focus-trap-modal** — trap focus inside an open dialog — verify Tab cycles within the modal and
  cannot escape it. (co-26)
- **ex-64 · roving-tabindex-menu** — a menu using roving `tabindex` — verify arrow keys move focus among
  items. (co-26)
- **ex-65 · discriminated-union-loading** — model UI state as `{status:'loading'|…}` and render per case —
  verify the loading branch renders a spinner. (co-27)
- **ex-66 · discriminated-union-error** — the `error` case renders a message — verify the error branch shows
  the error text. (co-27)
- **ex-67 · discriminated-union-empty** — the `empty` case renders an empty-state — verify a zero-length
  result shows the empty view. (co-27)
- **ex-68 · discriminated-union-exhaustive** — a `switch` over all states with a `never` default — verify
  `tsc` flags a newly added missing case. (co-27, co-28)
- **ex-69 · typed-props** — a TypeScript props interface for a component — verify `tsc` rejects a
  wrong-typed prop. (co-28)
- **ex-70 · typed-state** — type the component state — verify `tsc` catches an invalid state assignment.
  (co-28)
- **ex-71 · data-list-component** — a component rendering a list across loading/error/empty/loaded — verify
  each state renders correctly. (co-27, co-21)
- **ex-72 · validated-form-component** — a controlled form with `required` + `pattern` validation and error
  display — verify an invalid submit is blocked and errors show. (co-22, co-23, co-24)
- **ex-73 · filterable-list** — filter a rendered list by a controlled search input — verify only matching
  items remain in the DOM. (co-21, co-22)
- **ex-74 · derived-value-render** — compute a derived total from state and render it — verify it updates
  when the underlying state changes. (co-18, co-20)
- **ex-75 · fix-missing-label** — take a broken unlabeled input and add a label — verify the accessible name
  is now present. (co-24)
- **ex-76 · fix-div-button-to-semantic** — replace a click-only `div` with a real `button` — verify it is
  keyboard-operable and reports the button role. (co-25, co-26)
- **ex-77 · fix-color-contrast** — raise text/background contrast to WCAG AA — verify the computed contrast
  ratio is ≥ 4.5:1. (co-25, co-05)
- **ex-78 · delegated-dynamic-list** — add/remove items handled by one delegated listener on a re-rendered
  list — verify new items work without rebinding handlers. (co-15, co-21)
- **ex-79 · responsive-grid-component** — a card grid that reflows its column count across breakpoints —
  verify the column count changes with the viewport. (co-10, co-11)
- **ex-80 · accessible-interactive-widget** — assemble a keyboard-operable, labeled, state-driven disclosure
  widget — verify it toggles its content and is fully keyboard- and AT-operable. (co-25, co-26, co-18)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small accessible single-feature UI (e.g. a filterable task list with an add form)
  with typed props/state, loading/error/empty states via a discriminated union, keyboard-accessible
  controls, and Testing-Library unit tests — runnable and testable from the CLI.
- **Concepts exercised**: [ ] components + props + state [ ] list rendering + events [ ] controlled
  validated form [ ] discriminated-union UI states [ ] WCAG AA semantics + keyboard nav [ ] Vitest +
  Testing-Library tests.
- **Ordered steps**:
  1. `.../learning/capstone/code/` — the app scaffold + a typed `TaskList` component. Verify
     `npm run test` (Vitest) passes the initial render test.
  2. Add the add-form (controlled, validated) + filter. Verify tests cover valid/invalid submit + filter.
  3. Wire loading/error/empty states via a discriminated union. Verify each state renders + is tested.
  4. Accessibility pass: labels, roles, keyboard nav. Verify a Testing-Library query-by-role test passes.
- **Acceptance criteria**: all Vitest tests green; the feature is keyboard-operable; every UI state is
  reachable and tested; `tsc --noEmit` clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Don't Make Me Think, Revisited** — Steve Krug (3rd ed., 2014). Classic plain-language web-usability guide; the field's most-cited entry point.
- **CSS: The Definitive Guide** — Meyer, Weyl (5th ed., 2023). Canonical deep reference on CSS layout, box model, specificity.
- **Inclusive Components** — Heydon Pickering (2021). Accessibility-first patterns for building common UI components correctly.

**Papers & articles**

- **HTML Living Standard** — WHATWG (continuously updated). Official canonical HTML spec, versionless since 2011. <https://html.spec.whatwg.org/multipage/>
- **Web Content Accessibility Guidelines (WCAG) 2.2** — W3C (2023). Normative accessibility standard behind WCAG AA. <https://www.w3.org/TR/WCAG22/>

---

← Previous: [13 · Just Enough TypeScript](./13-just-enough-typescript.md) · Next: [15 · Software Testing](./15-software-testing.md) →
