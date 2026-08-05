---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 turn basic syntax into deliberate models. Each block is a self-contained
standard-library program; run it with `swift Example.swift`.

## Example 27: Define a Struct

_ex-27 · exercises co-15_

```swift
struct Point { var x: Int; var y: Int } // => a value type with stored state
let origin = Point(x: 0, y: 0) // => memberwise initializer is synthesized
print(origin.x) // => 0
```

**Key takeaway:** a struct is Swift's ordinary value model. **Why it matters:** use one when copies
should become independent state, which is the safe default for most domain data.

## Example 28: Construct and Read a Struct

_ex-28 · exercises co-15_

```swift
struct Task { let title: String } // => immutable stored property
let task = Task(title: "Read") // => labels come from property names
print(task.title) // => Read
```

**Key takeaway:** memberwise construction exposes a struct's data plainly. **Why it matters:** small
immutable records are easy to create in tests and difficult to leave half initialized.

## Example 29: Define a Class

_ex-29 · exercises co-16_

```swift
final class Counter { var value = 0 } // => reference type with one mutable property
let counter = Counter() // => creates one shared instance
print(counter.value) // => 0
```

**Key takeaway:** a class supplies identity and shared reference semantics. **Why it matters:** use
it deliberately for an object whose identity or coordinated mutation is central to the design.

## Example 30: Mutate a Class Through a Function

_ex-30 · exercises co-16, co-17_

```swift
final class Counter { var value = 0 } // => instance state
func increment(_ counter: Counter) { counter.value += 1 } // => receives the same reference
let counter = Counter(); increment(counter) // => function changes that instance
print(counter.value) // => 1
```

**Key takeaway:** passing a class does not copy it. **Why it matters:** aliasing is powerful but
requires clear ownership because any holder can observe a mutation.

## Example 31: Copy a Struct Value

_ex-31 · exercises co-17_

```swift
struct Score { var value: Int } // => value type
let original = Score(value: 1); var copy = original // => copy gets independent storage
copy.value = 2 // => mutates only copy
print("\(original.value), \(copy.value)") // => 1, 2
```

**Key takeaway:** assigning a struct copies its value. **Why it matters:** independent snapshots
make state transitions easier to reason about and reduce accidental cross-feature coupling.

## Example 32: Alias a Class Reference

_ex-32 · exercises co-17_

```swift
final class Score { var value: Int = 1 } // => reference type
let first = Score(); let second = first // => both names refer to the same object
second.value = 2 // => mutation is visible via first
print(first.value) // => 2
```

**Key takeaway:** copying a class variable copies a reference. **Why it matters:** this is the
central trade-off: shared identity needs explicit coordination, unlike copied structs.

## Example 33: Read and Write a Stored Property

_ex-33 · exercises co-18_

```swift
struct Progress { var completed = 0 } // => stored property keeps state
var progress = Progress(); progress.completed += 1 // => outer var permits replacement after mutation
print(progress.completed) // => 1
```

**Key takeaway:** stored properties hold a type's state. **Why it matters:** make state a named
property instead of smuggling it through unrelated global or local variables.

## Example 34: Derive a Computed Property

_ex-34 · exercises co-18_

```swift
struct Rectangle { let width: Int; let height: Int; var area: Int { width * height } }
let rectangle = Rectangle(width: 3, height: 4) // => source dimensions remain the stored truth
print(rectangle.area) // => 12, computed on read
```

**Key takeaway:** computed properties derive rather than duplicate data. **Why it matters:** one
source of truth avoids stale cached values when dimensions change.

## Example 35: Delay a Lazy Property

_ex-35 · exercises co-18_

```swift
struct Report { lazy var title: String = { print("building"); return "Weekly" }() }
var report = Report() // => initializer closure has not run
print(report.title) // => prints building, then Weekly
```

**Key takeaway:** `lazy` evaluates on first access. **Why it matters:** use it for work that may not
be needed; avoid it merely to hide an unclear initialization dependency.

