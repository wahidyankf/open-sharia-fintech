---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 finish the language slice Android work commonly needs. Examples 63–68 introduce
coroutines; the shared runner under `learning/coroutines/code/` contains matching source files,
supplies `kotlinx.coroutines` for the library-dependent examples, and documents `gradle run`.

## Example 55: Match a Value with `when`

_ex-55 · exercises co-23_

`when` selects a branch from a subject and can return a value.

```kotlin
fun main() { // => starts the example
    val label = when (2) { 1 -> "one"; else -> "other" } // => matches the else branch
    println(label) // => prints other
    // => closes the current scope
}
```

**Key takeaway:** `when` makes a multi-branch choice a first-class expression.

**Why it matters:** State labels and event handling are clearer when each alternative sits on its
own branch instead of being hidden in deeply nested conditionals.

## Example 56: Use a Condition-only `when`

_ex-56 · exercises co-23_

Omit the subject when each branch is a Boolean condition.

```kotlin
fun main() { // => program entry point
    val temperature = 28 // => value assessed by branch conditions
    val band = when { temperature > 30 -> "hot"; temperature > 20 -> "warm"; else -> "cool" } // => first match wins
    println(band) // => prints warm
    // => closes the current scope
}
```

**Key takeaway:** Condition-only `when` is an ordered, value-producing decision table.

**Why it matters:** It reads well when the conditions are related thresholds. Put more specific
conditions first so a broad earlier branch does not shadow a later one.

## Example 57: Assign a `when` Result

_ex-57 · exercises co-23_

The result of a `when` can initialize an immutable variable.

```kotlin
fun main() { // => entry point
    val status = when (true) { true -> "enabled"; false -> "disabled" } // => both Boolean cases covered
    println(status) // => prints enabled
    // => closes the current scope
}
```

**Key takeaway:** Expression branches can replace a mutable variable plus later assignments.

**Why it matters:** A single initialization makes it obvious that the chosen value is complete once
the decision ends. This is a useful shape for mapping domain state to display state.

## Example 58: Combine Cases

_ex-58 · exercises co-23_

Several matching values may share one branch.

```kotlin
fun main() { // => begins execution
    val weekend = when ("Sat") { "Sat", "Sun" -> true; else -> false } // => two labels share a result
    println(weekend) // => prints true
    // => closes the current scope
}
```

**Key takeaway:** Group equivalent inputs rather than duplicating an identical branch.

**Why it matters:** Grouping captures the business rule directly. It also reduces the chance that
two copied branches drift when their common behaviour changes.

## Example 59: Chain `if` Expressions

_ex-59 · exercises co-24_

`if`/`else if`/`else` can produce one complete value.

```kotlin
fun grade(score: Int) = if (score >= 80) "A" else if (score >= 60) "B" else "C" // => every score gets a label
fun main() { // => runs the classifier
    println(grade(70)) // => prints B
    // => closes the current scope
}
```

**Key takeaway:** Include the final `else` when an `if` contributes a value.

**Why it matters:** Total mappings avoid an uninitialized variable or a forgotten state. Choose
`when` instead when a named domain hierarchy communicates the alternatives better.

## Example 60: Model a Sealed Result

_ex-60 · exercises co-25_

A sealed class declares a closed set of direct subclasses.

```kotlin
sealed class LoadResult { // => all direct states live in this source set
    data class Data(val value: String) : LoadResult() // => successful state carries data
    data class Failed(val message: String) : LoadResult() // => failure carries context
    // => closes the current scope
}
fun main() { // => constructs a known state
    println(LoadResult.Data("ready")) // => prints generated data-class form
    // => closes the current scope
}
```

**Key takeaway:** A sealed hierarchy represents a finite domain state space.

**Why it matters:** UI state is often not simply nullable: it can load, succeed, or fail. Named
states prevent a scattered mix of booleans and optional values from contradicting each other.

## Example 61: Match a Sealed Hierarchy Exhaustively

_ex-61 · exercises co-25_

The compiler knows every direct sealed subclass, so an expression `when` can omit `else`.

