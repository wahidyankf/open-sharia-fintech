suspend fun loadDashboard(api: DashboardApi): Dashboard = coroutineScope {
  val profile = async { api.profile() }
  val notes = async { api.notes() }
  Dashboard(profile.await(), notes.await())
}
