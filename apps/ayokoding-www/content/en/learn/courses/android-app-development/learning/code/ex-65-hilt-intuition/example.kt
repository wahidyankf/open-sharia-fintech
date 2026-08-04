@HiltViewModel
class NotesViewModel @Inject constructor(
  private val repository: NotesRepository
) : ViewModel()

@Module @InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
  @Binds abstract fun bindNotesRepository(impl: OfflineNotesRepository): NotesRepository
}
