class RemoteNotesRepository(private val api: NotesApi) {
  suspend fun load(id: String): Result<Note> =
    runCatching { api.fetchNote(id).let { Note(it.id, it.title) } }
}
