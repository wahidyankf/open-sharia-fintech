---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish the Dart command loop, the type system, null safety, functions, and
collection literals. Each Dart block runs with `dart run example.dart` unless its text explicitly
asks you to uncomment a compiler-rejection or runtime-trap line.

## Dart CLI and values

### Example 1: Create a Console Project

_ex-01 · exercises co-01_

`dart create hello` scaffolds a package with a runnable `bin/hello.dart`. The program below is the
smallest useful shape that the generated entry point has.

```dart
void main() { // => Dart starts a console program here
  print('Hello, Dart'); // => prints a visible success signal
} // => closes the entry function
```

**Key takeaway:** Use `dart create hello`, then `dart run` from that package to establish a known-good toolchain.

**Why it matters:** Flutter projects add platform folders and generated configuration, but the Dart
code still runs from ordinary entry points. Starting with a console package separates a missing SDK
or broken terminal setup from framework concerns. That distinction makes the first Flutter errors
smaller and gives you a repeatable place to try language ideas.

### Example 2: Run a Dart File

_ex-02 · exercises co-01_

`dart run example.dart` executes a standalone file without creating a package first. Keep the
result observable while you learn a construct.

```dart
void main() { // => provides the file's entry point
  print(2 + 3); // => prints the evaluated integer: 5
} // => finishes after the print call
```

**Key takeaway:** `dart run` gives a small feedback loop for normal Dart files.

**Why it matters:** A short executable example makes a language rule concrete before it becomes
part of a widget tree. You can change one expression, rerun it, and distinguish a compile-time
diagnostic from a value-level surprise. That habit transfers directly to focused tests in an
application rather than guessing what state a UI should contain.

### Example 3: Run a Test Package

_ex-03 · exercises co-01_

`dart test` runs tests declared by a Dart package after `dart pub get`. This tiny program models
the assertion a test checks; the capstone supplies the materialized test file.

```dart
void main() { // => starts a deterministic behavior sample
  final passed = 2 + 2 == 4; // => evaluates the assertion condition
  print(passed); // => prints true, the expected test outcome
} // => ends the sample program
```

**Key takeaway:** Use `dart test` to make expected behavior executable instead of relying on a manual print.

**Why it matters:** Flutter code changes quickly because UI, asynchronous data, and state interact.
Tests preserve a small contract while you refactor those moving parts. Learning the command before
the framework means a later test failure reads as a useful statement about behavior, not another
new tool to decode during a feature change.

### Example 4: Resolve Package Metadata

_ex-04 · exercises co-02_

A package records its identity and SDK requirement in `pubspec.yaml`; `dart pub get` resolves the
declared dependencies and writes `pubspec.lock`. This source remains dependency-free.

```dart
void main() { // => represents code inside a package resolved by pub
  const packageName = 'dart_primer'; // => corresponds to package metadata
  print('running $packageName'); // => proves the resolved package can run
} // => exits without third-party runtime dependencies
```

**Key takeaway:** Declare package intent in `pubspec.yaml`, then run `dart pub get` before package commands.

**Why it matters:** Dependency resolution is a build input, not an incidental editor action. The
lockfile records the concrete resolution that a teammate or CI can reproduce. In Flutter, that
discipline prevents a device-only failure caused by an unresolved package from being mistaken for
a rendering or platform problem.

### Example 5: Infer a Type with `var`

_ex-05 · exercises co-03_

`var` asks Dart to infer a static type from an initializer. It does not make the binding dynamically typed.

```dart
void main() { // => begins a standalone program
  var retries = 3; // => infers an int from the integer literal
  print(retries + 1); // => prints 4 using int arithmetic
} // => closes the entry point
```

**Key takeaway:** Use `var` when the initializer makes the static type obvious.

**Why it matters:** Flutter code often has local values with obvious types, such as a count or a
widget list. Inference removes repeated type names while retaining compiler checking. Add an
annotation at an API boundary or whenever it communicates a guarantee that a future reader should
not have to reconstruct from an expression.

### Example 6: Choose `final` or `const`

