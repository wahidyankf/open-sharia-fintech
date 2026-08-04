@Composable
fun NoteMetadata(updated: String) {
  Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
    Icon(Icons.Outlined.Schedule, contentDescription = null); Text("Updated $updated")
  }
}
