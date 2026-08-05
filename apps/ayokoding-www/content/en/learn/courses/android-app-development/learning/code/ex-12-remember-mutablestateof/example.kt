@Composable
fun EditableLabel() {
  var label by remember { mutableStateOf("") }
  OutlinedTextField(value = label, onValueChange = { label = it }, label = { Text("Label") })
}
