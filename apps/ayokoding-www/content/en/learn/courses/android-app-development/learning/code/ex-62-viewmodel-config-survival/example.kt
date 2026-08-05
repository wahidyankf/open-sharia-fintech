class NotesViewModel(private val repository: NotesRepository) : ViewModel() {
  val notes = repository.observeNotes()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
  // Do not fetch from the composable: Activity recreation reuses this ViewModel.
}
