class SyncViewModel(private val repository: NotesRepository) : ViewModel() {
  fun refresh() = viewModelScope.launch {
    repository.refresh() // cancelled when the ViewModel is cleared
  }
}