```kotlin
sealed class Result { data class Ok(val value: Int) : Result(); data object Empty : Result() } // => closed states
fun label(result: Result) = when (result) { is Result.Ok -> "value ${result.value}"; Result.Empty -> "empty" } // => exhaustive
fun main() { // => runs the mapper
    println(label(Result.Empty)) // => prints empty
    // => closes the current scope
}
```

**Key takeaway:** Exhaustive matching turns a new state into a compiler-guided change.

**Why it matters:** When someone adds a state, every display or behaviour mapping must decide what
it means. The compiler points to the missing decisions instead of letting an `else` hide them.

## Example 62: Notice a Missing Sealed Case

_ex-62 · exercises co-25_

An expression `when` over a sealed type will not compile if a case is missing. Keep this broken
line commented so the example remains runnable.

```kotlin
sealed class Signal { data object On : Signal(); data object Off : Signal() } // => two possible states
// fun broken(value: Signal) = when (value) { Signal.On -> "on" } // => compiler requires Signal.Off
fun main() { // => successful complete version
    val signal: Signal = Signal.Off // => keeps the expression typed as the sealed parent
    val complete = when (signal) { Signal.On -> "on"; Signal.Off -> "off" } // => all cases covered
    println(complete) // => prints off
    // => closes the current scope
}
```

**Key takeaway:** Missing-state errors are a useful safety net, not boilerplate.

**Why it matters:** A deliberate closed model supports reliable refactoring. Do not defeat it with
an uninformative `else` unless the domain genuinely has an intentional catch-all policy.

## Example 63: Declare a Suspending Function

_ex-63 · exercises co-26_

`suspend` marks a function that may pause without blocking its thread. It can be called only from
another suspending function or a coroutine builder.

```kotlin
suspend fun greeting() = "hello" // => function may participate in suspension
suspend fun main() { // => Kotlin supports a suspending entry point
    println(greeting()) // => valid call from suspend context
    // => closes the current scope
}
```

**Key takeaway:** `suspend` changes the calling contract, not the return type.

**Why it matters:** A suspending API makes waiting visible to callers. It prevents blocking work
from masquerading as an ordinary immediate calculation.

## Example 64: Launch Child Work

_ex-64 · exercises co-26_

`coroutineScope` creates a structured parent scope and `launch` starts a child coroutine.

```kotlin
import kotlinx.coroutines.coroutineScope // => structured scope builder
import kotlinx.coroutines.launch // => child coroutine builder
suspend fun main() = coroutineScope { // => parent waits for children before returning
    launch { println("child") } // => starts concurrent child work
    println("parent") // => parent continues without waiting here
    // => closes the current scope
}
```

**Key takeaway:** Child work belongs to a parent scope with a known lifetime.

**Why it matters:** Structured concurrency prevents detached work from outliving the screen or task
that started it. Android scopes provide this same ownership idea at platform level.

## Example 65: Bridge with `runBlocking`

_ex-65 · exercises co-26_

`runBlocking` blocks the current thread until its coroutine completes. Use it only at a bridge such
as a simple CLI entry point or a test, not inside normal application paths.

```kotlin
import kotlinx.coroutines.runBlocking // => bridge from blocking main to suspend code
suspend fun fetch() = "done" // => suspending work contract
fun main() = runBlocking { // => waits before process exit
    println(fetch()) // => prints done
    // => closes the current scope
}
```

**Key takeaway:** `runBlocking` is a boundary tool, not a replacement for structured scopes.

**Why it matters:** Blocking a UI thread makes an app unresponsive. Keeping this bridge at an edge
preserves the non-blocking design promised by suspending APIs.

## Example 66: Suspend with `delay`

_ex-66 · exercises co-26_

`delay` pauses the coroutine while freeing its thread for other work.

```kotlin
import kotlinx.coroutines.delay // => non-blocking suspension primitive
suspend fun main() { // => suspend context allows delay
    delay(1) // => pauses coroutine for a short duration
    println("resumed") // => runs after the delay
    // => closes the current scope
}
```

**Key takeaway:** Suspending differs from sleeping a thread.

