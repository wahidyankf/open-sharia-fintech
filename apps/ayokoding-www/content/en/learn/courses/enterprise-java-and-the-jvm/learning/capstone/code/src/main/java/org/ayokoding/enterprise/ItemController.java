package org.ayokoding.enterprise;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/items")
class ItemController {
    private final ItemService service;
    ItemController(ItemService service) { this.service = service; }

    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    ItemResponse create(@Valid @RequestBody CreateItem request) {
        Item item = service.create(request.name());
        return new ItemResponse(item.id(), item.name());
    }

    @GetMapping("/{id}")
    ItemResponse get(@PathVariable long id) {
        Item item = service.get(id);
        return new ItemResponse(item.id(), item.name());
    }

    record CreateItem(@NotBlank String name) {}
    record ItemResponse(Long id, String name) {}
}
