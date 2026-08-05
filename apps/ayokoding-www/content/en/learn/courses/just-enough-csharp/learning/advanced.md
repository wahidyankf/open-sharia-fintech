---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Each snippet is a complete `Program.cs` for a console project. Run it with `dotnet run` after replacing the generated source; the final example points to the complete capstone project and its test suite.

## Example 55: switch expression

_ex-55 · exercises co-20_

This `switch` expression returns a value by selecting the matching relational-pattern arm.

```csharp
var score = 82; // => input
var result = score switch
{
    >= 80 => "distinction",
    >= 50 => "pass",
    _ => "retry",
};
Console.WriteLine(result); // => Output: pass
```

**Key takeaway:** a `switch` expression maps a value to exactly one result and makes its fallback arm explicit.

**Why it matters:** Pattern arms scale more clearly than nested conditionals when a domain has several classifications to maintain.

## Example 56: is pattern

_ex-56 · exercises co-20_

The type pattern both verifies that `value` is an `int` and binds that integer as `number`.

```csharp
object value = 7; // => object
if (value is int number) Console.WriteLine(number * 2); // => Output: 14
```

**Key takeaway:** `is int number` replaces a type check plus cast with one safe, scoped binding.

**Why it matters:** Type patterns make runtime shape checks explicit without risking invalid casts.

## Example 57: property pattern

_ex-57 · exercises co-20_

The property pattern checks `Point.X` declaratively without manually reading the property first.

```csharp
var point = new Point(0, 4); // => record
Console.WriteLine(point is { X: 0 } ? "axis" : "other"); // => Output: axis
record Point(int X, int Y);
```

**Key takeaway:** property patterns match values by the members relevant to the decision.

**Why it matters:** They keep classification logic close to the data shape and avoid nested property-check conditionals.

## Example 58: tuple pattern

_ex-58 · exercises co-20_

The tuple switch matches both coordinates together, including a discard for any vertical move.

```csharp
var move = (0, 1); // => tuple
var label = move switch { (0, 0) => "still", (0, _) => "vertical", _ => "other" }; // => match
Console.WriteLine(label); // => Output: vertical
```

**Key takeaway:** tuple patterns classify several related values in one ordered set of cases.

**Why it matters:** Matching a combined state prevents a maze of conditions that forget how individual values interact.

## Example 59: try and catch

_ex-59 · exercises co-21_

The risky parse throws `FormatException`, and the matching `catch` turns that failure into a controlled result.

```csharp
try { int.Parse("nope"); } // => fails
catch (FormatException) { Console.WriteLine("invalid"); } // => Output: invalid
```

**Key takeaway:** `try` encloses the operation that can fail, while `catch` handles the expected failure type.

**Why it matters:** Narrow exception handling preserves useful failure information without letting malformed input terminate a whole workflow.

## Example 60: specific exception

_ex-60 · exercises co-21_

The catch names `InvalidOperationException`, so it handles the known closed-state failure without swallowing unrelated errors.

```csharp
try { throw new InvalidOperationException("closed"); } // => expected failure
catch (InvalidOperationException error) { Console.WriteLine(error.Message); } // => Output: closed
```

**Key takeaway:** catch the most specific exception that the local code can genuinely recover from.

**Why it matters:** Specific catches keep programming defects and infrastructure failures visible instead of misreporting them as normal input problems.

## Example 61: finally block

_ex-61 · exercises co-21_

The `finally` block runs after the protected work regardless of whether that work completes or throws.

```csharp
try { Console.WriteLine("work"); } // => Output: work
finally { Console.WriteLine("cleanup"); } // => Output: cleanup
```

**Key takeaway:** `finally` is the guaranteed cleanup path associated with a `try` block.

**Why it matters:** Reliable cleanup protects resource lifetimes when an operation has more than one exit path.

## Example 62: custom exception

_ex-62 · exercises co-21_

`BalanceException` names a domain-specific failure, and the catch preserves its explanatory message.

```csharp
try { throw new BalanceException("insufficient"); } // => domain failure
catch (BalanceException e) { Console.WriteLine(e.Message); } // => Output: insufficient
class BalanceException(string message) : Exception(message);
```

**Key takeaway:** a custom exception type distinguishes a meaningful domain failure from generic runtime errors.

**Why it matters:** Callers can handle an expected business rule separately from parsing, network, or programming failures.

## Example 63: throw expression

_ex-63 · exercises co-21, co-11_

The null-coalescing expression either supplies a valid input or throws immediately at the boundary.

```csharp
string? input = null; // => absent input
try { var name = input ?? throw new ArgumentNullException(); } // => guard
catch (ArgumentNullException) { Console.WriteLine("required"); } // => Output: required
```

**Key takeaway:** `?? throw` states that a required value must be present before subsequent code runs.

**Why it matters:** Failing close to the invalid input prevents nullable uncertainty from spreading through unrelated logic.

