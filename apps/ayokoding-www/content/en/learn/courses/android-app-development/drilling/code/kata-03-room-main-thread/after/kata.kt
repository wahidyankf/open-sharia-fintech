@Dao
interface NoteDao {
  @Query("SELECT * FROM notes") fun observeAll(): Flow<List<NoteEntity>>
}
class NotesViewModel(dao: NoteDao) : ViewModel() {
  val notes = dao.observeAll().map { it.map(NoteEntity::toNote) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
}
