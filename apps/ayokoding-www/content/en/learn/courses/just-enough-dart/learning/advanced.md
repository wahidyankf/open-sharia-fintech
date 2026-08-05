---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 complete the bounded Dart surface that Flutter readers meet immediately: records,
patterns, `Future`, and `Stream`. They are still language examples, not a replacement for Flutter's
widget lifecycle or state-management practices.

## Records and patterns

### Example 55: Create a Positional Record

_ex-55 · exercises co-22_

A record can group a fixed set of positional values without declaring a named class.

```dart
void main() { // => starts a positional-record sample
  (int, int) point = (1, 2); // => creates an immutable two-int record
  print('${point.$1}:${point.$2}'); // => prints 1:2 using positional fields
} // => ends the example
```

**Key takeaway:** Use a positional record for a small, local aggregate whose positions remain obvious.

**Why it matters:** A helper may need to return two closely related values without introducing a
class that only one call site understands. Records make that relationship typed and immutable.
Choose a named class instead when the values acquire behavior, validation, persistence needs, or
a domain name; those signals mean readers benefit from more than numbered positional fields.

### Example 56: Create a Named Record

_ex-56 · exercises co-22_

Named record fields make each value's role visible at construction and read sites.

```dart
void main() { // => begins a named-record sample
  ({int x, int y}) point = (x: 1, y: 2); // => creates an immutable named aggregate
  print(point.x); // => prints the field selected by name
} // => finishes the example
```

**Key takeaway:** Prefer named record fields when a reader should not infer meaning from position.

**Why it matters:** A `(String, String)` return becomes ambiguous as soon as a caller asks which
string is a title and which is a subtitle. Named record fields preserve the compact syntax while
making the contract legible in editor completion and review. Promote the record to a class once
the value needs its own behavior or must cross a broad module boundary.

### Example 57: Destructure a Record

_ex-57 · exercises co-22_

A record pattern assigns its positional fields to local names in one declaration.

```dart
void main() { // => starts record destructuring
  final point = (3, 4); // => creates a positional record
  final (x, y) = point; // => binds both fields by pattern
  print(x + y); // => prints 7
} // => completes the destructuring
```

**Key takeaway:** Destructure a local record when names make its individual values easier to use.

**Why it matters:** Multiple return values are useful only if their consumers can make their roles
clear. Pattern binding prevents repeated `$1` and `$2` access from obscuring later calculations.
Keep the destructuring near the call that produced the record so a reader can see the original
contract; passing loose variables far away can lose the grouping the record was chosen to preserve.

### Example 58: Return Multiple Values

_ex-58 · exercises co-22_

A function can return a record when one calculation naturally produces several related results.

```dart
(int, int) minMax(List<int> values) { // => declares a two-result function contract
  return (values.reduce((a, b) => a < b ? a : b), values.reduce((a, b) => a > b ? a : b)); // => returns min and max
} // => closes the helper
void main() { // => consumes both results
  print(minMax([3, 1, 2])); // => prints (1, 3)
} // => finishes the example
```

**Key takeaway:** A record return keeps tightly related results typed without an ad-hoc mutable output object.

**Why it matters:** Parsing, layout calculations, and validation can yield more than one useful
value. A record makes that relationship explicit without inventing a class solely for a short-lived
pair. Still, avoid returning a large anonymous bundle: a named domain object communicates more
clearly when callers need to preserve, compare, document, or extend the result over time.

### Example 59: Destructure a List Pattern

_ex-59 · exercises co-23_

A list pattern matches a list's shape and binds its elements.

```dart
void main() { // => starts a list-pattern sample
  final values = [2, 3]; // => supplies exactly two list elements
  final [left, right] = values; // => destructures the matching list shape
  print(left * right); // => prints 6
} // => ends the example
```

**Key takeaway:** Patterns make an expected value shape explicit where you unpack it.

**Why it matters:** Flutter code often receives structured data that should have a particular
shape before rendering can continue. A pattern binds the useful parts while documenting that
assumption. Use a safer conditional pattern when external data may not match; a destructuring
declaration is best when the surrounding type or earlier validation already guarantees the shape.

### Example 60: Select a Pattern Branch

_ex-60 · exercises co-23_

A pattern `switch` can match both a type and a value form before choosing a branch.