**Why it matters:** UI and network tasks need responsiveness while waiting. Coroutine suspension
allows the runtime to use the thread for other eligible work.

## Example 67: Return a Coroutine Value

_ex-67 · exercises co-26_

A suspending function can still return a normal value after its work completes.

```kotlin
suspend fun twice(value: Int): Int { // => suspending function retains normal return typing
    return value * 2 // => returns a calculated Int
    // => closes the current scope
}
suspend fun main() { // => caller is also suspending
    println(twice(6)) // => prints 12
    // => closes the current scope
}
```

**Key takeaway:** `suspend` describes execution capability, not a special result wrapper.

**Why it matters:** Consumers can use the resulting value naturally after the suspension point.
The call site still documents that it must run in a properly owned coroutine.

## Example 68: Wait for Structured Children

_ex-68 · exercises co-26_

Leaving `coroutineScope` waits for all its children, even when their output order is not guaranteed.

```kotlin
import kotlinx.coroutines.coroutineScope // => structured parent scope
import kotlinx.coroutines.launch // => starts child jobs
suspend fun main() { // => returns Unit after both children finish
    coroutineScope {
        launch { println("first child") } // => child belongs to this scope
        launch { println("second child") } // => another sibling child
    } // => implicit join happens here
}
```

**Key takeaway:** Parent completion includes child completion in a structured scope.

**Why it matters:** This lifetime rule makes cancellation and error propagation predictable. It is
the foundation to understand before learning Android lifecycle coroutine scopes.

## Example 69: Drop Nulls While Mapping

_ex-69 · exercises co-06, co-17_

`mapNotNull` both transforms and removes absent results.

```kotlin
fun main() { // => starts the transformation
    val numbers = listOf("2", "x", "4").mapNotNull { it.toIntOrNull() } // => invalid input becomes null then drops
    println(numbers) // => prints [2, 4]
    // => closes the current scope
}
```

**Key takeaway:** Convert uncertain input once and keep only successful values.

**Why it matters:** Parsing user and network data should not turn one invalid value into a crash.
This pipeline makes the omission rule explicit and testable.

## Example 70: Use Data Equality in a Collection

_ex-70 · exercises co-16, co-20_

Collection membership uses the data class's generated equality.

```kotlin
data class User(val id: Int) // => equality compares id
fun main() { // => checks logical membership
    println(listOf(User(1)).contains(User(1))) // => prints true
    // => closes the current scope
}
```

**Key takeaway:** Value models compose naturally with collection operations.

**Why it matters:** Screen state often needs to check selection or remove an item represented by a
freshly constructed model. Structural equality makes that intent work as expected.

## Example 71: Project Data with a Lambda

_ex-71 · exercises co-14, co-20_

Lambdas make a data-class property projection concise.

```kotlin
data class User(val name: String) // => model has a readable name property
fun main() { // => projects users into labels
    println(listOf(User("Ada"), User("Lin")).map { it.name }) // => prints [Ada, Lin]
    // => closes the current scope
}
```

**Key takeaway:** A pipeline can expose only the fields the next stage needs.

**Why it matters:** Mapping domain models to UI labels prevents presentation code from carrying
unneeded data. Keep the transformation close to the boundary that needs it.

## Example 72: Dispatch through an Interface

_ex-72 · exercises co-21_

One collection can hold several implementations of the same behaviour.

```kotlin
interface Shape { fun area(): Int } // => common behaviour contract
class Square(private val side: Int) : Shape { override fun area() = side * side } // => one implementation
class Rectangle(private val width: Int, private val height: Int) : Shape { override fun area() = width * height } // => another
fun main() { // => uses polymorphism
    val shapes: List<Shape> = listOf(Square(2), Rectangle(2, 3)) // => one interface-typed collection
    println(shapes.map { it.area() }) // => dispatches dynamically and prints [4, 6]
    // => closes the current scope
}
```

**Key takeaway:** Callers can rely on an interface instead of branching on concrete classes.

**Why it matters:** UI renderers and services become easier to extend when a new implementation
does not require editing every existing consumer. Keep interfaces small and purpose-specific.

