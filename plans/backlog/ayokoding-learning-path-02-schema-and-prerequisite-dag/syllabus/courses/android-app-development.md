# Android App Development (By Example, Kotlin)

**Course ID**: `android-app-development` · **Format**: By Example · **Language**: Kotlin.

**Short summary**: Native Android apps with Kotlin and the SDK

**Scope note**: `◆` app-domain — building a real Android app: fundamentals (activities/lifecycle/manifest/
intents), Jetpack Compose UI + state, ViewModel/unidirectional-data-flow architecture, Room/DataStore/
Retrofit data, coroutines/flows, platform concerns, and applied testing. **Tooling note (DD-17)**: Android
Studio + the Android SDK/Gradle are the practical baseline (emulator/AVD); the topic favours the Gradle CLI
(`./gradlew`) for the raw build/test form.

## Why this exists · the big idea

- **The problem before the solution**: an Android app juggles UI, lifecycle, background work, local and
  remote data, and config changes at once — without a disciplined architecture these concerns tangle and
  the app loses its state on every screen rotation.
- **Keep-this-if-you-forget-everything**: hoist state out of the UI into a ViewModel and drive the screen
  with unidirectional data flow — the UI becomes a pure function of state that survives the platform yanking
  it around.
- **Big ideas touched**: `coupling-vs-cohesion` — ViewModel and repository layering keep what changes
  together (the UI) apart from what changes on its own schedule (data, lifecycle); `layering-and-leaks` —
  the Android platform (activities, config changes, permissions) bleeds into your app, and the architecture
  exists to seal those leaks.

## Prerequisites

- **Prior topics**: [topic 68 Just Enough Kotlin](./just-enough-kotlin.md) (the language + coroutines),
  [topic 14 Frontend Essentials](./frontend-essentials.md) (components, state, accessible UI), and
  [topic 47 Advanced Frontend](./advanced-frontend.md) (declarative UI, state management, optimistic
  updates).
- **Tools & environment**: a macOS/Linux (or Windows) machine; **Android Studio** + the **Android SDK** +
  **Gradle** (`./gradlew`); an emulator/AVD or a device; a JDK. Favour the Gradle CLI for build/test.
- **Assumed knowledge**: Kotlin syntax + coroutines (topic 68); component + state UI thinking (topics
  14/47); calling an HTTP API (topic 11).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: Jetpack Compose BOM ~**2026.06.01** (Compose core ~1.11.x); Android Studio stable
  line is "Quail" (2026.1.1 Patch 2, stable 2026-04-28). Room, DataStore, Retrofit, coroutines/flows, and
  JUnit + Compose UI testing via `./gradlew test` remain Google's/Square's current recommended stack.
- 2026-07-12 — verified (TIME-SENSITIVE, re-check at authoring): **minimum/target SDK** — starting
  **2026-08-31**, all **new** Google Play submissions/updates must **target Android 16 (API 36)**; existing
  published apps must target at least **Android 15 (API 35)** to stay visible on Android 16/17 devices
  (extensions to 2026-11-01 available). This deadline falls near the authoring window and Google has moved
  it before — re-confirm the exact date + API numbers immediately before publishing.
  (developer.android.com/google/play/requirements/target-sdk)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official developer.android.com / AndroidX / Square page the pre-authoring
> `web-researcher` sweep fetched and read. `[Needs Verification]` marks items not captured verbatim or with
> live currency risk. Android/Compose/AndroidX move fast — re-verify versions immediately before publish.

- **Versions** — Android Studio **Quail 2026.1.1** (stable) + AGP **9.2.0** + **Kotlin 2.4.0**; Jetpack
  Compose BOM ~**2026.06.01**. Android 16 (**API 36**) is unambiguously stable
  (developer.android.com/tools/releases/platforms); Android 17 (**API 37**) GA is asserted by the
  2026-06-16 Android Developers blog but the release-notes page still showed betas at fetch time —
  `[Needs Verification]` on Android 17 GA; cite API 36 as the safe current-stable in shipped text.
  `[Verified]` on Studio/AGP/Kotlin/Compose-BOM.
