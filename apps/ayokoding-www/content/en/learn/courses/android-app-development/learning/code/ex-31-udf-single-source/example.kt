data class EditorState(val title: String = "", val saving: Boolean = false)
class EditorViewModel : ViewModel() {
  private val _state = MutableStateFlow(EditorState())
  val state = _state.asStateFlow()
  fun onTitleChanged(title: String) { _state.update { it.copy(title = title) } }
}
