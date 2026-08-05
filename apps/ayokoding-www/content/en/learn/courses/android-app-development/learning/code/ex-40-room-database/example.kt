@Database(entities = [NoteEntity::class], version = 1, exportSchema = true)
abstract class FocusDatabase : RoomDatabase() {
  abstract fun noteDao(): NoteDao
}
