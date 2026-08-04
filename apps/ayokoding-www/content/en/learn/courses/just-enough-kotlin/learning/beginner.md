---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish Kotlin's ordinary syntax and its most important safety feature: nullability.
Every Markdown snippet is self-contained. Save a standard-library block as `Example.kt` and use the
compile-and-run command from Example 1.

## Example 1: Compile a Kotlin Program

_ex-01 · exercises co-01_

`fun main()` is a normal top-level function and the default program entry point. Compile this file
with `kotlinc Example.kt -include-runtime -d example.jar`, then run `java -jar example.jar`.

```kotlin
fun main() { // => Kotlin starts execution here
    println("Hello, Kotlin") // => prints one line and a newline
    // => closes the current scope
}
```

**Key takeaway:** A Kotlin source file needs no enclosing class to run.

**Why it matters:** Android projects have more structure, but their business logic is still Kotlin.
Starting with a two-line program separates the language from Android tooling and makes compiler
errors easier to understand when you later move into a Gradle project.

## Example 2: Print Values

_ex-02 · exercises co-01_

`println` accepts any value and appends a line break. Use it while learning to make state visible.

```kotlin
fun main() { // => program entry point
    println(2 + 3) // => prints the evaluated integer: 5
    // => closes the current scope
}
```

**Key takeaway:** Print an expression directly when checking what it evaluates to.

**Why it matters:** A small observable result makes examples testable without a framework. Later,
the same habit becomes targeted logging or a unit-test assertion rather than guessing about state.

## Example 3: Run a Gradle Application

_ex-03 · exercises co-01_

In a Kotlin/JVM application project, Gradle owns compilation and launching. The program itself is
still an ordinary `main` function.

```kotlin
fun main() { // => Gradle discovers this entry point
    println("run with gradle run") // => confirms the configured application ran
    // => closes the current scope
}
```

**Key takeaway:** Gradle automates the same compile-and-run loop used in Example 1.

**Why it matters:** Android uses Gradle heavily. Knowing that Gradle orchestrates Kotlin rather than
replacing it keeps build configuration from obscuring the language you are trying to learn.

## Example 4: Prefer `val`

_ex-04 · exercises co-02_

A `val` binds one value and cannot be reassigned. Uncommenting the second assignment produces a
compiler error, which is useful protection rather than a limitation.

```kotlin
fun main() { // => begins a self-contained program
    val course = "Kotlin" // => read-only binding after initialisation
    println(course) // => safely reads the original value
    // course = "Android" // => does not compile: val cannot be reassigned
    // => closes the current scope
}
```

**Key takeaway:** Choose `val` unless changing the binding is part of the design.

**Why it matters:** Immutable bindings reduce accidental state changes. Android UI code becomes
easier to reason about when a name cannot silently start referring to a different object halfway
through a function.

## Example 5: Use `var` for Deliberate Change

_ex-05 · exercises co-02_

`var` permits reassignment when the value genuinely changes. It does not make the underlying object
automatically thread-safe or immutable.

```kotlin
fun main() { // => program entry point
    var attempts = 0 // => mutable binding starts at zero
    attempts += 1 // => reassignment is permitted for var
    println(attempts) // => prints 1
    // => closes the current scope
}
```

**Key takeaway:** `var` communicates an intended state transition.

**Why it matters:** Mutable state is sometimes necessary, such as a local accumulator. Declaring it
explicitly makes review easier because readers can search for the few places where state can change.

## Example 6: Let Kotlin Infer a Type

_ex-06 · exercises co-03_

Kotlin infers `Int` from the integer literal. The inferred type remains static; inference is not
dynamic typing.

```kotlin
fun main() { // => starts the program
    val retries = 3 // => compiler infers Int from the literal
    println(retries + 1) // => Int arithmetic produces 4
    // => closes the current scope
}
```

**Key takeaway:** Inference removes repetition when the initial value is clear.

**Why it matters:** Kotlin code stays compact without hiding types from the compiler. Add an explicit
type when it clarifies an API boundary or prevents an unintended inference.

## Example 7: Write an Explicit Type

_ex-07 · exercises co-03_

An explicit annotation appears after the name. It documents the intended contract even if the
initializer later changes.

