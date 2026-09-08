package com.oseplatform.lms.health;

import com.oseplatform.lms.contracts.HealthResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Serves {@code GET /api/v1/health}, the contract's liveness endpoint. */
@RestController
@RequestMapping("/api/v1")
public class HealthController {

  static final String HEALTHY_STATUS = "healthy";

  @GetMapping("/health")
  public ResponseEntity<HealthResponse> getHealth() {
    return ResponseEntity.ok(new HealthResponse().status(HEALTHY_STATUS));
  }
}
