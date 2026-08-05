---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 turn a view tree into a testable application boundary. They use the iOS 17
Observation framework, MVVM, Codable/URLSession data, navigation and presentation, injection, and
permission outcomes. Put each slice in an iOS 17-or-later SwiftUI target before running it.

### Example 27: Observe a Model

_ex-27 · exercises co-07_

`@Observable` lets SwiftUI track properties read by a view.

```swift
import Observation // => Supplies the Observable macro.
import SwiftUI // => Supplies View and State.

@Observable final class CounterModel { var count = 0 } // => Tracks mutations on this class property.
struct CounterScreen: View { @State private var model = CounterModel(); var body: some View { Button("\(model.count)") { model.count += 1 } } } // => Re-renders the read property.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Use `@Observable` for an iOS 17-or-later class model whose properties drive UI.

### Example 28: Track Only What a View Reads

_ex-28 · exercises co-07_

Keep independently rendered properties independent.

```swift
import Observation // => Supplies the observation macro.
import SwiftUI // => Supplies View.

@Observable final class Profile { var name = "Ari"; var unread = 0 } // => Tracks each property separately.
struct NameLabel: View { let profile: Profile; var body: some View { Text(profile.name) } } // => Reads only name.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Fine-grained tracking follows actual reads; avoid making one broad refresh flag.

### Example 29: Derive a Bindable Model

_ex-29 · exercises co-08_

Turn an observable model property into a control binding inside a view.

```swift
import Observation // => Supplies Observable.
import SwiftUI // => Supplies Bindable and TextField.

@Observable final class Draft { var title = "" } // => Keeps the editable value in the model.
struct DraftField: View { let draft: Draft; var body: some View { @Bindable var draft = draft; return TextField("Title", text: $draft.title) } } // => Derives a two-way binding.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `@Bindable` exposes editing access without changing the model's ownership.

### Example 30: Move Logic into a View Model

_ex-30 · exercises co-18_

Keep transformation logic out of the rendering declaration.

```swift
import Observation // => Supplies Observable.
import SwiftUI // => Supplies View.

@Observable @MainActor final class TitleModel { var title = "focus"; func capitalize() { title = title.capitalized } } // => Owns state and logic.
struct TitleScreen: View { @State private var model = TitleModel(); var body: some View { Button(model.title) { model.capitalize() } } } // => Renders and sends intent.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: MVVM makes the view a declarative client of named model decisions.

### Example 31: Keep the View Dumb

_ex-31 · exercises co-18_

Let an event call a model method rather than embed a business rule in `body`.

```swift
import Observation // => Supplies Observable.
import SwiftUI // => Supplies Button.

@Observable @MainActor final class RefreshModel { var title = "Stale"; func refresh() { title = "Fresh" } } // => Owns the rule.
struct RefreshButton: View { @State private var model = RefreshModel(); var body: some View { Button("Refresh") { model.refresh() }; Text(model.title) } } // => Only forwards intent.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A view may start a named operation, but the model decides its state transition.

### Example 32: Model UI State as an Enum

_ex-32 · exercises co-19_

Make legitimate screen states finite and exhaustive.

```swift
import SwiftUI // => Supplies the rendering protocol.

enum LoadState { case loading, loaded([String]), failed(String) } // => Encodes mutually exclusive outcomes.
struct StateView: View { let state: LoadState; var body: some View { switch state { case .loading: Text("Loading"); case .loaded(let items): Text("\(items.count)"); case .failed(let message): Text(message) } } } // => Handles every case.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: An enum prevents a screen from accidentally being both loaded and failed.

### Example 33: Drive Loading, Success, and Failure

_ex-33 · exercises co-19_

Use deterministic fake outcomes before wiring a remote service.

```swift
import Observation // => Supplies Observable.

enum LoadState { case loading, loaded([String]), failed(String) } // => Names the finite UI outcomes.
@Observable @MainActor final class FakeLoadModel { var state: LoadState = .loading; func succeed() { state = .loaded(["Plan"]) }; func fail() { state = .failed("Offline") } } // => Makes transitions explicit.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A fake lets you inspect every rendered state without depending on a network.

### Example 34: Decode a Codable Value

_ex-34 · exercises co-20_

Decode local JSON into a typed model.

```swift
import Foundation // => Supplies Data and JSONDecoder.

