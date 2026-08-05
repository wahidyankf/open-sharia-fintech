---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Most snippets are complete `Program.cs` files for a console project. Run them with `dotnet run` after replacing the generated source. Examples that teach project creation, test execution, nullable configuration, or compiler diagnostics include the required command or project-file fragment as well.

## Example 1: dotnet new console

_ex-01 · exercises co-01_

`dotnet new console` creates the project and its top-level `Program.cs`; this recipe verifies both artifacts instead of printing the command name.

```bash
dotnet new console --output CsharpPrimer
dotnet run --project CsharpPrimer
```

The generated program prints `Hello, World!` and gives the next examples a real project home.

**Key takeaway:** `dotnet new console` scaffolds a compilable console application, not just a source file.

**Why it matters:** Starting from the SDK template establishes the project metadata that builds, tests, package references, and editor tooling all use.

## Example 2: dotnet run

_ex-02 · exercises co-01_

`dotnet run` builds the current project when needed and launches its entry point in one command.

```csharp
var answer = 42; // => inferred int
Console.WriteLine(answer); // => Output: 42
```

**Key takeaway:** `dotnet run` is the shortest feedback loop for a console project.

**Why it matters:** Running through the SDK keeps the command line, project configuration, and source code on the same path used by CI.

## Example 3: dotnet test command

_ex-03 · exercises co-01_

`dotnet test` builds a test project and executes its discovered tests. Create the SDK test project, replace its generated test, then run the command.

```bash
dotnet new xunit --output CsharpPrimer.Tests
```

```csharp
// CsharpPrimer.Tests/UnitTest1.cs
using Xunit;

public sealed class ArithmeticTests
{
    [Fact]
    public void AddsTwoNumbers() => Assert.Equal(5, 2 + 3);
}
```

```bash
dotnet test CsharpPrimer.Tests/CsharpPrimer.Tests.csproj
```

The final command reports one passing test.

**Key takeaway:** `dotnet test` is the repeatable way to build and verify an automated test project.

**Why it matters:** A test command is useful only when it executes an assertion whose pass/fail result can protect a later change.

## Example 4: top-level statements

_ex-04 · exercises co-02_

Top-level statements let a small program state its work directly, while the compiler supplies the entry point.

```csharp
var message = "top-level"; // => no Main class needed
Console.WriteLine(message); // => Output: top-level
```

**Key takeaway:** a console app needs one entry point, not necessarily a hand-written `Main` method.

**Why it matters:** Removing ceremonial startup code keeps small utilities and learning examples focused on their behavior.

## Example 5: var inference

_ex-05 · exercises co-04_

`var` asks the compiler to infer a local type from the expression on the right.

```csharp
var number = 42; // => compiler infers int
Console.WriteLine(number.GetType().Name); // => Output: Int32
```

**Key takeaway:** inference preserves static typing; `number` is still an `int`.

**Why it matters:** Use `var` when the initializer makes the type obvious, so declarations stay concise without becoming vague.

## Example 6: int, string, and bool

_ex-06 · exercises co-04_

The three declarations model a quantity, text, and a decision with their built-in C# types.

```csharp
int count = 3; // => whole number
string label = "ready"; // => text
bool enabled = true; // => decision
Console.WriteLine(label + ":" + count + ":" + enabled); // => Output: ready:3:True
```

**Key takeaway:** choose a type that expresses the kind of value, not merely how it will be printed.

**Why it matters:** Correct primitive types give the compiler useful checks before richer domain types are introduced.

## Example 7: value-type copy

_ex-07 · exercises co-03_

Assigning an `int` copies its value, so changing the second variable cannot affect the first.

```csharp
var first = 1; // => value
var second = first; // => copied value
second = 2; // => only second changes
Console.WriteLine(first); // => Output: 1
```

**Key takeaway:** value-type assignment creates independent values.

**Why it matters:** Knowing when data is copied prevents accidental shared-state assumptions in calculations and structs.

## Example 8: reference-type alias

_ex-08 · exercises co-03_

Assigning a class value copies its reference, so both variables point at the same `Counter` object.

```csharp
var first = new Counter(); // => one object
var second = first; // => same reference
second.Value = 2; // => shared mutation
Console.WriteLine(first.Value); // => Output: 2
class Counter { public int Value { get; set; } }
```

**Key takeaway:** reference assignment aliases an object; mutation through either alias is shared.

**Why it matters:** Alias awareness is essential when mutable model objects cross service or UI boundaries.

## Example 9: enable nullable analysis

_ex-09 · exercises co-05_

