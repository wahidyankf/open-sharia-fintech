val showArchived: Flow<Boolean> = context.dataStore.data
  .map { preferences -> preferences[SHOW_ARCHIVED] ?: false }
  .catch { error -> if (error is IOException) emit(emptyPreferences()) else throw error }
