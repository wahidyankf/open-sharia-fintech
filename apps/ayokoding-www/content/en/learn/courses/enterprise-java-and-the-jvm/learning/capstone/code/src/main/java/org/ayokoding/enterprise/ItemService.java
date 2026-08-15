package org.ayokoding.enterprise;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
class ItemService {
    private final ItemRepository repository;
    ItemService(ItemRepository repository) { this.repository = repository; }

    @Transactional
    Item create(String name) { return repository.save(new Item(name)); }

    Item get(long id) {
        return repository.findById(id).orElseThrow(() -> new ItemNotFound(id));
    }
}
