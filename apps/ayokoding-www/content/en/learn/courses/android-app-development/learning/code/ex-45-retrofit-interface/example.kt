interface NotesApi {
  @GET("notes") suspend fun fetchNotes(): List<NoteDto>
  @GET("notes/{id}") suspend fun fetchNote(@Path("id") id: String): NoteDto
}
