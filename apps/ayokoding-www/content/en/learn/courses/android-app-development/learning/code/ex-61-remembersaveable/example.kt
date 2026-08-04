@Composable
fun FilterField() {
  var query by rememberSaveable { mutableStateOf("") }
  OutlinedTextField(value = query, onValueChange = { query = it }, label = { Text("Filter") })
}
