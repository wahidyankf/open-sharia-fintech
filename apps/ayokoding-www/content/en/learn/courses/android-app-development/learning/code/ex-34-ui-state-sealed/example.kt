sealed interface NotesUiState {
  data object Loading : NotesUiState
  data class Content(val notes: List<Note>) : NotesUiState
  data class Error(val message: String) : NotesUiState
}