```kotlin
fun main() { // => starts a standalone program
    val label: String = "ready" // => explicit String contract
    println(label) // => prints ready
    // => closes the current scope
}
```

**Key takeaway:** `name: Type` is Kotlin's type-annotation form.

**Why it matters:** Public properties and function signatures benefit from visible types because
they tell callers what is guaranteed. Local obvious values usually benefit more from inference.

## Example 8: Convert Numbers Explicitly

_ex-08 · exercises co-04_

Kotlin does not silently widen an `Int` to a `Double`. Call a conversion method where the precision
change is intentional.

```kotlin
fun main() { // => program entry point
    val count = 3 // => inferred Int
    val average = count.toDouble() / 2 // => explicit conversion permits Double division
    println(average) // => prints 1.5
    // => closes the current scope
}
```

**Key takeaway:** Numeric conversions are visible at the point they happen.

**Why it matters:** Silent conversion can conceal rounding and overflow decisions. Explicit calls
make numeric intent reviewable in pricing, measurements, and Android layout calculations.

## Example 9: Boolean and Character Values

_ex-09 · exercises co-04_

`Boolean` models a true-or-false decision and `Char` holds one character. Kotlin uses single quotes
for `Char` and double quotes for `String`.

```kotlin
fun main() { // => begins execution
    val enabled = true // => Boolean value
    val grade = 'A' // => one Char, not a String
    println("$enabled:$grade") // => prints true:A
    // => closes the current scope
}
```

**Key takeaway:** A character and a string are separate types with separate literals.

**Why it matters:** Precise types prevent vague APIs. A flag should not become a magic string, and
a parser that expects one character should not accept an arbitrary-length label by accident.

## Example 10: Interpolate a String Template

_ex-10 · exercises co-05_

Use `$name` for a simple name and `${expression}` when computation is needed. Templates avoid noisy
string concatenation.

```kotlin
fun main() { // => program entry point
    val name = "Ada" // => value inserted by $name
    println("$name has ${1 + 2} tasks") // => evaluates expression inside braces
    // => closes the current scope
}
```

**Key takeaway:** String templates keep output close to the values it describes.

**Why it matters:** Status text is common in CLI tools and Android UI. Templates make it harder to
misplace separators and easier to spot which values are dynamic.

## Example 11: Use a Multi-line String

_ex-11 · exercises co-05_

Triple quotes preserve line breaks without escape sequences. `trimIndent` removes indentation that
belongs to the source formatting rather than the desired output.

```kotlin
fun main() { // => starts the sample
    // => opens a raw multi-line string
    val note = """
        Kotlin
        ready
    """.trimIndent() // => removes common leading indentation
    // => raw text contains Kotlin and ready on separate output lines
    // => source indentation is not part of the resulting value
    println(note) // => prints two lines
    // => closes the current scope
}
```

**Key takeaway:** Triple-quoted strings are useful for readable multi-line text.

**Why it matters:** Small examples often need display text, test fixtures, or structured snippets.
Keeping their source readable prevents escape characters from hiding the actual content.

## Example 12: Declare a Nullable Value

_ex-12 · exercises co-06_

Appending `?` says that a value may be absent. The compiler will require a safe access strategy
before you use it as a non-null `String`.

```kotlin
fun main() { // => program entry point
    val nickname: String? = null // => nullable String may hold null
    println(nickname) // => printing a nullable value is safe
    // => closes the current scope
}
```

**Key takeaway:** Nullability is part of a Kotlin type, not a comment convention.

**Why it matters:** Android data frequently arrives late or not at all. Recording that possibility
in the type moves a common runtime failure into a compiler-guided design decision.

## Example 13: Keep Non-null Values Non-null

_ex-13 · exercises co-06_

A plain `String` cannot receive `null`. The commented assignment demonstrates a compile-time error
rather than a later null-pointer failure.

```kotlin
fun main() { // => begins execution
    val title: String = "Inbox" // => String excludes null
    // val broken: String = null // => does not compile
    println(title) // => safe member use is allowed
    // => closes the current scope
}
```

**Key takeaway:** Non-null is Kotlin's default contract.

**Why it matters:** Default non-null types make ordinary code pleasant: you access properties without
defensive checks because the compiler has already ruled absence out.

## Example 14: Use a Safe Call

