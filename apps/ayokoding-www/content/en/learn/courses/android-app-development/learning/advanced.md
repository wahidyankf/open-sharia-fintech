---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 bring the pieces together with navigation, runtime permissions, configuration-change survival, dependency injection, tests, offline-first behaviour, and a capstone preview.

### Example 55: Set Up a NavHost

_ex-55 · exercises co-26_

Set Up a NavHost isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-55-navigation-navhost/example.kt`**

```kotlin
@Composable
fun FocusApp(navController: NavHostController = rememberNavController()) {
  NavHost(navController, startDestination = "list") {
    composable("list") { NotesRoute(onOpen = { id -> navController.navigate("detail/$id") }) }
    composable("detail/{noteId}") { NoteDetailRoute(onBack = navController::popBackStack) }
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Set Up a NavHost keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 56: Navigate to a Route

_ex-56 · exercises co-26_

Navigate to a Route isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-56-navigation-route/example.kt`**

```kotlin
fun openDetail(navController: NavController, noteId: String) {
  navController.navigate("detail/$noteId") {
    launchSingleTop = true
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Navigate to a Route keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 57: Pass a Navigation Argument

_ex-57 · exercises co-26_

Pass a Navigation Argument isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-57-navigation-args/example.kt`**

```kotlin
composable(
  route = "detail/{noteId}",
  arguments = listOf(navArgument("noteId") { type = NavType.StringType })
) { entry ->
  val noteId = checkNotNull(entry.arguments?.getString("noteId"))
  NoteDetailRoute(noteId = noteId)
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Pass a Navigation Argument keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 58: Pop the Back Stack

_ex-58 · exercises co-26_

Pop the Back Stack isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-58-navigation-back/example.kt`**

```kotlin
@Composable
fun DetailTopBar(onBack: () -> Unit) {
  TopAppBar(title = { Text("Note") },
    navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back") } })
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Pop the Back Stack keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 59: Request a Runtime Permission

_ex-59 · exercises co-27_

Request a Runtime Permission isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-59-permissions-request/example.kt`**

```kotlin
@Composable
fun CameraRequest(onGranted: () -> Unit) {
  val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
    if (granted) onGranted()
  }
  Button(onClick = { launcher.launch(Manifest.permission.CAMERA) }) { Text("Enable camera") }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Request a Runtime Permission keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 60: Handle Permission Denial

_ex-60 · exercises co-27_

Handle Permission Denial isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-60-permissions-denied/example.kt`**

```kotlin
@Composable
fun CameraGate(granted: Boolean, onRequest: () -> Unit, onUseAlternative: () -> Unit) {
  if (granted) CameraCapture()
  else Column {
    Text("Camera access is off. You can add a note manually instead.")
    Button(onClick = onRequest) { Text("Allow camera") }
    TextButton(onClick = onUseAlternative) { Text("Add manually") }
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Handle Permission Denial keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 61: Save UI State

_ex-61 · exercises co-28_

Save UI State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-61-remembersaveable/example.kt`**

```kotlin
@Composable
fun FilterField() {
  var query by rememberSaveable { mutableStateOf("") }
  OutlinedTextField(value = query, onValueChange = { query = it }, label = { Text("Filter") })
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Save UI State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 62: Avoid Refetching After Rotation

_ex-62 · exercises co-28, co-14_

Avoid Refetching After Rotation isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-62-viewmodel-config-survival/example.kt`**

```kotlin
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  val notes = repository.observeNotes()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
  // Do not fetch from the composable: Activity recreation reuses this ViewModel.
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Avoid Refetching After Rotation keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 63: Preserve UI and Data State

_ex-63 · exercises co-28_

Preserve UI and Data State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-63-rotation-state-preserved/example.kt`**

```kotlin
class EditorViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {
  var draft by mutableStateOf(savedStateHandle["draft"] ?: "")
    private set
  fun edit(value: String) { draft = value; savedStateHandle["draft"] = value }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Preserve UI and Data State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 64: Wire Manual Dependency Injection

_ex-64 · exercises co-29_

Wire Manual Dependency Injection isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-64-manual-di/example.kt`**

```kotlin
class FocusApplication : Application() {
  val container by lazy {
    val database = Room.databaseBuilder(this, FocusDatabase::class.java, "focus.db").build()
    AppContainer(OfflineNotesRepository(database.noteDao(), RetrofitNotesApi.create()))
  }
}
class AppContainer(val notesRepository: NotesRepository)

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Wire Manual Dependency Injection keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 65: Recognize Hilt Injection

_ex-65 · exercises co-29_

Recognize Hilt Injection isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-65-hilt-intuition/example.kt`**

```kotlin
@HiltViewModel
class NotesViewModel @Inject constructor(
  private val repository: NotesRepository
) : ViewModel()

@Module @InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
  @Binds abstract fun bindNotesRepository(impl: OfflineNotesRepository): NotesRepository
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Recognize Hilt Injection keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 66: Write a Local JUnit Test

_ex-66 · exercises co-30_

Write a Local JUnit Test isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-66-junit-unit-test/example.kt`**

```kotlin
class NoteMapperTest {
  @Test fun entity_maps_to_domain_note() {
    val entity = NoteEntity("1", "Plan", "Ship", 42)
    assertEquals(Note("1", "Plan"), entity.toNote())
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Write a Local JUnit Test keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 67: Test a ViewModel Transition

_ex-67 · exercises co-30, co-14_

Test a ViewModel Transition isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-67-viewmodel-unit-test/example.kt`**

```kotlin
class NotesViewModelTest {
  @Test fun retry_keeps_cached_content_when_refresh_fails() = runTest {
    val viewModel = NotesViewModel(FakeNotesRepository(notes = listOf(Note("1", "Cached")), refreshFails = true))
    viewModel.retry()
    assertEquals("Cached", viewModel.state.value.notes.single().title)
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Test a ViewModel Transition keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 68: Create a Compose UI Test Rule

_ex-68 · exercises co-30_

Create a Compose UI Test Rule isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-68-compose-ui-test-rule/example.kt`**

```kotlin
class NotesScreenTest {
  @get:Rule val composeRule = createComposeRule()
  @Test fun shows_cached_note() {
    composeRule.setContent { NotesScreen(ContentState(listOf(Note("1", "Cached"))), onRetry = {}) }
    composeRule.onNodeWithText("Cached").assertIsDisplayed()
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Create a Compose UI Test Rule keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 69: Test a Compose Click

_ex-69 · exercises co-30_

Test a Compose Click isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-69-compose-ui-test-click/example.kt`**

```kotlin
@Test fun clicking_row_reports_note_id() {
  var opened: String? = null
  composeRule.setContent { NoteRows(listOf(Note("7", "Read")), onOpen = { opened = it }) }
  composeRule.onNodeWithText("Read").performClick()
  assertEquals("7", opened)
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Test a Compose Click keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 70: Run an Instrumented Test

_ex-70 · exercises co-30_

Run an Instrumented Test isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-70-instrumented-test/example.kt`**

```kotlin
@RunWith(AndroidJUnit4::class)
class DatabaseInstrumentedTest {
  @Test fun inserts_and_reads_note() = runTest {
    val dao = Room.inMemoryDatabaseBuilder(ApplicationProvider.getApplicationContext(), FocusDatabase::class.java)
      .allowMainThreadQueries().build().noteDao()
    dao.insert(NoteEntity("1", "Plan", "Body", 1))
    assertEquals("Plan", dao.observeById("1").first()?.title)
  }
}

```

**Run**: `./gradlew connectedAndroidTest` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Run an Instrumented Test keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 71: Run the Local Test Suite

_ex-71 · exercises co-30_

Run the Local Test Suite isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-71-gradlew-test/example.kt`**

```kotlin
# Local JVM tests:
./gradlew testDebugUnitTest

# Android integration and Compose UI tests on an emulator/device:
./gradlew connectedDebugAndroidTest

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Run the Local Test Suite keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 72: Drive a Lazy List from a ViewModel

_ex-72 · exercises co-13, co-14_

Drive a Lazy List from a ViewModel isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-72-list-from-viewmodel/example.kt`**

```kotlin
@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel(), onOpen: (String) -> Unit) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  when (state) {
    is ContentState -> NoteRows((state as ContentState).notes, onOpen)
    else -> NotesLoadingOrError(state, viewModel::retry)
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Drive a Lazy List from a ViewModel keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 73: Render Loading and Error UI

_ex-73 · exercises co-17, co-05_

Render Loading and Error UI isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-73-loading-error-ui/example.kt`**

```kotlin
sealed interface ScreenState {
  data object Loading : ScreenState
  data class Content(val notes: List<Note>, val error: String? = null) : ScreenState
  data class Error(val message: String) : ScreenState
}
@Composable fun Screen(state: ScreenState, retry: () -> Unit) = when (state) {
  ScreenState.Loading -> CircularProgressIndicator()
  is ScreenState.Content -> NoteRows(state.notes, {})
  is ScreenState.Error -> RetryButton(retry)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Render Loading and Error UI keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 74: Render a Room Flow Reactively

_ex-74 · exercises co-25, co-16_

Render a Room Flow Reactively isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-74-flow-driven-reactive-ui/example.kt`**

```kotlin
class NotesViewModel(dao: NoteDao) : ViewModel() {
  val state = dao.observeAll().map { rows ->
    ScreenState.Content(rows.map(NoteEntity::toNote))
  }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ScreenState.Loading)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Render a Room Flow Reactively keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 75: Refresh an Offline-First Cache

_ex-75 · exercises co-19, co-18_

Refresh an Offline-First Cache isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-75-offline-first-cache/example.kt`**

```kotlin
class OfflineNotesRepository(private val dao: NoteDao, private val api: NotesApi) {
  fun observeCached() = dao.observeAll()
  suspend fun refresh() = runCatching {
    // Tests point Retrofit at MockWebServer with checked-in fixture JSON, never a live server.
    dao.upsertAll(api.fetchNotes().map(NoteDto::toEntity))
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Refresh an Offline-First Cache keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 76: Preserve Navigation Saved State

_ex-76 · exercises co-26, co-28_

Preserve Navigation Saved State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-76-navigation-saved-state/example.kt`**

```kotlin
class NoteDetailViewModel(savedStateHandle: SavedStateHandle, repository: NotesRepository) : ViewModel() {
  private val noteId: String = checkNotNull(savedStateHandle["noteId"])
  val note = repository.observeNotes().map { notes -> notes.firstOrNull { it.id == noteId } }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Preserve Navigation Saved State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 77: Wire Screen, ViewModel, and Repository

_ex-77 · exercises co-05, co-14, co-18_

Wire Screen, ViewModel, and Repository isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-77-screen-vm-repo-slice/example.kt`**

```kotlin
@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel(), onOpen: (String) -> Unit) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  NotesScreen(state = state, onOpen = onOpen, onRetry = viewModel::retry)
}
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  val state = repository.observeNotes().map { ContentState(it) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ContentState(emptyList()))
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Wire Screen, ViewModel, and Repository keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 78: Preview the Full App Capstone

_ex-78 · exercises co-05, co-14, co-18, co-26, co-30_

Preview the Full App Capstone isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-78-capstone-full-app/example.kt`**

```kotlin
// The app composes the capstone boundaries; each concrete source lives in learning/capstone/code.
@Composable
fun FocusApp(navController: NavHostController = rememberNavController()) {
  NavHost(navController, startDestination = "list") {
    composable("list") { FocusListRoute(onOpen = { navController.navigate("detail/$it") }) }
    composable("detail/{noteId}", arguments = listOf(navArgument("noteId") { type = NavType.StringType })) {
      FocusDetailRoute(onBack = navController::popBackStack)
    }
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Preview the Full App Capstone keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.
