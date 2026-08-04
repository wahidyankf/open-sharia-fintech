@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel(), onOpen: (String) -> Unit) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  when (state) {
    is ContentState -> NoteRows((state as ContentState).notes, onOpen)
    else -> NotesLoadingOrError(state, viewModel::retry)
  }
}
