---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to the learning track. Answer before opening each disclosure:
recognition is not the same as being able to choose a Kotlin construct under pressure.

## Recall Q&A

**Q1 (co-01).** What is the top-level Kotlin entry function and what CLI command compiles it into a runnable JAR?

<details><summary>Answer</summary>`fun main()` is the entry point. Run `kotlinc Example.kt -include-runtime -d example.jar`, then `java -jar example.jar`.</details>

**Q2 (co-02).** When do you use `val` instead of `var`?

<details><summary>Answer</summary>Use `val` by default: its binding cannot be reassigned. Use `var` only when the binding must change.</details>

**Q3 (co-03).** Does `val count = 3` make Kotlin dynamically typed?

<details><summary>Answer</summary>No. The compiler infers a static `Int` type from the initializer.</details>

**Q4 (co-04).** How do you combine an `Int` with a `Double` intentionally?

<details><summary>Answer</summary>Convert explicitly, for example `count.toDouble() / 2`; Kotlin does not silently widen the `Int`.</details>

**Q5 (co-05).** When do you use `$name` versus `${expression}` in a template?

<details><summary>Answer</summary>Use `$name` for one simple identifier and `${expression}` for a property access or calculation.</details>

**Q6 (co-06).** What does `String?` say that `String` does not?

<details><summary>Answer</summary>`String?` may hold `null`; plain `String` cannot.</details>

**Q7 (co-07).** What does `profile?.city` produce when `profile` is null?

<details><summary>Answer</summary>It produces `null` and does not invoke `city` access.</details>

**Q8 (co-08).** What does `value ?: fallback` return?

<details><summary>Answer</summary>It returns `value` when non-null; otherwise it evaluates and returns `fallback`.</details>

**Q9 (co-09).** Why should `!!` be rare?

<details><summary>Answer</summary>It asserts non-null at runtime and throws an NPE when the assertion is wrong, moving a compiler-guided decision into a crash.</details>

**Q10 (co-10).** What guarantee exists inside `name?.let { ... }`?

<details><summary>Answer</summary>The lambda runs only when `name` is non-null, so its parameter is a non-null `String`.</details>

**Q11 (co-11).** What return type may be omitted for an effect-only function?

<details><summary>Answer</summary>`Unit`; Kotlin infers it when no useful value is returned.</details>

**Q12 (co-12).** What two call-site benefits do default and named arguments provide?

<details><summary>Answer</summary>Defaults let callers omit ordinary options; named arguments document literals and permit choosing argument order.</details>

**Q13 (co-13).** Rewrite `fun double(x: Int): Int { return x * 2 }` as a single-expression function.

<details><summary>Answer</summary>`fun double(x: Int) = x * 2`.</details>

**Q14 (co-14).** When is `it` acceptable in a lambda?

<details><summary>Answer</summary>When the lambda has one parameter and its meaning is obvious; name it when nesting or domain meaning would make `it` unclear.</details>

**Q15 (co-15).** What is the type of a function that accepts an `Int` and returns a `String`?

<details><summary>Answer</summary>`(Int) -> String`.</details>

**Q16 (co-16).** Can a `val` holding a `MutableList` still add elements?

<details><summary>Answer</summary>Yes. `val` fixes the binding; the mutable list's contents can still change.</details>

**Q17 (co-17).** Which operation transforms every item, and which retains selected items?

<details><summary>Answer</summary>`map` transforms; `filter` retains values whose predicate is true.</details>

**Q18 (co-18).** What can an extension function not do?

<details><summary>Answer</summary>It cannot access the receiver's private state or truly modify the receiver's member table; it only adds a call syntax resolved statically.</details>

**Q19 (co-19).** When does an `init` block run?

<details><summary>Answer</summary>During construction, after primary-constructor properties are initialized and before callers receive the object.</details>

**Q20 (co-20).** Name two operations a data class generates.

<details><summary>Answer</summary>Any two of structural `equals`/`hashCode`, `toString`, `copy`, or `componentN` destructuring functions.</details>

**Q21 (co-21).** Why type a parameter as an interface?

<details><summary>Answer</summary>The caller depends on required behaviour rather than construction details, enabling multiple implementations and focused test doubles.</details>

**Q22 (co-22).** What is the difference between `object` and `companion object`?