## Example 36: Mark a Mutating Struct Method

_ex-36 · exercises co-19_

```swift
struct Meter { var value = 0; mutating func increment() { value += 1 } } // => mutating permits self change
var meter = Meter(); meter.increment()
print(meter.value) // => 1
```

**Key takeaway:** a value-type method changing `self` must say `mutating`. **Why it matters:** the
signature makes state transitions visible before a caller reads the method body.

## Example 37: Return Instead of Mutating

_ex-37 · exercises co-19_

```swift
struct Temperature { let celsius: Double; func fahrenheit() -> Double { celsius * 9 / 5 + 32 } }
let temperature = Temperature(celsius: 0) // => immutable input
print(temperature.fahrenheit()) // => 32.0
```

**Key takeaway:** non-mutating methods can derive values. **Why it matters:** calculations stay
referentially simple when they return a result instead of changing the receiver.

## Example 38: Define a Closed Enum

_ex-38 · exercises co-20_

```swift
enum Direction { case north, south } // => only these alternatives exist
let direction = Direction.north // => chooses one named case
print(direction == .north) // => true; no raw string comparison
```

**Key takeaway:** enums name finite alternatives. **Why it matters:** a compiler-known state space
is safer than loosely related strings such as "north" and "N".

## Example 39: Give Enum Cases Raw Values

_ex-39 · exercises co-20_

```swift
enum Status: Int { case ok = 200; case notFound = 404 } // => each case has an underlying Int
print(Status.ok.rawValue) // => 200
```

**Key takeaway:** raw values are uniform literal representations. **Why it matters:** use them at
serialization or protocol boundaries; keep enum cases as the internal model.

## Example 40: Carry an Associated Value

_ex-40 · exercises co-21_

```swift
enum LoadState { case success(String); case failure(String) } // => each state carries relevant context
let state = LoadState.success("ready")
print(state) // => success("ready")
```

**Key takeaway:** associated values make a case a tagged payload. **Why it matters:** success and
failure need different data, which avoids invalid combinations of nullable fields and flags.

## Example 41: Carry Multiple Values

_ex-41 · exercises co-21_

```swift
enum Shape { case point(Int, Int) } // => a case may carry more than one value
let shape = Shape.point(2, 3)
if case let .point(x, y) = shape { print("\(x),\(y)") } // => 2,3
```

**Key takeaway:** associated values can have independent types and arity. **Why it matters:** one
case models data that belongs together without a parallel side structure.

## Example 42: Switch Exhaustively

_ex-42 · exercises co-22_

```swift
enum Light { case red, green }
let light = Light.green
switch light { case .red: print("stop"); case .green: print("go") } // => every case is handled
```

**Key takeaway:** `switch` over an enum must cover its cases. **Why it matters:** adding a case
causes compiler-guided updates wherever behavior must be decided.

## Example 43: Bind an Associated Value

_ex-43 · exercises co-22, co-21_

```swift
enum Reply { case success(String); case failure }
let reply = Reply.success("saved")
switch reply { case let .success(message): print(message); case .failure: print("retry") }
```

**Key takeaway:** `case let` introduces a payload with its real type. **Why it matters:** pattern
matching proves which data is available in each branch instead of relying on casts.

## Example 44: Add a `where` Condition

_ex-44 · exercises co-22_

```swift
let score = 92
switch score { case let value where value >= 90: print("excellent"); default: print("keep going") }
```

**Key takeaway:** `where` refines a matched pattern. **Why it matters:** it keeps threshold rules
close to the case that owns them, without abandoning a readable switch structure.

## Example 45: Transform with `map`

_ex-45 · exercises co-14_

```swift
let doubled = [1, 2, 3].map { $0 * 2 } // => one output per input
print(doubled) // => [2, 4, 6]
```

**Key takeaway:** `map` preserves shape while transforming values. **Why it matters:** a declared
pipeline avoids a mutable accumulator and makes the result relation obvious.

## Example 46: Retain with `filter`

