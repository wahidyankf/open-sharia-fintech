---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 make Kotlin's concise collection and modelling idioms concrete. Each title maps to
Examples 27–54 make Kotlin's concise collection and modelling idioms concrete. Each Markdown block
is a self-contained standard-library program and follows the same run command as the beginner
examples.

## Example 27: Store a Lambda

_ex-27 · exercises co-14_

A lambda is a value, so a property can hold one and invoke it later.

```kotlin
fun main() { // => program entry point
    val square = { value: Int -> value * value } // => lambda accepts and returns Int
    println(square(3)) // => invokes the lambda and prints 9
    // => closes the current scope
}
```

**Key takeaway:** Lambdas make small behaviour values explicit.

**Why it matters:** Android callbacks and collection operations use functions as values constantly.
Giving one a descriptive name makes a reusable transformation easier to test and read.

## Example 28: Use a Trailing Lambda

_ex-28 · exercises co-14_

When a function's last argument is a lambda, Kotlin lets it sit after the parentheses.

```kotlin
fun main() { // => starts the example
    val doubled = listOf(1, 2, 3).map { it * 2 } // => trailing lambda transforms each element
    println(doubled) // => prints [2, 4, 6]
    // => closes the current scope
}
```

**Key takeaway:** Trailing lambdas keep a data pipeline readable from left to right.

**Why it matters:** This is Kotlin's most common collection style. Recognizing it immediately lets
you focus on transformation logic instead of punctuation.

## Example 29: Use Implicit `it`

_ex-29 · exercises co-14_

A single-parameter lambda may use `it` instead of declaring a name. Name the parameter when nested
lambdas would make `it` ambiguous.

```kotlin
fun main() { // => program entry point
    val positive = listOf(-1, 0, 2).filter { it > 0 } // => it is each Int in turn
    println(positive) // => prints [2]
    // => closes the current scope
}
```

**Key takeaway:** `it` is concise only while its receiver stays obvious.

**Why it matters:** Readability matters more than saving a word. Clear lambda parameters prevent
subtle errors in UI state transformations with several nested scopes.

## Example 30: Accept a Function Parameter

_ex-30 · exercises co-15_

Function types describe inputs and outputs just as normal types do.

```kotlin
fun apply(value: Int, transform: (Int) -> Int): Int { // => accepts behaviour as an argument
    return transform(value) // => delegates the calculation
    // => closes the current scope
}
fun main() { // => runs a supplied transformation
    println(apply(4) { it + 1 }) // => prints 5
    // => closes the current scope
}
```

**Key takeaway:** Higher-order functions separate a workflow from its variation.

**Why it matters:** This pattern powers reusable list operations, event handlers, and test seams.
The caller can select behaviour without the callee growing a branch for every option.

## Example 31: Pass a Function Reference

_ex-31 · exercises co-15_

`::name` turns a named function into a function value.

```kotlin
fun isEven(value: Int) = value % 2 == 0 // => named predicate
fun main() { // => entry point
    println(listOf(1, 2, 3, 4).filter(::isEven)) // => passes function without calling it first
    // => closes the current scope
}
```

**Key takeaway:** Function references reuse a named operation where a lambda is expected.

**Why it matters:** A named predicate gives the rule a home and a testable name. Use a lambda only
when the behaviour is short and truly local to the call site.

## Example 32: Return a Lambda

_ex-32 · exercises co-15_

A function can create another function while capturing configuration from its call.

```kotlin
fun multiplier(factor: Int): (Int) -> Int = { value -> value * factor } // => closure captures factor
fun main() { // => configures then uses behaviour
    println(multiplier(3)(4)) // => prints 12
    // => closes the current scope
}
```

**Key takeaway:** A returned lambda can retain values from its creation scope.

**Why it matters:** Factories for formatters, validators, and mappers often need this shape. Keep
captured mutable state small so a closure remains easy to reason about.

## Example 33: Start with a Read-only List

_ex-33 · exercises co-16_

`listOf` exposes a read-only `List` interface. It does not offer mutation methods.

