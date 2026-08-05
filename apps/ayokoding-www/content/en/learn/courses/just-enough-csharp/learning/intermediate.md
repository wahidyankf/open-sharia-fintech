---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Most snippets are complete `Program.cs` files for a console project. Run them with `dotnet run` after replacing the generated source; the NuGet example also includes the package-install command its source requires.

## Example 27: define an interface

_ex-27 · exercises co-08_

The interface declares an `Area` contract without choosing how a shape calculates it.

```csharp
IShape shape = new Square(3); // => contract reference
Console.WriteLine(shape.Area()); // => Output: 9
interface IShape { int Area(); }
class Square(int side) : IShape { public int Area() => side * side; }
```

**Key takeaway:** an interface specifies capabilities that callers can depend on independently of concrete types.

**Why it matters:** Contracts let application code accept a useful abstraction rather than being coupled to one implementation.

## Example 28: implement an interface

_ex-28 · exercises co-08_

`FixedClock` satisfies every member of `IClock`, so it can be used through the interface reference.

```csharp
IClock clock = new FixedClock(); // => implementation
Console.WriteLine(clock.Now()); // => Output: noon
interface IClock { string Now(); }
class FixedClock : IClock { public string Now() => "noon"; }
```

**Key takeaway:** `: IClock` commits a class to provide the interface's promised behavior.

**Why it matters:** Concrete implementations can be exchanged for test doubles or platform-specific services without changing callers.

## Example 29: default interface member

_ex-29 · exercises co-08_

The interface supplies `Greet`'s default body, so an implementer can inherit behavior it does not override.

```csharp
IGreeter greeter = new Greeter(); // => implementation inherits default
Console.WriteLine(greeter.Greet()); // => Output: hello
interface IGreeter { string Greet() => "hello"; }
class Greeter : IGreeter { }
```

**Key takeaway:** default interface members can evolve a contract without forcing every existing implementation to add boilerplate.

**Why it matters:** This is a compatibility tool; use it for coherent defaults, not to hide substantial implementation logic in interfaces.

## Example 30: base inheritance

_ex-30 · exercises co-09_

`Dog` derives from `Animal` and reads its protected name through the base-class relationship.

```csharp
var dog = new Dog("Milo"); // => derived object
Console.WriteLine(dog.Describe()); // => Output: animal:Milo
class Animal(string name) { protected string Name { get; } = name; }
class Dog(string name) : Animal(name) { public string Describe() => "animal:" + Name; }
```

**Key takeaway:** inheritance reuses a shared base contract while allowing a derived type to add focused behavior.

**Why it matters:** A meaningful "is-a" relationship can remove duplication; interfaces are usually safer for independently varying behavior.

## Example 31: virtual override

_ex-31 · exercises co-09_

The call dispatches to `Dog.Sound` even though the variable is statically typed as `Animal`.

```csharp
Animal animal = new Dog(); // => base-typed reference
Console.WriteLine(animal.Sound()); // => Output: bark
class Animal { public virtual string Sound() => "?"; }
class Dog : Animal { public override string Sound() => "bark"; }
```

**Key takeaway:** `virtual` opens a base member for polymorphism, and `override` replaces it in a derived type.

**Why it matters:** Polymorphic dispatch keeps callers stable while individual subclasses supply their own behavior.

## Example 32: define a record

_ex-32 · exercises co-12_

The positional record creates immutable value-like data with generated properties and a primary constructor.

```csharp
var point = new Point(2, 3); // => immutable data
Console.WriteLine(point.X + point.Y); // => Output: 5
record Point(int X, int Y);
```

**Key takeaway:** a record is a concise default for data whose identity is its contained values.

**Why it matters:** Records make messages, results, and configuration clearer by putting immutable data at the center.

## Example 33: record value equality

_ex-33 · exercises co-12_

Two separately constructed records compare equal because their corresponding values are equal.