_ex-06 · exercises co-03_

`final` permits one runtime assignment, while `const` requires a compile-time constant value. Both
prevent later reassignment of the name.

```dart
void main() { // => starts the comparison
  final greeting = DateTime.now().year; // => final accepts a runtime value once
  const limit = 3; // => const embeds a compile-time constant
  print('$greeting:$limit'); // => prints the two fixed bindings
} // => completes the comparison
```

**Key takeaway:** Prefer `final`; use `const` when the value is known at compile time.

**Why it matters:** Immutable bindings narrow the number of places where a value can change. In
Flutter, `const` can also describe immutable widget configuration, while `final` captures values
computed for one build or request. Making the distinction intentional prevents a reader from
assuming every immutable-looking value has the same allocation or evaluation behavior.

### Example 7: Opt Out with `dynamic`

_ex-07 · exercises co-03_

`dynamic` defers member and assignment checks until runtime. Use it only at an untyped boundary
that you immediately validate.

```dart
void main() { // => starts an intentionally dynamic sample
  dynamic value = 42; // => permits an int without fixing a static type
  value = 'forty-two'; // => later accepts a String as well
  print(value); // => prints forty-two
} // => closes the program
```

**Key takeaway:** `dynamic` trades compiler help for flexibility, so keep it at a narrow boundary.

**Why it matters:** JSON and plugin APIs can arrive without a useful static type. Letting that
uncertainty leak through an application postpones failures until a user takes an unlucky path.
Decode or validate the value at the edge, then return a concrete Dart type so the rest of the
Flutter feature can rely on the analyzer again.

### Example 8: Use Numeric Types Deliberately

_ex-08 · exercises co-04_

`int` and `double` are numeric types; `num` can hold either when a calculation genuinely needs both.

```dart
void main() { // => begins numeric work
  num total = 2 + 0.5; // => stores the double result under the num supertype
  print(total * 2); // => prints 5.0 after numeric multiplication
} // => ends the calculation
```

**Key takeaway:** Use `num` only when both integer and floating-point values are part of the contract.

**Why it matters:** Counts, prices, pixels, and ratios do not share the same rounding expectations.
A concrete type communicates whether fractional values are meaningful. Flutter layout and animation
code often uses `double`, while item counts are naturally `int`; preserving that distinction makes
accidental conversions and precision assumptions visible during review.

### Example 9: Keep Conditions Boolean

_ex-09 · exercises co-04_

Dart has `String` and `bool` values, but it has no truthy or falsy conversion. A condition must
evaluate to a `bool`.

```dart
void main() { // => starts a text and boolean sample
  const name = 'Ada'; // => creates a String value
  const enabled = true; // => creates the only valid condition type
  print(enabled ? 'Hi $name' : 'Disabled'); // => prints Hi Ada
} // => finishes the conditional output
```

**Key takeaway:** Write an explicit boolean condition instead of relying on a value's truthiness.

**Why it matters:** Explicit conditions make UI decisions readable: a button is enabled because
`isValid`, not because a string happens to be non-empty. That clarity protects refactors when a
value changes type or an empty value becomes meaningful. It also keeps the decision rule close to
the branch instead of hiding it in an implicit conversion.

### Example 10: Interpolate Text

_ex-10 · exercises co-05_

Use `$name` for one identifier and `${expression}` when text embeds a calculation or member path.

```dart
void main() { // => begins a text example
  const name = 'Ada'; // => supplies a simple interpolation value
  const age = 20; // => supplies a computed interpolation value
  print('Hi $name, next year: ${age + 1}'); // => prints Hi Ada, next year: 21
} // => closes the example
```

**Key takeaway:** Interpolation keeps dynamic text and its values together without noisy concatenation.

**Why it matters:** Status strings, accessibility labels, and diagnostics are small but important
parts of a Flutter application. Interpolation makes the changing portion visible and reduces
separator mistakes. Keep business formatting in a dedicated function once it grows beyond one
expression so UI code does not become the hidden owner of presentation policy.

## Null safety and functions

### Example 11: See Non-nullability by Default

