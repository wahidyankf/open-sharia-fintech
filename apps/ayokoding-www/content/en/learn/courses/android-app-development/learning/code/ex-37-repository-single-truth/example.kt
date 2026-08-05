class OfflineNotesRepository(private val dao: NoteDao, private val api: NotesApi) : NotesRepository {
  override fun observeNotes() = dao.observeAll().map { rows -> rows.map(NoteEntity::toNote) }
  override suspend fun refresh() = runCatching { dao.upsertAll(api.fetchNotes().map(NoteDto::toEntity)) }
}
