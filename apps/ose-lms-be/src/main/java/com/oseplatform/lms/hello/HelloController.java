package com.oseplatform.lms.hello;

import com.oseplatform.lms.contracts.HelloResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Serves {@code GET /api/v1/hello}, the reference request-to-response path. */
@RestController
@RequestMapping("/api/v1")
public class HelloController {

  static final String GREETING = "Hello, world!";

  @GetMapping("/hello")
  public ResponseEntity<HelloResponse> getHello() {
    return ResponseEntity.ok(new HelloResponse().message(GREETING));
  }
}