_ex-14 · exercises co-07_

`?.` calls a member only when its receiver exists; otherwise the whole expression evaluates to
`null`.

```kotlin
fun main() { // => starts a standalone program
    val nickname: String? = null // => receiver may be absent
    println(nickname?.length) // => prints null instead of throwing
    // => closes the current scope
}
```

**Key takeaway:** A safe call turns an absent receiver into an absent result.

**Why it matters:** This lets a data-access path express "no value available" without pretending it
is exceptional. Combine it with an explicit fallback when the caller needs a concrete value.

## Example 15: Chain Safe Calls

_ex-15 · exercises co-07_

Safe calls compose from outer object to nested property. The chain stops at the first missing link.

```kotlin
data class Profile(val city: String) // => simple nested value type
data class User(val profile: Profile?) // => profile itself may be absent
fun main() { // => program entry point
    val user: User? = User(null) // => user exists but profile does not
    println(user?.profile?.city) // => chain returns null safely
    // => closes the current scope
}
```

**Key takeaway:** One `?.` at each nullable boundary models a safe traversal.

**Why it matters:** Nested API responses are ordinary in mobile work. A safe chain states exactly
which links may be missing and avoids a forest of manually nested `if` checks.

## Example 16: Supply an Elvis Default

_ex-16 · exercises co-08_

The Elvis operator returns its left value when non-null and its right value otherwise. It reads like
a compact, value-producing null check.

```kotlin
fun main() { // => begins the example
    val nickname: String? = null // => no optional name available
    val display = nickname ?: "guest" // => fallback chosen for null
    println(display) // => prints guest
    // => closes the current scope
}
```

**Key takeaway:** `?:` turns optional data into a deliberate default.

**Why it matters:** Defaults belong at a boundary where the application can justify one. The operator
makes that policy visible instead of leaking nullable values into unrelated code.

## Example 17: Return Early with Elvis

_ex-17 · exercises co-08_

The right side of Elvis may return from the current function. This converts an optional lookup into
a short guard clause.

```kotlin
fun printScore(scores: Map<String, Int>, name: String) { // => function accepts a lookup table
    val score = scores[name] ?: return // => leave when the key is absent
    println(score) // => only runs with a concrete Int
    // => closes the current scope
}
fun main() { // => runs the safe lookup
    printScore(emptyMap(), "Ada") // => produces no unsafe access
    // => closes the current scope
}
```

**Key takeaway:** Unwrap-or-return keeps the normal path unindented.

**Why it matters:** Guard clauses make preconditions obvious. In Android handlers, they prevent a
missing ID or model from forcing every following line into another conditional block.

## Example 18: Treat `!!` as an Escape Hatch

_ex-18 · exercises co-09_

`!!` promises a nullable value is present, then throws an NPE if that promise is false. This sample
uses a present value so it runs, but it is rarely the right first choice.

```kotlin
fun main() { // => starts the program
    val token: String? = "abc" // => nullable type still contains a value here
    println(token!!.length) // => assertion converts to non-null for this expression
    // => closes the current scope
}
```

**Key takeaway:** `!!` moves uncertainty from the compiler to a potential runtime crash.

**Why it matters:** The operator can be justified after an externally enforced invariant, but most
application code communicates better with `?.`, `?:`, or an explicit validation error.

## Example 19: Enter a Safe `let` Block

_ex-19 · exercises co-10_

`?.let` invokes its lambda only for a present receiver. Inside the lambda, the value is non-null.

```kotlin
fun main() { // => starts execution
    val email: String? = "a@example.test" // => optional input is present
    email?.let { value -> println(value.uppercase()) } // => lambda receives non-null String
    // => closes the current scope
}
```

**Key takeaway:** Safe `let` scopes work that only makes sense for a value.

**Why it matters:** It is useful when rendering optional data or starting a transformation pipeline.
Use a named parameter when `it` would make nested lambdas difficult to read.

## Example 20: Define a Function

_ex-20 · exercises co-11_

Parameters and return type follow the function name. The body returns its last explicit `return`.

```kotlin
fun add(left: Int, right: Int): Int { // => declares inputs and result type
    return left + right // => returns the computed sum
    // => closes the current scope
}
fun main() { // => calls the reusable function
    println(add(2, 3)) // => prints 5
    // => closes the current scope
}
```

