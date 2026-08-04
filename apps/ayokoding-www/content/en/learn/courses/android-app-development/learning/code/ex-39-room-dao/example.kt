@Dao
interface NoteDao {
  @Query("SELECT * FROM notes ORDER BY updatedAt DESC") fun observeAll(): Flow<List<NoteEntity>>
  @Upsert suspend fun upsertAll(notes: List<NoteEntity>)
}
