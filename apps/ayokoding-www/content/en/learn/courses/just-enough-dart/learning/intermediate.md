---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 turn Dart's everyday modelling tools into Flutter-ready vocabulary: declarative
collections, type parameters, classes, constructors, mixins, and explicit error paths. Each block
is independent and runs with `dart run example.dart` unless marked otherwise.

## Declarative collections and generics

### Example 27: Add an Element Conditionally

_ex-27 · exercises co-14_

A collection `if` includes an element only when its condition holds.

```dart
void main() { // => starts a conditional collection
  const loggedIn = true; // => supplies the inclusion decision
  final actions = [if (loggedIn) 'Logout']; // => builds [Logout] when true
  print(actions); // => prints [Logout]
} // => finishes the literal construction
```

**Key takeaway:** Collection `if` keeps a small inclusion rule beside the literal it changes.

**Why it matters:** Flutter widget lists often contain an action, banner, or section only for one
state. Collection `if` keeps that decision declarative instead of mutating a list several lines
away. It is clearest for short branches; extract a named builder when the condition includes
validation, asynchronous state, or enough UI structure to hide the list's overall shape.

### Example 28: Build Elements with Collection `for`

_ex-28 · exercises co-14_

A collection `for` transforms each source item while constructing a literal.

```dart
void main() { // => starts a collection transformation
  final numbers = [1, 2, 3]; // => provides ordered source values
  final doubled = [for (final number in numbers) number * 2]; // => builds [2, 4, 6]
  print(doubled); // => prints the generated list
} // => ends the transformation
```

**Key takeaway:** Use collection `for` when a literal should visibly derive one element per input.

**Why it matters:** A Flutter `children` list commonly comes from domain records. This form keeps
the source, mapping, and resulting collection in one expression, making order easy to inspect.
When the mapping becomes a substantial widget or needs tests, move it into a named function so
the build method still communicates the screen's structure first.

### Example 29: Spread a Collection

_ex-29 · exercises co-14_

`...` inserts every element of one collection into another collection literal.

```dart
void main() { // => starts a list composition sample
  final middle = [1, 2]; // => supplies the elements to insert
  final values = [0, ...middle, 5]; // => creates [0, 1, 2, 5]
  print(values); // => prints the composed list
} // => completes the composition
```

**Key takeaway:** Spread keeps ordered collection composition readable without mutation.

**Why it matters:** Interfaces often combine fixed controls with data-driven controls. Spread says
that the elements retain their original order and become part of the surrounding list. It avoids
temporary mutable buffers whose update order is harder to trace. Use a normal expression rather
than a spread when the source must be filtered, validated, or transformed before inclusion.

### Example 30: Spread an Optional Collection

_ex-30 · exercises co-14_

`...?` inserts elements only when the collection itself is non-null.

```dart
void main() { // => begins optional list composition
  List<String>? extra; // => represents absent optional elements
  final menu = ['Home', ...?extra]; // => safely creates [Home]
  print(menu); // => prints [Home]
} // => completes without a null error
```

**Key takeaway:** Use `...?` when absent collection content should contribute no elements.

**Why it matters:** Optional server data should not force a widget list to branch manually just to
remain valid. A null-aware spread expresses the useful policy: no data means no extra elements.
Do not use it when absence requires an empty-state message or retry action; in that case the UI
needs an explicit branch because the product behavior is more than an omitted list item.

### Example 31: Constrain a Generic List

_ex-31 · exercises co-15_

An explicit `List<String>` restricts additions to strings; the rejected line stays commented.

```dart
void main() { // => starts a typed collection sample
  final names = <String>['Ada']; // => creates a List<String>
  // names.add(7); // => uncommenting fails static type checking
  print(names.single); // => prints Ada
} // => ends with a type-safe list
```

**Key takeaway:** Type arguments protect the contents of a reusable collection.

