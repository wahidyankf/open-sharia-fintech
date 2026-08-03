@Composable
fun NoteList(notes: List<String>) {
  LazyColumn { items(notes, key = { it }) { title -> Text(title, Modifier.padding(16.dp)) } }
}
