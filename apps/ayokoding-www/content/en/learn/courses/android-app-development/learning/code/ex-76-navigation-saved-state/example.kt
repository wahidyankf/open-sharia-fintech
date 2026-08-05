class NoteDetailViewModel(savedStateHandle: SavedStateHandle, repository: NotesRepository) : ViewModel() {
  private val noteId: String = checkNotNull(savedStateHandle["noteId"])
  val note = repository.observeNotes().map { notes -> notes.firstOrNull { it.id == noteId } }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)
}
