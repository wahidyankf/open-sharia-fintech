@Composable
fun NotesScaffold(content: @Composable (PaddingValues) -> Unit) {
  Scaffold(topBar = { TopAppBar(title = { Text("Focus notes") }) }, content = content)
}
