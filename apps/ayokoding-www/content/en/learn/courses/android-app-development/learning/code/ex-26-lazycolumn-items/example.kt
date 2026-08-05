data class Note(val id: String, val title: String)
@Composable
fun NoteRows(notes: List<Note>, onOpen: (String) -> Unit) {
  LazyColumn { items(notes, key = { it.id }) { note ->
    ListItem(headlineContent = { Text(note.title) }, modifier = Modifier.clickable { onOpen(note.id) })
  } }
}
