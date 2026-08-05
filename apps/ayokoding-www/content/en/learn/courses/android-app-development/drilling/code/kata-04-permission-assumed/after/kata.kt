@Composable
fun CameraGate(granted: Boolean, onRequest: () -> Unit, onManualEntry: () -> Unit) {
  if (granted) CameraCapture()
  else Column {
    Text("Camera access is required for scanning.")
    Button(onClick = onRequest) { Text("Allow camera") }
    TextButton(onClick = onManualEntry) { Text("Enter manually") }
  }
}
