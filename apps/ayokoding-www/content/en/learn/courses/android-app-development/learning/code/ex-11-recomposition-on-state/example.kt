@Composable
fun TapCount() {
  var taps by remember { mutableIntStateOf(0) }
  Button(onClick = { taps++ }) { Text("Tapped $taps times") }
}
