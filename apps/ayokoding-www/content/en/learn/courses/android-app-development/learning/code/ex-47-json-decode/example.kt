@Serializable
data class NoteDto(val id: String, val title: String, val body: String, @SerialName("updated_at") val updatedAt: Long)
val retrofit = Retrofit.Builder().baseUrl("https://example.invalid/")
  .addConverterFactory(Json.asConverterFactory("application/json".toMediaType())).build()
