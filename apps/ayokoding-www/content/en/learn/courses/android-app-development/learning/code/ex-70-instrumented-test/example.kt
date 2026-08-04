@RunWith(AndroidJUnit4::class)
class DatabaseInstrumentedTest {
  @Test fun inserts_and_reads_note() = runTest {
    val dao = Room.inMemoryDatabaseBuilder(ApplicationProvider.getApplicationContext(), FocusDatabase::class.java)
      .allowMainThreadQueries().build().noteDao()
    dao.insert(NoteEntity("1", "Plan", "Body", 1))
    assertEquals("Plan", dao.observeById("1").first()?.title)
  }
}
