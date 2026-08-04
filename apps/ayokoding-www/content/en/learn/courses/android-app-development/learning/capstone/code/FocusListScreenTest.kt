class FocusListScreenTest {
  @get:Rule val compose = createComposeRule()

  @Test fun clicking_cached_note_navigates_to_its_detail() {
    val note = FocusNote("7", "Read architecture guide", "Use the checked-in fixture", 7)
    compose.setContent { FocusApp(FocusListState.Content(listOf(note)), onRefresh = {}) }
    compose.onNodeWithText("Read architecture guide").performClick()
    compose.onNodeWithText("Use the checked-in fixture").assertIsDisplayed()
  }

  @Test fun cached_notes_remain_visible_when_sync_fails() {
    compose.setContent {
      FocusListScreen(FocusListState.Content(listOf(FocusNote("1", "Cached", "Body", 1)), "offline"), {}, {})
    }
    compose.onNodeWithText("Cached").assertIsDisplayed()
    compose.onNodeWithText("Retry sync").assertIsDisplayed()
  }
}
