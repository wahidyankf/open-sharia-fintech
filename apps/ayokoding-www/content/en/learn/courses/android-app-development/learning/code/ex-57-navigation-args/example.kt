composable(
  route = "detail/{noteId}",
  arguments = listOf(navArgument("noteId") { type = NavType.StringType })
) { entry ->
  val noteId = checkNotNull(entry.arguments?.getString("noteId"))
  NoteDetailRoute(noteId = noteId)
}
