@Composable
fun SelectedNote(title: String) {
  Text(title, Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.secondaryContainer)
    .padding(horizontal = 16.dp, vertical = 12.dp))
}
