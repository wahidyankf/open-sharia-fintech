val Context.dataStore by preferencesDataStore("settings")
val SHOW_ARCHIVED = booleanPreferencesKey("show_archived")
suspend fun Context.setShowArchived(value: Boolean) {
  dataStore.edit { preferences -> preferences[SHOW_ARCHIVED] = value }
}
