# iOS App Development (By Example, Swift)

**Course ID**: `ios-app-development` · **Format**: By Example · **Language**: Swift.

**Short summary**: Native iOS apps with Swift and the SDK

**Scope note**: `◆` app-domain — building a real iOS app: the app/scene lifecycle, SwiftUI (declarative
views + state/binding/observable), MVVM + the Observation framework, `Codable`/`URLSession` data, Swift
concurrency (`async`/`await`, actors), platform concerns, and applied testing. **Tooling note (DD-17)**:
Xcode is required (simulator, signing, SwiftUI previews); the topic uses Xcode where mandated and shows
the `swift`/`xcodebuild` CLI form where possible.

## Why this exists · the big idea

- **The problem before the solution**: a real iOS app coordinates the scene lifecycle, declarative views,
  observable state, networking, persistence, and actor-isolated concurrency — without a clear architecture
  these concerns smear together and every change risks the whole screen.
- **Keep-this-if-you-forget-everything**: a SwiftUI view is a declarative function of observable state —
  put the logic in the model, keep the view dumb, and the UI re-renders itself.
- **Big ideas touched**: `coupling-vs-cohesion` — MVVM and the Observation framework separate view from
  view-model so each changes independently; `layering-and-leaks` — Xcode, signing, the annual SDK mandate,
  and the simulator are platform layers that leak into every build.

## Prerequisites

- **Prior topics**: [topic 70 Just Enough Swift](./just-enough-swift.md) (the language + `async`/`await`),
  [topic 14 Frontend Essentials](./frontend-essentials.md) (component + state UI), and
  [topic 69 Android App Development](./android-app-development.md) (the mobile app pattern to contrast).
- **Tools & environment**: a **macOS** machine with **Xcode** (simulator, signing, SwiftUI previews);
  `swift` / `xcodebuild` from the CLI where possible; a simulator or a device.
- **Assumed knowledge**: Swift syntax + `async`/`await` (topic 70); declarative UI + state (topic 14);
  calling an HTTP API (topic 11).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the **Observation framework** (`@Observable` macro, classes only, fine-grained
  dependency tracking, iOS 17+) is the current replacement for manual `ObservableObject`/`@Published`.
  SwiftUI declarative views, `Codable`/`URLSession`, Core Data/SwiftData, Swift concurrency (actors,
  structured concurrency), and XCTest/XCUITest + `xcodebuild test` are all current/unchanged.
  (developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro)
