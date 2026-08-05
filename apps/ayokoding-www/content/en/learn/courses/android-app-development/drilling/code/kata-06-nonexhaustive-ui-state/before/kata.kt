// Broken: null could mean loading, empty content, or an error.
@Composable
fun BrokenScreen(notes: List<Note>?) {
  if (notes == null) CircularProgressIndicator() else NoteRows(notes, onOpen = {})
}
