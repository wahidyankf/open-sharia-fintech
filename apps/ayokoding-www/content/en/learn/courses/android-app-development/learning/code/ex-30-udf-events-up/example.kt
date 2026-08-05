@Composable
fun AddNoteScreen(title: String, onTitleChange: (String) -> Unit, onSave: () -> Unit) {
  OutlinedTextField(value = title, onValueChange = onTitleChange)
  Button(onClick = onSave) { Text("Save") }
}