- **Activity lifecycle** — developer.android.com/guide/components/activities/activity-lifecycle, verbatim
  callback order `onCreate → onStart → onResume → onPause → onStop → onDestroy`: "onCreate() ... You must
  implement this callback, which fires when the system first creates the activity"; "onPause() ... the
  first indication that the user is leaving your activity"; "onDestroy() is called before the activity is
  destroyed." `[Verified]`
- **Manifest** — developer.android.com/guide/topics/manifest/manifest-intro: the manifest "describes
  essential information about your app to the Android build tools, the Android operating system, and Google
  Play"; declares the app's components, the permissions it needs, and required device features.
  `[Verified]`
- **Intents** — developer.android.com/guide/components/intents-filters: an explicit intent "specifies which
  application will satisfy the intent, by supplying either the target app's package name or a fully-qualified
  component class name"; an implicit intent "declare[s] a general action to perform, which allows a component
  from another app to handle it"; started via `startActivity(intent)`. `[Verified]`
- **Compose** — developer.android.com/develop/ui/compose (Thinking in Compose / State): `@Composable`
  "tells the Compose compiler that this function is intended to convert data into UI"; recomposition is
  "the process of calling your composable functions again when inputs change"; `remember` "stores the
  object in the Composition during initial composition, and returns the stored value during
  recomposition"; `mutableStateOf` "creates an observable `MutableState<T>`"; state hoisting = "a pattern
  of moving state to a composable's caller to make a composable stateless" (`value: T` +
  `onValueChange: (T) -> Unit`). `setContent` and `@Preview` were not captured verbatim this pass —
  `[Needs Verification]` on those two, `[Verified]` on the rest.
- **ViewModel & UDF** — developer.android.com/topic/libraries/architecture/viewmodel + /topic/architecture:
  a ViewModel "allows your data to survive configuration changes such as screen rotations" and "exposes
  state to the UI and encapsulates related business logic"; `viewModelScope` is "a `CoroutineScope`
  ... automatically cancelled when the ViewModel is cleared"; UDF = "state flows down and events flow up";
  layers = UI / (optional) domain / data, with the repository classes "expos[ing] data to the rest of the
  app" and "centraliz[ing] changes to the data." `StateFlow` + `stateIn(viewModelScope,
