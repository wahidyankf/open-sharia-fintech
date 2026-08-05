@Composable
fun NotesScreen(state: NotesUiState, onRetry: () -> Unit) = when (state) {
  NotesUiState.Loading -> CircularProgressIndicator()
  is NotesUiState.Content -> NoteRows(state.notes, onOpen = {})
  is NotesUiState.Error -> Button(onClick = onRetry) { Text(state.message) }
}
