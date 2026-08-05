// Broken: manifest declaration is not a runtime camera grant.
@Composable
fun BrokenCamera() {
  Button(onClick = { CameraCapture().start() }) { Text("Scan") }
}