_ex-11 · exercises co-06_

An `int` cannot hold `null`; the analyzer rejects the commented assignment. Dart asks you to model
absence instead of discovering it through a null dereference.

```dart
void main() { // => starts a non-nullable sample
  int count = 1; // => count must always contain an int
  // count = null; // => uncommenting causes a compile-time error
  print(count); // => prints the guaranteed integer: 1
} // => ends with a safe value
```

**Key takeaway:** Plain `T` means a value is required; make absence explicit with `T?`.

**Why it matters:** UI code regularly receives optional network fields and delayed user input.
Sound null safety turns an ambiguous runtime crash into a design choice the analyzer can point to.
When every nullable boundary is visible in a type, reviewers can ask where the application should
display a fallback, request another value, or stop the current operation.

### Example 12: Declare a Nullable Type

_ex-12 · exercises co-06_

Appending `?` allows a type to hold either a normal value or `null`. The value still needs a safe
access strategy before code treats it as present.

```dart
void main() { // => begins a nullable-value example
  int? selectedId; // => null records that no ID has been selected
  print(selectedId); // => prints null without an unsafe dereference
} // => finishes with legal absence
```

**Key takeaway:** Use `T?` for meaningful absence, then handle that absence near its owner.

**Why it matters:** A selected row, authenticated user, or fetched result can be absent for a
legitimate reason. Recording that state in the type keeps it distinct from a magic ID or an empty
string. Later Flutter widgets can render an intentional empty state instead of treating a missing
value as an exceptional failure.

### Example 13: Delay Initialization with `late`

_ex-13 · exercises co-07_

`late` promises that a non-nullable variable will receive a value before its first read. The check
happens at runtime, so use it when ordinary constructor initialization cannot express the lifecycle.

```dart
class Session { // => models state initialized after construction
  late String token; // => defers the non-null initialization check
} // => closes the class definition
void main() { // => runs the lifecycle sample
  final session = Session(); // => creates a session with no token read yet
  session.token = 'ready'; // => initializes before the first read
  print(session.token); // => prints ready
} // => completes safely
```

**Key takeaway:** Prefer constructor parameters; reserve `late` for a real deferred lifecycle.

**Why it matters:** Flutter state sometimes depends on setup that occurs after an object exists,
such as a controller configured in an initialization hook. `late` makes that obligation explicit
but cannot prove the ordering. Favor constructor injection where possible, because a value that is
ready at construction avoids a later runtime failure on an unexpected path.

### Example 14: Access a Nullable Receiver Safely

_ex-14 · exercises co-08_

`?.` stops a member access when its receiver is `null` and returns `null` for the whole expression.

```dart
class User { // => supplies a nullable receiver type
  const User(this.name); // => stores a required display name
  final String name; // => exposes the non-null name
} // => completes the model
void main() { // => starts the safe access
  User? user; // => represents an absent user
  print(user?.name); // => prints null without reading name on null
} // => finishes safely
```

**Key takeaway:** Use `?.` when absence should flow through a member-access path.

**Why it matters:** Optional data frequently appears several properties away from the UI that
consumes it. A safe access documents that no value is an expected branch, not an accident. Add a
fallback or an early return where product behavior needs one; `?.` alone preserves absence rather
than deciding what the user should see.

### Example 15: Supply a Fallback with `??`

_ex-15 · exercises co-08_

`??` returns its left value when it is non-null and otherwise evaluates a fallback.

```dart
void main() { // => starts an absence-to-default mapping
  String? name; // => represents no supplied name
  final label = name ?? 'Guest'; // => chooses Guest only for null
  print(label); // => prints Guest
} // => completes the fallback decision
```

**Key takeaway:** Put a default beside the nullable value when the default expresses local policy.

**Why it matters:** A fallback is a product decision, not merely syntax. A profile might display
`Guest`, while a payment amount should stop the action instead. `??` makes the chosen policy
obvious at the conversion point and preserves sound types afterward, which keeps the rest of a
Flutter widget free from repeated nullable branches.

### Example 16: Assign Only When Null