_ex-46 · exercises co-14_

```swift
let evens = [1, 2, 3, 4].filter { $0.isMultiple(of: 2) } // => predicate keeps selected values
print(evens) // => [2, 4]
```

**Key takeaway:** `filter` selects, rather than changes, elements. **Why it matters:** separating
selection from transformation makes business rules easier to test and reorder deliberately.

## Example 47: Combine with `reduce`

_ex-47 · exercises co-14_

```swift
let total = [1, 2, 3].reduce(0, +) // => starts at zero and combines each value
print(total) // => 6
```

**Key takeaway:** `reduce` collapses a collection into one value. **Why it matters:** an explicit
initial value documents the identity and handles an empty collection safely.

## Example 48: Capture a Surrounding Value

_ex-48 · exercises co-13_

```swift
var prefix = "first" // => captured variable lives outside closure
let describe = { "\(prefix): task" } // => closure reads it when invoked
prefix = "second"; print(describe()) // => second: task
```

**Key takeaway:** closures capture surrounding variables by reference-like storage. **Why it matters:**
capture makes delayed behavior convenient, but mutable captures can make timing-sensitive code obscure.

## Example 49: Sort with a Closure

_ex-49 · exercises co-14_

```swift
let descending = [3, 1, 2].sorted { $0 > $1 } // => closure defines ordering
print(descending) // => [3, 2, 1]
```

**Key takeaway:** higher-order APIs let a caller provide a small policy. **Why it matters:** behavior
is localized at the call site when it has no reusable domain name.

## Example 50: Declare a Protocol

_ex-50 · exercises co-23_

```swift
protocol Shape { var area: Double { get } } // => requirement, not implementation
struct Square: Shape { let side: Double; var area: Double { side * side } } // => conforms
print(Square(side: 2).area) // => 4.0
```

**Key takeaway:** a protocol declares a behavioral contract. **Why it matters:** callers can depend
on what a value does rather than how a particular concrete type stores itself.

## Example 51: Conform a Struct

_ex-51 · exercises co-23_

```swift
protocol Named { var name: String { get } }
struct User: Named { let name: String } // => stored property fulfills get-only requirement
print(User(name: "Ada").name) // => Ada
```

**Key takeaway:** a simple property can satisfy a protocol requirement. **Why it matters:** values
stay lightweight while still participating in polymorphic APIs.

## Example 52: Use Protocol Polymorphism

_ex-52 · exercises co-23_

```swift
protocol Shape { var area: Double { get } }
struct Square: Shape { let side: Double; var area: Double { side * side } }
struct Circle: Shape { let radius: Double; var area: Double { Double.pi * radius * radius } }
let shapes: [any Shape] = [Square(side: 2), Circle(radius: 1)] // => explicit common protocol type
print(shapes.map { $0.area }) // => mixed conformers share the contract
```

**Key takeaway:** protocol-typed collections accept varied implementations. **Why it matters:**
the operation can evolve independently from the concrete models it works over.

## Example 53: Provide a Protocol Default

_ex-53 · exercises co-24_

```swift
protocol Named { var name: String { get } }
extension Named { func describe() -> String { "name: \(name)" } } // => default behavior
struct User: Named { let name: String }
print(User(name: "Ada").describe()) // => name: Ada
```

**Key takeaway:** a protocol extension shares behavior across conformers. **Why it matters:** keep
truly universal behavior once, while allowing a conformer to provide a more specific implementation.

## Example 54: Accept Any Conformer

_ex-54 · exercises co-23_

```swift
protocol Shape { var area: Double { get } }
struct Square: Shape { let side: Double; var area: Double { side * side } }
func describe(_ shape: some Shape) { print("area: \(shape.area)") } // => opaque parameter accepts a conformer
describe(Square(side: 3)) // => area: 9.0
```

**Key takeaway:** `some Protocol` expresses one unknown conforming concrete type. **Why it matters:**
the function stays generic in use without committing its callers to inheritance or a specific struct.
