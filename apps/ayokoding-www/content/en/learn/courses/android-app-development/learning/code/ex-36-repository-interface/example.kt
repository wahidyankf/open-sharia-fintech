interface NotesRepository {
  fun observeNotes(): Flow<List<Note>>
  suspend fun refresh(): Result<Unit>
}