_ex-16 · exercises co-08_

`??=` evaluates and assigns its right side only when the target currently holds `null`.

```dart
String compute() => 'cached'; // => represents a value that may be expensive to create
void main() { // => starts a lazy assignment sample
  String? value; // => begins without a cached value
  value ??= compute(); // => assigns cached because value is null
  print(value); // => prints cached
} // => ends after one initialization
```

**Key takeaway:** Use `??=` for a nullable cache or default that should initialize once.

**Why it matters:** A value that is optional before first use is different from one that should
recompute every time. `??=` documents that lifecycle in one expression. Keep side effects small
and visible in the right side: if initialization can fail, needs loading state, or crosses an async
boundary, model that process explicitly rather than disguising it as a cache assignment.

### Example 17: Treat `!` as a Checked Risk

_ex-17 · exercises co-08_

`!` asserts that a nullable expression is non-null. The assertion throws at runtime when wrong, so
the failing line remains commented here.

```dart
void main() { // => starts a deliberately risky sample
  String? value; // => value is null
  // print(value!); // => uncommenting throws because the assertion is false
  print(value ?? 'use a fallback'); // => prints the safe alternative
} // => completes without a trap
```

**Key takeaway:** Prefer a guard, safe access, or fallback; use `!` only after a proven invariant.

**Why it matters:** A force assertion converts a compiler-guided branch into a crash that may only
appear on a rare user path. Framework APIs can occasionally establish a real invariant, but most
application input cannot. Writing the check where the data enters the feature documents why it is
safe and gives a future change one clear place to revisit the assumption.

### Example 18: Declare a Function

_ex-18 · exercises co-09_

A named function declares input and output types, then returns a value with `return`.

```dart
int add(int left, int right) { // => accepts two required integer inputs
  return left + right; // => returns their calculated sum
} // => closes the reusable function
void main() { // => calls the function
  print(add(2, 3)); // => prints 5
} // => ends the program
```

**Key takeaway:** Give reusable behavior a name and a type-level contract.

**Why it matters:** Small named functions prevent a widget's build method from accumulating
calculation details. Inputs and results become testable without constructing a UI, and callers can
learn the intended types from the signature. This is the first seam for later validation, mapping,
or asynchronous work when a feature grows beyond a local expression.

### Example 19: Use an Arrow Function

_ex-19 · exercises co-09_

An arrow body is shorthand for a single returned expression.

```dart
int square(int value) => value * value; // => returns one expression without braces
void main() { // => starts the call site
  print(square(4)); // => prints 16
} // => finishes the concise program
```

**Key takeaway:** Use `=>` when one expression fully explains a function's result.

**Why it matters:** Dart UI code often needs a small formatter, predicate, or mapper. An arrow
function keeps that simple rule visible without ceremony. Switch to a block body when logging,
validation, multiple decisions, or a local name would clarify the work; compression should never
hide a meaningful branch from the next reader.

### Example 20: Pass a Named Parameter

_ex-20 · exercises co-10_

Named parameters use braces in a declaration and labels at the call site. They are optional unless
the declaration marks them `required`.

```dart
void greet({String? name}) { // => accepts an optional named value
  print('Hi ${name ?? 'Guest'}'); // => handles absence locally
} // => closes the function
void main() { // => demonstrates the named call syntax
  greet(name: 'Ada'); // => prints Hi Ada
} // => completes the example
```

**Key takeaway:** Use named parameters when an argument's role benefits from a visible label.

**Why it matters:** Constructors and widget APIs frequently have several values of the same type.
Names prevent accidental argument swaps and make a call read like configuration. Optional named
parameters also let an API grow without forcing every caller to pass placeholders, as long as the
default behavior remains coherent and clearly documented.

### Example 21: Require a Named Parameter

_ex-21 · exercises co-10_

`required` keeps the readability of a named call while preventing omission.

```dart
void showId({required int id}) { // => declares a mandatory named input
  print('id: $id'); // => uses the guaranteed value
} // => finishes the function
void main() { // => provides the required label
  showId(id: 7); // => prints id: 7
} // => ends with a valid call
```

