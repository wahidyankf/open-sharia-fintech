// Imports are intentionally omitted: this app module needs Room, Retrofit, lifecycle-viewmodel, and coroutines.
data class FocusNote(val id: String, val title: String, val body: String, val updatedAt: Long)

@Entity(tableName = "focus_notes")
data class FocusNoteEntity(@PrimaryKey val id: String, val title: String, val body: String, val updatedAt: Long) {
  fun toDomain() = FocusNote(id, title, body, updatedAt)
}

@Dao
interface FocusNoteDao {
  @Query("SELECT * FROM focus_notes ORDER BY updatedAt DESC")
  fun observeAll(): Flow<List<FocusNoteEntity>>
  @Upsert suspend fun upsertAll(notes: List<FocusNoteEntity>)
}

@Database(entities = [FocusNoteEntity::class], version = 1, exportSchema = true)
abstract class FocusDatabase : RoomDatabase() { abstract fun notes(): FocusNoteDao }

data class FocusNoteDto(val id: String, val title: String, val body: String, val updatedAt: Long) {
  fun toEntity() = FocusNoteEntity(id, title, body, updatedAt)
}
interface FocusNotesApi { @GET("notes") suspend fun fetchNotes(): List<FocusNoteDto> }

interface FocusNotesRepository {
  fun observeNotes(): Flow<List<FocusNote>>
  suspend fun refresh(): Result<Unit>
}

class OfflineFocusNotesRepository(private val dao: FocusNoteDao, private val api: FocusNotesApi) : FocusNotesRepository {
  override fun observeNotes() = dao.observeAll().map { rows -> rows.map(FocusNoteEntity::toDomain) }
  override suspend fun refresh(): Result<Unit> = runCatching {
    // Retrofit's result becomes the local Room cache; UI observes Room, never the network directly.
    dao.upsertAll(api.fetchNotes().map(FocusNoteDto::toEntity))
  }
}

sealed interface FocusListState {
  data object Loading : FocusListState
  data class Content(val notes: List<FocusNote>, val refreshError: String? = null) : FocusListState
  data class Error(val message: String) : FocusListState
}

class FocusListViewModel(private val repository: FocusNotesRepository) : ViewModel() {
  private val refreshError = MutableStateFlow<String?>(null)
  val state: StateFlow<FocusListState> = combine(repository.observeNotes(), refreshError) { notes, error ->
    when { notes.isNotEmpty() -> FocusListState.Content(notes, error)
      error != null -> FocusListState.Error(error)
      else -> FocusListState.Loading }
  }.stateIn(viewModelScope, SharingStarted.Eagerly, FocusListState.Loading)

  init { refresh() }
  fun refresh() = viewModelScope.launch {
    repository.refresh().onSuccess { refreshError.value = null }
      .onFailure { refreshError.value = it.message ?: "Refresh failed" }
  }
}

class FocusDetailViewModel(
  savedStateHandle: SavedStateHandle,
  repository: FocusNotesRepository
) : ViewModel() {
  private val noteId: String = checkNotNull(savedStateHandle["noteId"])
  val note: StateFlow<FocusNote?> = repository.observeNotes()
    .map { notes -> notes.firstOrNull { it.id == noteId } }
    .stateIn(viewModelScope, SharingStarted.Eagerly, null)
}
