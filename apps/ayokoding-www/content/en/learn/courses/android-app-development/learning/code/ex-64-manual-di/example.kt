class FocusApplication : Application() {
  val container by lazy {
    val database = Room.databaseBuilder(this, FocusDatabase::class.java, "focus.db").build()
    AppContainer(OfflineNotesRepository(database.noteDao(), RetrofitNotesApi.create()))
  }
}
class AppContainer(val notesRepository: NotesRepository)
