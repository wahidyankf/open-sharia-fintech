class FocusNotesRepositoryTest {
  private val server = MockWebServer()

  @After fun closeServer() = server.shutdown()

  @Test fun fixture_response_is_cached_in_room() = runTest {
    // Copy code/fixtures/focus-notes.json to app/src/test/resources/focus-notes.json.
    val fixture = checkNotNull(javaClass.classLoader?.getResource("focus-notes.json")) .readText()
    server.enqueue(MockResponse().setBody(fixture).setHeader("Content-Type", "application/json"))

    val dao = Room.inMemoryDatabaseBuilder(
      ApplicationProvider.getApplicationContext(), FocusDatabase::class.java
    ).build().notes()
    val api = Retrofit.Builder().baseUrl(server.url("/"))
      .addConverterFactory(Json.asConverterFactory("application/json".toMediaType())).build()
      .create(FocusNotesApi::class.java)

    assertTrue(OfflineFocusNotesRepository(dao, api).refresh().isSuccess)
    assertEquals("Review offline-first design", dao.observeAll().first().single().title)
  }
}