```csharp
var first = new Point(1, 2); // => value one
var second = new Point(1, 2); // => equal data
Console.WriteLine(first == second); // => Output: True
record Point(int X, int Y);
```

**Key takeaway:** record equality answers "do these values describe the same data?" rather than "are these the same allocation?".

**Why it matters:** Value equality makes assertions, deduplication, and change detection match how data is normally understood.

## Example 34: record with copy

_ex-34 · exercises co-12_

The `with` expression produces a new record with only `X` changed, leaving the original intact.

```csharp
var first = new Point(1, 2); // => original
var moved = first with { X = 5 }; // => changed copy
Console.WriteLine(first.X + ":" + moved.X); // => Output: 1:5
record Point(int X, int Y);
```

**Key takeaway:** `with` supports non-destructive updates to immutable record data.

**Why it matters:** Copying a changed value avoids surprising observers that still hold the original record.

## Example 35: positional record deconstruction

_ex-35 · exercises co-12_

The positional record exposes a matching deconstructor, so its two components can bind to local variables.

```csharp
var point = new Point(3, 4); // => record
var (x, y) = point; // => deconstruction
Console.WriteLine(x + y); // => Output: 7
record Point(int X, int Y);
```

**Key takeaway:** deconstruction extracts named parts of a value without repetitive property-access syntax.

**Why it matters:** It is useful at a local boundary, but retaining the record can be clearer when its domain meaning matters.

## Example 36: struct value semantics

_ex-36 · exercises co-26_

Copying the `Vec` struct creates independent data; mutating `right` cannot alter `left`.

```csharp
var left = new Vec { X = 1 }; // => value type
var right = left; right.X = 2; // => copy changes
Console.WriteLine(left.X); // => Output: 1
struct Vec { public int X { get; set; } }
```

**Key takeaway:** structs are value types, so assignment and parameter passing copy their value by default.

**Why it matters:** Small immutable value objects are a good struct fit; large or mutable structs can make copies costly and confusing.

## Example 37: struct versus class

_ex-37 · exercises co-26, co-03_

The same `X` mutation leaves the copied struct unchanged but changes the object seen through a class alias.

```csharp
var value = new Vec { X = 1 }; var valueCopy = value; valueCopy.X = 2; // => copy
var reference = new Box { X = 1 }; var alias = reference; alias.X = 2; // => alias
Console.WriteLine(value.X + ":" + reference.X); // => Output: 1:2
struct Vec { public int X { get; set; } }
class Box { public int X { get; set; } }
```

**Key takeaway:** choose a struct for independent value semantics and a class when shared identity is intentional.

**Why it matters:** This distinction determines whether a later mutation is isolated or observed by every holder of the value.

## Example 38: generic method

_ex-38 · exercises co-15_

The method's type parameter flows from the input sequence to its returned first element.

```csharp
Console.WriteLine(First(new[] { "a", "b" })); // => Output: a
static T First<T>(IEnumerable<T> xs) => xs.First(); // => type flows through
```

**Key takeaway:** `T` lets one method preserve type information for many element types without casts.

**Why it matters:** Generic helpers reduce duplication while keeping incorrect type combinations out of a build.

## Example 39: generic class

_ex-39 · exercises co-15_

`Box<int>` captures a concrete type argument, so its `Value` property is known to be an `int`.

```csharp
var box = new Box<int>(7); // => Box<int>
Console.WriteLine(box.Value); // => Output: 7
class Box<T>(T value) { public T Value { get; } = value; }
```

**Key takeaway:** a generic class carries its type parameter across stored state and operations.

**Why it matters:** Type-parameterized containers are reusable without sacrificing the safety of strongly typed members.

## Example 40: generic constraint

_ex-40 · exercises co-15_

The `IComparable<T>` constraint guarantees that the generic method may call `CompareTo` on its inputs.

```csharp
Console.WriteLine(Max(2, 5)); // => Output: 5
static T Max<T>(T a, T b) where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b; // => constraint
```

**Key takeaway:** `where T : ...` states the capability a type parameter must provide.