**Why it matters:** A list of models, IDs, or widgets should not silently accept an unrelated
value. Type arguments make the invariant visible at the allocation site and let completions and
the analyzer guide subsequent code. The compiler catches an incorrect append nearer to its cause
than a later renderer or mapper that assumes every list member has one shape.

### Example 32: Write a Generic Function

_ex-32 · exercises co-15_

A generic function can preserve the element type it receives and returns.

```dart
T first<T>(List<T> values) => values.first; // => returns the same element type T
void main() { // => calls the generic function twice
  print(first<int>([1, 2])); // => prints 1 as an int
  print(first<String>(['Ada', 'Lin'])); // => prints Ada as a String
} // => ends the generic demonstration
```

**Key takeaway:** Generic functions reuse an algorithm without erasing the caller's type information.

**Why it matters:** Flutter applications repeatedly transform typed collections: models, commands,
and widgets should keep their distinct contracts through helpers. A generic signature avoids one
copy per domain type and avoids `dynamic` casts later. Add a constraint only when the algorithm
needs an operation every possible type does not guarantee, such as ordering or a particular method.

### Example 33: Store a Generic Value

_ex-33 · exercises co-15_

A generic class gives one small container a statically known value type.

```dart
class Box<T> { // => declares a class parameterized by T
  Box(this.value); // => receives a value of that exact type
  final T value; // => stores the typed value immutably
} // => completes the generic class
void main() { // => constructs a concrete Box<int>
  print(Box<int>(7).value); // => prints 7
} // => finishes the program
```

**Key takeaway:** Put a type parameter on a class when its stored or returned values share one unknown type.

**Why it matters:** Generic models let a loading wrapper, result, or cache work for many domain
values without losing compiler knowledge. The concrete instantiation remains visible where data
enters the model. That is safer than storing `Object` and casting at every consumer, especially
when an asynchronous Flutter screen may handle several result types at once.

## Classes, constructors, and properties

### Example 34: Define Class Fields

_ex-34 · exercises co-16_

A class groups related state under one domain name.

```dart
class Point { // => starts a coordinate model
  Point(this.x, this.y); // => initializes both fields on construction
  final int x; // => stores horizontal position
  final int y; // => stores vertical position
} // => ends the model
void main() { // => creates a point value
  print(Point(2, 3).x); // => prints 2
} // => closes the example
```

**Key takeaway:** Group fields that describe one concept, then make their construction explicit.

**Why it matters:** A named model prevents a function from passing several unrelated primitive
values whose ordering callers must remember. Even small Flutter features benefit from a clear
domain shape for a coordinate, filter, or display item. Start with immutable fields; mutation
should represent a real changing identity rather than compensate for an unclear data flow.

### Example 35: Use a Positional Constructor

_ex-35 · exercises co-16_

A generative constructor creates a new instance and receives positional arguments in declaration order.

```dart
class Message { // => models one message value
  Message(this.text); // => assigns the required positional text
  final String text; // => exposes the immutable text
} // => finishes the class
void main() { // => creates an instance
  print(Message('ready').text); // => prints ready
} // => ends the program
```

**Key takeaway:** Positional constructors suit a short, obvious sequence of required inputs.

**Why it matters:** Concise construction is pleasant when one value fully identifies the object.
Once a class gains several values of the same type, positional calls become easy to swap. Flutter
uses named constructor parameters extensively for that reason. Let the call site determine the
choice: readability at every use matters more than saving punctuation in the class declaration.

### Example 36: Use Initializing Formals

_ex-36 · exercises co-16_

`this.field` in a constructor parameter writes the argument directly into that field.

```dart
class Size { // => models two dimensions
  const Size(this.width, this.height); // => initializes matching fields directly
  final int width; // => stores the width
  final int height; // => stores the height
} // => closes the value class
void main() { // => creates a Size
  print(Size(4, 2).height); // => prints 2
} // => finishes the sample
```

**Key takeaway:** Initializing formals remove boilerplate when parameter and field have the same role.