## Example 64: async method

_ex-64 · exercises co-22_

The `async Task` method awaits its operation and completes only after writing its result.

```csharp
await ReportAsync(); // => awaits completion
static async Task ReportAsync() { await Task.Delay(1); Console.WriteLine("done"); } // => Output: done
```

**Key takeaway:** an `async Task` represents asynchronous completion without a result value.

**Why it matters:** Returning `Task` lets callers await the real completion boundary instead of guessing when background work ends.

## Example 65: await a task

_ex-65 · exercises co-22_

`await` pauses this method's continuation until `ReadAsync` supplies its text result.

```csharp
var text = await ReadAsync(); // => continuation result
Console.WriteLine(text); // => Output: ready
static async Task<string> ReadAsync() { await Task.Delay(1); return "ready"; }
```

**Key takeaway:** awaiting `Task<T>` unwraps its eventual `T` while preserving asynchronous control flow.

**Why it matters:** Awaiting keeps result-dependent code ordered without blocking a thread during I/O or other asynchronous work.

## Example 66: async return value

_ex-66 · exercises co-22_

The method computes an integer asynchronously and returns its eventual value as `Task<int>`.

```csharp
var sum = await AddAsync(2, 3); // => Task<int>
Console.WriteLine(sum); // => Output: 5
static async Task<int> AddAsync(int a, int b) { await Task.Delay(1); return a + b; }
```

**Key takeaway:** `Task<T>` makes both the pending operation and its eventual result part of the method signature.

**Why it matters:** The type forces callers to decide when and where to await a result instead of accidentally treating it as immediate.

## Example 67: non-blocking await

_ex-67 · exercises co-22_

The caller can print `started` before awaiting the task; awaiting later resumes when the delayed work finishes.

```csharp
var task = LaterAsync(); // => starts task
Console.WriteLine("started"); // => Output: started
Console.WriteLine(await task); // => Output: finished
static async Task<string> LaterAsync() { await Task.Delay(1); return "finished"; }
```

**Key takeaway:** `await` registers a continuation rather than synchronously waiting on the current thread.

**Why it matters:** This behavior keeps responsive applications free to process other work while an asynchronous dependency is pending.

## Example 68: multiple awaits

_ex-68 · exercises co-22_

The second await starts only after the first result has been printed, making the sequential dependency explicit.

```csharp
Console.WriteLine(await StepAsync("one")); // => Output: one
Console.WriteLine(await StepAsync("two")); // => Output: two
static async Task<string> StepAsync(string x) { await Task.Delay(1); return x; }
```

**Key takeaway:** consecutive awaits preserve order when each step depends on the previous one.

**Why it matters:** Separating sequential work from independent work helps select `await` or `Task.WhenAll` for the correct semantics.

## Example 69: Task.WhenAll

_ex-69 · exercises co-22_

`Task.WhenAll` waits for both independent fetches and returns their results in the input task order.

```csharp
var values = await Task.WhenAll(GetAsync(1), GetAsync(2)); // => join tasks
Console.WriteLine(string.Join(",", values)); // => Output: 1,2
static async Task<int> GetAsync(int x) { await Task.Delay(1); return x; }
```

**Key takeaway:** `Task.WhenAll` expresses that several operations may run concurrently but must all complete before continuing.

**Why it matters:** Joining independent work can reduce latency while keeping one clear completion and error boundary.

## Example 70: async exception

_ex-70 · exercises co-22, co-21_

The exception stored in the faulted task is rethrown at the `await`, where the caller can handle it.

```csharp
try { await FailAsync(); } // => task faults
catch (InvalidOperationException) { Console.WriteLine("handled"); } // => Output: handled
static async Task FailAsync() { await Task.Delay(1); throw new InvalidOperationException(); }
```

**Key takeaway:** asynchronous exceptions follow the task and are observed by awaiting it.

**Why it matters:** Putting the `try`/`catch` around `await` handles the actual asynchronous failure rather than only task creation.

## Example 71: LINQ aggregate

_ex-71 · exercises co-17_

`Sum` reduces the sequence of integers to one total using LINQ's aggregate operation.

```csharp
var values = new[] { 1, 2, 3 }; // => source
Console.WriteLine(values.Sum()); // => Output: 6
```

**Key takeaway:** aggregation turns many values into one result, such as a total, count, minimum, or maximum.

**Why it matters:** Aggregates make report calculations declarative and avoid manual accumulator loops when the intent is standard.

## Example 72: generic LINQ combination

_ex-72 · exercises co-15, co-17_

The generic method filters null class references and returns the remaining elements as a typed LINQ sequence.

```csharp
Console.WriteLine(string.Join(",", NonNull(new string?[] { "a", null, "b" }))); // => Output: a,b
static IEnumerable<T> NonNull<T>(IEnumerable<T?> xs) where T : class => xs.Where(x => x is not null).Select(x => x!);
```

