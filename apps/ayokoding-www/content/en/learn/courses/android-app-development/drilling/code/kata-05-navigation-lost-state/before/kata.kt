// Broken: selected ID is composition-local and disappears when the route is restored.
@Composable
fun BrokenList() {
  var selectedId by remember { mutableStateOf<String?>(null) }
  NoteRows(notes = sampleNotes, onOpen = { selectedId = it })
}