Nullable reference types are activated at project scope. Put this property in the console project's `.csproj`, then compile the nullable-aware source.

```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>
```

```csharp
string name = "Ada"; // non-nullable by default when nullable analysis is enabled
Console.WriteLine(name.Length); // Output: 3
```

`dotnet build` now performs null-state analysis for every reference type in the project.

**Key takeaway:** `<Nullable>enable</Nullable>` makes non-nullability the default contract instead of an opt-in convention.

**Why it matters:** Project-wide analysis catches unsafe assumptions at compile time, before a UI or service dereferences missing data at runtime.

## Example 10: nullable annotation

_ex-10 · exercises co-05_

The `?` annotation declares that the absent value is part of this variable's contract.

```csharp
string? name = null; // => reference may be absent
Console.WriteLine(name ?? "guest"); // => Output: guest
```

**Key takeaway:** `string?` communicates possible absence, while `??` supplies an intentional fallback.

**Why it matters:** Expressing absence in the type makes callers confront it instead of relying on informal null conventions.

## Example 11: null analysis warning

_ex-11 · exercises co-05_

The compiler warns when a nullable value is dereferenced without a preceding null check. Build this source with Example 9's nullable configuration enabled.

```csharp
string? name = Console.ReadLine(); // may be null
Console.WriteLine(name.Length); // CS8602: Dereference of a possibly null reference
```

```bash
dotnet build
```

The build succeeds with the diagnostic unless the project elects to treat warnings as errors.

**Key takeaway:** a nullable annotation propagates uncertainty until the code proves the value is present.

**Why it matters:** Reading the warning at the dereference site leads to an explicit guard or fallback, rather than a latent `NullReferenceException`.

## Example 12: null-forgiving operator

_ex-12 · exercises co-06_

The null-forgiving operator tells the compiler that a value has already been proven present at this point.

```csharp
string? name = "Ada"; // => locally proven present
Console.WriteLine(name!.Length); // => Output: 3
// => ! suppresses analysis, not a runtime null check
```

**Key takeaway:** `!` changes null-state analysis only; it does not add a runtime check.

**Why it matters:** Reserve `!` for a documented invariant; a guard is safer whenever that invariant can fail.

## Example 13: string interpolation

_ex-13 · exercises co-23_

String interpolation embeds an expression directly in a string literal.

```csharp
var name = "Ada"; // => text
Console.WriteLine($"Hi {name}"); // => Output: Hi Ada
```

**Key takeaway:** prefixing a string literal with `$` lets braces contain the values being formatted.

**Why it matters:** Interpolation keeps messages readable when they combine fixed text with several variables or formatted values.

## Example 14: string methods

_ex-14 · exercises co-23_

Core `string` methods return transformed or inspected text without mutating the original string.

```csharp
var text = "ready,steady"; // => source
var parts = text.ToUpper().Split(','); // => transforms and splits
Console.WriteLine($"{parts[1]}:{text.Contains(",")}"); // => Output: STEADY:True
```

**Key takeaway:** `ToUpper`, `Split`, and `Contains` respectively transform, partition, and inspect text.

**Why it matters:** These operations are the basic vocabulary for parsing user input and shaping text for display without hidden mutation.

## Example 15: declare a namespace

_ex-15 · exercises co-24_

A namespace gives `Badge` a qualified identity instead of leaving it in the global scope.

```csharp
Console.WriteLine(new Primer.Badge().Name); // => Output: C#
namespace Primer { public class Badge { public string Name => "C#"; } }
```

**Key takeaway:** namespaces organize related types and prevent unrelated names from colliding.

**Why it matters:** Clear namespaces make a growing application easier to navigate and import selectively.

## Example 16: using directive

_ex-16 · exercises co-24_

A `using` directive makes extension methods in an imported namespace available by their short names.

```csharp
using System.Linq; // => imports LINQ
Console.WriteLine(new[] { 1, 2, 3 }.Count()); // => Output: 3
```

**Key takeaway:** `using System.Linq` brings LINQ's `Count` extension method into scope.

**Why it matters:** Imports keep source readable, but limiting them to needed namespaces keeps dependencies apparent.

## Example 17: define a class

_ex-17 · exercises co-07_

The class combines a named piece of state with the objects created from its definition.

```csharp
var card = new Card { Title = "Inbox" }; // => class instance
Console.WriteLine(card.Title); // => Output: Inbox
class Card { public string Title { get; set; } = ""; }
```

**Key takeaway:** a class defines the shape and behavior shared by each instance created with `new`.