```dart
String describe(Object value) { // => accepts an unknown runtime value
  return switch (value) { // => starts expression-based pattern matching
    int number when number > 0 => 'positive $number', // => binds and guards a positive int
    int number => 'non-positive $number', // => handles other integers
    _ => 'other', // => covers every remaining value
  }; // => returns the selected description
} // => closes the function
void main() { // => tries the positive branch
  print(describe(4)); // => prints positive 4
} // => completes the example
```

**Key takeaway:** A pattern switch combines matching, binding, and branching in one exhaustive expression.

**Why it matters:** State rendering commonly depends on a value's kind and the data attached to
that kind. A pattern switch makes every supported alternative visible and gives matched data a
local name. Avoid a catch-all branch for a closed domain when exhaustiveness can protect future
changes; adding a new state should prompt the renderer to decide what it means.

### Example 61: Use `if-case`

_ex-61 · exercises co-23_

`if-case` tests a pattern and exposes bound values only in the matching branch.

```dart
void main() { // => begins a conditional pattern sample
  final Object value = 7; // => stores a runtime value as Object
  if (value case int number) { // => matches and binds only integers
    print(number + 1); // => prints 8 inside the matched branch
  } // => skips the body for non-integers
} // => ends the program
```

**Key takeaway:** Use `if-case` for one conditional shape check that also needs a bound value.

**Why it matters:** A parser or platform boundary may need one narrow typed path without a full
multi-branch switch. `if-case` keeps the test and cast together, so the value cannot be used as an
`int` outside the proven branch. When several outcomes matter to the product, a `switch` gives
those alternatives equal visibility and reduces the temptation to forget an important case.

### Example 62: Destructure a Map Pattern

_ex-62 · exercises co-23_

A map pattern validates and binds a keyed value when its type matches.

```dart
void main() { // => starts a structured-data sample
  final json = <String, Object>{'user': 'Ada'}; // => supplies untyped boundary-shaped data
  if (json case {'user': String user}) { // => matches the key and narrows its value type
    print(user); // => prints Ada
  } // => handles only the valid shape
} // => completes the pattern example
```

**Key takeaway:** Map patterns make a small decoding assumption visible and type-safe at its use site.

**Why it matters:** JSON-like values start untrusted even when they come from a familiar service.
Matching the expected key and type before use prevents a cast failure from appearing later in a
widget. Keep full API decoding in dedicated mappers for larger payloads, but use a local pattern
when one small optional field needs safe extraction without introducing a broad dynamic surface.

## Futures and streams

### Example 63: Return a `Future`

_ex-63 · exercises co-24_

A `Future<T>` represents a typed value that completes later.

```dart
Future<int> fetchCount() => Future.value(7); // => completes later with an int result
Future<void> main() async { // => permits awaiting asynchronous work
  final count = await fetchCount(); // => waits for the Future<int> result
  print(count); // => prints 7 after completion
} // => completes the async entry point
```

**Key takeaway:** A `Future<T>` preserves the type of a result even while its timing is asynchronous.

**Why it matters:** Network calls, storage, and platform APIs cannot promise a value immediately.
Returning a `Future` makes that delay part of the function contract instead of hiding it in a
callback. Flutter code can then represent waiting, data, and error states intentionally. Keep the
future's result type concrete so a later widget does not need to rediscover what completed.

### Example 64: Read a Future with `await`

_ex-64 · exercises co-24_

`await` pauses the async function until its future completes, while the runtime can continue other work.

```dart
Future<String> fetchName() => Future.value('Ada'); // => creates a completing Future<String>
Future<void> main() async { // => declares an async entry point
  final name = await fetchName(); // => resumes with the completed string
  print('Hi $name'); // => prints Hi Ada after the await
} // => ends after the sequential-looking flow
```

**Key takeaway:** `async` and `await` make an asynchronous dependency read in the order it is used.

**Why it matters:** Nested callbacks make error handling and state transitions hard to follow.
`await` keeps the success path linear while preserving non-blocking completion semantics. It does
not automatically solve cancellation or lifecycle ownership; Flutter code still needs the right
place to start work and a way to avoid applying a completed result to a screen that no longer exists.

### Example 65: Attach a `then` Callback

_ex-65 · exercises co-24_

`then` registers work that runs when a future completes successfully.

```dart
Future<void> main() async { // => allows the program to wait for completion
  final later = Future.value(3); // => creates an already-scheduled future result
  await later.then((value) => print(value * 2)); // => prints 6 in the completion callback
} // => finishes only after the callback runs
```

