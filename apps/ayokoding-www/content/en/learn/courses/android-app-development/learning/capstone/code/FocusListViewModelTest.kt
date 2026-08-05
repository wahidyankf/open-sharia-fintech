class FocusListViewModelTest {
  @get:Rule val mainDispatcherRule = MainDispatcherRule()

  @Test fun refresh_failure_retains_cached_room_content() = runTest {
    val cached = FocusNote("1", "Cached plan", "Already saved", 1)
    val repository = FakeFocusNotesRepository(listOf(cached), Result.failure(IOException("offline")))
    val viewModel = FocusListViewModel(repository)
    advanceUntilIdle()
    assertEquals(FocusListState.Content(listOf(cached), "offline"), viewModel.state.value)
  }

  @Test fun refresh_success_clears_the_non_blocking_error() = runTest {
    val repository = FakeFocusNotesRepository(listOf(FocusNote("2", "Fixture note", "From fixture", 2)), Result.success(Unit))
    val viewModel = FocusListViewModel(repository)
    advanceUntilIdle()
    assertEquals(FocusListState.Content(repository.notes), viewModel.state.value)
  }
}

private class FakeFocusNotesRepository(
  val notes: List<FocusNote>, private val refreshResult: Result<Unit>
) : FocusNotesRepository {
  override fun observeNotes(): Flow<List<FocusNote>> = flowOf(notes)
  override suspend fun refresh(): Result<Unit> = refreshResult
}

private class MainDispatcherRule(
  private val dispatcher: TestDispatcher = StandardTestDispatcher()
) : TestWatcher() {
  override fun starting(description: Description) { Dispatchers.setMain(dispatcher) }
  override fun finished(description: Description) { Dispatchers.resetMain() }
}
