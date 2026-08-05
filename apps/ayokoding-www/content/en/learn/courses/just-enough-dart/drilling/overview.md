---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to the learning track. Answer before opening a disclosure:
recognizing a Dart feature in a Flutter codebase is not the same as selecting it under pressure.

## Recall Q&A

**Q1 (co-03).** What is the practical difference between `final` and `const`?

<details><summary>Answer</summary>`final` receives one value at runtime; `const` requires a compile-time constant. Neither name can be reassigned.</details>

**Q2 (co-06, co-08).** What does `String? name` require before code can use `name` as a `String`?

<details><summary>Answer</summary>It requires an explicit absence strategy such as `?.`, `??`, a guard, or a proven non-null invariant. Plain `String` is non-nullable.</details>

**Q3 (co-10).** When should a parameter be both named and `required`?

<details><summary>Answer</summary>When every caller must supply it but a label makes its role clearer, especially alongside other values of the same type.</details>

**Q4 (co-18).** What freedom does a factory constructor have that a generative constructor does not?

<details><summary>Answer</summary>A factory can return an existing instance, a cached instance, or a subtype rather than always allocating a new instance of its own class.</details>

**Q5 (co-24, co-25).** What is the difference between a `Future<T>` and a `Stream<T>`?

<details><summary>Answer</summary>A future completes with one later result or error; a stream delivers zero or more later events and has a subscription lifecycle.</details>

## Applied Problems

**AP1.** A map lookup may not contain an account ID, and the UI should show `Unknown`. Which expression keeps the result non-nullable?

<details><summary>Answer</summary>`final label = accounts[id] ?? 'Unknown';` maps expected absence to the local display policy.</details>

**AP2.** A widget constructor needs `title`, `message`, and a callback. Which parameter style prevents swapping the two strings?

<details><summary>Answer</summary>Use named parameters, marking inputs `required` when no sensible default exists.</details>

**AP3.** A function returns a local coordinate pair that has no behavior and is immediately destructured. Should it define a class?

<details><summary>Answer</summary>Not necessarily. A named record such as `({int x, int y})` is concise and preserves each role at the call site.</details>

**AP4.** A repository emits status changes until a screen closes. Does `await` on one future model that relationship?

<details><summary>Answer</summary>No. Model many values with a `Stream`, then ensure a screen or controller owns cancellation or stream completion behavior.</details>

**AP5.** A helper works for any sortable type. How can its signature prohibit a type without comparison?

<details><summary>Answer</summary>Use a bound such as `T extends Comparable<T>` so the implementation may call `compareTo` and callers get static checking.</details>

## Deliberate Practice

1. Write `String displayName(String? name)` that returns `Guest` for `null`, then change it to
   return early from a function that should print only present names.
2. Given `List<int>? extra`, build `[0, ...?extra, 5]`. Test both a null input and `[1, 2]`.
3. Create a `Temperature` class with a final Celsius field and a getter that computes Fahrenheit.
   Explain why a stored second field would create two sources of truth.
4. Create `mixin Timestamped` with one formatting method, apply it to a generic `Event<T>` class,
   and use it with `Event<String>`.
5. Write `Stream<int> countTo(int end) async*`, consume it with `await for`, and add a test that
   checks the emitted values arrive in order.

## Automaticity Checklist

- [ ] I can choose `var`, `final`, `const`, and `dynamic` based on their type and assignment contracts.
- [ ] I can replace an unsafe `!` with a safe access, fallback, validation error, or early return.
- [ ] I can choose named parameters for roles that need call-site labels.
- [ ] I can read collection `if`, `for`, spread, `map`, and a generic type parameter without translating them into mutation first.
- [ ] I can choose a class, named record, mixin, or factory based on the ownership and identity the value needs.
- [ ] I can distinguish one later `Future` value from a stream of events and identify who owns stream cleanup.

## Explain Why

**Why is `dynamic` a boundary tool rather than a convenient substitute for a missing model?**

<details><summary>Answer</summary>It postpones method and assignment errors to runtime. Validate untyped input once at the edge, then return a concrete type so the analyzer protects the rest of the feature.</details>

**Why does `??` require a product decision rather than merely fixing a compiler error?**

<details><summary>Answer</summary>The fallback decides what absence means to a user. `Guest` may be appropriate for a name, while an absent payment amount should stop the operation and request correction.</details>

**Why can a factory cache be harmful when used by default?**

<details><summary>Answer</summary>A registry has memory, lifecycle, and identity consequences. Use it only when canonical shared identity has a clear semantic or performance purpose; ordinary immutable values are usually simpler.</details>

**Why should a stream subscription have an owner?**

<details><summary>Answer</summary>Events can continue after the consumer's screen or request ends. An owner decides cancellation, error handling, and when updates are no longer meaningful, preventing stale work and leaks.</details>