```kotlin
fun main() { // => starts a standalone program
    val steps = listOf("plan", "build") // => read-only list value
    println(steps.size) // => safe read operation prints 2
    // => closes the current scope
}
```

**Key takeaway:** Read-only collection types protect a collection's shape through that reference.

**Why it matters:** Passing a `List` communicates that a function will inspect, not modify, its
input. It reduces accidental side effects at module boundaries.

## Example 34: Mutate a Mutable List

_ex-34 · exercises co-16_

A `val` prevents rebinding the variable, not changing an object that is itself mutable.

```kotlin
fun main() { // => program entry point
    val queue = mutableListOf<String>() // => binding is fixed; list is mutable
    queue.add("sync") // => mutates the list contents
    println(queue) // => prints [sync]
    // => closes the current scope
}
```

**Key takeaway:** Binding mutability and object mutability are different decisions.

**Why it matters:** This distinction prevents a common false sense of safety. Prefer immutable
collections across boundaries and keep intentional mutation local.

## Example 35: Build a Map

_ex-35 · exercises co-16_

The `to` infix function creates a key-value pair for `mapOf`.

```kotlin
fun main() { // => starts execution
    val ports = mapOf("http" to 80) // => builds a read-only key-value map
    println(ports["http"]) // => prints 80
    // => closes the current scope
}
```

**Key takeaway:** Map lookup returns a nullable value because a key may be absent.

**Why it matters:** Kotlin forces callers to decide what missing data means. That combines naturally
with safe calls and Elvis defaults from the beginner section.

## Example 36: Deduplicate with a Set

_ex-36 · exercises co-16_

A `Set` holds unique values. Adding the same logical value again does not create another entry.

```kotlin
fun main() { // => program entry point
    val roles = setOf("reader", "reader", "editor") // => duplicate reader collapses
    println(roles.size) // => prints 2
    // => closes the current scope
}
```

**Key takeaway:** Choose a set when membership and uniqueness matter more than duplicates.

**Why it matters:** Permissions, feature flags, and selected IDs usually model a set better than a
list. The data structure documents the invariant for every future caller.

## Example 37: Transform with `map`

_ex-37 · exercises co-17_

`map` returns a new list by applying a lambda to every input value.

```kotlin
fun main() { // => starts the program
    val labels = listOf("a", "b").map { it.uppercase() } // => creates transformed values
    println(labels) // => prints [A, B]
    // => closes the current scope
}
```

**Key takeaway:** `map` changes values without mutating the original collection.

**Why it matters:** Immutable transformations are a reliable way to prepare render models and API
data. They make the input/output relationship visible in one expression.

## Example 38: Select with `filter`

_ex-38 · exercises co-17_

`filter` retains only values whose predicate is true.

```kotlin
fun main() { // => entry point
    val active = listOf(true, false, true).filter { it } // => keeps only true values
    println(active.size) // => prints 2
    // => closes the current scope
}
```

**Key takeaway:** A filter expresses selection without manually managing an output list.

**Why it matters:** Filtering state before display is common in mobile interfaces. Keeping the
predicate close to the collection prevents loops from mixing traversal with several unrelated jobs.

## Example 39: Accumulate with `fold`

_ex-39 · exercises co-17_

`fold` starts from an explicit accumulator and updates it for every element.

```kotlin
fun main() { // => starts execution
    val total = listOf(2, 3, 4).fold(0) { sum, value -> sum + value } // => sums all values
    println(total) // => prints 9
    // => closes the current scope
}
```

**Key takeaway:** `fold` makes the initial value and accumulation rule explicit.

**Why it matters:** It handles totals, grouped state, and composite values without hidden mutation.
Pick an initial accumulator that correctly represents an empty input.

## Example 40: Visit with `forEach`

_ex-40 · exercises co-17_

`forEach` performs an effect for every item and returns `Unit`.

```kotlin
fun main() { // => program entry point
    listOf("one", "two").forEach { println(it) } // => prints each item in order
    // => closes the current scope
}
```

**Key takeaway:** Use `forEach` for effects, not for producing another collection.

**Why it matters:** Naming the intended operation helps readers distinguish rendering or logging
from a pure data transformation such as `map`.

