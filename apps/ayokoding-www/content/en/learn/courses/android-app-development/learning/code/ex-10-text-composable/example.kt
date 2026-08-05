@Composable
fun NoteTitle(title: String, modifier: Modifier = Modifier) {
  Text(text = title, modifier = modifier, style = MaterialTheme.typography.titleMedium)
}
