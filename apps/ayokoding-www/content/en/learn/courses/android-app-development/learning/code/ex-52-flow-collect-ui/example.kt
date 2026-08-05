class NotesViewModel(repository: NotesRepository) : ViewModel() {
  val state: StateFlow<NotesUiState> = repository.observeNotes()
    .map< List<Note>, NotesUiState> { NotesUiState.Content(it) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), NotesUiState.Loading)
}