- 2026-07-12 — verified (TIME-SENSITIVE, re-check at authoring): Apple mandates apps be **built with the
  current iOS SDK / Xcode** for App Store submissions on a **recurring annual deadline** (the 2026 cycle
  required the iOS 26 SDK / Xcode 26 from 2026-04-28 — an SDK-build requirement, independent of your app's
  deployment target, which can still be iOS 16/17). Frame this as the _annual SDK-mandate pattern_ (the iOS
  analogue of topic 66's Android Play target-API deadline), not a fixed date; pull the then-current deadline
  at authoring time. (developer.apple.com/news/upcoming-requirements)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official developer.apple.com / swift.org page the pre-authoring
> `web-researcher` sweep fetched and read. `[Needs Verification]` marks items not captured verbatim or with
> live currency risk. Apple's docs are JS-rendered — several exact API pages resisted verbatim capture and
> are flagged; re-verify immediately before publish.

- **Versions** — current toolchain is **Xcode 26.x** (26.6 line) bundling **Swift 6.3**; the **annual
  SDK-build mandate** (build with the current iOS SDK/Xcode to submit to the App Store) is a recurring
  pattern independent of the app's deployment target. Keep versions UNPINNED; frame the mandate as a
  pattern, not a fixed date. `[Verified]` on the mandate pattern (developer.apple.com/news/upcoming-requirements);
  `[Needs Verification]` on the exact current Xcode point-release at publish time.
- **App/scene lifecycle** — developer.apple.com/documentation/swiftui/app: the `App` protocol +
  `@main` "the entry point for your app"; a `Scene` (e.g. `WindowGroup`) "a part of an app's user interface
  with a life cycle managed by the system"; scene phases via `@Environment(\.scenePhase)`. `[Verified]`
- **SwiftUI views** — developer.apple.com/documentation/swiftui/view: "A type that represents part of your
  app's user interface and provides modifiers that you use to configure views." The `body` computed
  property "the content and behavior of the view." Declarative composition of subviews. `[Verified]`
- **State & binding** — developer.apple.com/documentation/swiftui/state + /binding: `@State` "A property
  wrapper type that can read and write a value managed by SwiftUI" (source of truth owned by the view);
  `@Binding` "A property wrapper type that can read and write a value owned by a source of truth" (a
  two-way connection, passed with `$`). `[Verified]`
- **Observation** — developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro:
  the `@Observable` macro (Observation framework, iOS 17+, **classes only**) provides fine-grained
  dependency tracking and is the current replacement for `ObservableObject`/`@Published`; use `@Bindable`
  to get bindings into an `@Observable` model from a view; `@State` holds the model instance. `[Verified]`
- **Layout & modifiers** — SwiftUI `VStack`/`HStack`/`ZStack` stack children; view modifiers
  (`.padding()`, `.frame(...)`, `.font(...)`) each return a new modified view. `[Verified]` on existence +
  behavior; exact per-modifier pages not captured verbatim.
- **Controls & containers** — `Text`, `Button(action:)`, `TextField`, `Toggle`, `List` + `ForEach`,
  `Form`/`Section` are standard SwiftUI building blocks. `List`, `Form`, and the `#Preview` macro pages
  resisted verbatim capture (JS-rendered) — `[Needs Verification]` on `#Preview`, `List`, `Form` exact
  wording; `[Verified]` on their existence + role.
- **Navigation** — developer.apple.com/documentation/swiftui/navigationstack: `NavigationStack` "displays a
  root view and enables you to present additional views over the root view"; `NavigationLink` + a
  `navigationDestination(for:)` value-based destination + an optional bound `path` for programmatic
  navigation. `[Verified]`
- **Codable & URLSession** — developer.apple.com/documentation/foundation/urlsession: `URLSession`'s
  `func data(from:) async throws -> (Data, URLResponse)` fetches asynchronously; `Codable` (`Encodable &
Decodable`) with `JSONDecoder().decode(T.self, from: data)` maps JSON to types. `[Verified]` on
  URLSession async + Codable; `[Needs Verification]` on the exact `JSONDecoder` page wording.
- **Swift concurrency** — developer.apple.com/documentation/swift/concurrency + swift.org: `async`/`await`
  functions; SwiftUI's `.task { }` modifier runs async work tied to the view's lifetime; an `actor`
  "protects its mutable state" from data races via isolation; `@MainActor` isolates UI-touching work to the
  main thread; structured concurrency via `async let` / task groups / cooperative cancellation.
  `[Verified]`
- **Persistence** — SwiftData (`@Model` macro, `ModelContainer`/`ModelContext`, iOS 17+) is the current
  Swift-native persistence layer; Core Data remains the mature underpinning. `[Verified]` on existence +
  role; exact `@Model` page not captured verbatim.
- **Testing** — developer.apple.com/documentation/xctest + swift.org/documentation/testing: XCTest
  (`XCTestCase`, `XCTAssert*`) and the newer **Swift Testing** framework (`@Test` functions, `#expect(...)`
  / `#require(...)` macros) run unit tests; XCUITest drives UI tests; `xcodebuild test -scheme <S>
-destination '<sim>'` runs them from the CLI. `[Verified]` on XCTest/Swift-Testing/xcodebuild;
  `[Needs Verification]` on the exact XCUITest API page.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · xcode-project** — an iOS app is an Xcode project built against an SDK and run on a simulator/device; the build SDK and the deployment target are distinct.
- **co-02 · app-scene-lifecycle** — the `App` protocol + `@main` is the entry point; a `Scene` (`WindowGroup`) has a system-managed lifecycle observable via `scenePhase`.
- **co-03 · swiftui-view** — a `View` is a value type whose `body` declaratively describes UI as a function of state.
- **co-04 · view-composition** — screens are built by composing small reusable subviews rather than one monolith.
- **co-05 · state** — `@State` owns a view's local mutable source of truth; mutating it re-renders the view.
- **co-06 · binding** — `@Binding` is a two-way reference to state owned elsewhere, passed with `$` so a child can read and write the parent's value.
- **co-07 · observable-macro** — the `@Observable` macro (iOS 17+, classes only) gives a model fine-grained dependency tracking, replacing `ObservableObject`/`@Published`.
- **co-08 · bindable** — `@Bindable` derives bindings into an `@Observable` model so a view can two-way-bind its properties.
- **co-09 · environment** — `@Environment` / environment injection passes shared values down the view tree without threading them through every initializer.
- **co-10 · layout-stacks** — `VStack`, `HStack`, and `ZStack` arrange children vertically, horizontally, and layered.
- **co-11 · view-modifiers** — modifiers (`.padding`, `.frame`, `.font`) each wrap a view returning a new configured view; order matters.
- **co-12 · controls** — `Text`, `Button`, `TextField`, and `Toggle` are the core interactive building blocks.
- **co-13 · lists** — `List` + `ForEach` render collections, including dynamic model-driven rows.
- **co-14 · forms** — `Form`/`Section` build settings-style input screens bound to state.
- **co-15 · preview** — the `#Preview` macro renders a view in Xcode without launching the app.
- **co-16 · navigation-stack** — `NavigationStack` + `NavigationLink` + `navigationDestination(for:)` push/pop destinations, with an optional bound `path` for programmatic navigation.
- **co-17 · sheets-and-alerts** — `.sheet` and `.alert` present modal content driven by bound state.
- **co-18 · mvvm** — MVVM keeps the view declarative and dumb while a view-model holds state and logic, so the model is testable headless.
- **co-19 · ui-state-modeling** — model a screen's state as loading/success/error (often an enum) so each case renders deterministically.
- **co-20 · codable** — `Codable` types encode to and decode from JSON via `JSONEncoder`/`JSONDecoder`.
- **co-21 · urlsession** — `URLSession.data(from:)` fetches data asynchronously with `async`/`await`, throwing on failure.
- **co-22 · async-await-ios** — `async`/`await` functions plus SwiftUI's `.task { }` modifier run asynchronous work tied to a view's lifetime.
- **co-23 · actors** — an `actor` serializes access to its mutable state, eliminating data races by isolation.
- **co-24 · main-actor** — `@MainActor` isolates UI-touching code to the main thread, enforced by the compiler.
- **co-25 · structured-concurrency** — `async let`, task groups, and cooperative cancellation compose concurrent work with clear lifetimes.
- **co-26 · persistence** — SwiftData (`@Model`) / Core Data persists model objects locally with a save/fetch round-trip that survives relaunch.
- **co-27 · dependency-injection** — injecting services (a networking client, a store) from outside a view-model rather than constructing them inside aids testability.
- **co-28 · permissions** — privacy-sensitive capabilities are requested at runtime and the app must handle grant/deny gracefully.
- **co-29 · unit-testing** — XCTest (`XCTestCase`, `XCTAssert*`) and Swift Testing (`@Test`, `#expect`) verify model/logic in isolation.
- **co-30 · ui-testing** — XCUITest drives the running UI; `xcodebuild test` runs the whole suite from the CLI.

## Worked examples

Colocated under `ios-app-development/learning/code/`; each runnable/testable via Xcode/`xcodebuild` (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · xcode-new-project** — create an iOS App target in Xcode and run it on a simulator — verify the launch screen appears. (co-01)
- **ex-02 · app-protocol-main** — declare `@main struct MyApp: App` — verify the app builds from the SwiftUI lifecycle. (co-02)
- **ex-03 · windowgroup-scene** — host the root view in a `WindowGroup` — verify it displays. (co-02)
- **ex-04 · swiftui-hello-view** — a `struct ContentView: View` returning `Text("Hello")` — verify the text renders. (co-03)
- **ex-05 · view-body** — read a property in `body` — verify the view reflects it. (co-03)
- **ex-06 · compose-subview** — extract a row into its own `View` and reuse it — verify composition renders. (co-04)
- **ex-07 · state-counter** — `@State private var count = 0` incremented by a button — verify the label updates. (co-05)
- **ex-08 · state-toggle** — a `@State` bool driving conditional content — verify toggling shows/hides. (co-05)
- **ex-09 · binding-textfield** — bind a `TextField` to `@State` via `$text` — verify typing updates state. (co-06)
- **ex-10 · binding-parent-child** — pass `$value` as a `@Binding` to a child — verify the child mutates the parent's state. (co-06)
- **ex-11 · environment-value** — read `@Environment(\.colorScheme)` — verify the view adapts to light/dark. (co-09)
- **ex-12 · vstack** — stack three views in a `VStack` — verify vertical order. (co-10)
- **ex-13 · hstack** — lay out items in an `HStack` with `Spacer()` — verify horizontal spread. (co-10)
- **ex-14 · zstack-overlay** — overlay a badge with `ZStack` — verify layering. (co-10)
- **ex-15 · modifier-padding-frame** — apply `.padding()` + `.frame(width:height:)` — verify sizing/spacing. (co-11)
- **ex-16 · modifier-chain** — chain `.font().foregroundStyle().padding()` — verify all apply. (co-11)
- **ex-17 · text-view** — render dynamic `Text(name)` — verify the value displays. (co-12)
- **ex-18 · button-action** — a `Button("Tap") { }` — verify the action fires. (co-12)
- **ex-19 · textfield-input** — an input `TextField` — verify entered text is captured. (co-12)
- **ex-20 · toggle-control** — a `Toggle` bound to state — verify flipping updates state. (co-12)
- **ex-21 · list-static** — a `List` of static rows — verify they render scrollably. (co-13)
- **ex-22 · list-foreach** — `List { ForEach(items) { } }` — verify each element renders once. (co-13)
- **ex-23 · form-section** — a `Form` with two `Section`s — verify grouped layout. (co-14)
- **ex-24 · form-binding** — a form field bound to state — verify edits propagate. (co-14)
- **ex-25 · preview-macro** — add `#Preview { ContentView() }` — verify the canvas renders. (co-15)
- **ex-26 · preview-multiple** — two `#Preview`s for light/dark — verify both render. (co-15)

### Intermediate

- **ex-27 · observable-model** — an `@Observable final class ViewModel` — verify a view observing it re-renders on change. (co-07)
- **ex-28 · observable-tracking** — mutate one of two observable properties — verify only the dependent view updates. (co-07)
- **ex-29 · bindable-in-view** — `@Bindable var model` to bind a `TextField` into the model — verify two-way binding. (co-08)
- **ex-30 · mvvm-viewmodel** — move logic into the view-model — verify the view only renders state. (co-18)
- **ex-31 · mvvm-view-dumb** — the view calls `model.load()` on an event — verify no business logic in the view. (co-18)
- **ex-32 · ui-state-enum** — `enum State { case loading, loaded([Item]), failed(String) }` — verify an exhaustive switch renders each. (co-19)
- **ex-33 · loading-success-error** — drive the three states from a fake service — verify each branch renders. (co-19)
- **ex-34 · codable-decode** — `JSONDecoder().decode(User.self, from:)` — verify JSON maps to fields. (co-20)
- **ex-35 · codable-encode** — `JSONEncoder().encode(user)` — verify the round-trip. (co-20)
- **ex-36 · codable-nested** — decode a nested/array payload — verify structure maps. (co-20)
- **ex-37 · urlsession-async** — `let (data, _) = try await URLSession.shared.data(from: url)` — verify a fetch completes. (co-21, co-22)
- **ex-38 · urlsession-decode** — decode the fetched `data` into a `Codable` model — verify typed values. (co-21, co-20)
- **ex-39 · task-modifier** — load data in `.task { await model.load() }` — verify it runs on appear. (co-22)
- **ex-40 · async-button-action** — a button launching `Task { await ... }` — verify async work runs. (co-22)
- **ex-41 · network-error-state** — surface a thrown `URLError` as `.failed` — verify the error UI and retry. (co-19, co-21)
- **ex-42 · navigationstack-basic** — a `NavigationStack` with a title — verify the bar renders. (co-16)
- **ex-43 · navigationlink** — a `NavigationLink` to a detail view — verify the push. (co-16)
- **ex-44 · navigation-path** — a programmatic `NavigationStack(path:)` — verify appending navigates. (co-16)
- **ex-45 · navigation-value-destination** — `navigationDestination(for: Item.self)` — verify value-based routing. (co-16)
- **ex-46 · sheet-present** — `.sheet(isPresented:)` — verify the modal presents/dismisses. (co-17)
- **ex-47 · alert-present** — `.alert(...)` on an error — verify the alert shows. (co-17)
- **ex-48 · list-from-model** — a `List` driven by observable model data — verify rows reflect state. (co-13, co-07)
- **ex-49 · observable-list-update** — append to the model's array — verify the list adds a row live. (co-07, co-13)
- **ex-50 · environment-inject** — inject a shared object via `.environment(...)` — verify a deep child reads it. (co-09)
- **ex-51 · di-protocol-service** — define a `Service` protocol + a fake — verify the view-model depends on the protocol. (co-27)
- **ex-52 · di-inject-viewmodel** — inject the service into the view-model's initializer — verify no `URLSession` inside the model. (co-27)
- **ex-53 · permission-request** — request notification/camera permission — verify the system prompt appears. (co-28)
- **ex-54 · permission-denied** — handle a denied permission — verify graceful degradation (no crash). (co-28)

### Advanced

- **ex-55 · actor-define** — `actor Cache { }` — verify it compiles as an isolated type. (co-23)
- **ex-56 · actor-isolated-cache** — store fetched items in the actor — verify concurrent access is serialized. (co-23)
- **ex-57 · actor-await-access** — read the actor with `await cache.get(id)` — verify cross-actor access requires `await`. (co-23)
- **ex-58 · mainactor-viewmodel** — annotate the view-model `@MainActor` — verify UI updates stay on the main thread. (co-24)
- **ex-59 · mainactor-ui-update** — hop back to `@MainActor` after a background fetch — verify the compiler enforces isolation. (co-24)
- **ex-60 · async-let-concurrent** — `async let a = ...; async let b = ...` then `await (a, b)` — verify both run concurrently. (co-25)
- **ex-61 · task-group** — a `withTaskGroup` fetching N items — verify all complete before aggregation. (co-25)
- **ex-62 · task-cancellation** — check `Task.isCancelled` / throw on cancel — verify a cancelled task stops. (co-25)
- **ex-63 · cancel-on-disappear** — `.task` cancels when the view disappears — verify the in-flight fetch is cancelled. (co-25, co-22)
- **ex-64 · swiftdata-model** — an `@Model final class Note` — verify SwiftData tracks it. (co-26)
- **ex-65 · swiftdata-insert-query** — insert via `modelContext` + a `@Query` — verify the row appears. (co-26)
- **ex-66 · persistence-roundtrip** — save, relaunch, fetch — verify data survives. (co-26)
- **ex-67 · xctest-unit** — an `XCTestCase` asserting a mapping function — verify `xcodebuild test` runs it. (co-29)
- **ex-68 · swift-testing-expect** — a `@Test` function with `#expect(...)` — verify the Swift Testing case passes. (co-29)
- **ex-69 · viewmodel-test** — test the view-model with a fake service — verify state transitions loading→loaded. (co-29, co-18)
- **ex-70 · async-test** — an `async` test awaiting the model's load — verify the awaited result. (co-29, co-22)
- **ex-71 · xcuitest-launch** — an XCUITest launching the app — verify a labeled element exists. (co-30)
- **ex-72 · xcuitest-interaction** — tap a button and assert the resulting screen — verify the UI flow. (co-30)
- **ex-73 · xcodebuild-test-cli** — `xcodebuild test -scheme App -destination '<sim>'` — verify the suite runs headless. (co-30)
- **ex-74 · actor-cache-integration** — the repository reads the actor cache before hitting `URLSession` — verify cache-first behavior. (co-23, co-21)
- **ex-75 · observable-driven-ui** — a screen re-rendering purely from `@Observable` state — verify no manual refresh. (co-07, co-03)
- **ex-76 · navigation-passed-state** — pass a selected item's state through navigation — verify the detail shows it. (co-16, co-05)
- **ex-77 · screen-vm-service-slice** — wire one screen end-to-end: view ← view-model ← injected service — verify the full path. (co-03, co-18, co-27)
- **ex-78 · capstone-full-app** — assemble a two-screen app with an `@Observable` model, `URLSession`/`Codable` networking, an actor cache, navigation, persistence, and an XCUITest — verify `xcodebuild test` is green and the flow works on a simulator. (co-03, co-07, co-21, co-16, co-23, co-30)

## Capstone spec — intra-topic (subject → full runnable app)

- **Goal**: build a small but complete iOS app — SwiftUI views under MVVM with an `@Observable` model,
  `URLSession`/`Codable` networking via `async`/`await` with loading/error states, an actor-isolated cache,
  navigation with passed state, and a persistence round-trip — covered by XCTest + an XCUITest,
  buildable/testable via `xcodebuild`.
- **Concepts exercised**: [ ] SwiftUI + `@State`/`@Binding` (co-03, co-05, co-06) [ ] MVVM + `@Observable`
  (co-18, co-07) [ ] `async`/`await` `URLSession`/`Codable` networking + loading/error states (co-21,
  co-20, co-22, co-19) [ ] an actor-isolated cache (co-23) [ ] navigation + passed state + a persistence
  round-trip (co-16, co-26) [ ] XCTest + XCUITest (co-29, co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a SwiftUI screen under MVVM with an `@Observable` model. Verify state
     changes update the view and `xcodebuild test` runs.
  2. Add `async`/`await` `URLSession` networking (`Codable`) with loading/error states + an actor cache.
     Verify a network error shows the error state and the cache is actor-isolated (an XCTest covers the
     model).
  3. Add navigation with passed state + a persistence round-trip. Verify navigating preserves state and data
     survives relaunch; add an XCUITest asserting the flow.
- **Acceptance criteria**: the app builds + runs on a simulator; networking has proper loading/error states;
  the cache is actor-isolated; navigation + persistence work; XCTest + XCUITest pass via `xcodebuild test`.
- **Done bar**: runnable end-to-end (simulator/device) + tests green + web-verified.

## Read more

**Books**

- **iOS Programming: The Big Nerd Ranch Guide**, 7th ed. — Christian Keur & Aaron Hillegass (2020, Big Nerd Ranch/Addison-Wesley). The longstanding classic hands-on iOS primer (Swift 5 / iOS 13 era; pair with official SwiftUI docs for current practice).

**Papers & articles**

- **Human Interface Guidelines** — Apple, official. The canonical design reference for all Apple platforms, including iOS. <https://developer.apple.com/design/human-interface-guidelines/>
- **SwiftUI Tutorials** — Apple Developer Documentation, official. Apple's own hands-on onboarding path for modern SwiftUI-based iOS development. <https://developer.apple.com/tutorials/swiftui>
- **SwiftUI documentation** — Apple Developer Documentation, official. The authoritative API reference for SwiftUI. <https://developer.apple.com/documentation/swiftui>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Mobile & CLI platforms — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Mobile & desktop platforms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 11 · Mobile & desktop platforms.

> _Content originated in the now-closed FS-SE plan (topic 71); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
