class NotesViewModel : ViewModel() {
  private val _title = MutableStateFlow("Focus notes")
  val title: StateFlow<String> = _title.asStateFlow()
}
@Composable
fun NotesRoute(viewModel: NotesViewModel = viewModel()) {
  Text(viewModel.title.collectAsStateWithLifecycle().value)
}