## Example 41: Chain Collection Operations

_ex-41 · exercises co-17_

Pipelines can filter before mapping, retaining a single readable data flow.

```kotlin
fun main() { // => starts the pipeline
    val result = listOf(-1, 2, 3).filter { it > 0 }.map { it * 10 } // => selects then transforms
    println(result) // => prints [20, 30]
    // => closes the current scope
}
```

**Key takeaway:** Order pipeline stages by the data decision they make.

**Why it matters:** Filtering early avoids transforming values that will be discarded. A short chain
often reads better than a loop with flags and temporary mutable collections.

## Example 42: Add an Extension Function

_ex-42 · exercises co-18_

An extension gives a receiver type an additional call syntax without inheriting from it.

```kotlin
fun String.shout() = uppercase() + "!" // => extension receiver is String
fun main() { // => program entry point
    println("ready".shout()) // => calls extension like a member
    // => closes the current scope
}
```

**Key takeaway:** Extensions improve local vocabulary without modifying the original class.

**Why it matters:** Formatting helpers stay near their domain and preserve a natural call site.
They do not gain private access, so do not mistake them for actual member functions.

## Example 43: Add an Extension Property

_ex-43 · exercises co-18_

An extension property computes from public receiver state; it cannot store backing state.

```kotlin
val String.firstChar: Char get() = first() // => computed property on String
fun main() { // => starts execution
    println("Kotlin".firstChar) // => prints K
    // => closes the current scope
}
```

**Key takeaway:** Extension properties are concise computed views.

**Why it matters:** They help name repeated derived values. Use a function instead when computing
the value is expensive or the property syntax would conceal meaningful work.

## Example 44: Put Properties in a Primary Constructor

_ex-44 · exercises co-19_

`val` properties in a class header are constructed and exposed in one place.

```kotlin
class Point(val x: Int, val y: Int) // => primary constructor declares two properties
fun main() { // => program entry point
    println(Point(2, 5).x) // => reads the constructed x value
    // => closes the current scope
}
```

**Key takeaway:** Constructor properties make simple models compact and explicit.

**Why it matters:** UI and domain models carry data more often than behaviour. A short constructor
reveals their stable state without boilerplate getters.

## Example 45: Validate in `init`

_ex-45 · exercises co-19_

An `init` block runs as the instance is created and can enforce an invariant.

```kotlin
class Percentage(val value: Int) { // => constructor receives the raw value
    init { require(value in 0..100) } // => rejects invalid instances immediately
    // => closes the current scope
}
fun main() { // => constructs a valid value
    println(Percentage(80).value) // => prints 80
    // => closes the current scope
}
```

**Key takeaway:** `init` protects an object before callers can observe it.

**Why it matters:** Keeping invalid state out of the model simplifies every consumer. The constructor
becomes the single place responsible for guarding its representation.

## Example 46: Add a Class Method

_ex-46 · exercises co-19_

Instance methods can use constructor properties directly.

```kotlin
class Greeting(private val name: String) { // => instance stores its input
    fun message() = "Hello, $name" // => method derives output from instance state
    // => closes the current scope
}
fun main() { // => calls the instance method
    println(Greeting("Ada").message()) // => prints Hello, Ada
    // => closes the current scope
}
```

**Key takeaway:** An instance method belongs where it uses that instance's state.

**Why it matters:** Cohesive classes keep data and the small operations that preserve its meaning
together. Avoid turning every helper into a method when it does not need object state.

## Example 47: Declare a Data Class

_ex-47 · exercises co-20_

`data class` signals a value-like model and generates useful diagnostics and equality.

```kotlin
data class User(val name: String) // => Kotlin generates value operations
fun main() { // => program entry point
    println(User("Ada")) // => generated toString prints User(name=Ada)
    // => closes the current scope
}
```

**Key takeaway:** Data classes make ordinary records honest and concise.

**Why it matters:** API and screen state models should compare by their contained data. Generated
operations remove repetitive boilerplate while preserving clear intent.

## Example 48: Copy a Data Value

_ex-48 · exercises co-20_

`copy` creates another instance with selected constructor properties changed.

