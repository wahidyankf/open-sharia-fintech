@Test fun clicking_row_reports_note_id() {
  var opened: String? = null
  composeRule.setContent { NoteRows(listOf(Note("7", "Read")), onOpen = { opened = it }) }
  composeRule.onNodeWithText("Read").performClick()
  assertEquals("7", opened)
}
