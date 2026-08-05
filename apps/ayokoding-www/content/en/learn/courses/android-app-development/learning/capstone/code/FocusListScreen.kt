@Composable
fun FocusApp(state: FocusListState, onRefresh: () -> Unit, navController: NavHostController = rememberNavController()) {
  NavHost(navController, startDestination = "list") {
    composable("list") {
      FocusListScreen(state, onOpen = { noteId -> navController.navigate("detail/$noteId") }, onRetry = onRefresh)
    }
    composable("detail/{noteId}", arguments = listOf(navArgument("noteId") { type = NavType.StringType })) { entry ->
      val noteId = checkNotNull(entry.arguments?.getString("noteId"))
      FocusDetailScreen(noteId, (state as? FocusListState.Content)?.notes.orEmpty(), navController::popBackStack)
    }
  }
}

@Composable
fun FocusListScreen(state: FocusListState, onOpen: (String) -> Unit, onRetry: () -> Unit) {
  when (state) {
    FocusListState.Loading -> CircularProgressIndicator()
    is FocusListState.Error -> Column { Text(state.message); Button(onClick = onRetry) { Text("Retry") } }
    is FocusListState.Content -> LazyColumn {
      if (state.refreshError != null) item {
        Text("Showing saved notes; sync failed: ${state.refreshError}")
        TextButton(onClick = onRetry) { Text("Retry sync") }
      }
      items(state.notes, key = { it.id }) { note ->
        ListItem(headlineContent = { Text(note.title) }, supportingContent = { Text(note.body) },
          modifier = Modifier.clickable { onOpen(note.id) })
      }
    }
  }
}

@Composable
private fun FocusDetailScreen(noteId: String, notes: List<FocusNote>, onBack: () -> Unit) {
  val note = notes.firstOrNull { it.id == noteId }
  Scaffold(topBar = { TopAppBar(title = { Text(note?.title ?: "Note") },
    navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back") } }) }) {
    Text(note?.body ?: "This note is no longer available.", Modifier.padding(it))
  }
}