**Key takeaway:** `then` is useful for a small continuation, while `await` is usually clearer for sequences.

**Why it matters:** You will encounter `then` in existing Dart APIs and codebases, so recognizing
it helps you follow completion flow. For several dependent steps, `await` keeps local variables,
error handling, and cleanup in one readable block. Choose one style per short operation rather
than nesting `then` inside `await` code until the timing and error ownership become difficult to see.

### Example 66: Catch an Async Error

_ex-66 · exercises co-24, co-26_

An awaited future can throw into the surrounding `try`/`catch` block.

```dart
Future<String> fetch() => Future.error(StateError('offline')); // => completes with an error
Future<void> main() async { // => starts asynchronous error handling
  try { // => owns the recovery decision
    await fetch(); // => throws the future's error on completion
  } catch (error) { // => receives the async failure
    print(error); // => prints Bad state: offline
  } // => completes the handled branch
} // => ends the program
```

**Key takeaway:** Place `await` inside `try` when the current layer can recover from its failure.

**Why it matters:** A future error is not less important because it arrives later. Catching it near
the operation lets a feature map an offline request to retry UI or a useful message, while still
allowing unexpected failures to reach shared reporting. Avoid treating every asynchronous error
as absent data; failure and legitimate empty content lead to different product decisions.

### Example 67: Await in Sequence

_ex-67 · exercises co-24_

Two `await` expressions run in the written sequence when the second depends on the first.

```dart
Future<String> step(String value) => Future.value('$value!'); // => returns one later transformation
Future<void> main() async { // => starts ordered async work
  final first = await step('one'); // => completes before the next line starts
  final second = await step(first); // => uses the first result in order
  print(second); // => prints one!!
} // => ends after both completions
```

**Key takeaway:** Sequential `await`s communicate a data dependency and preserve readable order.

**Why it matters:** A token refresh may need to finish before a request, and a parsed ID may need
to exist before storage lookup. Writing the dependency in sequence prevents accidental use of an
unfinished value. Start independent work concurrently only when the operation truly permits it;
unnecessary concurrency makes cancellation, ordering, and failure behavior harder to explain in
a UI feature.

### Example 68: Listen to a Stream

_ex-68 · exercises co-25_

`listen` receives every event from a stream through a callback and returns a subscription.

```dart
Future<void> main() async { // => keeps the process alive until stream completion
  final stream = Stream.fromIterable([1, 2]); // => creates two ordered events
  final done = stream.listen((value) => print(value)).asFuture<void>(); // => prints each event and exposes completion
  await done; // => waits until the subscription finishes
} // => ends after both events arrive
```

**Key takeaway:** A subscription represents an ongoing stream relationship that may later need cancellation.

**Why it matters:** A stream can represent user input, database updates, or device events rather
than one eventual response. The listener must have a lifecycle owner so it does not continue after
a screen or feature disappears. Recognizing the returned subscription prepares you for Flutter
cleanup rules, where failing to cancel a long-lived listener can update stale state or leak work.

### Example 69: Consume with `await for`

_ex-69 · exercises co-25_

`await for` reads stream events in order using a familiar loop shape.

```dart
Future<void> main() async { // => permits asynchronous loop consumption
  final stream = Stream.fromIterable(['a', 'b']); // => provides ordered string events
  await for (final value in stream) { // => waits for each next event
    print(value); // => prints a, then b
  } // => exits after the stream closes
} // => completes the async program
```

**Key takeaway:** Use `await for` when one async function should process each event sequentially.

**Why it matters:** Some streams represent a small finite sequence that a task must fully consume,
such as paged results or generated progress events. The loop keeps per-event logic and ordering
visible without nested callbacks. For an unbounded UI stream, decide explicitly how cancellation
and errors work; a loop is not a substitute for a lifecycle policy owned by the surrounding feature.

### Example 70: Produce a Stream with `async*`

_ex-70 · exercises co-25_

An `async*` generator creates a `Stream`, and each `yield` emits one event without ending the function.

```dart
Stream<int> count() async* { // => declares a stream-producing async generator
  yield 1; // => emits the first event
  yield 2; // => emits the second event
} // => closes the generator after its events
Future<void> main() async { // => consumes the generated stream
  await for (final value in count()) { print(value); } // => prints 1 then 2
} // => completes after consumption
```

