# 48 · Build Your Own Reactive UI (By Example, TypeScript †)

**prd row**: Pass 3 · Build for the Real World · By Example · TypeScript † · Learn 148 / Drill 248 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the build-your-own tier for the frontend band — a minimal reactive UI runtime that
demystifies React/Vue/Solid by building the core two ways: a virtual DOM + diff/patch, and a
signals-based fine-grained reactive graph, each with its own render loop. Interleaved after
[`47-advanced-frontend`](./47-advanced-frontend.md), it turns "the framework re-renders" into a
mechanism you can single-step. `†`: TypeScript, strict-mode typed throughout — components, virtual
nodes, and signals are all fully typed.

## Why this exists · the big idea

- **The problem before the solution**: hand-written DOM code drifts out of sync with your data — you
  change state in one place and forget to update the three spots that display it, and "why didn't the
  screen update?" becomes a daily bug. Frameworks solve this, but as a black box you can't debug a
  stale render or a performance cliff you don't understand.
- **Keep-this-if-you-forget-everything**: a reactive UI is a function of state to view, plus a way to
  re-run only what changed — whether by diffing a virtual tree against the last one, or by tracking
  which computations read which signals and re-running exactly those. Same goal, two mechanisms.
- **Big ideas touched**: `abstraction-and-its-cost` (a framework hides the DOM behind declarative
  render — building it reveals the diff/subscription bookkeeping that convenience costs, and where it
  bites performance), `taming-state` (the entire topic is a strategy for making mutable UI state
  reason-about-able — the virtual DOM and the signal graph are two different disciplines for the same
  enemy).

## Prerequisites