**Why it matters:** Constraints turn an otherwise cryptic generic implementation requirement into a compiler-enforced contract.

## Example 41: LINQ query where

_ex-41 · exercises co-16_

Query syntax filters the source with a `where` clause before selecting each matching value.

```csharp
var xs = new[] { -1, 2, 3 }; // => source
var positive = from x in xs where x > 0 select x; // => query filter
Console.WriteLine(string.Join(",", positive)); // => Output: 2,3
```

**Key takeaway:** `from`/`where`/`select` reads like a data query over any `IEnumerable<T>`.

**Why it matters:** Query syntax is often the clearest form when a transformation has several clauses to read top-to-bottom.

## Example 42: LINQ query select

_ex-42 · exercises co-16_

The `select` clause projects each source string into an uppercase result while preserving the query's shape.

```csharp
var xs = new[] { "ada", "lin" }; // => source
var upper = from x in xs select x.ToUpper(); // => query projection
Console.WriteLine(string.Join(",", upper)); // => Output: ADA,LIN
```

**Key takeaway:** projection creates a new sequence of the values a caller actually needs.

**Why it matters:** Projecting early prevents later layers from depending on more source data than they require.

## Example 43: LINQ method where

_ex-43 · exercises co-17_

The `Where` extension method receives a predicate lambda and yields only values that satisfy it.

```csharp
var xs = new[] { 1, 2, 3, 4 }; // => source
var even = xs.Where(x => x % 2 == 0); // => method filter
Console.WriteLine(string.Join(",", even)); // => Output: 2,4
```

**Key takeaway:** method-syntax `Where` expresses filtering as a composable operation on a sequence.

**Why it matters:** Method syntax composes naturally with extension methods and is the foundation for most day-to-day LINQ pipelines.

## Example 44: LINQ method orderby

_ex-44 · exercises co-17_

`OrderBy` produces an ordered view of the source using the key selected by its lambda.

```csharp
var xs = new[] { "Lin", "Ada" }; // => source
var ordered = xs.OrderBy(x => x); // => ordering query
Console.WriteLine(string.Join(",", ordered)); // => Output: Ada,Lin
```

**Key takeaway:** ordering is explicit and non-mutating: the original array remains in its original order.

**Why it matters:** Sorting at a report boundary makes presentation order intentional instead of relying on incidental input order.

## Example 45: LINQ chain

_ex-45 · exercises co-17_

The chain filters, transforms, and orders values as three readable stages of one query.

```csharp
var xs = new[] { 3, 1, 2 }; // => source
var result = xs.Where(x => x > 1).Select(x => x * 10).OrderBy(x => x); // => pipeline
Console.WriteLine(string.Join(",", result)); // => Output: 20,30
```

**Key takeaway:** each LINQ operator returns a sequence that the next operator can refine.

**Why it matters:** Separating pipeline stages makes business rules easier to inspect and change without interleaving loops and temporary state.

## Example 46: deferred execution

_ex-46 · exercises co-18_

The query does not read `xs` until it is enumerated, so the later `3` is included in its output.

```csharp
var xs = new List<int> { 1, 2 }; // => mutable source
var query = xs.Where(x => x > 1); // => deferred query
xs.Add(3); // => source changes
Console.WriteLine(string.Join(",", query)); // => Output: 2,3
```

**Key takeaway:** many LINQ operators describe a query now and execute it later when a consumer iterates it.

**Why it matters:** Deferred queries can reflect later source changes or repeat work, so their enumeration point should be deliberate.

## Example 47: immediate execution

_ex-47 · exercises co-18_

`ToList` materializes the filtered values before the source changes, creating a stable snapshot.

```csharp
var xs = new List<int> { 1, 2 }; // => source
var snapshot = xs.Where(x => x > 1).ToList(); // => immediate list
xs.Add(3); // => later change
Console.WriteLine(string.Join(",", snapshot)); // => Output: 2
```

