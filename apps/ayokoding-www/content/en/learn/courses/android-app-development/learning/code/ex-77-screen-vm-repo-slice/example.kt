@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel(), onOpen: (String) -> Unit) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  NotesScreen(state = state, onOpen = onOpen, onRetry = viewModel::retry)
}
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  val state = repository.observeNotes().map { ContentState(it) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ContentState(emptyList()))
}