- **Prior topics**: [topic 13 Just Enough TypeScript](./13-just-enough-typescript.md) (generics,
  discriminated unions, strict typing) and [topic 47 Advanced Frontend](./47-advanced-frontend.md)
  (rendering models, reconciliation, the framework you're now rebuilding).
- **Tools & environment**: a macOS/Linux terminal; **Node.js** at a current LTS with **TypeScript**
  in strict mode; a bundler/dev server and a jsdom-or-browser test harness; no UI framework — that's
  the point; Neovim/VSCode with the TypeScript LSP (DD-17).
- **Assumed knowledge**: DOM APIs and events from the outside (topic 14/47); using a component
  framework as a consumer (topic 47); TypeScript generics and unions (topic 13).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the two mechanisms are correctly framed as coexisting, not one superseding
  the other — the **virtual-DOM + reconciler** lineage (React's Fiber) and the **fine-grained signals**
  lineage (Solid, Vue's reactivity, Preact Signals) are both current, mainstream approaches. Left
  version-unpinned since the concepts, not any framework release, are the subject.
- 2026-07-12 — verified (GAP for plan owner): signals have broadly converged across frameworks but the
  exact API surface (e.g. a proposed TC39 Signals standard) is still moving — teach the _mechanism_
  (dependency tracking + a reactive graph) rather than any one library's or proposal's current API,
  and re-check the standardization status at drafting time.

> DD-35 primary-source pass (2026-07-12). Mechanics traced to official docs (react.dev,
> legacy.reactjs.org for reconciliation, vuejs.org reactivity, preactjs.com signals, lit.dev,
> facebook/react's react-reconciler README) and fetched/read. Builder tutorials and core-member
> write-ups are flagged as non-spec. Unverifiable items flagged `[Needs Verification]`.

- **Reconciliation heuristic** — "the state of the art algorithms have a complexity in the order of O(n³)
  … React instead implements a heuristic O(n) algorithm" on two assumptions: (1) "Two elements of different
  types will produce different trees"; (2) "the developer can hint at which child elements may be stable …
  with a `key` prop." "Whenever the root elements have different types, React will tear down the old tree
  and build the new tree from scratch." Source: [Reconciliation (legacy.reactjs.org)](https://legacy.reactjs.org/docs/reconciliation.html) — the **frozen** but canonical explainer ("old and won't be updated").
- **Keys** — "When children have keys, React uses the key to match children in the original tree with
  children in the subsequent tree"; "unstable keys (like those produced by `Math.random()`) will cause many
  … DOM nodes to be unnecessarily recreated." Current framing: identity is by tree **position**, and keys
  override it. Source: [react.dev, Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state) (fetched).
- **Hyperscript / createElement** — `h()` "is short for **hyperscript** — 'JavaScript that produces HTML'"
  ([Vue render-function docs](https://vuejs.org/guide/extras/render-function.html)); `createElement(type, props, ...children)` returns an object with `type`, `props`, `ref`, `key`, and "`<Something />` is
  equivalent to `createElement(Something)`" ([react.dev, createElement](https://react.dev/reference/react/createElement)). Both fetched, verbatim.
- **Signals** — "a signal is an object with a `.value` property … the signal itself always stays the same";
  "computed signals track which signals are accessed and re-run their callback when those signals change";
  "Accessing a signal's `.value` … within a component automatically re-renders" it. Source: [Preact Signals](https://preactjs.com/guide/v10/signals/) (fetched, verbatim).
- **Automatic dependency tracking** — Vue's illustrative `track()`: "we check whether there is a currently
  running effect. If there is one, we lookup the subscriber effects … and add the effect to the Set,"
  stored as `WeakMap<target, Map<key, Set<effect>>>`; `trigger()` "invoke[s] them." MobX: "reacts to any
  existing observable property that is read during the execution of a tracked function" (async reads are
  **not** tracked). Sources: [Vue — Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth), [MobX — Understanding Reactivity](https://mobx.js.org/understanding-reactivity.html) (fetched). Vue notes the snippets are simplified, "not Vue's literal source."
- **Proxy vs getter/setter** — "In Vue 3, **Proxies** are used for reactive objects and getter/setters are
  used for refs." Source: [Vue — Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth) (fetched).
- **Compiled fine-grained (Solid)** — "Instead of using a Virtual DOM, it compiles its templates to real
  DOM nodes and updates them with fine-grained reactions"; "when a piece of state changes, only the code
  that depends on it will rerun." Source: [solidjs/solid README](https://github.com/solidjs/solid) (fetched). `docs.solidjs.com` is Cloudflare-blocked to fetch — verbatim SolidJS-docs quotes `[Needs Verification]`.
- **Observer pattern** — ReactiveX "extends the observer pattern to support sequences of data and/or events"
  and is "a 'push' equivalent to Iterable, which is a 'pull'." Source: [ReactiveX Introduction](https://reactivex.io/intro.html) (fetched). The GoF 1994 "Observer" definition is bibliographically solid but `[Needs Verification]` as a fetched primary quote.
- **Hooks call-order rule** — "you can only call [Hooks] at the top level of your component … You can't call
  [them] inside loops or conditions." Source: [react.dev, useState](https://react.dev/reference/react/useState) + [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) (fetched). The _why_ (per-fiber call-index state) is community/Fiber knowledge, `[Needs Verification]` as an official quote.
- **useEffect timing** — "Effects run at the end of a commit after the screen updates"; cleanup runs "with
  the old values" before the next setup; deps compared with `Object.is`. Source: [react.dev, useEffect](https://react.dev/reference/react/useEffect) (fetched).
- **Event delegation** — pre-React-17 "React attaches one handler per event type directly at the `document`
  node"; React 17+ "attach[es] them to the root DOM container … `rootNode.addEventListener()` under the
  hood." Source: [React v17 RC — Changes to Event Delegation](https://legacy.reactjs.org/blog/2020/08/10/react-v17-rc.html) (fetched).
- **Batching / scheduling** — "Batching is when React groups multiple state updates into a single re-render";
  React 18 automatic batching extends this to promises/`setTimeout`/native handlers ([react.dev, v18 release](https://react.dev/blog/2022/03/29/react-v18)). Vue "buffers [DOM updates] until the 'next tick' to ensure that each component updates only once" via a Promise (microtask) — `nextTick` ([Vue API](https://vuejs.org/api/general.html)).
- **Templates → DOM (lit)** — "Lit templates are written using JavaScript template literals tagged with the
  `html` tag … an array of strings (the static portions) and an array of expressions (the dynamic
  portions)," so Lit "can re-render only the parts … that have changed." Source: [Lit — Templates overview](https://lit.dev/docs/templates/overview/) (fetched).
- **Reconciler / renderer split** — `react-reconciler` is "an **experimental** package for creating custom
  React renderers"; a renderer provides a **host config** "that describes how to make something happen in
  the 'host' environment (e.g. DOM, canvas, console)." Source: [react-reconciler README](https://github.com/facebook/react/tree/main/packages/react-reconciler) (fetched — note "experimental"). Companion: [acdlite/react-fiber-architecture](https://github.com/acdlite/react-fiber-architecture) — a fiber is "a **unit of work** … a virtual stack frame" — **authored by a React core member but explicitly "not an official document"**; flag on every citation.
- **Reactivity glitches / diamond** — MobX's creator: "All reactions happen synchronously and … glitch-free,"
  achieved by counting ready/stale messages so a shared computed "will only re-evaluate after [its
  dependency] has become stable." Source: [Weststrate, "Becoming fully reactive"](https://medium.com/hackernoon/becoming-fully-reactive-an-in-depth-explanation-of-mobservable-55995262a254) (2015, author = MobX creator; personal blog, not official docs). Note: the claim that Knockout's docs coin "diamond dependency problem" / expose `ko.atomically()` was **not** confirmed in the actual docs — treat that naming as `[Needs Verification]`; Knockout's docs call it the "cascade problem."
- **Disposal / cleanup** — Vue's `effectScope()` "can capture the reactive effects … so that these effects
  can be disposed together"; `onScopeDispose(fn)` "will be invoked when the associated effect scope is
  stopped." Source: [Vue — Reactivity Advanced](https://vuejs.org/api/reactivity-advanced.html) (fetched). SolidJS `onCleanup` "runs when that scope is disposed or refreshed" — `[Needs Verification]` (docs.solidjs.com Cloudflare-blocked).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · view-as-function-of-state** — the UI is a pure function of state; a render loop keeps the DOM matching it.
- **co-02 · hyperscript** — `h(type, props, children)` constructs a virtual node object.
- **co-03 · jsx-to-h** — JSX compiles down to `h()`/`createElement` calls.
- **co-04 · virtual-node-tree** — a plain-object tree (`{ type, props, children }`) describing the UI.
- **co-05 · mount-render** — recursively render a virtual tree into real DOM nodes (props, children, text).
- **co-06 · diff-algorithm** — compute the minimal set of changes between two virtual trees.
- **co-07 · patch-apply** — apply the computed diff to the real DOM, mutating only what changed.
- **co-08 · reconciliation-heuristic** — the O(n) heuristic resting on the different-type and key assumptions (React).
- **co-09 · same-type-reuse** — a same-type element reuses (and preserves the identity of) its existing DOM node.
- **co-10 · different-type-rebuild** — a different-type element tears down the old subtree and builds a new one.
- **co-11 · keys-list-diffing** — keys match list children across renders so a reorder moves nodes.
- **co-12 · keys-identity-bug** — unstable/positional keys recreate nodes and lose their state.
- **co-13 · signal-primitive** — a signal holds a value behind a `.value` getter/setter; the signal itself is stable.
- **co-14 · computed** — a derived signal that recomputes from its dependencies.
- **co-15 · effect** — a side-effecting computation that re-runs when its dependencies change.
- **co-16 · automatic-dependency-tracking** — reading a signal during a computation subscribes the running computation to it.
- **co-17 · reactive-graph** — the dependency graph linking signals → computeds → effects.
- **co-18 · observer-pattern** — the pub/sub substrate: a subject notifies its dependents on change.
- **co-19 · fine-grained-update** — only the dependent computations re-run; no whole-tree diff.
- **co-20 · component-model** — function components with read-only props flowing parent → child.
- **co-21 · state-hook** — closure/index-based local component state (a `useState` clone).
- **co-22 · hooks-call-order** — hooks are matched by call order, so they must be called at the top level unconditionally.
- **co-23 · effect-hook** — a lifecycle hook that runs after render, cleans up, and honours a dependency array.
- **co-24 · event-delegation** — one root/document listener dispatching to handlers vs a listener per node.
- **co-25 · batching-scheduling** — group multiple state changes into a single flush (microtask / `requestAnimationFrame`).
- **co-26 · proxy-reactivity** — a `Proxy`-based `reactive()` whose get trap tracks and set trap triggers (Vue).
- **co-27 · compiled-reactivity** — compile templates to direct DOM updates with no virtual DOM (Solid).
- **co-28 · memoization** — cache a computed value and recompute only when a dependency changes.
- **co-29 · template-literal-dom** — a tagged template (`html\`…\``) splitting static strings from dynamic holes (lit-html style).
- **co-30 · reconciler-renderer-split** — a reconciler plus a host-config renderer targeting DOM/canvas/anything.
- **co-31 · diamond-problem** — glitch-free updates via topological ordering so a shared node recomputes once.
- **co-32 · disposal-cleanup** — dispose reactive computations/scopes to release subscriptions and avoid leaks.

## Worked examples

Colocated under `build-your-own-reactive-ui/learning/code/` as TypeScript strict-mode source (no `any`);
each runnable in a browser/jsdom harness (DD-20/DD-30/DD-34). Contiguous `ex-01..ex-80`. Every example
cites the `co-NN` it exercises; concepts are taught before the examples that use them.

### Beginner

- **ex-01 · h-function** — a typed `h(type, props, children)` — verify it returns a well-formed VNode. (co-02)
- **ex-02 · h-nested** — nested `h()` calls build a tree — verify the child structure. (co-02, co-04)
- **ex-03 · vnode-shape** — a `VNode` type `{ type, props, children }` — verify the type discriminates element vs text. (co-04)
- **ex-04 · jsx-desugar** — JSX compiles to `h()` calls — verify the desugared output matches manual `h()`. (co-03)
- **ex-05 · text-vnode** — a text virtual node — verify it renders a text node. (co-04)
- **ex-06 · mount-element** — render an element VNode to a DOM node — verify the tag matches. (co-05)
- **ex-07 · mount-props** — apply props/attributes on mount — verify the attributes appear. (co-05)
- **ex-08 · mount-children** — recursively mount children — verify nesting in the DOM. (co-05)
- **ex-09 · mount-text** — mount a text node — verify the text content. (co-05)
- **ex-10 · view-as-function** — a `render(state)` produces a tree — verify the tree reflects the state. (co-01)
- **ex-11 · rerender-naive** — naive full re-mount on state change — verify the DOM updates (but loses identity). (co-01)
- **ex-12 · diff-text-change** — diff detects a changed text node — verify the delta names it. (co-06)
- **ex-13 · patch-text** — patch updates only the text node — verify siblings are untouched. (co-07)
- **ex-14 · diff-prop-change** — diff detects a changed attribute — verify the delta. (co-06)
- **ex-15 · patch-prop** — patch updates the attribute in place — verify the node is reused. (co-07)
- **ex-16 · diff-add-child** — diff detects an added child — verify the delta. (co-06)
- **ex-17 · patch-add-child** — patch appends the new node — verify insertion. (co-07)
- **ex-18 · diff-remove-child** — diff detects a removed child — verify the delta. (co-06)
- **ex-19 · patch-remove-child** — patch removes the node — verify removal. (co-07)
- **ex-20 · same-type-reuse** — a same-type element reuses its DOM node — verify node identity preserved. (co-08, co-09)
- **ex-21 · different-type-replace** — a different-type element replaces the node — verify the old node is gone. (co-10)
- **ex-22 · node-identity-preserved** — assert an unchanged node keeps its identity across renders — verify `===`. (co-09)
- **ex-23 · event-listener-bind** — bind an `onClick` handler on mount — verify the click fires. (co-24)
- **ex-24 · event-update** — patch swaps the handler on update — verify the new handler fires. (co-24)
- **ex-25 · signal-value** — a signal holds and returns a value — verify the read. (co-13)
- **ex-26 · signal-set** — setting `.value` updates the stored value — verify the next read. (co-13)

### Intermediate

- **ex-27 · keyed-list-diff** — keys match list children across renders — verify matched nodes. (co-11)
- **ex-28 · keyed-reorder-moves** — a reorder moves keyed nodes rather than recreating them — verify node identity preserved. (co-11)
- **ex-29 · unkeyed-list-bug** — an unkeyed reorder recreates/mismatches — verify the wrong reuse. (co-12)
- **ex-30 · unstable-key-loses-state** — random keys lose input state — verify the reset. (co-12)
- **ex-31 · keyed-insert** — insert into a keyed list — verify existing nodes survive. (co-11)
- **ex-32 · keyed-remove** — remove from a keyed list — verify the right node is removed. (co-11)
- **ex-33 · signal-effect** — an effect re-runs when its signal changes — verify the re-run. (co-15, co-16)
- **ex-34 · effect-dependency-track** — the effect subscribes by reading the signal — verify only-read signals are tracked. (co-16)
- **ex-35 · computed-derive** — a computed derives from signals — verify the derived value. (co-14)
- **ex-36 · computed-lazy** — a computed recomputes only when read after a change — verify laziness. (co-14, co-28)
- **ex-37 · computed-cache** — a computed caches until a dependency changes — verify no recompute without change. (co-28)
- **ex-38 · reactive-graph-build** — the graph links signals → computeds → effects — verify the edges. (co-17)
- **ex-39 · fine-grained-update** — only dependents re-run on a change — verify unrelated computations don't. (co-19)
- **ex-40 · observer-subscribe** — a subject notifies its observers — verify all are called. (co-18)
- **ex-41 · observer-unsubscribe** — remove an observer — verify it stops being called. (co-18)
- **ex-42 · effect-cleanup** — an effect's cleanup runs before its re-run — verify order. (co-23, co-32)
- **ex-43 · dispose-effect** — disposing an effect stops it re-running — verify no further runs. (co-32)
- **ex-44 · dispose-avoids-leak** — disposal frees subscriptions — verify the graph edge is gone. (co-32)
- **ex-45 · component-function** — a function component returns a tree — verify the rendered output. (co-20)
- **ex-46 · component-props** — props flow parent → child, read-only — verify a child can't mutate props. (co-20)
- **ex-47 · usestate-closure** — a closure/index-based `useState` — verify state persists across renders. (co-21)
- **ex-48 · usestate-rerender** — `setState` triggers a re-render — verify the DOM updates. (co-21)
- **ex-49 · hooks-call-order** — hooks are indexed by call order — verify state maps to the right hook. (co-22)
- **ex-50 · hooks-conditional-bug** — a conditional hook breaks the index — verify the mismatch. (co-22)
- **ex-51 · useeffect-after-render** — an effect runs after render — verify ordering. (co-23)
- **ex-52 · useeffect-deps** — the dependency array gates the effect — verify a stable dep skips it. (co-23)
- **ex-53 · memoize-computed** — memoize an expensive derived value — verify one computation per change. (co-28)
- **ex-54 · signal-vs-vdom-update** — a signal update skips the diff — verify no tree walk occurs. (co-19)

### Advanced

- **ex-55 · batching-multiple-sets** — batch multiple sets into one flush — verify a single re-render. (co-25)
- **ex-56 · microtask-schedule** — schedule the flush on a microtask — verify it runs after the current task. (co-25)
- **ex-57 · raf-schedule** — schedule DOM work on `requestAnimationFrame` — verify it runs before paint. (co-25)
- **ex-58 · proxy-reactive** — a `Proxy`-based `reactive()` with get/set traps — verify reads/writes are intercepted. (co-26)
- **ex-59 · proxy-track** — the get trap tracks the active effect — verify the subscription. (co-26, co-16)
- **ex-60 · proxy-trigger** — the set trap triggers subscribers — verify they re-run. (co-26)
- **ex-61 · ref-getter-setter** — a `ref()` as a getter/setter signal — verify `.value` semantics. (co-13, co-26)
- **ex-62 · compiled-updates** — a compiled template updates the DOM directly (no VDOM) — verify no diff runs. (co-27)
- **ex-63 · compiled-vs-vdom** — compare compiled fine-grained vs VDOM diff — verify the work difference. (co-27, co-19)
- **ex-64 · template-literal-html** — a tagged `html\`…\`` template — verify it produces DOM. (co-29)
- **ex-65 · template-static-dynamic** — split static strings from dynamic holes — verify the parts array. (co-29)
- **ex-66 · template-update-holes** — update only the dynamic holes — verify static parts are untouched. (co-29, co-19)
- **ex-67 · reconciler-host-config** — a reconciler parameterized by a host config — verify it drives a target. (co-30)
- **ex-68 · custom-renderer** — a custom renderer to a non-DOM target (e.g. a string/canvas) — verify the output. (co-30)
- **ex-69 · fiber-unit-of-work** — a fiber as a unit of work in a work loop — verify incremental processing. (co-30)
- **ex-70 · diamond-problem** — build a diamond dependency graph — verify the shared node's two paths. (co-31)
- **ex-71 · diamond-glitch** — a naive graph recomputes the shared node twice (a glitch) — verify the double run. (co-31)
- **ex-72 · topological-order** — topological ordering fixes the glitch — verify the order. (co-31)
- **ex-73 · diamond-single-recompute** — the shared node recomputes once — verify a single run. (co-31)
- **ex-74 · cleanup-on-unmount** — a component's cleanup runs on unmount — verify the teardown. (co-32, co-23)
- **ex-75 · effect-scope-dispose** — dispose a scope of effects together — verify all stop. (co-32)
- **ex-76 · nested-effects** — nested effects track independently — verify each has its own deps. (co-15, co-17)
- **ex-77 · signal-batch-consistency** — a batch keeps derived values consistent — verify no intermediate glitch is observed. (co-25, co-31)
- **ex-78 · event-delegation-root** — one root listener dispatches to handlers — verify a single `addEventListener`. (co-24)
- **ex-79 · view-function-full** — a full `view = f(state)` loop driven by signals — verify state changes flow to the DOM. (co-01, co-19)
- **ex-80 · reactive-ui-capstone** — the same to-do/counter app twice — a typed virtual DOM with keyed diffing and a render loop, and a fine-grained signal graph — plus a measured comparison — verify both render/update correctly, keyed diffing preserves node identity, signal updates are fine-grained, and the comparison reports where each does more/less work. (co-05, co-07, co-11, co-16, co-19, co-30)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a minimal reactive UI runtime twice over the same small app (a to-do/counter list)
  — once as a typed virtual DOM with keyed diffing and a render loop, once as a fine-grained signal
  graph — and produce a short measured comparison of their update behaviour, proving you understand
  both mechanisms the mainstream frameworks use.
- **Concepts exercised**: [ ] hyperscript/virtual node tree (co-02, co-04) [ ] diff/patch to minimal DOM
  mutations (co-06, co-07) [ ] keyed list reconciliation (co-11) [ ] signal/computed/effect dependency
  tracking (co-13, co-14, co-15, co-16) [ ] component state + cleanup (co-21, co-32) [ ] a measured
  virtual-DOM-vs-signals comparison (co-19).
- **Ordered steps**:
  1. `.../learning/capstone/code/vdom/` — a typed `h`/`render`/`diff`/`patch` runtime. Verify the same
     app re-renders by mutating only changed nodes (assert DOM node identity is preserved where
     unchanged); TypeScript strict, no `any`.
  2. `.../learning/capstone/code/vdom/reconcile.ts` — add keyed list diffing. Verify a reorder moves
     existing nodes rather than recreating them.
  3. `.../learning/capstone/code/signals/` — a `signal`/`computed`/`effect` runtime with dependency
     tracking. Verify that changing one signal re-runs only its dependents.
  4. `.../learning/capstone/code/compare.md` + a bench script — build the app on both and measure. Verify
     the note reports where each mechanism does more/less work and why.
- **Acceptance criteria**: both runtimes render and update the app correctly; keyed diffing preserves
  node identity; signal updates are fine-grained; the comparison is concrete and measured; all
  TypeScript is strict-mode typed with no `any`.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Papers & articles**

- **Build your own React** — Rodrigo Pombo (2019). The most widely shared, interactive walkthrough of
  building a Fiber-style reconciler and virtual DOM from scratch, based on React 16.8's architecture.
  <https://pomb.us/build-your-own-react/>
- **How to write your own Virtual DOM** — Denis Radin (2017). Compact, widely referenced tutorial
  implementing a virtual DOM's `h`/`render`/`diff`/`patch` functions from first principles.
  <https://medium.com/@deathmood/how-to-write-your-own-virtual-dom-ee74acc13060>
- **Svelte 3: Rethinking Reactivity** — Rich Harris (2019). The post/talk that reframed UI reactivity
  around compile-time signals rather than a virtual DOM, influential across the signals-based framework
  generation (Solid, Vue 3, Preact Signals). <https://svelte.dev/blog/svelte-3-rethinking-reactivity>
- **Building a Reactive Library from Scratch** — Ryan Carniato (2020). Written by SolidJS's creator;
  walks through implementing fine-grained signal-based reactivity from first principles.
  <https://dev.to/ryansolid/building-a-reactive-library-from-scratch-1i0p>

---

← Previous: [47 · Advanced Frontend](./47-advanced-frontend.md) · Next: [49 · Information Architecture & SEO](./49-information-architecture-and-seo.md) →
