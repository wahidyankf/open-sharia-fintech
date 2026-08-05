class SearchViewModel : ViewModel() {
  private val _query = MutableStateFlow("")
  val query: StateFlow<String> = _query.asStateFlow()
  fun search(value: String) { _query.value = value }
}
