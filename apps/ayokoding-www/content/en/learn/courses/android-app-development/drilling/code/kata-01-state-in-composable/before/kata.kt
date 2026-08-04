// Broken: rendering owns data and fetches synchronously from a repository.
@Composable
fun BrokenNotes(repository: NotesRepository) {
  var notes by remember { mutableStateOf(emptyList<Note>()) }
  Button(onClick = { notes = repository.loadNow() }) { Text("Refresh") }
  NoteRows(notes, onOpen = {})
}