**Key takeaway:** `async*` and `yield` express a typed sequence of later values.

**Why it matters:** A generator is useful when a producer naturally exposes incremental results
instead of allocating a complete list first. It also makes event order explicit for consumers and
tests. Keep generators focused on producing values; error recovery, buffering, and UI state belong
at the layer that understands why a particular event stream matters to the user.

### Example 71: Transform a Stream

_ex-71 · exercises co-25_

`map` transforms each stream event while preserving event order.

```dart
Future<void> main() async { // => begins an async stream pipeline
  final numbers = Stream.fromIterable([1, 2]); // => supplies two source events
  final doubled = numbers.map((value) => value * 2); // => transforms events to 2 and 4
  await for (final value in doubled) { print(value); } // => prints 2 then 4
} // => ends after the transformed stream closes
```

**Key takeaway:** Stream transforms keep a producer and consumer decoupled while preserving typed events.

**Why it matters:** Raw device, repository, or network events often need a small mapping before
the UI can use them. A stream transform expresses that one-for-one relationship without mixing it
into the listener. Be cautious with long transform chains: give a meaningful multi-step mapping a
named function so debugging an unexpected event does not require mentally interpreting many inline
closures across a screen's data flow.

## Composition and capstone preview

### Example 72: Add a Generic Constraint

_ex-72 · exercises co-15_

A type bound states the capability a generic algorithm needs from its values.

```dart
T maxValue<T extends Comparable<T>>(T left, T right) { // => requires values that compare to T
  return left.compareTo(right) >= 0 ? left : right; // => chooses the greater typed value
} // => closes the constrained generic function
void main() { // => uses a type that satisfies Comparable<int>
  print(maxValue(2, 5)); // => prints 5
} // => ends the sample
```

**Key takeaway:** Add `extends` only when a generic implementation needs a guaranteed operation.

**Why it matters:** An unconstrained `T` can be stored and passed but cannot promise ordering,
formatting, or domain methods. The bound records exactly what an algorithm relies on, so callers
receive an early diagnostic when they supply an incompatible type. Narrow constraints keep helpers
reusable; requiring a broad base class solely for convenience creates unnecessary coupling between
otherwise independent models.

### Example 73: Combine Two Mixins

_ex-73 · exercises co-21_

Multiple mixins compose their focused behavior from left to right with one `with` clause.

```dart
mixin Named { String get name => 'Ada'; } // => provides a name capability
mixin Welcoming { String greet() => 'hi'; } // => provides a greeting capability
class Person with Named, Welcoming {} // => combines both focused behaviors
void main() { // => uses the composed class
  final person = Person(); // => constructs the mixin host
  print('${person.greet()} ${person.name}'); // => prints hi Ada
} // => completes the example
```

**Key takeaway:** Compose small orthogonal mixins only when their combined API remains easy to explain.

**Why it matters:** Multiple inheritance-like composition can avoid a proliferation of thin base
classes, but it also hides where behavior originates. Small capabilities such as diagnostics or
formatting work well because they have one purpose. If mixins coordinate mutable state, rely on
ordering, or need several dependencies, a normal composed object is usually clearer to construct,
test, and replace in a Flutter feature.

### Example 74: Cache Through a Factory

_ex-74 · exercises co-18_

A factory can return an existing instance from a registry for the same normalized key.

```dart
class User { // => models a cached identity value
  User._(this.name); // => restricts direct construction to the class
  static final _cache = <String, User>{}; // => stores one instance per name
  factory User.named(String name) => _cache.putIfAbsent(name, () => User._(name)); // => reuses or creates one instance
  final String name; // => exposes immutable identity data
} // => closes the cache-owning class
void main() { // => requests the same identity twice
  print(identical(User.named('Ada'), User.named('Ada'))); // => prints true
} // => ends the demonstration
```

**Key takeaway:** A factory may preserve identity when callers request the same canonical value.

**Why it matters:** Caching can be valuable for canonical objects, parsing, or framework values
where identity has a real semantic or performance purpose. It is not a default optimization: global
registries create lifecycle and memory responsibilities. Keep a factory's reuse policy documented
and testable, and prefer ordinary immutable values when equal content matters more than sharing
the exact object instance.

### Example 75: Chain Null-safe Access

_ex-75 · exercises co-08_

A chain of `?.` operators stops at the first absent receiver, and `??` supplies the final fallback.

