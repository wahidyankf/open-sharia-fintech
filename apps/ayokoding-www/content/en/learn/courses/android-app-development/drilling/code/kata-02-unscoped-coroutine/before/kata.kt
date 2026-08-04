// Broken: GlobalScope can complete after this screen has disappeared.
fun refresh(repository: NotesRepository) {
  GlobalScope.launch { repository.refresh() }
}