```kotlin
data class User(val name: String, val active: Boolean) // => immutable value model
fun main() { // => creates a changed value without mutation
    println(User("Ada", false).copy(active = true)) // => prints active=true copy
    // => closes the current scope
}
```

**Key takeaway:** Copying models a state transition as a new value.

**Why it matters:** Immutable screen state is easier to observe and test. A `copy` call identifies
exactly what changed while retaining the rest of the value unchanged.

## Example 49: Destructure a Data Class

_ex-49 · exercises co-20_

Data classes provide `componentN` functions that support destructuring.

```kotlin
data class User(val name: String, val age: Int) // => two constructor components
fun main() { // => destructures the value
    val (name, age) = User("Ada", 36) // => assigns component1 and component2
    println("$name:$age") // => prints Ada:36
    // => closes the current scope
}
```

**Key takeaway:** Destructure only when both extracted names improve the code.

**Why it matters:** Destructuring can clarify small transformations, but accessing a descriptive
property is often clearer when only one field is needed.

## Example 50: Compare Data by Value

_ex-50 · exercises co-20_

Two data-class instances with the same constructor values compare equal with `==`.

```kotlin
data class User(val name: String) // => equality uses name
fun main() { // => compares independent instances
    println(User("Ada") == User("Ada")) // => prints true
    // => closes the current scope
}
```

**Key takeaway:** Data-class equality reflects contents, not allocation identity.

**Why it matters:** Collection membership and UI state comparisons usually care about the data a
model represents. This default matches that expectation.

## Example 51: Implement an Interface

_ex-51 · exercises co-21_

An interface states required behaviour; a class supplies it with `override`.

```kotlin
interface Formatter { fun format(value: Int): String } // => behaviour contract
class HexFormatter : Formatter { override fun format(value: Int) = value.toString(16) } // => implementation
fun main() { // => uses the implementation through the interface shape
    println(HexFormatter().format(15)) // => prints f
    // => closes the current scope
}
```

**Key takeaway:** Interfaces separate a caller's need from one implementation.

**Why it matters:** A platform service can change without forcing its consumers to depend on its
construction details. Interfaces also create small, focused test doubles.

## Example 52: Supply an Interface Default

_ex-52 · exercises co-21_

Interfaces can provide default method bodies that implementations inherit.

```kotlin
interface Named { fun label() = "unnamed" } // => default behaviour is part of the contract
class Draft : Named // => inherits label without an override
fun main() { // => runs the inherited method
    println(Draft().label()) // => prints unnamed
    // => closes the current scope
}
```

**Key takeaway:** Defaults express a safe shared behaviour, not a hidden state store.

**Why it matters:** A default can make simple implementations smaller while leaving special cases
free to override. Keep it unsurprising because every implementer receives it.

## Example 53: Create an Object Singleton

_ex-53 · exercises co-22_

An `object` declaration creates one lazily initialised singleton instance.

```kotlin
object Counter { // => one shared object declaration
    var value = 0 // => singleton-owned mutable state
    // => closes the current scope
}
fun main() { // => accesses the sole instance
    Counter.value += 1 // => updates its one shared value
    println(Counter.value) // => prints 1
    // => closes the current scope
}
```

**Key takeaway:** `object` gives deliberately shared behaviour a visible owner.

**Why it matters:** Shared state needs restraint even when initialization is safe. Prefer passing
dependencies, and reserve objects for stable utilities or truly global coordination.

## Example 54: Add a Companion Factory

_ex-54 · exercises co-22_

A companion object holds class-level members callable through the class name.

```kotlin
class Email private constructor(val value: String) { // => constructor remains controlled
    companion object { fun from(value: String) = Email(value.trim()) } // => factory normalises input
    // => closes the current scope
}
fun main() { // => calls factory through class name
    println(Email.from(" a@example.test ").value) // => prints trimmed value
    // => closes the current scope
}
```

**Key takeaway:** A companion factory gives construction a meaningful name and policy.

**Why it matters:** Factories can validate, normalize, or select an implementation without leaking
those choices across call sites. They are clearer than overloaded constructors when intent differs.
