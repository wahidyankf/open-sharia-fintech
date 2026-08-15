package org.ayokoding.enterprise;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
class ApiErrors {
    @ExceptionHandler(ItemNotFound.class) @ResponseStatus(HttpStatus.NOT_FOUND)
    Map<String, String> notFound(ItemNotFound error) { return Map.of("code", "not_found", "message", error.getMessage()); }
}
class ItemNotFound extends RuntimeException {
    ItemNotFound(long id) { super("item " + id + " was not found"); }
}
