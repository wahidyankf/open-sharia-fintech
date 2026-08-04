@Composable
fun SearchField(query: String, onQueryChange: (String) -> Unit) {
  OutlinedTextField(value = query, onValueChange = onQueryChange, label = { Text("Search notes") }, singleLine = true)
}
