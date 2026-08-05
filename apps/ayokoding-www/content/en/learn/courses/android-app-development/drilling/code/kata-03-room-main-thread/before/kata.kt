// Broken: Room I/O runs while Compose is rendering.
@Composable
fun BrokenRoomScreen(dao: NoteDao) {
  val notes = dao.readAllBlocking()
  NoteRows(notes.map(NoteEntity::toNote), onOpen = {})
}
