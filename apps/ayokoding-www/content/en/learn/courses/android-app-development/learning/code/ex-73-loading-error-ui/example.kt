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
