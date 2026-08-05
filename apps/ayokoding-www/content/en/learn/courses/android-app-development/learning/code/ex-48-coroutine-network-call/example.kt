class SyncViewModel(private val repository: NotesRepository) : ViewModel() {
  private val _message = MutableStateFlow<String?>(null)
  fun refresh() = viewModelScope.launch {
    _message.value = repository.refresh().exceptionOrNull()?.message
  }
}
