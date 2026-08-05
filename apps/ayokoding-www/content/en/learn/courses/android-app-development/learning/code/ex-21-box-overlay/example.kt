@Composable
fun SyncBadge(syncing: Boolean) {
  Box {
    Icon(Icons.Outlined.Cloud, contentDescription = "Cloud sync")
    if (syncing) CircularProgressIndicator(Modifier.align(Alignment.BottomEnd).size(12.dp))
  }
}
