@Composable
fun FocusApp(navController: NavHostController = rememberNavController()) {
  NavHost(navController, startDestination = "list") {
    composable("list") { NotesRoute(onOpen = { id -> navController.navigate("detail/$id") }) }
    composable("detail/{noteId}") { NoteDetailRoute(onBack = navController::popBackStack) }
  }
}