**Why it matters:** Dart constructors stay short without concealing what state an object owns.
That makes immutable configuration classes easy to scan in Flutter code. Use an initializer list
instead when a field needs conversion, validation, or a derived value; assigning directly is
valuable only while it accurately states that the argument is already the final field value.

### Example 37: Initialize a Final Field

_ex-37 · exercises co-16_

A `final` field must receive its value before construction completes, often through an initializing formal.

```dart
class Ticket { // => defines an immutable ticket model
  Ticket(this.id); // => assigns id during construction
  final String id; // => cannot be reassigned afterward
} // => ends the class
void main() { // => constructs a valid ticket
  print(Ticket('A-1').id); // => prints A-1
} // => completes the example
```

**Key takeaway:** Make required identity available at construction and keep it final by default.

**Why it matters:** A ticket ID, route argument, or configuration value should not become partially
initialized while a Flutter screen is already using it. `final` narrows the object's legal states
and avoids defensive checks elsewhere. If a value truly changes over an object's lifetime, make
that transition an explicit operation rather than leaving every consumer to infer mutation rules.

### Example 38: Name a Construction Path

_ex-38 · exercises co-17_

A named constructor gives a distinct construction intent a readable identifier.

```dart
class Point { // => models a coordinate
  const Point(this.x, this.y); // => provides the ordinary construction path
  const Point.origin() : x = 0, y = 0; // => names the zero-coordinate path
  final int x; // => stores horizontal position
  final int y; // => stores vertical position
} // => finishes the class
void main() { // => uses the named path
  print(Point.origin().x); // => prints 0
} // => ends the program
```

**Key takeaway:** Use a named constructor when construction has a meaningful domain interpretation.

**Why it matters:** `origin`, `empty`, `fromJson`, and similar names explain why a particular set
of values is valid. They reduce call-site comments and keep construction invariants near the class.
Flutter APIs use named constructors to make alternatives discoverable without overloading one
ambiguous positional signature, which makes editor completion a useful guide rather than a list
of indistinguishable parameter sequences.

### Example 39: Return an Instance from a Factory

_ex-39 · exercises co-18_

A `factory` constructor can choose which instance to return instead of always allocating a fresh one.

```dart
class Flag { // => defines a small canonicalized value
  Flag._(this.value); // => keeps direct construction private
  factory Flag.from(bool value) => Flag._(value); // => controls the public creation path
  final bool value; // => stores the normalized value
} // => closes the class
void main() { // => uses the factory
  print(Flag.from(true).value); // => prints true
} // => completes the sample
```

**Key takeaway:** Use a factory when callers should request a value, not assume a new allocation.

**Why it matters:** A factory can validate, normalize, select a subtype, or reuse an existing
object behind a stable public API. That flexibility is useful for parsing and framework-facing
models. Do not add a factory merely for ceremony: a normal constructor communicates the simpler
and more common promise that one call creates one new object with the supplied state.

### Example 40: Derive a Field in an Initializer List

_ex-40 · exercises co-19_

An initializer list computes final fields before the constructor body runs.

```dart
class Doubled { // => models a derived immutable value
  Doubled(int value) : result = value * 2; // => initializes result before the body
  final int result; // => stores the computed value
} // => closes the class
void main() { // => constructs the derived value
  print(Doubled(3).result); // => prints 6
} // => finishes the example
```

**Key takeaway:** Use an initializer list when a final field derives from a constructor argument.

**Why it matters:** Immutable objects should never be visible with a missing or temporarily wrong
derived value. Initializer lists make the relationship obvious and preserve the final-field rule.
They are especially useful for lightweight UI models whose display label, normalized ID, or
validated range must be ready before any widget can read the instance.

### Example 41: Expose a Getter

_ex-41 · exercises co-20_

A getter presents a computed property through field-like syntax.

