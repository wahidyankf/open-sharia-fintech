data class ContentState(val notes: List<Note>, val refreshError: String? = null)
class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  fun retry() = viewModelScope.launch {
    repository.refresh().onFailure { /* retain cached notes; expose non-blocking error */ }
  }
}
