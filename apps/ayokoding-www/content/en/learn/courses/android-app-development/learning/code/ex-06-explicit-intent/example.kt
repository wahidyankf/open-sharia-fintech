fun Context.openNote(noteId: String) {
  startActivity(Intent(this, NoteDetailActivity::class.java)
    .putExtra(NoteDetailActivity.NOTE_ID, noteId))
}
