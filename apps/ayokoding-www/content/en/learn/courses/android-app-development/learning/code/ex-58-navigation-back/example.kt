@Composable
fun DetailTopBar(onBack: () -> Unit) {
  TopAppBar(title = { Text("Note") },
    navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back") } })
}