```dart
class Rectangle { // => models dimensions
  Rectangle(this.width, this.height); // => initializes both inputs
  final double width; // => stores width
  final double height; // => stores height
  double get area => width * height; // => computes a fresh derived value
} // => completes the class
void main() { // => reads the computed property
  print(Rectangle(2, 3).area); // => prints 6.0
} // => ends the program
```

**Key takeaway:** A getter gives a derived value a simple, discoverable read surface.

**Why it matters:** Clients should ask a model for `area`, `isValid`, or `displayName` rather than
repeat its derivation. Centralizing the rule prevents slight variations from drifting across widgets.
Keep getters cheap and side-effect free because callers expect field-like access; work that loads,
mutates, or can fail deserves a method whose name reveals that larger operation.

### Example 42: Validate Through a Setter

_ex-42 · exercises co-20_

A setter can reject invalid writes while retaining a property-like client surface.

```dart
class Percent { // => models a bounded mutable value
  int _value = 0; // => stores the private backing value
  set value(int next) { // => receives proposed assignments
    if (next < 0 || next > 100) throw RangeError.range(next, 0, 100); // => rejects invalid input
    _value = next; // => records a valid value
  } // => closes validation logic
  int get value => _value; // => exposes the current valid value
} // => completes the model
void main() { // => performs a valid write
  final percent = Percent()..value = 50; // => assigns through the setter
  print(percent.value); // => prints 50
} // => ends the sample
```

**Key takeaway:** Use a setter when writes must preserve an invariant.

**Why it matters:** UI state should not accept impossible values simply because a field is public.
A narrow setter localizes the boundary and turns a bad assignment into a clear error close to its
cause. For larger state transitions, prefer an intent-revealing method such as `applyDiscount` or
`selectItem`; that name explains the business operation instead of exposing raw storage mutation.

### Example 43: Compute from Two Fields

_ex-43 · exercises co-20_

A getter can derive a formatted property from several stored fields without duplicating state.

```dart
class Person { // => models two parts of a name
  Person(this.first, this.last); // => initializes both source fields
  final String first; // => stores the first name
  final String last; // => stores the last name
  String get fullName => '$first $last'; // => derives display text on demand
} // => closes the class
void main() { // => reads the derived name
  print(Person('Ada', 'Lovelace').fullName); // => prints Ada Lovelace
} // => finishes the example
```

**Key takeaway:** Derive values when possible instead of storing two sources of truth.

**Why it matters:** Repeating a derived label in state introduces synchronization work whenever an
input changes. A computed property keeps the invariant structural: if first or last name changes,
the display value follows automatically. This keeps Flutter rendering simple and avoids subtle bugs
where one widget displays a cached field while another displays newly edited source data.

## Mixins, functions, and errors

### Example 44: Define a Mixin

_ex-44 · exercises co-21_

A mixin declares reusable behavior that a compatible class can incorporate.

```dart
mixin Logger { // => defines behavior without constructing an instance
  void log(String message) => print('log: $message'); // => provides one reusable method
} // => ends the mixin
class Service with Logger {} // => makes the behavior available on Service
void main() { // => invokes the mixed-in behavior
  Service().log('ready'); // => prints log: ready
} // => ends the program
```

**Key takeaway:** A mixin shares a small capability across classes without forcing one base class.

**Why it matters:** Flutter types may already extend a framework base class but still need a local
capability such as diagnostics or value formatting. A mixin can express that cross-cutting behavior
without inventing an artificial inheritance hierarchy. Keep a mixin focused and stateless when
possible; many unrelated responsibilities in one mixin create hidden dependencies at every use.

### Example 45: Apply a Mixin with `with`

_ex-45 · exercises co-21_

`with` adds the methods of a mixin to a class.

```dart
mixin Labelled { // => defines reusable label behavior
  String label() => 'ready'; // => provides a shared method
} // => completes the mixin
class Task with Labelled {} // => receives label as an instance method
void main() { // => constructs the receiving class
  print(Task().label()); // => prints ready
} // => completes the call
```

