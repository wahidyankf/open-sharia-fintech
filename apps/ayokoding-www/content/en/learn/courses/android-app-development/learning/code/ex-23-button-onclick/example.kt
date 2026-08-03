@Composable
fun RetryButton(onRetry: () -> Unit) {
  Button(onClick = onRetry) { Text("Retry sync") }
}
