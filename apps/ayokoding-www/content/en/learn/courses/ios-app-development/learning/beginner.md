---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish an Xcode target, the SwiftUI lifecycle, declarative view composition,
local state, bindings, layout, controls, lists, forms, and previews. Put each SwiftUI slice in an
iOS App project and run it in an Xcode simulator; each block includes all imports it needs.

### Example 1: Create an Xcode iOS App Target

_ex-01 · exercises co-01_

Create an iOS App target in Xcode with the SwiftUI lifecycle, then select a simulator and run it.

```text
Product Name: FocusList       // => Names the app target and scheme.
Interface: SwiftUI            // => Creates the declarative app entry point.
Deployment Target: iOS 17.0   // => Enables Observation and SwiftData examples.
Run Destination: iPhone       // => Uses a simulated device, not a live service.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: The project target, deployment target, build SDK, and simulator each answer a
different question; do not treat them as one version setting.

### Example 2: Declare the App Entry Point

_ex-02 · exercises co-02_

`@main` identifies the SwiftUI app entry point.

```swift
import SwiftUI // => Imports the native declarative UI framework.

@main // => Starts this app when iOS launches its process.
struct FocusListApp: App { // => App declares the scene hierarchy.
  var body: some Scene { WindowGroup { Text("Focus List") } } // => Creates the first scene.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: The `App` protocol owns scene declaration; it is not a view model or a data store.

### Example 3: Host a Root View in a Window Group

_ex-03 · exercises co-02_

Host the root view in a system-managed `WindowGroup` and observe its scene phase.

```swift
import SwiftUI // => Supplies View and the environment property wrapper.

struct FocusListApp: App { // => Declares the app's root scene.
  @Environment(\.scenePhase) private var phase // => Reads the system lifecycle value.
  var body: some Scene { WindowGroup { Text(phase == .active ? "Active" : "Not active") } } // => Hosts the root view in a window scene.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `WindowGroup` hosts the root view; observe lifecycle transitions, but persist data
explicitly when it must survive a relaunch.

### Example 4: Render a SwiftUI View

_ex-04 · exercises co-03_

A `View` describes UI with a value-returning `body`.

```swift
import SwiftUI // => Makes the View protocol and Text available.

struct GreetingView: View { // => A view is a lightweight value type.
  var body: some View { Text("Hello, iOS") } // => Describes the rendered content.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A view declares the UI that state requires; it does not imperatively edit widgets.

### Example 5: Read a Property in `body`

_ex-05 · exercises co-03_

Pass data into a view and let `body` reflect it.

```swift
import SwiftUI // => Supplies the declarative UI types.

struct TitleView: View { // => Defines a reusable rendering unit.
  let title: String // => Receives immutable input from its owner.
  var body: some View { Text(title) } // => Renders the current input value.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Values flowing into `body` make a view easy to preview and test mentally.

### Example 6: Compose a Reusable Subview

_ex-06 · exercises co-04_

Extract a repeated row rather than growing one monolithic screen.

```swift
import SwiftUI // => Supplies VStack, Text, and View.

struct NoteRow: View { let title: String; var body: some View { Text(title) } } // => Names one row.
struct NoteList: View { // => Composes rows into a larger screen.
  var body: some View { VStack { NoteRow(title: "Plan"); NoteRow(title: "Review") } } // => Reuses the row.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Composition gives each view one clear rendering responsibility.

### Example 7: Own Local Counter State

_ex-07 · exercises co-05_

Use `@State` when this view owns a small mutable value.

```swift
import SwiftUI // => Supplies State and Button.

struct CounterView: View { // => Owns a local interaction state.
  @State private var count = 0 // => Stores a SwiftUI-managed source of truth.
  var body: some View { Button("Count: \(count)") { count += 1 } } // => Mutation triggers a re-render.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `@State` belongs to the view that owns the value, not every view that displays it.

### Example 8: Drive Conditional Content with State

_ex-08 · exercises co-05_

Let a boolean state choose the rendered branch.

```swift
import SwiftUI // => Supplies Toggle and conditional views.

struct DetailsView: View { // => Owns whether details are visible.
  @State private var expanded = false // => Begins in the collapsed state.
  var body: some View { VStack { Toggle("Details", isOn: $expanded); if expanded { Text("Shown") } } } // => Renders from state.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Conditional UI derives from state; do not manually hide an existing view.

### Example 9: Bind a Text Field to State

_ex-09 · exercises co-06_

Pass `$text` to a control that edits state owned by the view.

```swift
import SwiftUI // => Supplies TextField and State.

struct NameField: View { // => Owns the editable string.
  @State private var name = "" // => Starts with an empty source of truth.
  var body: some View { TextField("Name", text: $name).textFieldStyle(.roundedBorder) } // => Binds typing to name.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: The `$` projection creates the two-way connection required by `TextField`.

### Example 10: Let a Child Edit Parent State

_ex-10 · exercises co-06_

Use `@Binding` when a child edits a value whose owner is elsewhere.

```swift
import SwiftUI // => Supplies Binding and Toggle.

struct Parent: View { @State private var done = false; var body: some View { DoneToggle(done: $done) } } // => Owns done.
struct DoneToggle: View { // => Receives access, not ownership.
  @Binding var done: Bool // => Writes through to Parent's state.
  var body: some View { Toggle("Done", isOn: $done) } // => Edits the parent value.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Binding clarifies that the child can edit a value without creating a duplicate.

### Example 11: Read an Environment Value

_ex-11 · exercises co-09_

Use an environment value for a system-provided concern.

```swift
import SwiftUI // => Supplies ColorScheme and Environment.

struct SchemeLabel: View { // => Adapts its rendering to an inherited value.
  @Environment(\.colorScheme) private var scheme // => Reads light or dark appearance.
  var body: some View { Text(scheme == .dark ? "Dark" : "Light") } // => Avoids threading the value manually.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Environment values reduce parameter threading, but still make dependencies visible.

### Example 12: Arrange Content Vertically

_ex-12 · exercises co-10_

`VStack` places children in vertical order.

```swift
import SwiftUI // => Supplies VStack and Text.

struct VerticalLabels: View { // => Defines a vertically arranged screen.
  var body: some View { VStack { Text("Inbox"); Text("Today"); Text("Archive") } } // => Renders top to bottom.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Choose a stack for the spatial relationship the interface needs.

### Example 13: Arrange Content Horizontally

_ex-13 · exercises co-10_

`HStack` plus `Spacer` distributes a row.

```swift
import SwiftUI // => Supplies HStack and Spacer.

struct HeaderRow: View { // => Defines a single horizontal row.
  var body: some View { HStack { Text("Notes"); Spacer(); Text("3") } } // => Pushes the count to the trailing edge.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `Spacer` consumes flexible space rather than requiring fixed coordinates.

### Example 14: Overlay a Badge

_ex-14 · exercises co-10_

`ZStack` layers views deliberately.

```swift
import SwiftUI // => Supplies ZStack and shape views.

struct Badge: View { // => Creates a layered visual relationship.
  var body: some View { ZStack { Circle().fill(.blue); Text("3").foregroundStyle(.white) } } // => Draws text over a circle.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Use `ZStack` for intentional overlap, not as a substitute for screen structure.

### Example 15: Size and Space a View

_ex-15 · exercises co-11_

Apply padding and a frame as independent modifiers.

```swift
import SwiftUI // => Supplies Text modifiers.

struct SizedLabel: View { // => Demonstrates a modifier chain.
  var body: some View { Text("Focus").padding().frame(width: 160, height: 48) } // => Adds space then proposes a size.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Modifiers return new configured views, so each operation has a place in the chain.

### Example 16: Order a Modifier Chain

_ex-16 · exercises co-11_

Chain typography, foreground style, background, and padding in a readable order.

```swift
import SwiftUI // => Supplies styles and modifiers.

struct StyledLabel: View { // => Builds a view by successive wrapping.
  var body: some View { Text("Ready").font(.headline).foregroundStyle(.white).padding().background(.blue) } // => Paints after padding.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Modifier order changes the result; make the order communicate the intended layers.

### Example 17: Render Dynamic Text

_ex-17 · exercises co-12_

Use `Text` for a value supplied by the model.

```swift
import SwiftUI // => Supplies Text and View.

struct Greeting: View { // => Receives a rendering input.
  let name: String // => Keeps the value immutable in this view.
  var body: some View { Text("Welcome, \(name)") } // => Interpolates the current name.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Controls render state; they should not smuggle in business decisions.

### Example 18: Respond to a Button Action

_ex-18 · exercises co-12_

Give a button a visible label and a narrow state change.

```swift
import SwiftUI // => Supplies Button and State.

struct TapView: View { // => Owns the displayed interaction result.
  @State private var tapped = false // => Starts before the action.
  var body: some View { Button("Tap") { tapped = true }; Text(tapped ? "Tapped" : "Waiting") } // => Renders the result.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A button emits intent; the owner decides the resulting state.

### Example 19: Capture Text Input

_ex-19 · exercises co-12_

Bind user input and immediately show the owned value.

```swift
import SwiftUI // => Supplies TextField and Text.

struct EchoField: View { // => Keeps one source of truth for input.
  @State private var query = "" // => Holds the current text.
  var body: some View { VStack { TextField("Search", text: $query); Text(query) } } // => Shows edits as they occur.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A controlled input exposes its value and its update route together.

### Example 20: Toggle a Boolean

_ex-20 · exercises co-12_

Use `Toggle` for a binary user preference.

```swift
import SwiftUI // => Supplies Toggle and State.

struct NotificationsToggle: View { // => Owns a local preference draft.
  @State private var enabled = true // => Provides the initial control value.
  var body: some View { Toggle("Notifications", isOn: $enabled) } // => Reads and writes enabled.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A toggle changes application state; permission and persistence need separate edges.

### Example 21: Render Static List Rows

_ex-21 · exercises co-13_

Use `List` for a scrollable collection of known rows.

```swift
import SwiftUI // => Supplies List and Text.

struct StaticNotes: View { // => Defines a list screen.
  var body: some View { List { Text("Plan"); Text("Write"); Text("Review") } } // => Creates three accessible rows.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: `List` provides platform list behavior without manual scrolling infrastructure.

### Example 22: Render Model-Driven Rows

_ex-22 · exercises co-13_

Use `ForEach` over identifiable data.

```swift
import Foundation // => Supplies UUID for stable note identity.
import SwiftUI // => Supplies List and ForEach.

struct Note: Identifiable { let id = UUID(); let title: String } // => Gives each row stable identity.
struct NoteRows: View { let notes = [Note(title: "Plan"), Note(title: "Ship")]; var body: some View { List(notes) { Text($0.title) } } } // => Renders each model once.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Stable identity lets SwiftUI track rows as data changes.

### Example 23: Group Settings in a Form

_ex-23 · exercises co-14_

Use sections to group related settings controls.

```swift
import SwiftUI // => Supplies Form and Section.

struct SettingsForm: View { // => Describes a settings-style screen.
  var body: some View { Form { Section("Profile") { Text("Name") }; Section("About") { Text("Version") } } } // => Gives groups labels.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Semantic grouping helps readers scan a form and helps assistive technologies.

### Example 24: Edit a Form Value

_ex-24 · exercises co-14_

Bind a form field to state owned by the screen.

```swift
import SwiftUI // => Supplies Form, TextField, and State.

struct ProfileForm: View { // => Owns the profile draft.
  @State private var name = "Ari" // => Supplies the initial editable value.
  var body: some View { Form { TextField("Name", text: $name) } } // => Writes edits into name.
}
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: A form edits state; a save action later decides whether and where to persist it.

### Example 25: Preview a View

_ex-25 · exercises co-15_

Add a preview so Xcode can render a view without launching the app.

```swift
import SwiftUI // => Supplies the previewed view types.

struct PreviewedTitle: View { var body: some View { Text("Focus") } } // => Defines a small renderable slice.
#Preview { PreviewedTitle() } // => Sends the slice to Xcode's canvas.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Previews speed visual feedback but do not replace simulator or device verification.

### Example 26: Preview Multiple Appearances

_ex-26 · exercises co-15_

Render the same view under light and dark schemes.

```swift
import SwiftUI // => Supplies preferredColorScheme.

struct AppearanceView: View { var body: some View { Text("Focus").padding() } } // => Defines the common UI.
#Preview("Light") { AppearanceView().preferredColorScheme(.light) } // => Checks light appearance.
#Preview("Dark") { AppearanceView().preferredColorScheme(.dark) } // => Checks dark appearance.
// => End of this self-contained example.
// => Read the inline annotations before changing a value.
```

**Key takeaway**: Preview meaningful environments so contrast and layout assumptions become visible.

## Why these fundamentals matter

iOS can activate a scene, recreate a view value, and render the same state repeatedly. The examples
make ownership visible from the start: state has one owner, editable children get bindings, and
layout describes relationships instead of mutating an opaque screen tree.
