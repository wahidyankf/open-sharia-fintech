@Dao
interface NoteDao {
  @Query("SELECT * FROM notes WHERE id = :id")
  fun observeById(id: String): Flow<NoteEntity?>
}