**Key takeaway:** generics and LINQ compose when a reusable query must preserve the caller's element type.

**Why it matters:** A single null-filtering helper can serve many reference types without weakening results to `object` or casts.

## Example 73: record pattern match

_ex-73 · exercises co-12, co-20_

The switch inspects the record's `Ok` property and chooses a result without manually unpacking the record.

```csharp
var result = new Result(true, "saved"); // => record
Console.WriteLine(result switch { { Ok: true } => "ok", _ => "retry" }); // => Output: ok
record Result(bool Ok, string Message);
```

**Key takeaway:** property patterns let records participate directly in domain-state decisions.

**Why it matters:** Pattern matching keeps result handling exhaustive-looking and close to the shape that produced it.

## Example 74: nullable LINQ

_ex-74 · exercises co-05, co-17_

The query filters null entries before dereferencing each remaining name to calculate its length.

```csharp
string?[] names = ["Ada", null, "Lin"]; // => nullable source
var sizes = names.Where(x => x is not null).Select(x => x!.Length); // => safe query
Console.WriteLine(string.Join(",", sizes)); // => Output: 3,3
```

**Key takeaway:** establish non-nullness with `Where` before projecting nullable elements into non-null operations.

**Why it matters:** Null-safe sequence processing prevents one incomplete record from turning a whole report into a runtime failure.

## Example 75: generic interface

_ex-75 · exercises co-08, co-15_

`IRepository<string>` describes a storage seam whose returned elements remain strongly typed.

```csharp
IRepository<string> repo = new MemoryRepository<string>(["Ada"]); // => typed seam
Console.WriteLine(repo.All().Single()); // => Output: Ada
interface IRepository<T> { IEnumerable<T> All(); }
class MemoryRepository<T>(IEnumerable<T> xs) : IRepository<T> { public IEnumerable<T> All() => xs; }
```

**Key takeaway:** a generic interface gives one abstraction a consistent contract across many domain types.

**Why it matters:** Typed repository seams make swapping storage implementations possible without reducing everything to untyped objects.

## Example 76: async LINQ pipeline

_ex-76 · exercises co-22, co-17_

The program awaits the asynchronous fetch before applying a normal in-memory LINQ filter to its result.

```csharp
var values = await FetchAsync(); // => async fetch
Console.WriteLine(string.Join(",", values.Where(x => x > 1))); // => Output: 2,3
static async Task<int[]> FetchAsync() { await Task.Delay(1); return [1, 2, 3]; }
```

**Key takeaway:** await the asynchronous boundary first, then use LINQ over the materialized values unless an async-query API is intended.

**Why it matters:** Keeping the async boundary visible avoids implying that ordinary `IEnumerable<T>` operators themselves perform asynchronous I/O.

## Example 77: domain model slice

_ex-77 · exercises co-07, co-12, co-08_

The record carries a notification value, the interface defines delivery, and the class supplies one concrete delivery behavior.

```csharp
INotifier notifier = new ConsoleNotifier(); // => interface seam
notifier.Send(new Notice("Saved")); // => Output: Saved
record Notice(string Text);
interface INotifier { void Send(Notice n); }
class ConsoleNotifier : INotifier { public void Send(Notice n) => Console.WriteLine(n.Text); }
```

**Key takeaway:** records, interfaces, and classes each have distinct roles in a small domain model.

**Why it matters:** Separating data from a capability and its implementation keeps future delivery channels from leaking into the model.

## Example 78: capstone CLI

_ex-78 · exercises co-05, co-12, co-16, co-08, co-22, co-01_

The complete capstone combines a nullable-aware lookup, records, a query-syntax LINQ report, an interface seam, and an awaited operation.

```csharp
ICatalog catalog = new MemoryCatalog([new Product("A", "Adapter")]);
var products = await Task.WhenAll([catalog.FindAsync("A"), catalog.FindAsync("missing")]);
var report =
    from product in products
    where product is not null
    select product.Name;
Console.WriteLine(string.Join(",", report)); // Output: Adapter

record Product(string Id, string Name);
interface ICatalog { Task<Product?> FindAsync(string id); }
sealed class MemoryCatalog(IEnumerable<Product> products) : ICatalog
{
    public Task<Product?> FindAsync(string id) =>
        Task.FromResult(products.SingleOrDefault(product => product.Id == id));
}
```

Run the complete project with `dotnet run --project capstone/code/CatalogReport/CatalogReport.csproj` and its assertions with `dotnet test capstone/code/CatalogReport.Tests/CatalogReport.Tests.csproj`.

**Key takeaway:** the capstone composes the primer's type, abstraction, query, and async tools into one verifiable CLI boundary.

**Why it matters:** Small end-to-end composition exposes the contracts between language features that isolated snippets cannot show.