**Key takeaway:** materializers such as `ToList` force a deferred query to run at a chosen moment.

**Why it matters:** A snapshot is useful when later mutations must not alter a report, response, or multi-pass calculation.

## Example 48: lambda expression

_ex-48 · exercises co-19_

A lambda creates a callable value that doubles whichever integer is supplied to it.

```csharp
Func<int, int> doubleIt = x => x * 2; // => lambda value
Console.WriteLine(doubleIt(4)); // => Output: 8
```

**Key takeaway:** `x => x * 2` is a compact function definition whose parameter and return types are checked.

**Why it matters:** Lambdas let behavior travel as data into APIs such as LINQ without inventing one-off named methods.

## Example 49: Func delegate

_ex-49 · exercises co-19_

`Func<string, int>` states that the delegate accepts a string and produces an integer result.

```csharp
Func<string, int> length = text => text.Length; // => typed callback
Console.WriteLine(length("C#")); // => Output: 2
```

**Key takeaway:** `Func<...>` represents a callback with a return value.

**Why it matters:** Explicit delegate signatures document what a higher-order API needs from its caller.

## Example 50: Action delegate

_ex-50 · exercises co-19_

`Action<string>` carries an effectful callback that accepts text and returns no result.

```csharp
Action<string> show = text => Console.WriteLine(text); // => effect callback
show("saved"); // => Output: saved
```

**Key takeaway:** `Action<...>` models work performed for its side effect rather than for a returned value.

**Why it matters:** Event handlers and configurable notifications commonly need this no-result callback shape.

## Example 51: lambda in LINQ

_ex-51 · exercises co-19, co-17_

The lambda passed to `Select` extracts one initial from each name in the source sequence.

```csharp
var names = new[] { "Ada", "Lin" }; // => source
var initials = names.Select(name => name[0]); // => lambda projection
Console.WriteLine(string.Join(",", initials)); // => Output: A,L
```

**Key takeaway:** LINQ lambdas define the per-element rule while the operator controls the iteration.

**Why it matters:** This separation clarifies whether a bug belongs in the transformation rule or in the collection traversal.

## Example 52: list of records

_ex-52 · exercises co-12, co-14_

The list stores immutable `Point` records, then LINQ projects their X coordinates into a report.

```csharp
var points = new List<Point> { new(1, 2), new(3, 4) }; // => records
Console.WriteLine(string.Join(",", points.Select(p => p.X))); // => Output: 1,3
record Point(int X, int Y);
```

**Key takeaway:** records and generic collections combine typed data modeling with ordinary sequence operations.

**Why it matters:** This is the common shape of in-memory application data before it is filtered or rendered.

## Example 53: interface polymorphism

_ex-53 · exercises co-08, co-09_

The `IShape[]` holds different implementations, and each call dispatches to the matching `Area` method.

```csharp
IShape[] shapes = [new Square(2), new Circle(1)]; // => mixed implementations
Console.WriteLine(string.Join(",", shapes.Select(x => x.Area()))); // => Output: 4,3
interface IShape { int Area(); }
class Square(int x) : IShape { public int Area() => x * x; }
class Circle(int x) : IShape { public int Area() => x * 3; }
```

**Key takeaway:** a collection of interface values can invoke one shared operation across heterogeneous types.

**Why it matters:** Interface polymorphism lets new implementations join an existing workflow without a growing type-switch.

## Example 54: NuGet package command

_ex-54 · exercises co-25_

Add a package to the project before importing its API. This example uses Humanizer, then calls its `ToWords` extension method.

```bash
dotnet add package Humanizer
```

```csharp
using Humanizer;

Console.WriteLine(3.ToWords()); // Output: three
```

Run `dotnet run` after the add command; restore resolves the package and the import compiles.

**Key takeaway:** `dotnet add package` records a dependency in the project file so restore can make its APIs available.

**Why it matters:** Declaring the dependency before using its namespace keeps builds reproducible on another machine or CI runner.