struct User: Codable { let id: Int; let name: String } // => Maps JSON keys to typed properties.
let data = Data(#"{"id":1,"name":"Ari"}"#.utf8) // => Provides deterministic JSON bytes.
let user = try! JSONDecoder().decode(User.self, from: data) // => Decodes into User(id: 1, name: "Ari").
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Decode transport data at the boundary, then pass typed values inward.

### Example 35: Encode a Codable Value

_ex-35 · exercises co-20_

Encode a model and verify a round trip locally.

```swift
import Foundation // => Supplies JSONEncoder and decoder.

struct Note: Codable, Equatable { let title: String } // => Defines a serializable app value.
let bytes = try! JSONEncoder().encode(Note(title: "Plan")) // => Produces JSON data.
let note = try! JSONDecoder().decode(Note.self, from: bytes) // => Restores the same typed note.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A round trip checks that the app's encoding contract matches its decoding contract.

### Example 36: Decode Nested JSON

_ex-36 · exercises co-20_

Model arrays and nested objects with nested `Codable` types.

```swift
import Foundation // => Supplies JSONDecoder.

struct Project: Codable { struct Owner: Codable { let name: String }; let title: String; let owner: Owner; let tags: [String] } // => Matches nested object and array data.
let json = Data(#"{"title":"Focus","owner":{"name":"Ari"},"tags":["ios","swift"]}"#.utf8) // => Uses a nested inline fixture.
let project = try! JSONDecoder().decode(Project.self, from: json) // => Produces typed nested and array values.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Keep remote shape at the edge and make structure explicit in types.

### Example 37: Fetch Data Asynchronously

_ex-37 · exercises co-21, co-22_

Use `URLSession.data(from:)` in an async boundary.

```swift
import Foundation // => Supplies URL and URLSession.

func fetch(_ url: URL) async throws -> Data { // => Declares suspension and failure in the signature.
  let (data, response) = try await URLSession.shared.data(from: url) // => Waits without blocking a thread.
  guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) } // => Validates HTTP success.
  return data // => Returns only validated response bytes.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Network work is asynchronous and fallible; model both facts at the service boundary.

### Example 38: Fetch and Decode

_ex-38 · exercises co-21, co-20_

Combine a fetch boundary with typed decoding.

```swift
import Foundation // => Supplies networking and decoding APIs.

struct RemoteNote: Codable { let id: Int; let title: String } // => Defines the remote contract.
func loadNote(from url: URL) async throws -> RemoteNote { // => Returns a typed async result.
  let (data, _) = try await URLSession.shared.data(from: url) // => Retrieves response bytes.
  return try JSONDecoder().decode(RemoteNote.self, from: data) // => Decodes before returning inward.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Let the service return a typed result so views never decode raw JSON.

### Example 39: Load When a View Appears

_ex-39 · exercises co-22_

Attach view-owned async work with `.task`.

```swift
import SwiftUI // => Supplies the task modifier.

struct LoadOnAppear: View { // => Defines a screen with a view lifetime.
  @State private var message = "Waiting" // => Stores its rendered result.
  var body: some View { Text(message).task { message = "Loaded" } } // => Starts work when the view appears.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `.task` gives view-related work a visible lifecycle and cancellation relationship.

### Example 40: Start Async Work from a Button

_ex-40 · exercises co-22_

Create a task when an interaction initiates async work.

```swift
import SwiftUI // => Supplies Button and Task context.

struct AsyncButton: View { // => Owns a small visible result.
  @State private var message = "Ready" // => Starts before the action.
  var body: some View { Button("Load") { Task { message = await Task { "Loaded" }.value } }; Text(message) } // => Runs an async child task.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Keep the task body narrow; production work should call a model or service method.

### Example 41: Render a Retryable Network Error

_ex-41 · exercises co-19, co-21_

Turn a thrown error into a distinct, retryable state.

```swift
import Foundation // => Supplies URLError.
import Observation // => Supplies Observable.

enum LoadState { case loading, loaded([String]), failed(String) } // => Names the rendered conditions.
protocol TitlesClient { func fetch() async throws -> [String] } // => Makes transport replaceable for retry tests.
@Observable @MainActor final class ErrorModel { let client: any TitlesClient; var state: LoadState = .loading; init(client: any TitlesClient) { self.client = client }; func load() async { state = .loading; do { state = .loaded(try await client.fetch()) } catch is URLError { state = .failed("Check your connection") } catch { state = .failed("Try again") } } } // => Converts a typed failure to visible state; retry calls load again.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A failure is an expected outcome with a recovery action, not an unhandled callback.

### Example 42: Create a Navigation Stack

_ex-42 · exercises co-16_

Wrap a root screen in `NavigationStack`.

```swift
import SwiftUI // => Supplies NavigationStack.

struct NotesRoot: View { // => Declares a navigable root.
  var body: some View { NavigationStack { Text("Notes").navigationTitle("Focus List") } } // => Provides a navigation context and title.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Navigation state has an explicit root rather than being scattered across buttons.

### Example 43: Push a Detail View

_ex-43 · exercises co-16_

Use `NavigationLink` for an accessible value-driven push.

```swift
import SwiftUI // => Supplies NavigationLink.

struct DetailLink: View { // => Defines a simple list-to-detail route.
  var body: some View { NavigationStack { NavigationLink("Open note") { Text("Note detail") } } } // => Pushes the destination on activation.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A link expresses navigation intent and gives the platform a semantic control.

### Example 44: Navigate with a Path

_ex-44 · exercises co-16_

Bind a path when code must initiate navigation.

```swift
import SwiftUI // => Supplies NavigationPath.

struct ProgrammaticRoute: View { // => Owns the navigation history.
  @State private var path = NavigationPath() // => Starts at the root destination.
  var body: some View { NavigationStack(path: $path) { Button("Open") { path.append("detail") }.navigationDestination(for: String.self) { Text($0) } } } // => Appends a typed route value.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Programmatic navigation still uses typed values and declared destinations.

### Example 45: Declare a Value Destination

_ex-45 · exercises co-16_

Match a navigation value to one destination declaration.

```swift
import Foundation // => Supplies UUID.
import SwiftUI // => Supplies NavigationStack destinations.

struct NoteID: Hashable { let rawValue: UUID } // => Carries a stable, small route value.
struct ValueRoute: View { let id = NoteID(rawValue: UUID()); var body: some View { NavigationStack { NavigationLink("Open", value: id).navigationDestination(for: NoteID.self) { Text($0.rawValue.uuidString) } } } // => Resolves by type.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Pass an ID or other stable value, then resolve mutable data in the destination.

### Example 46: Present a Sheet

_ex-46 · exercises co-17_

Drive modal presentation from a boolean state.

```swift
import SwiftUI // => Supplies sheet presentation.

struct AddSheet: View { // => Owns whether the sheet is visible.
  @State private var showingAdd = false // => Starts without a modal.
  var body: some View { Button("Add") { showingAdd = true }.sheet(isPresented: $showingAdd) { Text("New note") } } // => Presents and dismisses through binding.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A sheet is state-driven UI, not an imperative side channel.

### Example 47: Present an Alert

_ex-47 · exercises co-17_

Use an alert for a concise, recoverable error message.

```swift
import SwiftUI // => Supplies alert presentation.

struct ErrorAlert: View { // => Owns an error-presentation flag.
  @State private var showError = false // => Starts with no alert.
  var body: some View { Button("Fail") { showError = true }.alert("Could not save", isPresented: $showError) { Button("OK", role: .cancel) {} } } // => Gives a dismiss action.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Alert state should reflect a modelled condition, not replace error handling.

### Example 48: Drive a List from a Model

_ex-48 · exercises co-13, co-07_

Render observable model data with stable identity.

```swift
import Observation // => Supplies Observable.
import SwiftUI // => Supplies List and Button.
import SwiftUI // => Supplies List.

@Observable final class NotesModel { var notes = ["Plan", "Review"] } // => Publishes list changes.
struct ModelList: View { @State private var model = NotesModel(); var body: some View { List(model.notes, id: \.self) { Text($0) } } } // => Renders current notes.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: The list reads the model; it does not mirror the array in local state.

### Example 49: Update an Observable List

_ex-49 · exercises co-07, co-13_

Mutate the model's source of truth and let the list update.

```swift
import Observation // => Supplies Observable.

struct Note: Identifiable { let id = UUID(); let title: String } // => Gives List a stable identity.
@Observable @MainActor final class NoteAdder { var notes = [Note(title: "Plan")]; func add() { notes.append(Note(title: "Review")) } } // => Owns the mutation.
struct NoteList: View { @State private var model = NoteAdder(); var body: some View { List(model.notes) { Text($0.title) }.toolbar { Button("Add", action: model.add) } } } // => Reads the observable list directly.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Change the owner once; dependent SwiftUI views re-render from the changed value.

### Example 50: Inject a Shared Environment Model

_ex-50 · exercises co-09_

Pass an observable dependency down the view tree deliberately.

```swift
import Observation // => Supplies Observable.
import SwiftUI // => Supplies environment injection.

@Observable final class Session { var user = "Ari" } // => Defines a shared app dependency.
struct SessionRoot: View { @State private var session = Session(); var body: some View { SessionChild().environment(session) } } // => Injects once at the boundary.
struct SessionChild: View { @Environment(Session.self) private var session; var body: some View { Text(session.user) } } // => Reads explicitly by type.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Environment injection removes plumbing, not the need to choose ownership carefully.

### Example 51: Depend on a Service Protocol

_ex-51 · exercises co-27_

Define the capability a model needs, plus a deterministic fake.

```swift
protocol NoteService { func fetch() async throws -> [String] } // => Defines the app-facing boundary.
struct FakeNoteService: NoteService { func fetch() async throws -> [String] { ["Plan"] } } // => Makes tests deterministic.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A protocol lets a model depend on a capability rather than a network singleton.

### Example 52: Inject a Service into a Model

_ex-52 · exercises co-27_

Provide the dependency when constructing the view model.

```swift
import Observation // => Supplies Observable.

protocol NoteService { func fetch() async throws -> [String] } // => Defines the model's required capability.
struct FakeNoteService: NoteService { func fetch() async throws -> [String] { ["Plan"] } } // => Provides deterministic data.
@Observable @MainActor final class NotesViewModel { let service: any NoteService; init(service: any NoteService) { self.service = service } } // => Receives, rather than constructs, its boundary.
let model = NotesViewModel(service: FakeNoteService()) // => Wires a deterministic implementation at the composition root.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Constructor injection makes production wiring and test wiring equally explicit.

### Example 53: Request a Notification Permission

_ex-53 · exercises co-28_

Ask for a privacy-sensitive capability at the moment a feature needs it.

```swift
import UserNotifications // => Supplies the notification authorization API.

func requestNotifications() async throws -> Bool { // => Returns the user decision asynchronously.
  try await UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound]) // => Lets the system present its prompt.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: An entitlement or usage description does not equal a runtime grant.

### Example 54: Handle Permission Denial

_ex-54 · exercises co-28_

Render a denied capability as a usable state.

```swift
import SwiftUI // => Supplies the fallback rendering types.

enum PermissionState { case granted, denied } // => Represents both outcomes explicitly.
struct PermissionView: View { let state: PermissionState; var body: some View { switch state { case .granted: Text("Camera ready"); case .denied: Text("Choose a photo instead") } } } // => Avoids a crash path.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Permission denial is a normal product state with an honest fallback.

## Why these boundaries matter

The intermediate layer separates UI decisions from transport, lifecycle, and system outcomes. That
makes every important screen state reproducible with a fake, every dependency replaceable, and every
navigation or permission transition visible to both readers and tests.