**Why it matters:** Classes become the boundary for cohesive application responsibilities, not merely bags of fields.

## Example 18: class constructor

_ex-18 · exercises co-07_

The primary constructor requires the `User` name at creation and exposes it as read-only state.

```csharp
var user = new User("Ada"); // => required construction state
Console.WriteLine(user.Name); // => Output: Ada
class User(string name) { public string Name { get; } = name; }
```

**Key takeaway:** constructors establish invariants before an object can be used.

**Why it matters:** Required construction data prevents partially initialized objects from leaking through an application.

## Example 19: instance method

_ex-19 · exercises co-07_

The instance method reads the `Meter`'s state and returns a calculation associated with that object.

```csharp
var meter = new Meter(3); // => model state
Console.WriteLine(meter.Next()); // => Output: 4
class Meter(int value) { public int Next() => value + 1; }
```

**Key takeaway:** instance methods place behavior next to the state they operate on.

**Why it matters:** Cohesive methods make a model easier to reason about and test than scattered procedural logic.

## Example 20: auto-property

_ex-20 · exercises co-10_

An auto-property lets the compiler manage storage while the type exposes a public get/set contract.

```csharp
var item = new Item(); // => object
item.Name = "Review"; // => property set
Console.WriteLine(item.Name); // => Output: Review
class Item { public string Name { get; set; } = ""; }
```

**Key takeaway:** `{ get; set; }` is appropriate for mutable state whose storage needs no custom logic yet.

**Why it matters:** Properties give a stable public surface even if validation or computed behavior is added later.

## Example 21: init-only property

_ex-21 · exercises co-10_

An `init` accessor accepts an object-initializer value but rejects later reassignment.

```csharp
var item = new Item { Id = 7 }; // => allowed at construction
Console.WriteLine(item.Id); // => Output: 7
class Item { public int Id { get; init; } }
```

**Key takeaway:** `{ get; init; }` supports convenient construction while preserving immutable state afterward.

**Why it matters:** Immutable configuration and message data are safer to share because their values cannot change unexpectedly.

## Example 22: expression-bodied member

_ex-22 · exercises co-11_

The expression-bodied property computes area directly from the constructor values.

```csharp
var box = new Box(3, 4); // => dimensions
Console.WriteLine(box.Area); // => Output: 12
class Box(int w, int h) { public int Area => w * h; }
```

**Key takeaway:** `=>` is concise when a member has one clear expression and no additional steps.

**Why it matters:** Compact derived values read like their mathematical definition while remaining normal properties to callers.

## Example 23: define an enum

_ex-23 · exercises co-13_

An enum names a closed set of integral values; a `switch` makes every state decision visible.

```csharp
var state = Status.Ready; // => named state
var message = state switch
{
    Status.Ready => "start",
    Status.Loading => "wait",
    Status.Failed => "retry",
    _ => "retry",
};
Console.WriteLine(message); // => Output: start
enum Status { Loading, Ready, Failed }
```

**Key takeaway:** an enum replaces magic numeric or string state markers with a type-checked vocabulary.

**Why it matters:** Switching over named states makes incomplete or unexpected state handling much easier to find during review.

## Example 24: array

_ex-24 · exercises co-14_

The array stores a fixed-length ordered sequence and uses a zero-based index for retrieval.

```csharp
int[] values = [1, 2, 3]; // => fixed sequence
Console.WriteLine(values[1]); // => Output: 2
```

**Key takeaway:** arrays are best when the collection size and element type are known and stable.

**Why it matters:** Array indexing is fast and direct, but callers must respect its fixed bounds.

## Example 25: generic list

_ex-25 · exercises co-14_

`List<string>` grows as names are added while preserving the element type and insertion order.

```csharp
var names = new List<string> { "Ada" }; // => typed list
names.Add("Lin"); // => grows list
Console.WriteLine(string.Join(",", names)); // => Output: Ada,Lin
```

**Key takeaway:** `List<T>` is the general-purpose mutable sequence for values of one known type.

**Why it matters:** Generic collections move type mistakes to compile time instead of requiring casts at every use.

## Example 26: dictionary

_ex-26 · exercises co-14_

The dictionary associates the `pen` key with its price and retrieves the value by that key.

```csharp
var prices = new Dictionary<string, int> { ["pen"] = 2 }; // => key map
Console.WriteLine(prices["pen"]); // => Output: 2
```

**Key takeaway:** `Dictionary<TKey, TValue>` models lookup by a unique key rather than by positional index.

**Why it matters:** Keyed lookup is a natural fit for IDs and codes, but missing keys need deliberate handling in production code.
