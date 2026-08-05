class EditorViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {
  var draft by mutableStateOf(savedStateHandle["draft"] ?: "")
    private set
  fun edit(value: String) { draft = value; savedStateHandle["draft"] = value }
}