```dart
class Profile { const Profile(this.city); final String? city; } // => supplies an optional nested value
class User { const User(this.profile); final Profile? profile; } // => supplies an optional nested object
void main() { // => begins a chained nullable read
  const User? user = User(null); // => has no profile
  print(user?.profile?.city ?? 'Unknown'); // => prints Unknown after short-circuiting
} // => ends the safe chain
```

**Key takeaway:** Use a null-safe chain for an optional navigation path, then choose one explicit default.

**Why it matters:** Nested API models often contain optional links, and checking each link manually
can obscure the result a widget needs. The chain clearly preserves absence until the final policy
point. Avoid using it to hide missing required data; if a profile must exist after authentication,
validate that invariant at the boundary and expose a non-null model to downstream UI.

### Example 76: Combine a Future and Stream

_ex-76 · exercises co-24, co-25_

An `async*` generator can await a future before yielding each resulting stream event.

```dart
Future<int> doubleLater(int value) => Future.value(value * 2); // => models an async per-item transform
Stream<int> doubled(Stream<int> source) async* { // => starts an async stream producer
  await for (final value in source) { // => receives each input event in order
    yield await doubleLater(value); // => waits, then emits the doubled result
  } // => ends after source completion
} // => closes the generator
Future<void> main() async { // => consumes the combined asynchronous flow
  await for (final value in doubled(Stream.fromIterable([1, 2]))) { print(value); } // => prints 2 then 4
} // => finishes the program
```

**Key takeaway:** An async generator can express ordered work that has both per-item delay and multiple results.

**Why it matters:** A feature may receive several identifiers and asynchronously enrich each one
before displaying a sequence. Keeping the await next to the yielded value makes the ordering policy
clear. This example intentionally processes sequentially; if independent work should run in
parallel, design its concurrency limit, error behavior, ordering, and cancellation rather than
assuming that an async loop automatically supplies the right throughput.

### Example 77: Combine a Class, Mixin, and Generic Type

_ex-77 · exercises co-16, co-21, co-15_

A generic class can receive behavior from a generic mixin while retaining the element type.

```dart
mixin Printable<T> { String describe(T value) => 'value: $value'; } // => defines typed reusable behavior
class Store<T> with Printable<T> { // => applies the mixin for the same T
  Store(this.value); // => initializes a typed stored value
  final T value; // => preserves the concrete type for callers
} // => closes the generic class
void main() { // => constructs a Store<String>
  print(Store<String>('ready').describe('ready')); // => prints value: ready
} // => completes the composition
```

**Key takeaway:** Type parameters can flow through composed behavior without losing static guarantees.

**Why it matters:** A reusable Flutter helper may need to format, validate, or adapt values of many
domain types. Keeping `T` in both the host and mixin makes mistakes visible before runtime and
prevents a cast-heavy `Object` API. Keep this composition modest: when behavior needs several
services or application policy, inject a collaborator rather than turning a generic mixin into a
hidden dependency container.

### Example 78: Preview the Console Capstone

_ex-78 · exercises co-06, co-21, co-15, co-24, co-25_

This small preview combines the exact primer surface that the materialized capstone tests under
`learning/capstone/code/`.

```dart
mixin Labelled { String label() => 'available'; } // => provides reusable display behavior
class Item<T> with Labelled { Item(this.value); final T value; } // => combines a generic class and mixin
Future<int> laterCount() => Future.value(1); // => supplies one async result
Stream<String> events() async* { yield 'first'; } // => supplies one async sequence event
Future<void> main() async { // => coordinates the async operations
  final Item<String>? item = Item('Dart'); // => uses a nullable, generic model
  print('${item?.value ?? 'none'} ${item?.label()} ${await laterCount()}'); // => prints Dart available 1
  await for (final event in events()) { print(event); } // => prints first after stream consumption
} // => completes the light consolidation program
```

**Key takeaway:** The capstone combines ordinary Dart features without introducing Flutter or a large architecture.

**Why it matters:** Readiness for Flutter means recognizing how language features cooperate in a
small realistic flow: optional data becomes displayable text, a model gains focused behavior, and
later values arrive through typed async contracts. The full capstone adds a runnable package and
test so you can verify that combined surface. Keep its boundary small; framework concerns belong
in the course that consumes this primer.

## Next step

Run the [Dart Availability CLI capstone](./capstone/overview.md), then begin Hybrid App Development
when the syntax reads naturally.
