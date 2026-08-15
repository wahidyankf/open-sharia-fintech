package org.ayokoding.enterprise;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ItemServiceTest {
    @Autowired ItemService service;

    @Test void persistsAndReadsAnItem() {
        Item saved = service.create("primer");
        assertEquals("primer", service.get(saved.id()).name());
    }

    @Test void returnsAStableNotFoundFailure() {
        assertThrows(ItemNotFound.class, () -> service.get(999999L));
    }
}
