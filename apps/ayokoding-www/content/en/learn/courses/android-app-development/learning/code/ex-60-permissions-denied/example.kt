@Composable
fun CameraGate(granted: Boolean, onRequest: () -> Unit, onUseAlternative: () -> Unit) {
  if (granted) CameraCapture()
  else Column {
    Text("Camera access is off. You can add a note manually instead.")
    Button(onClick = onRequest) { Text("Allow camera") }
    TextButton(onClick = onUseAlternative) { Text("Add manually") }
  }
}
