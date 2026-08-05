class NotesViewModelTest {
  @Test fun retry_keeps_cached_content_when_refresh_fails() = runTest {
    val viewModel = NotesViewModel(FakeNotesRepository(notes = listOf(Note("1", "Cached")), refreshFails = true))
    viewModel.retry()
    assertEquals("Cached", viewModel.state.value.notes.single().title)
  }
}