**Key takeaway:** A typed function gives a name to one focused behaviour.

**Why it matters:** Small functions isolate decisions and make tests direct. Android code benefits
when formatters and mappers are ordinary Kotlin functions rather than hidden UI callbacks.

## Example 21: Return `Unit`

_ex-21 · exercises co-11_

Functions that primarily perform an effect return `Unit`; Kotlin lets you omit it. `println` is an
example of a useful effect with no meaningful result.

```kotlin
fun announce(message: String) { // => implicit Unit return type
    println(message) // => performs the function's effect
    // => closes the current scope
}
fun main() { // => entry point
    announce("saved") // => prints saved
    // => closes the current scope
}
```

**Key takeaway:** Omit `: Unit` when the function communicates through an effect.

**Why it matters:** This distinguishes commands from queries. A clear return contract helps callers
avoid assuming that an operation has produced a value they should use.

## Example 22: Add a Default Argument

_ex-22 · exercises co-12_

A parameter can provide its own fallback. Callers may omit it when the default expresses the common
case.

```kotlin
fun greet(name: String, greeting: String = "Hello") { // => greeting has a default value
    println("$greeting, $name") // => uses supplied or default greeting
    // => closes the current scope
}
fun main() { // => invokes both forms
    greet("Ada") // => prints Hello, Ada
    // => closes the current scope
}
```

**Key takeaway:** Defaults can replace overloads that differ only in ordinary options.

**Why it matters:** Compact APIs reduce duplicate implementation paths. Keep defaults stable and
unsurprising because they become behaviour callers rely on without writing them explicitly.

## Example 23: Name Arguments at the Call Site

_ex-23 · exercises co-12_

Named arguments document what a literal means and let a caller choose parameter order. They are
especially helpful when two arguments share a type.

```kotlin
fun greet(name: String, greeting: String = "Hello") { // => accepts two named parameters
    println("$greeting, $name") // => formats the message
    // => closes the current scope
}
fun main() { // => calls by parameter names
    greet(greeting = "Welcome", name = "Ada") // => order is intentionally reversed
    // => closes the current scope
}
```

**Key takeaway:** Named arguments make a call's intent visible.

**Why it matters:** A Boolean or integer literal is often ambiguous at a positional call site.
Naming it makes reviews faster and prevents argument-order mistakes.

## Example 24: Use a Single-expression Function

_ex-24 · exercises co-13_

When the body is one expression, `=` replaces braces and `return`. Kotlin infers the return type
from that expression.

```kotlin
fun double(value: Int) = value * 2 // => expression result becomes the return value
fun main() { // => starts execution
    println(double(4)) // => prints 8
    // => closes the current scope
}
```

**Key takeaway:** Single-expression functions are concise for transparent calculations.

**Why it matters:** This form works well for formatters, predicates, and mappings. Avoid it when a
multi-step body would be clearer than compressing several operations into one expression.

## Example 25: Accept Varargs

_ex-25 · exercises co-11_

`vararg` collects zero or more call-site arguments into an array-like value. It is appropriate for
a natural list of homogeneous inputs.

```kotlin
fun total(vararg values: Int): Int { // => accepts any number of Int arguments
    return values.sum() // => sums the collected values
    // => closes the current scope
}
fun main() { // => calls the vararg function
    println(total(1, 2, 3)) // => prints 6
    // => closes the current scope
}
```

**Key takeaway:** Varargs improve calls that naturally read as a list.

**Why it matters:** They are convenient for small APIs, but a `List` is clearer when values are
already collected or when an API needs a stable collection abstraction.

## Example 26: Use `if` as a Value

_ex-26 · exercises co-24_

Kotlin's `if` can produce a value. When used that way it requires an `else` branch, so both outcomes
are accounted for.

```kotlin
fun main() { // => begins execution
    val largest = if (7 > 4) 7 else 4 // => chooses one Int value
    println(largest) // => prints 7
    // => closes the current scope
}
```

**Key takeaway:** Value-producing conditionals make assignment logic direct.

**Why it matters:** This style is useful when a UI label, validation result, or calculated value has
two clear alternatives. It avoids mutable variables initialized only to be changed later.
