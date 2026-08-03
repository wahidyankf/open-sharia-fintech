class NotesViewModel(dao: NoteDao) : ViewModel() {
  val state = dao.observeAll().map { rows ->
    ScreenState.Content(rows.map(NoteEntity::toNote))
  }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ScreenState.Loading)
}
