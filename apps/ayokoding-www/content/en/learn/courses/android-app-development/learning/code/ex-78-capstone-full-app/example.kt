// The app composes the capstone boundaries; each concrete source lives in learning/capstone/code.
@Composable
fun FocusApp(navController: NavHostController = rememberNavController()) {
  NavHost(navController, startDestination = "list") {
    composable("list") { FocusListRoute(onOpen = { navController.navigate("detail/$it") }) }
    composable("detail/{noteId}", arguments = listOf(navArgument("noteId") { type = NavType.StringType })) {
      FocusDetailRoute(onBack = navController::popBackStack)
    }
  }
}
