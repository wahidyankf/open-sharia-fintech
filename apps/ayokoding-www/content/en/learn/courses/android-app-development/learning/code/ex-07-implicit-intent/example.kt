fun Context.shareNote(text: String) {
  startActivity(Intent.createChooser(
    Intent(Intent.ACTION_SEND).setType("text/plain").putExtra(Intent.EXTRA_TEXT, text), "Share note"))
}
