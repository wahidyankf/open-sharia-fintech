fun openDetail(navController: NavController, noteId: String) {
  navController.navigate("detail/$noteId") {
    launchSingleTop = true
  }
}
