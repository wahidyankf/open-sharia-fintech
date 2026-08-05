@Composable
fun QuantityStepper(value: Int, onValueChange: (Int) -> Unit) {
  Row { Button(onClick = { onValueChange(value - 1) }) { Text("-") }
    Text("$value"); Button(onClick = { onValueChange(value + 1) }) { Text("+") } }
}