**Key takeaway:** Mark a named parameter `required` when no sensible default exists.

**Why it matters:** Required named inputs make important configuration hard to forget while keeping
the call self-documenting. Flutter constructors use this pattern for values such as a child or a
callback. It produces a compiler error at the caller rather than a delayed failure inside a widget
whose essential input was silently omitted.

### Example 22: Default an Optional Positional Parameter

_ex-22 · exercises co-11_

Square brackets declare optional positional parameters. A default keeps ordinary calls short.

```dart
String say(String text, [String end = '!']) { // => makes the second position optional
  return '$text$end'; // => combines text with its chosen ending
} // => closes the formatter
void main() { // => uses the default argument
  print(say('Ready')); // => prints Ready!
} // => completes the program
```

**Key takeaway:** Use optional positional parameters only when the order remains obvious without a label.

**Why it matters:** A compact positional option fits a familiar modifier such as a separator or
suffix. Once a function has multiple booleans, strings, or domain values, named parameters make
calls safer to scan. Choosing the clearer form early matters in Flutter code, where constructor
calls can already contain many visual configuration values.

### Example 23: Capture Local State in a Closure

_ex-23 · exercises co-12_

A closure can read variables from its surrounding scope, including their current value.

```dart
void main() { // => starts the closure's surrounding scope
  var prefix = 'first'; // => creates mutable captured state
  String label() => prefix; // => closure reads prefix when invoked
  prefix = 'updated'; // => changes the captured value before the call
  print(label()); // => prints updated
} // => ends with the captured result
```

**Key takeaway:** Closures retain access to their lexical scope, so capture mutable state deliberately.

**Why it matters:** Callbacks in Flutter commonly capture values from a build or event handler.
That convenience can become surprising when the captured object later changes or outlives the
screen that created it. Prefer capturing stable values and pass explicit parameters when behavior
needs to remain understandable independently of the surrounding mutable scope.

### Example 24: Create a List Literal

_ex-24 · exercises co-13_

A list literal preserves order and Dart infers its element type from the items.

```dart
void main() { // => begins an ordered collection example
  final steps = [1, 2, 3]; // => infers a List<int> in insertion order
  print(steps.length); // => prints 3
} // => closes the list example
```

**Key takeaway:** Use `List<T>` when order and duplicate elements matter.

**Why it matters:** Widget children, navigation items, and loaded records commonly have a visible
order. A list expresses that contract directly and works naturally with collection-for and mapping
patterns later in this primer. Add an explicit `List<T>` annotation when an empty literal or API
boundary would otherwise make the intended element type unclear.

### Example 25: Create a Map Literal

_ex-25 · exercises co-13_

A map associates unique keys with values and looks them up by key.

```dart
void main() { // => starts a keyed collection example
  final scores = {'ada': 10}; // => infers a Map<String, int>
  print(scores['ada']); // => prints the value stored under ada
} // => completes the lookup
```

**Key takeaway:** Use `Map<K, V>` when a key is the natural way to find a value.

**Why it matters:** Application state often needs efficient lookup by an ID, route name, or field
key. A map's lookup can return `null`, so its result naturally connects to Dart's null-safe
operators. Keep map keys within one domain and convert untrusted string input at the boundary;
otherwise every lookup must also compensate for an unclear key contract.

### Example 26: Create a Set Literal

_ex-26 · exercises co-13_

A set holds unique elements; repeated literals collapse to one member.

```dart
void main() { // => begins a uniqueness example
  final tags = {1, 1, 2}; // => infers a Set<int> and removes the duplicate 1
  print(tags.length); // => prints 2
} // => finishes the set sample
```

**Key takeaway:** Use `Set<T>` when membership and uniqueness matter more than indexed order.

**Why it matters:** Selected IDs, enabled features, and permissions should not gain a duplicate
just because two inputs describe the same thing. A set encodes that rule in the data structure
instead of relying on every caller to check first. Use a list when display order is the requirement;
the two collections communicate different promises to readers.
