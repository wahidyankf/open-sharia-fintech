# 73 · Hybrid App Development ◆ (By Example, Dart †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · Dart † · Learn 173 / Drill 273 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: one codebase, many targets — Flutter's widget model, state management, and building for
mobile plus desktop from a single Dart codebase, with the cross-platform trade-offs kept explicit rather
than hidden. The usable language slice is the prerequisite [`72-just-enough-dart`](./72-just-enough-dart.md),
and the UI-composition instincts carry over from [`14-frontend-essentials`](./14-frontend-essentials.md).
`†`: Dart driving the Flutter framework and the `flutter` CLI.

## Why this exists · the big idea

- **The problem before the solution**: shipping the same app to iOS, Android, and desktop meant writing and
  maintaining it two or three times over, in three languages and toolchains, with the platforms drifting out
  of sync — a tax on every feature and a source of "it works on Android but not iOS" bugs.
- **Keep-this-if-you-forget-everything**: Flutter renders its own pixels instead of wrapping each
  platform's native widgets, so one Dart codebase looks and behaves identically everywhere — you trade the
  last mile of native fidelity for a single UI you build once. Know exactly what that trade buys and what
  it costs.
- **Big ideas touched**: `abstraction-and-its-cost` (the single-codebase abstraction hides three platforms,
  and the hidden thing — platform-specific behavior, native look, plugin gaps — leaks precisely where the
  abstraction is thinnest), `coupling-vs-cohesion` (the widget tree keeps a screen's structure and behavior
  cohesive, while state management decides how tightly UI couples to the data that drives it).

## Prerequisites

- **Prior topics**: [topic 72 Just Enough Dart](./72-just-enough-dart.md) (null-safe Dart, async/await,
  classes/mixins) and [topic 14 Frontend Essentials](./14-frontend-essentials.md) (declarative UI,
  component composition, layout thinking).
- **Tools & environment**: a macOS/Linux/Windows machine; the **Flutter SDK** (`flutter`) and Dart SDK
  pinned to a current stable; at least one target toolchain (an Android emulator, an iOS simulator on macOS,
  or a desktop target); Neovim/VSCode with the Dart LSP (DD-17).
- **Assumed knowledge**: writing null-safe Dart with async/await and classes (topic 72); thinking in a
  declarative component tree (topic 14); running a CLI build/run tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the Flutter/Dart SDK at "a current stable" in shipped text — the widget model,
  `StatelessWidget`/`StatefulWidget`, `BuildContext`, the `flutter` CLI (`create`/`run`/`build`/`test`), and
  the multi-target build story (mobile + desktop) are stable and correctly unpinned. Flutter and Dart
  release on a moving cadence, so a pinned number would go stale fast.
- 2026-07-12 — verified (GAP for plan owner): the body names Flutter's built-in state options but does not
  commit to a specific third-party state-management package — re-verify the chosen package name/version once
  the worked examples are drafted, and keep the vanilla-first (`setState`) tier as the baseline.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official docs.flutter.dev / api.flutter.dev / pub.dev page the
> pre-authoring `web-researcher` sweep fetched and read. `[Verified]` = a directly-read primary quote;
> `[Needs Verification]` = currency or capture caveat. Keep the SDK/package versions UNPINNED in shipped
> prose — Flutter and its ecosystem move fast.

- **Versions** — current stable per Flutter's release feed is **Flutter 3.44.6** bundling **Dart 3.12.2**
  (2026-07-09); `http` **1.6.0**, `shared_preferences` **2.5.5**, `sqflite` **2.4.3**, `go_router` **17.3.0**,
  `provider` **6.1.5+1** at fetch time. Keep all UNPINNED; tell learners to run `flutter --version`.
  `[Verified]` on the feed snapshot; a within-patch Dart-version churn note is `[Needs Verification]` but
  immaterial since the body pins no number.
- **Widgets** — docs.flutter.dev/ui: "you build your UI out of widgets"; author widgets "as subclasses of
  either `StatelessWidget` or `StatefulWidget`, depending on whether your widget manages any state." A
  `StatefulWidget`'s `State` object is "persistent between calls to `build()`, allowing them to remember
  information." `build(BuildContext)` "is called when this widget is inserted into the tree ... and when the
  dependencies of this widget change" (api.flutter.dev). `[Verified]`