**Key takeaway:** Read `with` as “this class gains this focused behavior.”

**Why it matters:** Composition lets a class combine narrowly scoped abilities without a deep
inheritance tree. That is useful when platform classes already have a required superclass. Still,
prefer a regular collaborator when the behavior needs substantial configuration or dependencies;
an explicit field makes ownership and testing clearer than a mixin whose state appears indirectly
on every class that adopts it.

### Example 46: Restrict a Mixin's Host

_ex-46 · exercises co-21_

An `on` clause says which superclass API a mixin requires from its host.

```dart
class Base { // => supplies the capability required by the mixin
  String get name => 'base'; // => provides a readable name
} // => closes the base class
mixin NamedLog on Base { // => restricts hosts to Base subtypes
  void logName() => print(name); // => safely uses Base's API
} // => completes the constrained mixin
class Child extends Base with NamedLog {} // => satisfies the on constraint
void main() { // => uses the valid composition
  Child().logName(); // => prints base
} // => ends the example
```

**Key takeaway:** Use `on` when a mixin depends on a specific host contract.

**Why it matters:** A mixin that silently expects fields or methods from its host becomes fragile
when reused elsewhere. The `on` clause makes that dependency compile-checkable and tells readers
where `super` and shared members come from. It protects framework integrations where a capability
only makes sense for a particular state or rendering base type.

### Example 47: Pass a Function as an Argument

_ex-47 · exercises co-12_

Functions are values, so one function can receive another as a parameter.

```dart
int apply(int value, int Function(int) transform) { // => accepts behavior as typed input
  return transform(value); // => invokes the supplied function
} // => finishes the reusable workflow
void main() { // => supplies local behavior
  print(apply(4, (value) => value + 1)); // => prints 5
} // => ends the program
```

**Key takeaway:** A function parameter separates a stable workflow from a caller-selected variation.

**Why it matters:** Event handlers, validators, and item builders all use this shape in Flutter.
The receiving API owns when behavior runs; the caller owns what it does. A typed function signature
documents both sides and makes a focused fake easy in tests. Name a complex callback rather than
nesting logic at the call site where it obscures the surrounding configuration.

### Example 48: Map a Collection with a Function

_ex-48 · exercises co-12, co-13_

`map` applies a function to each item and returns an iterable of transformed results.

```dart
void main() { // => starts a functional collection transform
  final values = [1, 2, 3]; // => provides source integers
  final doubled = values.map((value) => value * 2); // => produces an Iterable<int>
  print(doubled.toList()); // => prints [2, 4, 6]
} // => completes the pipeline
```

**Key takeaway:** Use `map` to state a one-for-one transformation without a mutable accumulator.

**Why it matters:** Transforming models into labels or widgets is routine in Flutter. `map` makes
the one-output-per-input contract visible and keeps the source collection unchanged. Convert to a
list only when the receiving API needs list operations or stable materialization. A loop remains
better when the operation needs early exit, several effects, or an irregular number of outputs.

### Example 49: Iterate a List

_ex-49 · exercises co-13_

A `for-in` loop visits each list element in order.

```dart
void main() { // => begins ordered iteration
  final values = [1, 2, 3]; // => supplies three items in order
  for (final value in values) { // => binds each item once
    print(value); // => prints 1, then 2, then 3
  } // => closes the loop body
} // => ends the program
```

**Key takeaway:** Use `for-in` when each item needs an explicit sequential effect.

**Why it matters:** Iteration is clearer than a functional chain when code performs logging,
validation with an early decision, or an effect per item. The loop names the current value and
shows its order directly. Keep UI construction declarative when possible, but do not force every
operation through `map` when an ordinary loop better communicates the required control flow.

### Example 50: Iterate Map Entries

_ex-50 · exercises co-13_

`map.entries` exposes each key and value together for keyed iteration.