SharingStarted.WhileSubscribed(5_000), initialValue)` is the recommended UI-state output;
  `collectAsStateWithLifecycle` (in `lifecycle-runtime-compose`) collects lifecycle-aware. Exact
  `collectAsStateWithLifecycle` signature not captured verbatim — `[Needs Verification]` on the signature,
  `[Verified]` on existence + dependency + UDF/ViewModel quotes.
- **Room** — developer.android.com/training/data-storage/room: `@Entity` (a table via a data class),
  `@Dao` ("contains the methods used for accessing the database"), `@Database` (abstract class extending
  `RoomDatabase`); "In Room 2.1 and higher, you can use the `suspend` keyword ... to make your DAO queries
  asynchronous"; "In Room 2.2 and higher, you can use Kotlin's `Flow` ... to write observable queries";
  "Room doesn't allow database access on the main thread." `[Verified]`
- **DataStore** — developer.android.com/topic/libraries/architecture/datastore: "Jetpack DataStore is a
  data storage solution that ... uses Kotlin coroutines and Flow to store data asynchronously"; "If you're
  currently using SharedPreferences to store data, consider migrating to DataStore instead" (a
  recommendation to migrate, NOT a formal deprecation of SharedPreferences). `[Verified]`
- **Retrofit** — github.com/square/retrofit: `suspend`-function support landed in **2.6.0** (2019). The
  current stable line is **Retrofit 3.x** (**3.0.0**, on OkHttp 4.12) — most tutorials still cite 2.x, so
  pin `com.squareup.retrofit2:retrofit:3.0.0` (or state a 2.x pin deliberately). Version-drift flagged.
  `[Verified]`
- **Coroutines/Flow on Android** — developer.android.com/kotlin/coroutines: `viewModelScope` "is a
  predefined `CoroutineScope` that is included with the ViewModel KTX extensions ... automatically
  cancelled"; structured concurrency yields "fewer memory leaks." `lifecycleScope` +
  `repeatOnLifecycle(Lifecycle.State.STARTED)` for UI-layer collection: `[Needs Verification]` on exact
  wording (not fetched verbatim), API existence not in doubt.
- **Testing** — developer.android.com/training/testing: local unit tests live under `src/test/` and run on
  the JVM (`junit:junit`); instrumented tests under `src/androidTest/` run on a device/emulator via
  `AndroidJUnitRunner` + Espresso; Compose UI tests use `createComposeRule()` /
  `createAndroidComposeRule<Activity>()` with `@get:Rule`, `.onNodeWithText(...)`, `.performClick()`,
  `.assertIsDisplayed()`; `./gradlew test` runs local tests (reports under `build/reports/tests/`),
  `./gradlew connectedAndroidTest` runs instrumented tests. `[Verified]`

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · project-and-gradle** — an Android app is a Gradle project (`settings.gradle`, module `build.gradle`, `./gradlew` wrapper); the build produces an APK/AAB.
- **co-02 · manifest** — `AndroidManifest.xml` declares the app's components, the permissions it needs, and required device features to the OS and Play.
- **co-03 · activity-lifecycle** — an activity moves through `onCreate → onStart → onResume → onPause → onStop → onDestroy`; each callback marks a visibility/foreground transition.
- **co-04 · intents** — an `Intent` starts a component; explicit intents name the target class/package, implicit intents declare an action another app can handle.
- **co-05 · composable-functions** — `@Composable` functions describe UI as a function of data; `setContent { }` hosts the Compose tree in an activity.
- **co-06 · recomposition** — Compose re-invokes composables when their inputs change, skipping those whose inputs did not — UI is redrawn from state, not mutated in place.
- **co-07 · compose-state** — `remember { mutableStateOf(...) }` holds observable state across recompositions; reading it subscribes the composable to changes.
- **co-08 · state-hoisting** — moving state up to a caller makes a composable stateless: it takes `value` + an `onValueChange` event callback, so state has a single owner.
- **co-09 · modifiers** — `Modifier` chains decorate a composable (padding, size, click, background); order matters and each call returns a new modifier.
- **co-10 · preview** — `@Preview` renders a composable in the IDE without running the app, for fast visual iteration.
- **co-11 · layout-composables** — `Column`, `Row`, and `Box` arrange children vertically, horizontally, and stacked; alignment/arrangement position them.
- **co-12 · material-components** — `Scaffold`, `TopAppBar`, `Button`, `Text`, and `TextField` are Material 3 building blocks for a standard screen.
- **co-13 · lazy-lists** — `LazyColumn` renders only the visible items of a large list via an `items(...)` block, recycling as you scroll.
- **co-14 · viewmodel** — a `ViewModel` holds UI state and business logic, survives configuration changes, and owns a `viewModelScope` that is cancelled when it clears.
- **co-15 · unidirectional-data-flow** — state flows down (ViewModel → UI) and events flow up (UI → ViewModel); the UI is a rendering of a single source of truth.
- **co-16 · stateflow** — a ViewModel exposes UI state as an immutable `StateFlow`; the UI collects it lifecycle-aware via `collectAsStateWithLifecycle()`.
- **co-17 · ui-state-modeling** — model a screen's state as loading/success/error (often a sealed hierarchy) so every case renders deterministically.
- **co-18 · repository-pattern** — a repository abstracts data sources behind an interface and is the single source of truth the ViewModel talks to.
- **co-19 · room-entities-dao** — Room maps `@Entity` data classes to tables, `@Dao` methods to queries, and an abstract `@Database` to the SQLite database.
- **co-20 · room-suspend-flow** — Room DAO methods can be `suspend` (one-shot, off the main thread) or return a `Flow` (observable, re-emitting on change).
- **co-21 · datastore** — DataStore stores key-value or typed preferences asynchronously via coroutines/Flow, and is the recommended replacement for SharedPreferences.
- **co-22 · retrofit** — Retrofit turns an annotated Kotlin interface into a type-safe HTTP client; `suspend` functions integrate with coroutines.
- **co-23 · json-parsing** — a converter (Moshi / kotlinx.serialization / Gson) deserializes JSON responses into Kotlin data classes.
- **co-24 · coroutines-on-android** — `viewModelScope`/`lifecycleScope` launch structured coroutines that cancel with their owner, keeping async work off the main thread.
- **co-25 · flows-on-android** — a `Flow` is a cold asynchronous stream; operators (`map`, `filter`) transform it and the UI collects it to react to changing data.
- **co-26 · navigation** — Navigation Compose routes between destinations with a `NavHost`/`NavController`, passing arguments and handling back.
- **co-27 · runtime-permissions** — dangerous permissions are requested at runtime; the app must handle grant/deny and degrade gracefully.
- **co-28 · config-change-survival** — rotation/config changes recreate the activity; `rememberSaveable` and the ViewModel preserve state across recreation.
- **co-29 · dependency-injection** — DI supplies collaborators (repositories, data sources) from outside a class rather than constructing them inside, aiding testability (manual DI or Hilt).
- **co-30 · applied-testing** — local JUnit unit tests (`src/test/`), instrumented tests (`src/androidTest/`), and Compose UI tests via `createComposeRule()`, run with `./gradlew test` / `connectedAndroidTest`.

## Worked examples

Colocated under `android-app-development/learning/code/`; each runnable/testable via Gradle (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · scaffold-project** — create an app module and build it with `./gradlew assembleDebug` — verify an APK lands under `build/outputs/apk/`. (co-01)
- **ex-02 · manifest-declare-activity** — declare the launcher activity in `AndroidManifest.xml` — verify the app launches to that screen. (co-02)
- **ex-03 · manifest-permission** — add `<uses-permission android:name="android.permission.INTERNET"/>` — verify a network call is permitted. (co-02)
- **ex-04 · activity-oncreate** — override `onCreate` and call `setContent` — verify the screen renders on launch. (co-03, co-05)
- **ex-05 · lifecycle-logging** — log each of the six lifecycle callbacks — verify Logcat prints them in `onCreate→onStart→onResume` order on launch. (co-03)
- **ex-06 · explicit-intent** — start a second activity with `Intent(this, DetailActivity::class.java)` — verify navigation lands on the detail screen. (co-04)
- **ex-07 · implicit-intent** — fire `Intent(Intent.ACTION_VIEW, uri)` — verify a browser opens the URL. (co-04)
- **ex-08 · composable-hello** — write a `@Composable fun Greeting()` rendering `Text("Hello")` — verify the text shows. (co-05)
- **ex-09 · setcontent-tree** — host a composable via `setContent { }` — verify no XML layout is needed. (co-05)
- **ex-10 · text-composable** — render dynamic `Text(name)` from a parameter — verify the passed value displays. (co-05)
- **ex-11 · recomposition-on-state** — a counter whose `Text` shows a state value — verify tapping updates the text (recomposition). (co-06)
- **ex-12 · remember-mutablestateof** — hold `var count by remember { mutableStateOf(0) }` — verify state persists across recompositions but resets on relaunch. (co-07)
- **ex-13 · state-counter** — a `Button` increments the remembered counter — verify each tap increments. (co-07)
- **ex-14 · hoisted-state** — hoist the counter's state to the caller, passing `value` + `onIncrement` — verify the child is stateless. (co-08)
- **ex-15 · stateless-reuse** — reuse the hoisted composable in two places with independent state — verify each instance counts separately. (co-08)
- **ex-16 · modifier-padding** — apply `Modifier.padding(16.dp)` — verify visible spacing. (co-09)
- **ex-17 · modifier-chain** — chain `.fillMaxWidth().padding(8.dp).clickable{}` — verify all three take effect. (co-09)
- **ex-18 · preview-annotation** — add `@Preview` to a composable — verify it renders in the IDE preview pane. (co-10)
- **ex-19 · column-layout** — stack three `Text`s in a `Column` — verify vertical order. (co-11)
- **ex-20 · row-layout** — place items in a `Row` with `Arrangement.SpaceBetween` — verify horizontal spread. (co-11)
- **ex-21 · box-overlay** — overlay a badge on an image with `Box` — verify the badge sits on top. (co-11)
- **ex-22 · scaffold-topbar** — wrap a screen in `Scaffold` with a `TopAppBar` — verify the bar renders above content. (co-12)
- **ex-23 · button-onclick** — a Material `Button(onClick = ...)` — verify the click fires. (co-12)
- **ex-24 · textfield-input** — an `OutlinedTextField` bound to hoisted state — verify typed text updates state. (co-12)
- **ex-25 · lazycolumn-list** — render 1,000 rows in a `LazyColumn` — verify smooth scroll (only visible rows composed). (co-13)
- **ex-26 · lazycolumn-items** — use `items(list) { row -> ... }` — verify each element renders once. (co-13)

### Intermediate

- **ex-27 · viewmodel-basic** — a `ViewModel` holding a counter, obtained via `viewModel()` — verify the composable reads it. (co-14)
- **ex-28 · viewmodelscope-coroutine** — launch work in `viewModelScope` — verify it cancels when the ViewModel clears. (co-14, co-24)
- **ex-29 · viewmodel-survives-rotation** — hold list state in the ViewModel — verify rotating the device keeps the data. (co-14, co-28)
- **ex-30 · udf-events-up** — pass a UI event lambda up to the ViewModel — verify the ViewModel mutates state, not the UI. (co-15)
- **ex-31 · udf-single-source** — render the screen purely from ViewModel state — verify no UI-local mutable state duplicates it. (co-15)
- **ex-32 · stateflow-expose** — expose `StateFlow<UiState>` from the ViewModel via `stateIn(...)` — verify the initial value emits. (co-16)
- **ex-33 · collect-lifecycle** — collect it with `collectAsStateWithLifecycle()` — verify collection pauses when the screen is backgrounded. (co-16)
- **ex-34 · ui-state-sealed** — model `sealed interface UiState { Loading; Success(data); Error(msg) }` — verify an exhaustive `when` renders each. (co-17)
- **ex-35 · loading-success-error** — drive the three states from a fake repository — verify each renders its branch. (co-17)
- **ex-36 · repository-interface** — define a `Repository` interface + a fake impl — verify the ViewModel depends only on the interface. (co-18)
- **ex-37 · repository-single-truth** — route all reads through the repository — verify the UI never touches a data source directly. (co-18)
- **ex-38 · room-entity** — annotate a `@Entity data class Note` — verify Room generates the table. (co-19)
- **ex-39 · room-dao** — a `@Dao` with `@Insert` + `@Query` methods — verify insert-then-query round-trips. (co-19)
- **ex-40 · room-database** — an abstract `@Database` exposing the DAO — verify `Room.databaseBuilder` opens it. (co-19)
- **ex-41 · room-suspend-insert** — a `suspend fun insert(...)` called from `viewModelScope` — verify it runs off the main thread. (co-20, co-24)
- **ex-42 · room-flow-query** — a `fun observeAll(): Flow<List<Note>>` — verify inserting a row re-emits the list. (co-20, co-25)
- **ex-43 · datastore-write** — write a preference with Preferences DataStore — verify it persists across relaunch. (co-21)
- **ex-44 · datastore-read-flow** — read the preference as a `Flow` — verify a write re-emits the new value. (co-21, co-25)
- **ex-45 · retrofit-interface** — declare `@GET("users") suspend fun users(): List<User>` — verify Retrofit builds the client. (co-22)
- **ex-46 · retrofit-call** — call it from the repository — verify a real response deserializes. (co-22, co-24)
- **ex-47 · json-decode** — configure a Moshi/kotlinx.serialization converter — verify JSON maps to the data class fields. (co-23)
- **ex-48 · coroutine-network-call** — wrap the network call in a `try/catch` in `viewModelScope` — verify success and error both surface as state. (co-24, co-17)
- **ex-49 · viewmodelscope-launch** — launch two calls concurrently with `async`/`await` — verify both complete before combining. (co-24)
- **ex-50 · structured-concurrency** — cancel the ViewModel mid-call — verify the in-flight coroutine is cancelled (no leak). (co-24)
- **ex-51 · flow-map-transform** — `map` a `Flow<List<Note>>` to a `Flow<Int>` count — verify the count re-emits on change. (co-25)
- **ex-52 · flow-collect-ui** — collect a transformed flow into UI state — verify the screen reacts. (co-25, co-16)
- **ex-53 · repo-room-plus-retrofit** — a repository that caches Retrofit results in Room — verify it serves cache on the second call. (co-18, co-19, co-22)
- **ex-54 · network-error-state** — surface a Retrofit `IOException` as `UiState.Error` — verify the error UI shows and a retry re-fetches. (co-17, co-22)

### Advanced

- **ex-55 · navigation-navhost** — set up a `NavHost` with two composable destinations — verify the start destination renders. (co-26)
- **ex-56 · navigation-route** — navigate `navController.navigate("detail")` — verify the detail destination shows. (co-26)
- **ex-57 · navigation-args** — pass an id via a route argument `detail/{id}` — verify the detail reads it. (co-26)
- **ex-58 · navigation-back** — pop with the back button/`popBackStack()` — verify it returns to the list. (co-26)
- **ex-59 · permissions-request** — request `CAMERA` at runtime with the Activity Result API — verify the system dialog appears. (co-27)
- **ex-60 · permissions-denied** — handle a denied permission — verify the app degrades gracefully (no crash). (co-27)
- **ex-61 · remembersaveable** — hold scroll/input state in `rememberSaveable` — verify it survives rotation. (co-28)
- **ex-62 · viewmodel-config-survival** — keep the loaded list in the ViewModel — verify rotation does not re-fetch. (co-28, co-14)
- **ex-63 · rotation-state-preserved** — combine `rememberSaveable` + ViewModel across a full rotation — verify both UI and data survive. (co-28)
- **ex-64 · manual-di** — construct the repository in an `Application`/factory and pass it into the ViewModel — verify no `new` inside the ViewModel. (co-29)
- **ex-65 · hilt-intuition** — annotate with `@HiltViewModel` + `@Inject` (conceptual) — verify the graph supplies the repository. (co-29)
- **ex-66 · junit-unit-test** — a pure JUnit test of a mapping function under `src/test/` — verify `./gradlew test` runs it. (co-30)
- **ex-67 · viewmodel-unit-test** — test the ViewModel with a fake repository + a test dispatcher — verify state transitions loading→success. (co-30, co-14)
- **ex-68 · compose-ui-test-rule** — a Compose UI test with `createComposeRule()` — verify `onNodeWithText(...).assertIsDisplayed()`. (co-30)
- **ex-69 · compose-ui-test-click** — `onNodeWithText("Add").performClick()` then assert the new item — verify interaction. (co-30)
- **ex-70 · instrumented-test** — an instrumented test under `src/androidTest/` run via `connectedAndroidTest` — verify it executes on an emulator. (co-30)
- **ex-71 · gradlew-test** — run the whole local suite with `./gradlew test` — verify the HTML report under `build/reports/tests/`. (co-30)
- **ex-72 · list-from-viewmodel** — a `LazyColumn` driven by ViewModel state — verify items render from state. (co-13, co-14)
- **ex-73 · loading-error-ui** — render a spinner and an error card from `UiState` — verify each state's composable. (co-17, co-05)
- **ex-74 · flow-driven-reactive-ui** — a screen that live-updates as a Room `Flow` changes — verify an insert appears without a refresh. (co-25, co-16)
- **ex-75 · offline-first-cache** — read from Room first, refresh from Retrofit in the background — verify the UI shows cached data instantly. (co-19, co-18)
- **ex-76 · navigation-saved-state** — navigate away and back across a rotation — verify the back-stack and screen state survive. (co-26, co-28)
- **ex-77 · screen-vm-repo-slice** — wire one screen end-to-end: composable ← ViewModel ← repository — verify the full data path. (co-05, co-14, co-18)
- **ex-78 · capstone-full-app** — assemble a two-screen app (list + detail) with Room+Retrofit repository, navigation, config-change survival, and a Compose UI test — verify `./gradlew test` is green and the flow works on an emulator. (co-05, co-14, co-18, co-26, co-30)

## Capstone spec — intra-topic (subject → full runnable app)

- **Goal**: build a small but complete Android app — a Compose UI backed by a ViewModel + unidirectional
  data flow, a repository over Room (local) and a Retrofit coroutine call (remote) with loading/error
  states, navigation with saved state, and survival across a config change — covered by JUnit + a Compose
  UI test, buildable and testable from `./gradlew`.
- **Concepts exercised**: [ ] Compose UI + state hoisting (co-05, co-08) [ ] a ViewModel + unidirectional
  data flow (co-14, co-15) [ ] a repository over Room + Retrofit/coroutines (co-18, co-19, co-22, co-24)
  [ ] loading/error states (co-17) [ ] navigation + saved state + config-change survival (co-26, co-28)
  [ ] JUnit + a Compose UI test (co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a Compose screen driven by a ViewModel + state. Verify state changes
     recompose the UI and `./gradlew test` runs.
  2. Add a repository over Room + a Retrofit coroutine call with loading/error states. Verify data persists
     locally and a network error shows the error state (a unit test covers the ViewModel logic).
  3. Add navigation with saved state + config-change survival. Verify navigating and rotating preserves
     state; add a Compose UI test asserting the flow.
- **Acceptance criteria**: the app builds + runs on an emulator; local + remote data work with proper
  loading/error states; navigation + config-change preserve state; JUnit + Compose UI tests pass via
  `./gradlew test`.
- **Done bar**: runnable end-to-end (emulator/device) + tests green + web-verified.

## Read more

**Books**

- **Android Programming: The Big Nerd Ranch Guide**, 5th ed. — Bryan Sills, Brian Gardner, Kristin Marsicano & Chris Stewart (2022, Addison-Wesley). Long-running, widely respected hands-on Android primer, now covering Kotlin and Jetpack Compose.

**Papers & articles**

- **Guide to app architecture** — Android Developers, official (Google). Google's canonical recommended architecture for modern Android apps. <https://developer.android.com/topic/architecture>
- **Jetpack Compose documentation** — Android Developers, official (Google). The authoritative reference for Android's modern declarative UI toolkit. <https://developer.android.com/develop/ui/compose/documentation>
- **Kotlin overview for Android** — Android Developers, official (Google). Google's own framing of Kotlin as the primary Android language. <https://developer.android.com/kotlin/overview>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Mobile & CLI platforms — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Mobile & desktop platforms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 11 · Mobile & desktop platforms.

> _Content originated in the now-closed FS-SE plan (topic 69); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