- **State lifecycle & setState** — api.flutter.dev/State: `createState()` → `initState()` → `build()`;
  `dispose()` "Subclasses should override this method to release any resources retained by this object";
  `setState()` "indicates that some internal state has changed in a way that might impact the user
  interface in this subtree." `[Verified]`
- **InheritedWidget & state management** — api.flutter.dev/InheritedWidget: "Base class for widgets that
  efficiently propagate information down the tree." docs.flutter.dev/data-and-backend/state-mgmt/options
  explicitly names **`package:provider`** ("This is what `package:provider` ... use[s] under the hood") and
  the "Simple app state management" page teaches `ChangeNotifier` + `ChangeNotifierProvider` + `Consumer`.
  **IMPORTANT (DD-35)**: the current official state-mgmt pages name ONLY `provider`; **Riverpod / bloc are
  widely-used COMMUNITY packages, NOT officially name-checked by docs.flutter.dev at fetch time** — frame
  them as ecosystem options (pub.dev), not an official recommendation. `[Verified]` on provider;
  `[Needs Verification]` that official docs name Riverpod (they do not, per direct fetch).
- **Layout** — docs.flutter.dev/ui/layout: a `Row`/`Column` takes "a list of children widgets"; alignment
  via `mainAxisAlignment` and `crossAxisAlignment` ("For a row, the main axis runs horizontally and the
  cross axis runs vertically"); `Container` adds padding/margins/borders around a single child; `Stack`
  arranges widgets "on top of a base widget"; `Expanded` sizes a child "to fit within a row or column."
  `[Verified]` (`Flexible`'s dedicated page not fetched verbatim — `[Needs Verification]` on its exact
  quote).
- **Material & Cupertino** — api.flutter.dev: `MaterialApp` "An application that uses Material Design ...
  wraps a number of widgets that are commonly required"; `Scaffold` "Implements the basic Material Design
  visual layout structure"; `ElevatedButton` "A Material Design 'elevated button'"; `CupertinoApp` "An
  application that uses Cupertino design." (`Text` is a `widgets`-library basic — `[Needs Verification]` on
  its exact page.) `[Verified]` on the rest.
- **Navigation** — docs.flutter.dev/ui/navigation: `Navigator.of(context).push(MaterialPageRoute(...))` /
  `.pop()`; named routes via `MaterialApp.routes` + `Navigator.pushNamed`; and the OFFICIAL steer to
  `go_router`: "We don't recommend using named routes for most applications. Instead, use [go_router] ... or
  use `Navigator` with `MaterialPageRoute`." `go_router` is published by the verified **flutter.dev**
  publisher (a "declarative router ... supporting deep linking"). `[Verified]`
- **Async UI** — api.flutter.dev: `FutureBuilder` "builds itself based on the latest snapshot of interaction
  with a `Future`"; `StreamBuilder` the `Stream` analogue; both require obtaining the future/stream in
  `initState`, not `build`. `[Verified]`
- **Networking & persistence** — pub.dev: `http` (dart.dev publisher) "a composable, Future-based library
  for making HTTP requests"; `dart:convert`'s `jsonDecode` "Parses the string and returns the resulting Json
  object"; `shared_preferences` (flutter.dev) "reading and writing simple key-value pairs. Wraps
  NSUserDefaults on iOS and SharedPreferences on Android"; `sqflite` "Flutter plugin for SQLite." `[Verified]`
- **Platform channels** — docs.flutter.dev/platform-integration/platform-channels: `MethodChannel` "A named
  channel ... to communicate with platform plugins using asynchronous method calls ... not type safe";
  "Messages and responses are passed asynchronously"; invoke channel methods "on the platform's main
  thread." `[Verified]`
- **Multi-target build & CLI** — docs.flutter.dev/reference/flutter-cli: `flutter create` "Creates a new
  project", `flutter run` "Runs a Flutter program", `flutter build <target>` "Build a target-specific
  bundle", `flutter test` "Runs tests in this package. Use instead of `dart test`", `flutter pub get`.
  DevTools is "a suite of performance and debugging tools." `[Verified]`
