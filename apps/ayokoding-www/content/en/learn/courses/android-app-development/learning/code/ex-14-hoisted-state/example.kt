@Composable
fun Counter(value: Int, onIncrement: () -> Unit) {
  Button(onClick = onIncrement) { Text("Count: $value") }
}
@Composable
fun CounterOwner() {
  var value by remember { mutableIntStateOf(0) }
  Counter(value, onIncrement = { value++ })
}
