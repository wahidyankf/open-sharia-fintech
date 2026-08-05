---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 add a ViewModel-centred unidirectional data flow, state models, repositories, Room, DataStore, Retrofit, coroutines, and Flow. Each example keeps ownership and cancellation visible.

### Example 27: Read State from a ViewModel

_ex-27 · exercises co-14_

Read State from a ViewModel isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-27-viewmodel-basic/example.kt`**

```kotlin
class NotesViewModel : ViewModel() {
  private val _title = MutableStateFlow("Focus notes")
  val title: StateFlow<String> = _title.asStateFlow()
}
@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel()) {
  Text(viewModel.title.collectAsStateWithLifecycle().value)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Read State from a ViewModel keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 28: Launch Work in viewModelScope

_ex-28 · exercises co-14, co-24_

Launch Work in viewModelScope isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-28-viewmodelscope-coroutine/example.kt`**

```kotlin
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  fun refresh() = viewModelScope.launch {
    repository.refresh() // cancelled automatically when this ViewModel is cleared
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Launch Work in viewModelScope keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 29: Keep Data Through Rotation

_ex-29 · exercises co-14, co-28_

Keep Data Through Rotation isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-29-viewmodel-survives-rotation/example.kt`**

```kotlin
class NoteDetailViewModel(savedStateHandle: SavedStateHandle) : ViewModel() {
  val noteId: String = checkNotNull(savedStateHandle["noteId"])
  // The same ViewModel instance survives an Activity configuration change.
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Keep Data Through Rotation keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 30: Send Events Upward

_ex-30 · exercises co-15_

Send Events Upward isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-30-udf-events-up/example.kt`**

```kotlin
@Composable
fun AddNoteScreen(title: String, onTitleChange: (String) -> Unit, onSave: () -> Unit) {
  OutlinedTextField(value = title, onValueChange = onTitleChange)
  Button(onClick = onSave) { Text("Save") }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Send Events Upward keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 31: Use a Single Source of Truth

_ex-31 · exercises co-15_

Use a Single Source of Truth isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-31-udf-single-source/example.kt`**

```kotlin
data class EditorState(val title: String = "", val saving: Boolean = false)
class EditorViewModel : ViewModel() {
  private val _state = MutableStateFlow(EditorState())
  val state = _state.asStateFlow()
  fun onTitleChanged(title: String) { _state.update { it.copy(title = title) } }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Use a Single Source of Truth keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 32: Expose a StateFlow

_ex-32 · exercises co-16_

Expose a StateFlow isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-32-stateflow-expose/example.kt`**

```kotlin
class SearchViewModel : ViewModel() {
  private val _query = MutableStateFlow("")
  val query: StateFlow<String> = _query.asStateFlow()
  fun search(value: String) { _query.value = value }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Expose a StateFlow keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 33: Collect State Lifecycle-Aware

_ex-33 · exercises co-16_

Collect State Lifecycle-Aware isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-33-collect-lifecycle/example.kt`**

```kotlin
@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel()) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  NotesScreen(state = state, onRetry = viewModel::refresh)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Collect State Lifecycle-Aware keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 34: Model a Sealed UI State

_ex-34 · exercises co-17_

Model a Sealed UI State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-34-ui-state-sealed/example.kt`**

```kotlin
sealed interface NotesUiState {
  data object Loading : NotesUiState
  data class Content(val notes: List<Note>) : NotesUiState
  data class Error(val message: String) : NotesUiState
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Model a Sealed UI State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 35: Render Loading, Success, and Error

_ex-35 · exercises co-17_

Render Loading, Success, and Error isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-35-loading-success-error/example.kt`**

```kotlin
@Composable
fun NotesScreen(state: NotesUiState, onRetry: () -> Unit) = when (state) {
  NotesUiState.Loading -> CircularProgressIndicator()
  is NotesUiState.Content -> NoteRows(state.notes, onOpen = {})
  is NotesUiState.Error -> Button(onClick = onRetry) { Text(state.message) }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Render Loading, Success, and Error keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 36: Depend on a Repository Interface

_ex-36 · exercises co-18_

Depend on a Repository Interface isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-36-repository-interface/example.kt`**

```kotlin
interface NotesRepository {
  fun observeNotes(): Flow<List<Note>>
  suspend fun refresh(): Result<Unit>
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Depend on a Repository Interface keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 37: Centralize Reads in a Repository

_ex-37 · exercises co-18_

Centralize Reads in a Repository isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-37-repository-single-truth/example.kt`**

```kotlin
class OfflineNotesRepository(private val dao: NoteDao, private val api: NotesApi) : NotesRepository {
  override fun observeNotes() = dao.observeAll().map { rows -> rows.map(NoteEntity::toNote) }
  override suspend fun refresh() = runCatching { dao.upsertAll(api.fetchNotes().map(NoteDto::toEntity)) }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Centralize Reads in a Repository keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 38: Define a Room Entity

_ex-38 · exercises co-19_

Define a Room Entity isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-38-room-entity/example.kt`**

```kotlin
@Entity(tableName = "notes")
data class NoteEntity(
  @PrimaryKey val id: String,
  val title: String,
  val body: String,
  val updatedAt: Long
)

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Define a Room Entity keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 39: Define a Room DAO

_ex-39 · exercises co-19_

Define a Room DAO isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-39-room-dao/example.kt`**

```kotlin
@Dao
interface NoteDao {
  @Query("SELECT * FROM notes ORDER BY updatedAt DESC") fun observeAll(): Flow<List<NoteEntity>>
  @Upsert suspend fun upsertAll(notes: List<NoteEntity>)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Define a Room DAO keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 40: Open a Room Database

_ex-40 · exercises co-19_

Open a Room Database isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-40-room-database/example.kt`**

```kotlin
@Database(entities = [NoteEntity::class], version = 1, exportSchema = true)
abstract class FocusDatabase : RoomDatabase() {
  abstract fun noteDao(): NoteDao
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Open a Room Database keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 41: Insert with a Suspend DAO Method

_ex-41 · exercises co-20, co-24_

Insert with a Suspend DAO Method isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-41-room-suspend-insert/example.kt`**

```kotlin
@Dao
interface NoteDao {
  @Insert(onConflict = OnConflictStrategy.REPLACE)
  suspend fun insert(note: NoteEntity)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Insert with a Suspend DAO Method keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 42: Observe Room with Flow

_ex-42 · exercises co-20, co-25_

Observe Room with Flow isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-42-room-flow-query/example.kt`**

```kotlin
@Dao
interface NoteDao {
  @Query("SELECT * FROM notes WHERE id = :id")
  fun observeById(id: String): Flow<NoteEntity?>
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Observe Room with Flow keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 43: Write a DataStore Preference

_ex-43 · exercises co-21_

Write a DataStore Preference isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-43-datastore-write/example.kt`**

```kotlin
val Context.dataStore by preferencesDataStore("settings")
val SHOW_ARCHIVED = booleanPreferencesKey("show_archived")
suspend fun Context.setShowArchived(value: Boolean) {
  dataStore.edit { preferences -> preferences[SHOW_ARCHIVED] = value }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Write a DataStore Preference keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 44: Read DataStore as Flow

_ex-44 · exercises co-21, co-25_

Read DataStore as Flow isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-44-datastore-read-flow/example.kt`**

```kotlin
val showArchived: Flow<Boolean> = context.dataStore.data
  .map { preferences -> preferences[SHOW_ARCHIVED] ?: false }
  .catch { error -> if (error is IOException) emit(emptyPreferences()) else throw error }

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Read DataStore as Flow keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 45: Define a Retrofit Interface

_ex-45 · exercises co-22_

Define a Retrofit Interface isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-45-retrofit-interface/example.kt`**

```kotlin
interface NotesApi {
  @GET("notes") suspend fun fetchNotes(): List<NoteDto>
  @GET("notes/{id}") suspend fun fetchNote(@Path("id") id: String): NoteDto
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Define a Retrofit Interface keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 46: Call Retrofit from a Repository

_ex-46 · exercises co-22, co-24_

Call Retrofit from a Repository isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-46-retrofit-call/example.kt`**

```kotlin
class RemoteNotesRepository(private val api: NotesApi) {
  suspend fun load(id: String): Result<Note> =
    runCatching { api.fetchNote(id).let { Note(it.id, it.title) } }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Call Retrofit from a Repository keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 47: Decode JSON into Data Classes

_ex-47 · exercises co-23_

Decode JSON into Data Classes isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-47-json-decode/example.kt`**

```kotlin
@Serializable
data class NoteDto(val id: String, val title: String, val body: String, @SerialName("updated_at") val updatedAt: Long)
val retrofit = Retrofit.Builder().baseUrl("https://example.invalid/")
  .addConverterFactory(Json.asConverterFactory("application/json".toMediaType())).build()

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Decode JSON into Data Classes keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 48: Surface a Network Result

_ex-48 · exercises co-24, co-17_

Surface a Network Result isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-48-coroutine-network-call/example.kt`**

```kotlin
class SyncViewModel(private val repository: NotesRepository) : ViewModel() {
  private val _message = MutableStateFlow<String?>(null)
  fun refresh() = viewModelScope.launch {
    _message.value = repository.refresh().exceptionOrNull()?.message
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Surface a Network Result keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 49: Combine Concurrent Calls

_ex-49 · exercises co-24_

Combine Concurrent Calls isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-49-viewmodelscope-launch/example.kt`**

```kotlin
suspend fun loadDashboard(api: DashboardApi): Dashboard = coroutineScope {
  val profile = async { api.profile() }
  val notes = async { api.notes() }
  Dashboard(profile.await(), notes.await())
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Combine Concurrent Calls keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 50: Cancel Structured Work

_ex-50 · exercises co-24_

Cancel Structured Work isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-50-structured-concurrency/example.kt`**

```kotlin
class SearchViewModel(private val api: NotesApi) : ViewModel() {
  private var searchJob: Job? = null
  fun search(query: String) {
    searchJob?.cancel()
    searchJob = viewModelScope.launch { api.fetchNotes() /* update state */ }
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Cancel Structured Work keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 51: Transform a Flow

_ex-51 · exercises co-25_

Transform a Flow isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-51-flow-map-transform/example.kt`**

```kotlin
val titles: Flow<List<String>> = dao.observeAll()
  .map { notes -> notes.filterNot { it.title.isBlank() }.map { it.title } }

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Transform a Flow keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 52: Collect a Flow into UI State

_ex-52 · exercises co-25, co-16_

Collect a Flow into UI State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-52-flow-collect-ui/example.kt`**

```kotlin
class NotesViewModel(repository: NotesRepository) : ViewModel() {
  val state: StateFlow<NotesUiState> = repository.observeNotes()
    .map< List<Note>, NotesUiState> { NotesUiState.Content(it) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), NotesUiState.Loading)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Collect a Flow into UI State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 53: Cache Retrofit Data in Room

_ex-53 · exercises co-18, co-19, co-22_

Cache Retrofit Data in Room isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-53-repo-room-plus-retrofit/example.kt`**

```kotlin
class OfflineNotesRepository(private val dao: NoteDao, private val api: NotesApi) {
  fun observe() = dao.observeAll()
  suspend fun refresh(): Result<Unit> = runCatching {
    dao.upsertAll(api.fetchNotes().map { NoteEntity(it.id, it.title, it.body, it.updatedAt) })
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Cache Retrofit Data in Room keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 54: Offer a Retryable Error State

_ex-54 · exercises co-17, co-22_

Offer a Retryable Error State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-54-network-error-state/example.kt`**

```kotlin
data class ContentState(val notes: List<Note>, val refreshError: String? = null)
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  fun retry() = viewModelScope.launch {
    repository.refresh().onFailure { /* retain cached notes; expose non-blocking error */ }
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Offer a Retryable Error State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.
