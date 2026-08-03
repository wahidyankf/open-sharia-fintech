class NoteMapperTest {
  @Test fun entity_maps_to_domain_note() {
    val entity = NoteEntity("1", "Plan", "Ship", 42)
    assertEquals(Note("1", "Plan"), entity.toNote())
  }
}