## Example 73: Extend a Nullable Receiver

_ex-73 · exercises co-06, co-18_

Extensions can target a nullable receiver and decide how `null` should display.

```kotlin
fun String?.orGuest() = this ?: "guest" // => extension handles nullable receiver explicitly
fun main() { // => invokes the nullable extension
    val name: String? = null // => absent optional input
    println(name.orGuest()) // => prints guest
    // => closes the current scope
}
```

**Key takeaway:** Nullable extensions centralize a repeated null policy.

**Why it matters:** A named helper can make presentation defaults consistent. Use it only when the
fallback is genuinely shared rather than hiding a domain-specific decision.

## Example 74: Render a Sealed Result

_ex-74 · exercises co-23, co-25_

`when` maps each sealed result to a display value without an `else` escape hatch.

```kotlin
sealed class Api { data class Success(val value: String) : Api(); data class Error(val message: String) : Api() } // => closed results
fun render(result: Api) = when (result) { is Api.Success -> result.value; is Api.Error -> "Error: ${result.message}" } // => exhaustive mapping
fun main() { // => renders one result
    println(render(Api.Success("loaded"))) // => prints loaded
    // => closes the current scope
}
```

**Key takeaway:** A sealed result and exhaustive `when` produce total rendering logic.

**Why it matters:** Loading code should not discard failure detail or accidentally show stale data.
Each state gets a deliberate, reviewable outcome.

## Example 75: Pass a Lambda to a Higher-order Function

_ex-75 · exercises co-14, co-15_

The caller can choose a transformation at a generic call site.

```kotlin
fun transform(value: String, operation: (String) -> String) = operation(value) // => delegates the rule
fun main() { // => supplies local behaviour
    println(transform("kotlin") { it.uppercase() }) // => prints KOTLIN
    // => closes the current scope
}
```

**Key takeaway:** Higher-order APIs become specific through a supplied lambda.

**Why it matters:** This supports reusable utilities without hard-coding one product rule. Keep the
lambda's responsibility narrow so errors and side effects remain clear.

## Example 76: Filter, Map, and Sum

_ex-76 · exercises co-17_

Several small collection operations compose into one immutable calculation.

```kotlin
fun main() { // => runs a complete pipeline
    val total = listOf(-2, 1, 3).filter { it > 0 }.map { it * 10 }.sum() // => 10 + 30
    println(total) // => prints 40
    // => closes the current scope
}
```

**Key takeaway:** A pipeline makes each transformation stage inspectable.

**Why it matters:** This form is ideal for transparent calculations. If a chain grows long or
reuses intermediate meaning, give a stage a name instead of forcing readers to parse everything at once.

## Example 77: Compile Multiple Kotlin Files

_ex-77 · exercises co-01, co-19_

Kotlin classes and `main` can live in separate source files within one compilation.

```kotlin
class Greeting(val name: String) // => place this class in Greeting.kt when splitting files
fun main() { // => place this entry function in Main.kt in a multi-file project
    println(Greeting("Ada").name) // => compiles with both source files and prints Ada
    // => closes the current scope
}
```

**Key takeaway:** Split files by coherent responsibility, then compile them together.

**Why it matters:** Android projects contain many Kotlin files, but the language rule stays simple:
imports and packages organize code; Gradle compiles the selected source set as a unit.

## Example 78: Preview the Capstone Shape

_ex-78 · exercises co-06, co-14, co-20, co-21, co-26_

The capstone deliberately combines the primer's highest-value pieces without adding Android APIs.

```kotlin
data class Item(val sku: String) // => immutable model
interface Catalog { suspend fun find(sku: String): Item? } // => nullable async lookup contract
suspend fun main() { // => structured suspending entry point
    val labels = listOf("a").map { it.uppercase() } // => collection lambda preview
    println(labels) // => prints [A]
    // => closes the current scope
}
```

**Key takeaway:** Kotlin features remain small when each one has a precise job.

**Why it matters:** The [capstone](./capstone/overview.md) proves these pieces work together. That is the right
handoff point to Android, where lifecycle and UI concerns add their own complexity.
