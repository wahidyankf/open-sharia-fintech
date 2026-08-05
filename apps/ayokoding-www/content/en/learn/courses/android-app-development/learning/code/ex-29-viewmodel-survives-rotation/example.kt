class NoteDetailViewModel(savedStateHandle: SavedStateHandle) : ViewModel() {
  val noteId: String = checkNotNull(savedStateHandle["noteId"])
  // The same ViewModel instance survives an Activity configuration change.
}