```dart
void main() { // => starts a map traversal
  final scores = {'ada': 10}; // => supplies one keyed value
  for (final entry in scores.entries) { // => visits a MapEntry<String, int>
    print('${entry.key}:${entry.value}'); // => prints ada:10
  } // => closes the traversal
} // => ends the example
```

**Key takeaway:** Iterate entries when an operation needs both a map key and its value.

**Why it matters:** A UI may render a settings label from a key alongside a value from the same
record. Iterating entries preserves that association and avoids a second lookup that could return
null or observe a changed map. When keys have domain meaning, prefer a typed model at the boundary
instead of letting arbitrary external strings determine presentation throughout a feature.

### Example 51: Catch a Thrown Error

_ex-51 · exercises co-26_

`try` surrounds risky code and `catch` receives an error when that code throws.

```dart
void main() { // => starts an error-handling example
  try { // => begins the operation that may fail
    throw FormatException('bad input'); // => raises a concrete error
  } catch (error) { // => receives the thrown value
    print(error); // => prints FormatException: bad input
  } // => completes the handled path
} // => ends the program
```

**Key takeaway:** Catch an error only where code can choose a useful recovery or user-facing result.

**Why it matters:** Swallowing an exception makes a failing feature appear successful while losing
the reason it failed. A local catch can map malformed input to validation feedback or enrich an
error with domain context. Let errors propagate when the current layer cannot decide what recovery
means; a higher boundary often owns logging, retry, or visible error state.

### Example 52: Throw an Exception

_ex-52 · exercises co-26_

`throw` stops normal execution and reports an error to the nearest matching handler.

```dart
void requirePositive(int value) { // => declares a value-validation boundary
  if (value <= 0) throw ArgumentError.value(value, 'value'); // => rejects an invalid input
} // => closes the validation function
void main() { // => demonstrates a valid input
  requirePositive(1); // => returns normally because 1 is positive
  print('valid'); // => prints valid
} // => ends without an error
```

**Key takeaway:** Throw when an operation cannot honor its contract with the supplied input or state.

**Why it matters:** An exception should carry a violated invariant, not control ordinary branching.
For expected absence, return a nullable value or a domain result that callers can handle normally.
When invalid input truly crosses a boundary, throwing early gives the caller and test a precise
failure point instead of allowing corrupt state to travel into rendering or asynchronous work.

### Example 53: Define a Custom Exception

_ex-53 · exercises co-26_

A domain-specific exception can implement `Exception` and carry an explanatory message.

```dart
class ValidationException implements Exception { // => names a domain failure type
  ValidationException(this.message); // => captures failure context
  final String message; // => exposes the diagnostic text
  @override String toString() => 'ValidationException: $message'; // => formats the error
} // => completes the exception class
void main() { // => throws and catches the precise type
  try { throw ValidationException('email required'); } catch (error) { print(error); } // => prints the custom error
} // => ends the handled path
```

**Key takeaway:** Use a custom exception when callers need to distinguish one domain failure from another.

**Why it matters:** A generic error message forces every boundary to parse text before deciding how
to recover. A named exception lets a form, repository, or application shell choose an appropriate
response based on type and attached context. Keep the hierarchy small: expected validation results
often fit ordinary return values better than exceptions that every caller must catch.

### Example 54: Clean Up with `finally`

_ex-54 · exercises co-26_

`finally` runs whether the `try` body completes or throws.

```dart
void main() { // => begins guaranteed cleanup
  try { // => starts work that could throw
    print('work'); // => prints the normal work marker
  } finally { // => runs after success or failure
    print('cleanup'); // => prints cleanup unconditionally
  } // => ends the cleanup boundary
} // => completes the program
```

**Key takeaway:** Put release or closing work in `finally` when it must happen on every path.

**Why it matters:** Streams, controllers, files, and subscriptions can require cleanup even when an
operation fails. `finally` makes that ownership visible instead of relying on one happy-path return
to remember it. Keep the cleanup itself reliable and small; if it can fail independently, decide
which error should remain visible rather than accidentally replacing the original failure.
