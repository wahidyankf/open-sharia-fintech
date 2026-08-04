composable("detail/{noteId}", arguments = listOf(navArgument("noteId") { type = NavType.StringType })) {
  DetailRoute()
}
class DetailViewModel(savedStateHandle: SavedStateHandle) : ViewModel() {
  val noteId: String = checkNotNull(savedStateHandle["noteId"])
}
fun NavController.openNote(id: String) = navigate("detail/$id")
