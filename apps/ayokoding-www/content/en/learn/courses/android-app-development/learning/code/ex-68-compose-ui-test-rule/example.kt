class NotesScreenTest {
  @get:Rule val composeRule = createComposeRule()
  @Test fun shows_cached_note() {
    composeRule.setContent { NotesScreen(ContentState(listOf(Note("1", "Cached"))), onRetry = {}) }
    composeRule.onNodeWithText("Cached").assertIsDisplayed()
  }
}
