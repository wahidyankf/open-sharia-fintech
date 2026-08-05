val titles: Flow<List<String>> = dao.observeAll()
  .map { notes -> notes.filterNot { it.title.isBlank() }.map { it.title } }
