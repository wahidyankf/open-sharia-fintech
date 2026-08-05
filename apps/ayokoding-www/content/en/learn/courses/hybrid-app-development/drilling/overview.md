---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This active-recall track rehearses Flutter design choices before code. Answer each prompt before opening its disclosure; the target is a defensible owner, boundary, or fallback rather than memorizing widget names.

## Recall Q&A

**Q1 (co-03, co-04).** When should a widget be stateless rather than stateful?

<details><summary>Answer</summary>Use `StatelessWidget` when configuration fully determines the render. Use a stateful widget only when that location owns a mutable lifecycle-bound value or resource.</details>

**Q2 (co-07, co-08).** What belongs in `initState`, `dispose`, and `setState`?

<details><summary>Answer</summary>Acquire one-time owned resources in `initState`, release them in `dispose`, and use `setState` only for local changes that affect this subtree's render.</details>

**Q3 (co-16, co-18).** Why is a cart a poor fit for one screen's `setState`?

<details><summary>Answer</summary>Multiple screens need the same source of truth. Put the cart in app state and let each screen observe it rather than copying state during navigation.</details>

**Q4 (co-22, co-23).** Where should a future be created for a `FutureBuilder`?

<details><summary>Answer</summary>Create it outside `build`, commonly in `initState` or a state owner. Recreating it during every build can restart changing work unexpectedly.</details>

**Q5 (co-25, co-30).** What is the safe result of a missing platform channel implementation?

<details><summary>Answer</summary>Catch the expected unsupported path at the channel boundary and render a documented fallback. Do not let an optional native capability crash a shared UI.</details>

## Applied Problems

**AP1.** A detail screen and a badge on the list must update after saving one article. What owns that value?

<details><summary>Answer</summary>A shared app-state object such as `ChangeNotifier` supplied above both screens. The detail route receives an ID or article value, not a copied saved collection.</details>

**AP2.** A phone list needs a detail route, but a wide desktop layout should show list and detail together. What remains stable?

<details><summary>Answer</summary>The selected article state and the detail widget. `LayoutBuilder` chooses containment and layout; it should not create a second data source.</details>

**AP3.** An HTTP call fails after cached rows are already visible. What should the screen render?

<details><summary>Answer</summary>Keep useful cached content, surface a non-blocking failure and retry action, and let a named state owner decide the transition. Do not replace meaningful content with a blank error.</details>

**AP4.** A team proposes a state library before any provider or inherited-state model is understood. What question should block the decision?

<details><summary>Answer</summary>Which concrete coordination problem exceeds the core model? A package is justified by a named state boundary or workflow, not by its popularity.</details>

**AP5.** A capability is available only on Android. Where should platform branching live?

<details><summary>Answer</summary>At a small plugin or channel adapter with a fallback result. Widgets should render that result without scattering platform checks through the screen tree.</details>

## Deliberate Practice

1. Turn a monolithic `Scaffold` into a stateless row widget, a stateful filter widget, and a provider-owned saved collection. Name each owner's mutation authority.
2. Write a `FutureBuilder` with loading, data, empty, and error branches. Move the future out of `build`, then explain the rebuild bug you prevented.
3. Build a narrow list/detail route and a wide `LayoutBuilder` master-detail rendering from the same selected ID.
4. Wrap `MethodChannel.invokeMethod` in an adapter that converts `MissingPluginException` into a user-readable fallback. Keep all platform strings there.
5. Write a widget test that taps a save control, pumps the tree, and asserts both the button label and saved-count text changed.

## Automaticity Checklist

- [ ] I can choose a widget, local state owner, or app state owner by who needs to mutate and observe a value.
- [ ] I can explain the `initState` / `build` / `dispose` lifecycle without treating rebuild as recreation.
- [ ] I can choose `Navigator` or a declarative router after identifying deep-link and restoration requirements.
- [ ] I can keep loading, content, empty, and error states distinct in asynchronous UI.
- [ ] I can make a platform capability and its unsupported fallback explicit at one edge.
- [ ] I can use `LayoutBuilder` to change layout without duplicating application state.
- [ ] I can choose unit, widget, or integration tests according to the claim being made.

## Explain Why

**Why does Flutter's shared rendering model not eliminate native-platform work?**

<details><summary>Answer</summary>Permissions, keyboards, background behaviour, new OS APIs, packaging, and last-mile visual conventions still belong to their targets. Flutter shares the app surface, but every real product needs an explicit policy for those seams.</details>

**Why is a visible fallback better than silently ignoring an unsupported plugin feature?**

<details><summary>Answer</summary>A visible fallback protects user trust and gives support staff an observable state. Silent failure makes a platform limitation look like a random data or interaction bug.</details>

**Why should a course teach `setState` before provider?**

<details><summary>Answer</summary>Local state makes ownership and rebuild behaviour concrete. Provider solves a different problem—sharing a source of truth—so introducing it first hides the reason its additional structure exists.</details>
