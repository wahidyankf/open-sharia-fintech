class SearchViewModel(private val api: NotesApi) : ViewModel() {
  private var searchJob: Job? = null
  fun search(query: String) {
    searchJob?.cancel()
    searchJob = viewModelScope.launch { api.fetchNotes() /* update state */ }
  }
}
