class OfflineNotesRepository(private val dao: NoteDao, private val api: NotesApi) {
  fun observe() = dao.observeAll()
  suspend fun refresh(): Result<Unit> = runCatching {
    dao.upsertAll(api.fetchNotes().map { NoteEntity(it.id, it.title, it.body, it.updatedAt) })
  }
}
