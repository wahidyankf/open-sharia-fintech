---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish the small Swift surface you will see before any Xcode-specific API. Save a
normal block as `Example.swift` and use `swift Example.swift`; intentional failing lines stay
commented so the file itself always runs.

## Example 1: Compile a Swift File

_ex-01 · exercises co-01_

`swiftc hello.swift -o hello && ./hello` compiles a standalone executable; `swift hello.swift` is a
faster learning loop for scripts.

```swift
print("Hello, Swift") // => swiftc builds a program whose observable result is one line
```

**Key takeaway:** The CLI is enough to learn Swift before an IDE. **Why it matters:** a two-line
program separates language errors from project configuration.

## Example 2: Try the REPL

_ex-02 · exercises co-01_

At a terminal, run `swift`, enter `1 + 2`, then exit with `:quit`. The REPL reports `3`; this file
records the same expression as runnable source.

```swift
print(1 + 2) // => prints 3, the value the REPL would echo
```

**Key takeaway:** Use the REPL for one expression, a file for a repeatable example. **Why it matters:**
repeatable files become tests and small experiments rather than unrecoverable terminal history.

## Example 3: Prefer `let`

_ex-03 · exercises co-02_

```swift
let course = "Swift" // => immutable binding after initialization
print(course) // => Swift
// course = "iOS" // => compiler error: cannot assign to a let constant
```

**Key takeaway:** `let` prevents rebinding. **Why it matters:** choosing immutability first narrows
the places reviewers must inspect for state changes.

## Example 4: Use `var` for a Real Transition

_ex-04 · exercises co-02_

```swift
var attempts = 0 // => mutable binding starts at zero
attempts += 1 // => intentional reassignment
print(attempts) // => 1
```

**Key takeaway:** `var` communicates a planned change. **Why it matters:** it is useful for a local
accumulator, but it does not make shared state safe by itself.

## Example 5: Let Swift Infer a Type

_ex-05 · exercises co-03_

```swift
let name = "Ada" // => compiler infers String from the literal
print(name.uppercased()) // => ADA proves String methods are available
```

**Key takeaway:** inference is static, not dynamic typing. **Why it matters:** avoid redundant
annotations when the initializer tells the reader the type clearly.

## Example 6: State a Type Contract

_ex-06 · exercises co-03_

```swift
let retryCount: Int = 3 // => explicit annotation documents the API-level intent
print(retryCount + 1) // => 4
```

**Key takeaway:** annotations are useful at boundaries. **Why it matters:** a visible contract can
prevent an initializer refactor from silently changing an inferred numeric type.

## Example 7: Convert Numeric Types Explicitly

_ex-07 · exercises co-04_

```swift
let count = 3 // => Int
let average = Double(count) / 2 // => conversion makes the precision choice explicit
print(average) // => 1.5
```

**Key takeaway:** Swift does not silently mix `Int` and `Double`. **Why it matters:** visible
conversions expose rounding and precision decisions in business calculations.

## Example 8: Combine Boolean Conditions

_ex-08 · exercises co-04_

```swift
let signedIn = true // => Bool condition one
let acceptedTerms = false // => Bool condition two
print(signedIn && acceptedTerms) // => false: both must be true
```

**Key takeaway:** `&&` requires both conditions; `||` accepts either. **Why it matters:** named
conditions make authorization and UI-state decisions easier to audit than nested flags.

## Example 9: Interpolate Values

_ex-09 · exercises co-05_

```swift
let name = "Ada" // => a String value
let tasks = 3 // => an Int value
print("Hi \(name), you have \(tasks) tasks") // => evaluates each parenthesized expression
```

**Key takeaway:** `\(expression)` embeds a value in text. **Why it matters:** interpolation keeps
status messages readable without fragile concatenation punctuation.

## Example 10: Declare an Optional

_ex-10 · exercises co-06_

```swift
var middleName: String? = nil // => the type permits absence
print(middleName as Any) // => nil, printed through Any only for this demonstration
```

**Key takeaway:** `String?` means a string may be absent. **Why it matters:** the type makes every
consumer acknowledge that absence instead of assuming a magic empty value.

## Example 11: Assign an Optional

_ex-11 · exercises co-06_

```swift
var nickname: String? = nil // => initially absent
nickname = "Ace" // => now stores a String inside Optional
print(nickname ?? "missing") // => Ace
```

**Key takeaway:** an optional has a present value or `nil`. **Why it matters:** modeling those two
states directly avoids a second Boolean such as `hasNickname` drifting out of sync.

## Example 12: Bind a Present Value

_ex-12 · exercises co-07_

```swift
let input: String? = "ready" // => optional source
if let value = input { // => value is non-optional inside this branch
    print(value.uppercased()) // => READY
}
```

**Key takeaway:** `if let` gates work on presence. **Why it matters:** it keeps unsafe unwrapping
out of ordinary display and parsing code.

## Example 13: Exit Early with `guard let`

_ex-13 · exercises co-07_

```swift
func announce(_ input: String?) { // => accepts possibly absent input
    guard let value = input else { print("nothing to announce"); return } // => leaves the nil path
    print(value) // => value remains non-optional for the rest of the function
}
announce(nil) // => nothing to announce
```

