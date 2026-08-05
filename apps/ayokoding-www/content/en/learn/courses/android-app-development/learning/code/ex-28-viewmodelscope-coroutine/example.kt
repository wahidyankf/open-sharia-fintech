class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  fun refresh() = viewModelScope.launch {
    repository.refresh() // cancelled automatically when this ViewModel is cleared
  }
}
