sealed interface NotesUiState {
  data object Loading : NotesUiState
  data class Content(val notes: List<Note>) : NotesUiState
  data class Error(val message: String) : NotesUiState
}
@Composable fun NotesScreen(state: NotesUiState, retry: () -> Unit) = when (state) {
  NotesUiState.Loading -> CircularProgressIndicator()
  is NotesUiState.Content -> NoteRows(state.notes, onOpen = {})
  is NotesUiState.Error -> Button(onClick = retry) { Text("Retry") }
}