<details><summary>Answer</summary>An `object` is a singleton value; a companion object is a singleton associated with a class for class-level members such as factories.</details>

**Q23 (co-23).** When must a `when` expression be exhaustive?

<details><summary>Answer</summary>When it produces a value; a sealed hierarchy lets the compiler determine the complete set of cases.</details>

**Q24 (co-24).** Why does an expression `if` need `else`?

<details><summary>Answer</summary>Both outcomes must provide the value assigned or returned by the expression.</details>

**Q25 (co-25).** What is the payoff of a sealed result model?

<details><summary>Answer</summary>A new state causes compiler-guided updates to exhaustive `when` expressions instead of being silently swallowed by an `else`.</details>

**Q26 (co-26).** What is structured concurrency in one sentence?

<details><summary>Answer</summary>Coroutines form a parent-child lifetime tree: a parent scope waits for, cancels, and observes its children together.</details>

## Applied Problems

**AP1.** A map lookup may not contain an account ID and the caller should simply skip it. Which idiom avoids nesting the rest of the function?

<details><summary>Answer</summary>`val account = accounts[id] ?: return` unwraps the value or exits the current function.</details>

**AP2.** A model needs mutually exclusive `Loading`, `Content`, and `Failure` states. Should it be three booleans, nullable content plus an error, or a sealed hierarchy?

<details><summary>Answer</summary>A sealed hierarchy. It makes invalid combinations unrepresentable and enables exhaustive rendering.</details>

**AP3.** A list of text inputs should produce only valid integer IDs. Which collection operation fits?

<details><summary>Answer</summary>`mapNotNull { it.toIntOrNull() }` converts each input and drops failed parses explicitly.</details>

**AP4.** A CLI test needs to call a suspending repository function. Is `runBlocking` appropriate inside an Android click handler?

<details><summary>Answer</summary>It is reasonable as a CLI/test bridge, but not in a UI handler because it blocks the current thread. Use an owned coroutine scope in application code.</details>

**AP5.** Two arguments are both strings, `title` and `message`. How can a call prevent swapping them?

<details><summary>Answer</summary>Use named arguments, for example `show(title = "Saved", message = "Changes stored")`.</details>

## Deliberate Practice

1. Write `fun displayName(name: String?): String` using `?:` with a `guest` fallback. Then change it
   to return early from a function that prints only present names.
2. Model a `Download` sealed hierarchy with `Queued`, `Running(percent)`, and `Failed(reason)`.
   Write an exhaustive `when` that produces one label per state.
3. Given `listOf("1", "oops", "3")`, produce `[2, 6]` without a mutable accumulator.
4. Define `interface Clock { suspend fun now(): String }`, then create a fake implementation for a
   small `suspend fun` that renders its result.
5. Convert a class with `name` and `selected` into a data class, then use `copy(selected = true)`
   to represent the transition without mutating the old value.

## Automaticity Checklist

- [ ] I choose `val` before `var` and can explain the difference from mutable objects.
- [ ] I can traverse optional data with `?.` and decide where a fallback belongs.
- [ ] I can replace unsafe `!!` with a safe call, Elvis guard, or explicit validation.
- [ ] I can read `map`, `filter`, `fold`, and trailing lambdas without translating them into loops.
- [ ] I can model finite UI or network state with a sealed hierarchy and exhaustive `when`.
- [ ] I can explain why `runBlocking` belongs at a boundary and why coroutine children need an owner.

## Explain Why

**Why is `val items = mutableListOf<String>()` not an immutable collection?**

<details><summary>Answer</summary>`val` prohibits assigning a different list to `items`; it does not remove mutation methods from the `MutableList` object already referenced.</details>

**Why is `null` not an adequate replacement for every loading or failure state?**

<details><summary>Answer</summary>`null` loses meaning: it cannot distinguish not-yet-loaded, absent-by-design, and failed-with-context. A sealed state preserves the difference.</details>

**Why prefer a structured coroutine scope over a detached `launch`?**

<details><summary>Answer</summary>Ownership supplies a lifetime for cancellation, completion, and error propagation. Detached work can outlive the request or screen that made it meaningful.</details>

**Why are extension functions not a substitute for changing a class's design?**

<details><summary>Answer</summary>They cannot access private representation and are resolved statically. Use them for local vocabulary, not to hide an incoherent type boundary.</details>
