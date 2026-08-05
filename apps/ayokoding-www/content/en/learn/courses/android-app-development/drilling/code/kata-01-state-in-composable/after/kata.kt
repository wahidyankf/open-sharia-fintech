data class NotesState(val notes: List<Note> = emptyList())
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  private val _state = MutableStateFlow(NotesState())
  val state = _state.asStateFlow()
  fun refresh() = viewModelScope.launch { _state.value = NotesState(repository.load()) }
}
@Composable fun NotesRoute(viewModel: NotesViewModel = viewModel()) {
  val state by viewModel.state.collectAsStateWithLifecycle()
  NoteRows(state.notes, onOpen = {})
}
