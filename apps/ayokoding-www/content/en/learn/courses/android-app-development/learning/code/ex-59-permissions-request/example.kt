@Composable
fun CameraRequest(onGranted: () -> Unit) {
  val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
    if (granted) onGranted()
  }
  Button(onClick = { launcher.launch(Manifest.permission.CAMERA) }) { Text("Enable camera") }
}
