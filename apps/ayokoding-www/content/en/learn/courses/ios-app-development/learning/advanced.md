---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 apply actor and main-actor isolation, structured concurrency and cancellation,
SwiftData, unit/UI test layers, cache-first data, and the complete application slice. Use a current
iOS 17-or-later Xcode target and replace fixture values with a test server only at the integration
boundary.

### Example 55: Define an Actor

_ex-55 · exercises co-23_

An actor owns mutable state that concurrent callers must access through isolation.

```swift
actor NoteCache { // => Declares an isolated reference type.
  private var values: [String: String] = [:] // => Keeps mutable cache state inside the actor.
  func count() -> Int { values.count } // => Provides serialized access to the state.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Put shared mutable state behind an actor before multiple tasks can touch it.

### Example 56: Store Data in an Actor Cache

_ex-56 · exercises co-23_

Give the cache named read and write operations.

```swift
actor NoteCache { // => Isolates the dictionary from external mutation.
  private var values: [String: String] = [:] // => Stores entries only inside the actor.
  func put(_ value: String, for key: String) { values[key] = value } // => Serializes a write.
  func get(_ key: String) -> String? { values[key] } // => Serializes a read.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: The actor, not its callers, owns the mutation policy for cache data.

### Example 57: Await Cross-Actor Access

_ex-57 · exercises co-23_

Crossing an actor boundary requires `await`.

```swift
actor NoteCache { // => Owns mutable cache values in this complete example.
  private var values: [String: String] = [:] // => Keeps the dictionary isolated.
  func put(_ value: String, for key: String) { values[key] = value } // => Serializes a write.
  func get(_ key: String) -> String? { values[key] } // => Serializes a read.
}
let cache = NoteCache() // => Creates the actor instance.
Task { // => Starts an asynchronous context.
  await cache.put("Plan", for: "1") // => Awaits isolated mutation.
  let title = await cache.get("1") // => Awaits isolated read.
  print(title ?? "Missing") // => Prints Plan after both operations complete.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `await` makes an isolation boundary visible at the call site.

### Example 58: Main-Actor-Isolate a View Model

_ex-58 · exercises co-24_

Keep UI-facing state on the main actor.

```swift
import Observation // => Supplies Observable.

@Observable @MainActor final class NotesViewModel { // => Restricts mutable UI state to the main actor.
  var title = "Focus List" // => Is safe for SwiftUI to observe.
  func rename(_ value: String) { title = value } // => Mutates under main-actor isolation.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Main-actor annotation communicates and enforces the UI-state ownership boundary.

### Example 59: Return to the Main Actor for UI State

_ex-59 · exercises co-24_

Perform a background-friendly operation, then update the UI model on its actor.

```swift
import Foundation // => Supplies Task and URL-related concurrency support.

@MainActor final class StatusModel { // => Owns UI-visible status.
  var status = "Waiting" // => Starts in a rendered state.
  func load() async { let value = await Task.detached { "Loaded" }.value; status = value } // => Resumes model mutation on MainActor.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Do not evade isolation; return to the UI owner before changing UI state.

### Example 60: Run Independent Work with `async let`

_ex-60 · exercises co-25_

Start independent child operations concurrently and await both results.

```swift
func label(_ value: String) async -> String { value } // => Defines a suspending child operation.
func loadLabels() async -> [String] { // => Owns the structured child tasks.
  async let first = label("Plan") // => Starts the first child concurrently.
  async let second = label("Review") // => Starts the second child concurrently.
  return await [first, second] // => Joins both children before returning.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `async let` suits a known, small set of independent child operations.

### Example 61: Aggregate a Task Group

_ex-61 · exercises co-25_

Use a task group when the number of child tasks comes from data.

```swift
func squareAll(_ values: [Int]) async -> [Int] { // => Owns dynamic child work.
  await withTaskGroup(of: Int.self, returning: [Int].self) { group in // => Collects integer results.
    for value in values { group.addTask { value * value } } // => Adds one child per input.
    return await group.reduce(into: []) { $0.append($1) } // => Waits for every child result.
  }
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A task group scopes a variable number of children to one parent lifetime.

### Example 62: Cooperate with Cancellation

_ex-62 · exercises co-25_

Check cancellation inside work that may outlive its usefulness.

```swift
enum WorkError: Error { case cancelled } // => Names the cancellation outcome for this example.
func validateWork() throws { // => Represents a cancellable synchronous checkpoint.
  if Task.isCancelled { throw WorkError.cancelled } // => Stops before doing unnecessary work.
  // => Continue only when the parent task still needs the result.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Cancellation is cooperative; code must reach a suspension point or check it.

### Example 63: Tie Loading to View Lifetime

_ex-63 · exercises co-25, co-22_

Use `.task` so SwiftUI cancels view-related work when the view disappears.

```swift
import SwiftUI // => Supplies the task modifier.

struct CancellableLoad: View { // => Defines a screen-scoped operation.
  @State private var status = "Waiting" // => Owns the visible state.
  var body: some View { Text(status).task { do { try await Task.sleep(for: .seconds(1)); try Task.checkCancellation(); status = "Loaded" } catch is CancellationError { } catch { status = "Failed" } } } // => SwiftUI cancels this task when the view disappears; cancellation is checked before mutation.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: View lifetime is a useful owner for view-specific work, not for durable syncing.

### Example 64: Model a SwiftData Entity

_ex-64 · exercises co-26_

Use `@Model` for a persistable app object.

```swift
import SwiftData // => Supplies the Model macro.

@Model final class StoredNote { // => Marks this class for SwiftData persistence.
  var title: String // => Persists the note title.
  init(title: String) { self.title = title } // => Creates a stored model instance.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: SwiftData models represent durable local data, not transient view state.

### Example 65: Insert and Query SwiftData

_ex-65 · exercises co-26_

Insert through a context and render a query result.

```swift
import SwiftData // => Supplies ModelContext and Query.
import SwiftUI // => Supplies View and List.

@Model final class StoredNote { var title: String; init(title: String) { self.title = title } } // => Defines the persisted row shape.
struct StoredNotesView: View { @Environment(\.modelContext) private var context; @Query private var notes: [StoredNote]; var body: some View { List(notes) { Text($0.title) }.toolbar { Button("Add") { context.insert(StoredNote(title: "Plan")) } } } // => Inserts and observes stored rows.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Keep context mutation at a named action and let queries drive rendering.

### Example 66: Verify a Persistence Round Trip

_ex-66 · exercises co-26_

Use a model container to save and fetch a local value.

```swift
import SwiftData // => Supplies in-memory model storage for a deterministic example.

@Model final class StoredNote { var title: String; init(title: String) { self.title = title } } // => Defines the stored type for this round trip.
let container = try ModelContainer(for: StoredNote.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true)) // => Creates isolated storage.
let context = ModelContext(container) // => Opens a context for reads and writes.
context.insert(StoredNote(title: "Plan")); try context.save() // => Writes the model transaction.
let notes = try context.fetch(FetchDescriptor<StoredNote>()) // => Fetches the stored value back.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A round trip proves the persistence contract separately from a screen relaunch test.

### Example 67: Write an XCTest Unit Test

_ex-67 · exercises co-29_

Test a pure mapping with XCTest.

```swift
import XCTest // => Supplies XCTestCase and assertions.

final class TitleTests: XCTestCase { // => Groups unit tests.
  func testCapitalizesTitle() { XCTAssertEqual("focus".capitalized, "Focus") } // => Proves one deterministic rule.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Start with the smallest test layer that proves the behavior you care about.

### Example 68: Write a Swift Testing Expectation

_ex-68 · exercises co-29_

Use the newer Swift Testing framework for a focused expectation.

```swift
import Testing // => Supplies Test and expect macros.

@Test func titleCapitalizes() { // => Declares a test without a test-case class.
  #expect("focus".capitalized == "Focus") // => Fails when the observed result differs.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: XCTest and Swift Testing both support unit-level claims; use the project's chosen
test style consistently.

### Example 69: Test a View-Model Transition

_ex-69 · exercises co-29, co-18_

Inject a fake and assert the model's observable state.

```swift
import XCTest // => Supplies asynchronous test assertions.
import Observation // => Supplies Observable for the test model.

protocol NoteService { func fetch() async throws -> [String] } // => Defines the model dependency.
struct FakeNoteService: NoteService { func fetch() async throws -> [String] { ["Plan"] } } // => Avoids live I/O in a unit test.
@Observable @MainActor final class NotesViewModel { let service: any NoteService; var notes = [String](); init(service: any NoteService) { self.service = service }; func load() async throws { notes = try await service.fetch() } } // => Owns a testable transition.
@MainActor final class ViewModelTests: XCTestCase { // => Runs UI-model setup on its actor.
  func testLoadsFakeNotes() async throws { let model = NotesViewModel(service: FakeNoteService()); try await model.load(); XCTAssertEqual(model.notes, ["Plan"]) } // => Asserts loading-to-content.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A fake service keeps view-model tests deterministic and independent of the network.

### Example 70: Await in a Unit Test

_ex-70 · exercises co-29, co-22_

Mark a test `async` when the behavior suspends.

```swift
import XCTest // => Supplies XCTestCase.

final class AsyncTests: XCTestCase { // => Groups asynchronous unit tests.
  func testAsyncValue() async { let value = await Task { "Loaded" }.value; XCTAssertEqual(value, "Loaded") } // => Awaits before asserting.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Await the operation under test; do not race an assertion against unfinished work.

### Example 71: Launch an XCUITest

_ex-71 · exercises co-30_

Launch the app and verify an accessible element exists.

```swift
import XCTest // => Supplies XCUIApplication and UI assertions.

final class FocusListUITests: XCTestCase { // => Runs against the installed app.
  func testLaunchShowsTitle() { let app = XCUIApplication(); app.launch(); XCTAssertTrue(app.staticTexts["Focus List"].exists) } // => Checks visible launch behavior.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: UI tests assert what a reader can actually find and use in a running app.

### Example 72: Test a UI Interaction

_ex-72 · exercises co-30_

Tap a semantic control and assert the destination.

```swift
import XCTest // => Supplies UI automation APIs.

final class NavigationUITests: XCTestCase { // => Defines an interaction test.
  func testOpensDetail() { let app = XCUIApplication(); app.launch(); app.buttons["Plan"].tap(); XCTAssertTrue(app.staticTexts["Plan detail"].exists) } // => Proves list-to-detail flow.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Accessibility labels and visible names make UI tests resilient and useful.

### Example 73: Run Tests from the Command Line

_ex-73 · exercises co-30_

Use `xcodebuild` so local and CI test entry points match.

```bash
xcodebuild test \                          # => Builds and runs the selected scheme's tests.
  -scheme FocusList \                       # => Selects the app and its test targets.
  -destination 'platform=iOS Simulator,name=iPhone 16' # => Selects an installed simulator destination.
# => End of this self-contained example.
# => Read the inline annotations before changing a value.
```

**Key takeaway**: Keep the test command reproducible; substitute a simulator name that exists locally.

### Example 74: Read Cache Before Network

_ex-74 · exercises co-23, co-21_

Make cache-first behavior a repository decision.

```swift
import Foundation // => Supplies URLSession and JSONDecoder.
actor TitleCache { var value: String?; func get() -> String? { value }; func put(_ title: String) { value = title } } // => Owns cache mutation.
struct TitleResponse: Decodable { let title: String } // => Defines the remote JSON boundary.
struct TitleRepository { let cache: TitleCache; let session: URLSession; func title(from url: URL) async throws -> String { if let cached = await cache.get() { return cached }; let (data, response) = try await session.data(from: url); guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }; let fresh = try JSONDecoder().decode(TitleResponse.self, from: data).title; await cache.put(fresh); return fresh } } // => Decodes URLSession data only after a cache miss.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: The repository chooses the source; the view model receives one application-facing
result.

### Example 75: Render Purely from Observable State

_ex-75 · exercises co-07, co-03_

Let a screen derive all visible content from one observable model.

```swift
import Observation // => Supplies Observable.
import SwiftUI // => Supplies View.

@Observable final class CountModel { var count = 0 } // => Owns the source state.
struct CountScreen: View { @State private var model = CountModel(); var body: some View { VStack { Text("\(model.count)"); Button("Add") { model.count += 1 } } } // => Needs no manual refresh.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: When state is authoritative, UI refresh follows the data dependency automatically.

### Example 76: Pass Selected State through Navigation

_ex-76 · exercises co-16, co-05_

Keep selection as state and pass a stable value to the destination.

```swift
import SwiftUI // => Supplies value navigation APIs.

struct Article: Identifiable, Hashable { let id: UUID; let title: String } // => Carries a stable route and selected display state.
struct SelectionRoute: View { let articles = [Article(id: UUID(), title: "Plan")]; var body: some View { NavigationStack { List(articles) { article in NavigationLink(article.title, value: article) }.navigationDestination(for: Article.self) { article in Text(article.title).navigationTitle("Article") } } } // => Passes the selected immutable value to detail.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Selection belongs to navigation state; the detail resolves current data from a stable key.

### Example 77: Wire View, View Model, and Service

_ex-77 · exercises co-03, co-18, co-27_

Wire one screen end to end while keeping each role narrow.

```swift
import Observation // => Supplies Observable for the model.
import SwiftUI // => Supplies the view layer.

protocol TitleService { func load() async -> String } // => Defines the changing-data capability.
@Observable @MainActor final class TitleModel { let service: any TitleService; var title = "Loading"; init(service: any TitleService) { self.service = service }; func load() async { title = await service.load() } } // => Owns screen state and decision.
struct TitleRoute: View { @State var model: TitleModel; var body: some View { Text(model.title).task { await model.load() } } } // => Renders state and starts named work.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Views render, models decide, and services cross changing boundaries.

### Example 78: Assemble the Capstone Slice

_ex-78 · exercises co-03, co-07, co-21, co-16, co-23, co-30_

Join the course boundaries in one two-screen, testable app slice.

```swift
import Observation // => Supplies observable state for SwiftUI.
import SwiftUI // => Supplies root navigation and rendering.

actor NoteCache { var values: [String: String] = [:]; func get(_ key: String) -> String? { values[key] }; func put(_ value: String, for key: String) { values[key] = value } } // => Owns mutable cache state.
@Observable @MainActor final class FocusModel { var notes = ["Plan"]; var cache = NoteCache(); func refresh() async { if await cache.get("1") == nil { await cache.put("Plan", for: "1") } } } // => Owns state and asks an actor cache.
struct FocusAppView: View { @State private var model = FocusModel(); var body: some View { NavigationStack { List(model.notes, id: \.self) { NavigationLink($0, value: $0) }.navigationDestination(for: String.self) { Text("\($0) detail") }.task { await model.refresh() } } } // => Renders navigation from observable state.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A complete app remains understandable when each concern still has a named owner.

## Production boundary

These examples deliberately use only platform APIs and deterministic fixtures. Before release,
confirm the current SDK submission requirement, exercise real permission outcomes on a device, and
run the project test suite against an installed simulator. Do not replace clear ownership with an
unstructured dependency just because the application grows.