**Key takeaway:** `guard let` flattens the normal path. **Why it matters:** early exits prevent
important work from becoming nested beneath every validation condition.

## Example 14: Chain Optional Members

_ex-14 · exercises co-08_

```swift
struct Address { let city: String } // => value model
struct User { let address: Address? } // => address may be missing
let user: User? = User(address: nil) // => a user exists without an address
print(user?.address?.city as Any) // => nil; no member access crashes
```

**Key takeaway:** `?.` stops at the first absent link. **Why it matters:** it represents a safe read
through a partial model without turning every lookup into a pyramid of `if` statements.

## Example 15: Supply a Fallback

_ex-15 · exercises co-09_

```swift
let label: String? = nil // => absence is explicit
print(label ?? "Guest") // => Guest, the local display policy
```

**Key takeaway:** `??` uses the left value or a fallback. **Why it matters:** put fallback policy
where a consumer needs it rather than erasing absence at the data boundary.

## Example 16: See Why `!` Is Dangerous

_ex-16 · exercises co-10_

```swift
let token: String? = nil // => no value exists
print(token ?? "missing") // => safe outcome
// print(token!) // => uncomment to trigger a runtime trap on nil
```

**Key takeaway:** force unwrapping asserts a fact at runtime. **Why it matters:** prefer binding,
chaining, or validation unless a local invariant genuinely proves the value exists.

## Example 17: Define an Effectful Function

_ex-17 · exercises co-11_

```swift
func greet(_ name: String) { // => no arrow means a Void result
    print("Hello, \(name)") // => effect is printing
}
greet("Ada") // => Hello, Ada
```

**Key takeaway:** `_` omits an external label when a simple call reads naturally. **Why it matters:**
function signatures make repeatable behavior testable and name its input.

## Example 18: Return a Value

_ex-18 · exercises co-11_

```swift
func square(_ number: Int) -> Int { // => declares an Int result
    number * number // => single-expression return is implicit
}
print(square(4)) // => 16
```

**Key takeaway:** `-> Int` makes a result part of the contract. **Why it matters:** callers can
compose a returned value instead of relying on hidden mutation or output.

## Example 19: Use Argument Labels

_ex-19 · exercises co-12_

```swift
func move(from start: Int, to destination: Int) { // => labels name the call-site roles
    print("\(start) -> \(destination)")
}
move(from: 1, to: 2) // => labels are part of the call
```

**Key takeaway:** labels make same-typed arguments harder to swap. **Why it matters:** APIs read
closer to a sentence when a literal's role is visible.

## Example 20: Default an Ordinary Option

_ex-20 · exercises co-12_

```swift
func log(_ message: String, level: String = "info") { print("[\(level)] \(message)") }
log("saved") // => [info] saved
log("retrying", level: "warning") // => caller overrides only when needed
```

**Key takeaway:** defaults keep common calls short. **Why it matters:** one signature serves a
normal path and an explicit override without duplicate overloads.

## Example 21: Make an Array

_ex-21 · exercises co-27_

```swift
let tasks = ["read", "run", "review"] // => Array<String> inferred from literals
print(tasks.count) // => 3
```

**Key takeaway:** an array preserves order and permits repeated values. **Why it matters:** ordered
input is the usual starting point for display and transformation pipelines.

## Example 22: Make a Dictionary

_ex-22 · exercises co-27_

```swift
let points = ["Ada": 10, "Lin": 8] // => Dictionary<String, Int>
print(points["Ada"] ?? 0) // => lookup is optional because a key may be absent
```

**Key takeaway:** dictionary lookup returns an optional. **Why it matters:** Swift prevents a
missing key from masquerading as a real zero or empty value.

## Example 23: Make a Set

_ex-23 · exercises co-27_

```swift
let tags: Set = ["swift", "swift", "ios"] // => duplicate entries collapse
print(tags.count) // => 2
```

**Key takeaway:** a set models membership, not order. **Why it matters:** it makes uniqueness a
property of the data structure instead of a cleanup rule every loop must remember.

## Example 24: Iterate an Array

_ex-24 · exercises co-27_

```swift
let steps = ["open", "edit", "run"] // => ordered collection
for step in steps { print(step) } // => visits each element once in order
```

**Key takeaway:** `for-in` reads a collection without index bookkeeping. **Why it matters:** use it
when the operation is an effect; use transformations later when creating a new collection.

## Example 25: Store a Closure

_ex-25 · exercises co-13_

```swift
let add = { (left: Int, right: Int) in left + right } // => closure is a typed behavior value
print(add(2, 3)) // => 5
```

**Key takeaway:** a closure can be passed, stored, and called. **Why it matters:** callbacks and
collection operators use behavior as data, without requiring a new named type.

## Example 26: Use Trailing-Closure Syntax

_ex-26 · exercises co-13_

```swift
func repeatTwice(_ work: () -> Void) { work(); work() } // => accepts a closure
repeatTwice { print("run") } // => trailing closure is the final argument
```

**Key takeaway:** trailing syntax keeps a call's main action visually attached. **Why it matters:**
it is idiomatic in Swift APIs, so recognizing it prevents punctuation from hiding control flow.
