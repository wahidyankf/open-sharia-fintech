@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel()) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  NotesScreen(state = state, onRetry = viewModel::refresh)
}
