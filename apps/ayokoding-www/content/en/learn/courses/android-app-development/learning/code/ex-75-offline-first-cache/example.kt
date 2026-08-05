class OfflineNotesRepository(private val dao: NoteDao, private val api: NotesApi) {
  fun observeCached() = dao.observeAll()
  suspend fun refresh() = runCatching {
    // Tests point Retrofit at MockWebServer with checked-in fixture JSON, never a live server.
    dao.upsertAll(api.fetchNotes().map(NoteDto::toEntity))
  }
}