- **Testing** — docs.flutter.dev/testing/overview: unit test ("a single function, method, or class"), widget
  test ("a single widget ... verify that the widget's UI looks and interacts as expected"), integration test
  ("a complete app or a large part of an app ... runs on a real device or an OS emulator"); the SDK ships the
  `integration_test` package; `testWidgets(...)` "Runs the callback inside the Flutter test environment"
  passing a `WidgetTester`. `[Verified]`

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · flutter-cli** — `flutter create`/`run`/`build`/`test` scaffold, run, build, and test an app; DevTools inspects a running app.
- **co-02 · everything-is-a-widget** — a Flutter UI is a tree of widgets; layout, styling, and structure are all widgets.
- **co-03 · stateless-widget** — a `StatelessWidget` describes UI purely from its configuration via `build(BuildContext)`.
- **co-04 · stateful-widget** — a `StatefulWidget` pairs with a persistent `State` object that survives rebuilds and holds mutable state.
- **co-05 · build-context** — `BuildContext` locates a widget in the tree and gives access to inherited data and theme.
- **co-06 · widget-composition** — screens are built by composing small widgets (composition over inheritance).
- **co-07 · state-lifecycle** — `State` runs `initState()` on creation and `dispose()` on removal to acquire and release resources.
- **co-08 · setstate** — `setState(() => ...)` marks state dirty so Flutter rebuilds the affected subtree (the vanilla state tier).
- **co-09 · layout-widgets** — `Row`, `Column`, `Container`, and `Stack` arrange and decorate children.
- **co-10 · flex-layout** — `Expanded`/`Flexible` distribute space; `mainAxisAlignment`/`crossAxisAlignment` position children along the axes.
- **co-11 · constraints-model** — layout is "constraints go down, sizes go up"; Flutter draws its own pixels rather than wrapping native controls.
- **co-12 · material-widgets** — `MaterialApp`, `Scaffold`, `AppBar`, `Text`, and `ElevatedButton` build a standard Material screen.
- **co-13 · cupertino-widgets** — `CupertinoApp` and the Cupertino widgets provide an iOS-styled alternative (survey).
- **co-14 · lists** — `ListView` / `ListView.builder` render scrolling collections, building rows lazily.
- **co-15 · inherited-widget** — an `InheritedWidget` propagates data down the tree efficiently, the basis of most state solutions.
- **co-16 · provider** — `package:provider` (`ChangeNotifier` + `ChangeNotifierProvider` + `Consumer`) is the practical shared-state tier.
- **co-17 · reactive-store** — for larger apps, a reactive store (community packages like Riverpod/bloc) scales state beyond provider.
- **co-18 · ephemeral-vs-app-state** — local UI state belongs in `setState`; state shared across screens belongs in an app-state solution.
- **co-19 · navigation-imperative** — `Navigator.push`/`pop` with `MaterialPageRoute` moves between screens imperatively.
- **co-20 · named-routes** — a `routes` map + `Navigator.pushNamed` centralizes route names.
- **co-21 · go-router** — `go_router` (Flutter's recommended package over named routes) declares routes with deep-linking support.
- **co-22 · async-ui** — `FutureBuilder`/`StreamBuilder` render UI from the latest snapshot of a `Future`/`Stream`.
- **co-23 · networking** — the `http` package fetches data; `dart:convert`'s `jsonDecode` parses JSON into Dart maps/objects.
- **co-24 · local-persistence** — `shared_preferences` stores key-value pairs; `sqflite` provides a local SQLite database.
- **co-25 · platform-channels** — a `MethodChannel` reaches native platform code with asynchronous, untyped method calls.
- **co-26 · plugins** — pub.dev plugins package native capabilities behind a Dart API so you rarely write channel code by hand.
- **co-27 · multi-target-build** — `flutter build` produces mobile and desktop artifacts from one Dart codebase.
- **co-28 · adaptive-responsive-layout** — `LayoutBuilder`/`MediaQuery` reflow the UI across phone and desktop form factors.
- **co-29 · testing** — Flutter has unit, widget (`testWidgets` + `WidgetTester` from `flutter_test`), and integration (`integration_test`) test tiers.
- **co-30 · cross-platform-tradeoffs** — own-pixel rendering trades last-mile native fidelity and binary size for one consistent codebase; the abstraction leaks at platform edges.

## Worked examples

Colocated under `hybrid-app-development/learning/code/`; each runnable via the `flutter` CLI on at least one target (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · flutter-create** — `flutter create myapp` scaffolds an app — verify it runs on a target. (co-01)
- **ex-02 · flutter-run** — `flutter run` the counter template — verify hot reload works. (co-01)
- **ex-03 · flutter-test-cmd** — `flutter test` the default widget test — verify it passes. (co-01)
- **ex-04 · everything-widget** — build a screen entirely from widgets — verify no non-widget UI. (co-02)
- **ex-05 · stateless-widget** — a `StatelessWidget` rendering `Text` — verify it displays. (co-03)
- **ex-06 · build-method** — read config in `build(BuildContext context)` — verify the value renders. (co-03, co-05)
- **ex-07 · compose-widgets** — extract a card into its own widget and reuse it — verify composition. (co-06)
- **ex-08 · stateful-widget** — a `StatefulWidget` with a `State` field — verify state persists across rebuilds. (co-04)
- **ex-09 · setstate-counter** — increment in `setState` — verify the label updates. (co-08, co-04)
- **ex-10 · state-initstate** — acquire a resource in `initState` — verify it runs once on creation. (co-07)
- **ex-11 · state-dispose** — release it in `dispose` — verify cleanup on removal. (co-07)
- **ex-12 · buildcontext-use** — read `Theme.of(context)` — verify theme access. (co-05)
- **ex-13 · column-layout** — stack widgets in a `Column` — verify vertical order. (co-09)
- **ex-14 · row-layout** — lay out a `Row` — verify horizontal order. (co-09)
- **ex-15 · container-decoration** — a `Container` with padding + color — verify styling. (co-09)
- **ex-16 · stack-overlay** — overlay a badge with `Stack` — verify layering. (co-09)
- **ex-17 · expanded-flex** — `Expanded` children sharing space — verify proportional sizing. (co-10)
- **ex-18 · mainaxis-alignment** — `mainAxisAlignment: spaceBetween` — verify spacing. (co-10)
- **ex-19 · crossaxis-alignment** — `crossAxisAlignment: start` — verify cross-axis position. (co-10)
- **ex-20 · materialapp-scaffold** — wrap the app in `MaterialApp` + `Scaffold` — verify structure. (co-12)
- **ex-21 · appbar** — a `Scaffold` `AppBar` with a title — verify the bar renders. (co-12)
- **ex-22 · elevatedbutton** — an `ElevatedButton(onPressed:)` — verify the tap fires. (co-12)
- **ex-23 · text-widget** — a styled `Text` — verify the string displays. (co-12)
- **ex-24 · cupertino-survey** — a `CupertinoApp`/`CupertinoButton` — verify the iOS-styled widget renders. (co-13)
- **ex-25 · listview-static** — a `ListView` of fixed children — verify scrolling. (co-14)
- **ex-26 · listview-builder** — `ListView.builder` over 1,000 items — verify lazy row building. (co-14)

### Intermediate

- **ex-27 · constraints-model** — a widget sized by parent constraints — verify constraints-down/sizes-up behavior. (co-11)
- **ex-28 · own-pixels-render** — the same widget renders identically on two platforms — verify pixel consistency. (co-11)
- **ex-29 · inherited-widget** — a custom `InheritedWidget` exposing data — verify descendants read it. (co-15)
- **ex-30 · inherited-of-context** — `MyData.of(context)` — verify the lookup returns the value. (co-15)
- **ex-31 · provider-changenotifier** — a `ChangeNotifier` model + `ChangeNotifierProvider` — verify it's provided. (co-16)
- **ex-32 · provider-consumer** — a `Consumer` reading the model — verify it rebuilds on `notifyListeners`. (co-16)
- **ex-33 · provider-across-screens** — shared model across two screens — verify both reflect updates. (co-16)
- **ex-34 · ephemeral-state** — a checkbox using `setState` — verify local-only state. (co-18)
- **ex-35 · app-state-shared** — cart state lifted to app-state — verify it survives screen changes. (co-18)
- **ex-36 · reactive-store-intuition** — sketch the same state in a reactive store (Riverpod/bloc) — verify the scaling rationale. (co-17)
- **ex-37 · navigator-push** — `Navigator.push` a detail screen — verify the push. (co-19)
- **ex-38 · navigator-pop** — `Navigator.pop` back — verify return to the list. (co-19)
- **ex-39 · materialpageroute** — a `MaterialPageRoute` builder — verify the transition. (co-19)
- **ex-40 · named-route** — a `routes` map — verify route names resolve. (co-20)
- **ex-41 · pushnamed** — `Navigator.pushNamed(context, '/detail')` — verify navigation. (co-20)
- **ex-42 · go-router-declarative** — a `GoRouter` with two routes — verify declarative routing. (co-21)
- **ex-43 · go-router-params** — a path parameter `/item/:id` — verify the id passes. (co-21)
- **ex-44 · futurebuilder** — a `FutureBuilder` over an async load — verify loading/done states. (co-22)
- **ex-45 · streambuilder** — a `StreamBuilder` over a stream — verify live updates. (co-22)
- **ex-46 · http-get** — `http.get(url)` — verify a response returns. (co-23)
- **ex-47 · json-decode** — `jsonDecode(body)` into a model — verify typed fields. (co-23)
- **ex-48 · http-to-widget** — a `FutureBuilder` rendering fetched JSON — verify the list shows. (co-23, co-22)
- **ex-49 · shared-preferences** — write/read a preference — verify it persists across relaunch. (co-24)
- **ex-50 · sqflite-crud** — insert + query with `sqflite` — verify the round-trip. (co-24)
- **ex-51 · persistence-roundtrip** — save data, relaunch, read — verify survival. (co-24)
- **ex-52 · listview-from-network** — a `ListView.builder` over fetched data — verify rows reflect the response. (co-14, co-23)
- **ex-53 · loading-error-state** — spinner + error UI from an async load — verify each state. (co-22, co-08)
- **ex-54 · provider-list-update** — add an item via provider — verify the list rebuilds. (co-16, co-14)

### Advanced

- **ex-55 · platform-channel-method** — a `MethodChannel` invoke from Dart — verify the call reaches native. (co-25)
- **ex-56 · platform-channel-native-side** — implement the native handler — verify it returns a value. (co-25)
- **ex-57 · plugin-use** — use a pub.dev plugin for a native capability — verify it works via its Dart API. (co-26)
- **ex-58 · platform-fallback** — handle an unsupported platform gracefully — verify the documented fallback. (co-25, co-30)
- **ex-59 · flutter-build-android** — `flutter build apk` — verify an Android artifact is produced. (co-27)
- **ex-60 · flutter-build-desktop** — `flutter build macos`/`windows`/`linux` — verify a desktop artifact. (co-27)
- **ex-61 · single-codebase-two-targets** — build the same code for two targets — verify one codebase, two binaries. (co-27)
- **ex-62 · layoutbuilder-adaptive** — a `LayoutBuilder` switching layout on width — verify the branch. (co-28)
- **ex-63 · mediaquery-breakpoint** — `MediaQuery.of(context).size` breakpoint — verify the responsive choice. (co-28)
- **ex-64 · phone-desktop-reflow** — a list that becomes a master-detail on wide screens — verify the reflow. (co-28)
- **ex-65 · responsive-master-detail** — a full master-detail adaptive layout — verify both form factors. (co-28)
- **ex-66 · widget-test-testwidgets** — a `testWidgets` pumping a widget — verify a `find` locates it. (co-29)
- **ex-67 · widget-test-tap** — `tester.tap` + `pump` then assert — verify interaction. (co-29)
- **ex-68 · unit-test-logic** — a pure unit test of a model method — verify the assertion. (co-29)
- **ex-69 · integration-test** — an `integration_test` driving the app — verify the flow on a device/emulator. (co-29)
- **ex-70 · flutter-test-run** — `flutter test` the whole suite — verify all pass. (co-29, co-01)
- **ex-71 · tradeoff-fidelity** — compare a Material widget's look to native — verify the fidelity gap is understood. (co-30)
- **ex-72 · tradeoff-binary-size** — measure the app's install size vs a thin native app — verify the overhead. (co-30)
- **ex-73 · leak-at-edges** — surface a platform-specific behavior (permissions/keyboard) — verify the leak is contained in channel code. (co-30, co-25)
- **ex-74 · provider-navigation-combined** — pass provider-held state through navigation — verify the detail reads it. (co-16, co-19)
- **ex-75 · adaptive-with-state** — an adaptive layout driven by shared state — verify both reflow and state work. (co-28, co-16)
- **ex-76 · network-list-persisted** — fetch, cache in `sqflite`, show offline — verify cached data appears. (co-23, co-24)
- **ex-77 · screen-widget-state-slice** — wire one screen: composed widgets ← provider state ← a stateful root — verify the slice. (co-03, co-04, co-16)
- **ex-78 · capstone-multiplatform** — a multi-screen app with a composed widget tree, provider state, navigation, adaptive layout, a platform-channel call with a fallback, built for two targets — verify `flutter run` works on phone + desktop and `flutter build` succeeds for both. (co-06, co-16, co-19, co-28, co-25, co-27)

## Tensions & trade-offs — when NOT to reach for this

- **When native fidelity is the product**: an app whose value is deep platform integration, the exact
  native look-and-feel, or bleeding-edge OS APIs is fighting Flutter's own-rendering model. If your users
  will notice the difference, a native codebase (or a platform-native design system) may win despite the
  duplication.
- **The abstraction leaks at the edges**: date pickers, keyboards, permissions, background execution, and
  new OS features surface platform-specific behavior right through the "write once" promise. Every serious
  Flutter app carries some platform-channel and per-platform code — budget for it rather than being
  surprised by it.
- **Binary size and cold start**: bundling a rendering engine costs app size and startup time versus a thin
  native app. For a tiny utility or an app where install size is a conversion metric, that overhead may not
  be worth the shared codebase.

## Lineage — why it beat the alternative

- Cross-platform UI has a graveyard of approaches: write-native-twice (correct but expensive),
  WebView-in-a-shell hybrids like early Cordova/PhoneGap (one codebase but sluggish and un-native), and
  bridge-to-native-widgets like React Native (native controls but a serialization bridge and per-platform
  quirks). Flutter took a different bet — ship a rendering engine and draw every pixel itself — which
  eliminated the bridge and delivered pixel-identical, high-frame-rate UI across targets, at the cost of
  native-widget fidelity. That bet won for teams who value one consistent UI and a single codebase over
  last-mile nativeness. The widget-composition and state-management instincts built here transfer directly
  to the next primer's platform work in [`74-just-enough-csharp`](./74-just-enough-csharp.md) and to any
  declarative-UI framework you meet later.

## Capstone materials

Colocated under `hybrid-app-development/learning/code/`; each runnable via the `flutter` CLI on at least
one target (DD-20/DD-30).

- **beginner** — a `StatelessWidget` screen composed from smaller widgets, plus a `StatefulWidget` counter
  driven by `setState`.
- **intermediate** — the same app refactored to a provider/inherited-state approach with navigation between
  two screens, run on two form factors (phone + desktop) to show adaptive layout.
- **advanced** — reach a native capability through a platform channel/plugin and handle the
  platform-specific fallback, making the abstraction's leak explicit and contained.

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build one Flutter app from a single Dart codebase that runs on mobile and desktop — a multi-
  screen app with a chosen state-management approach, adaptive layout across form factors, and one native
  capability reached through a platform channel with a documented per-platform fallback.
- **Concepts exercised**: [ ] composed widget tree (Stateless + Stateful) (co-03, co-04, co-06) [ ] a
  state-management approach beyond `setState` (co-16) [ ] navigation across screens (co-19) [ ] adaptive
  layout for phone + desktop (co-28) [ ] a platform-channel/plugin call (co-25) [ ] `flutter build` for two
  targets (co-27).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a multi-screen app with a composed widget tree and navigation. Verify
     `flutter run` renders and navigates on one target.
  2. Introduce a state-management approach (provider/inherited or a reactive store) driving shared state.
     Verify state updates propagate across screens without manual `setState` plumbing.
  3. Add adaptive layout so the UI reflows between phone and desktop. Verify `flutter run` looks correct on
     both form factors.
  4. Reach one native capability via a platform channel/plugin with a fallback. Verify the feature works on
     one platform and degrades gracefully where unsupported, and that `flutter build` succeeds for two
     targets.
- **Acceptance criteria**: one codebase builds and runs on two targets; state management works across
  screens; layout adapts to form factor; the native call succeeds with a documented fallback; the
  platform-specific leak is contained, not hidden.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Flutter in Action** — Eric Windmill (2020, Manning). A well-regarded, widely recommended book-length
  primer on Flutter and Dart for building cross-platform apps.

**Papers & articles**

- **Flutter documentation** — official (docs.flutter.dev). The authoritative source for widgets, guides,
  and platform integration. <https://docs.flutter.dev/>
- **Flutter API reference** — official (api.flutter.dev). The canonical framework API reference.
  <https://api.flutter.dev/>

---

← Previous: [72 · Just Enough Dart](./72-just-enough-dart.md) · Next: [74 · Just Enough C#](./74-just-enough-csharp.md) →
