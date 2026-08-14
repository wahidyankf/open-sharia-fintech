---
title: "Anti-Pattern: Dependency Injection Frameworks Without Manual Wiring"
description: The production consequences (circular dependencies, lifecycle confusion) of using a DI framework without manual-wiring fundamentals.
when_to_use: Use when explaining the risk of teaching a DI framework before manual dependency wiring.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - in-the-field
  - education
  - production-ready
created: 2026-02-04
---

# Anti-Pattern: Dependency Injection Frameworks Without Manual Wiring

**FAIL: Starting with Spring DI without understanding object composition**

```java
// Developer jumps directly to Spring DI
@Service
public class OrderService {
    @Autowired
    private PaymentService paymentService;
    // How does @Autowired work?
    // When is paymentService injected?
    // Why NullPointerException on startup?
}
```

**Problems**:

- Doesn't understand object lifecycle (when beans created, injected)
- Can't debug circular dependencies (Spring fails with cryptic error)
- Doesn't know when to use constructor vs field injection
- Magic behavior: Doesn't understand what @Autowired does

**PASS: Learning manual DI first, then Spring**

```java
// Step 1: Understand manual dependency injection (standard approach)
public class OrderService {
    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;  // Manual injection
    }
}

// Wiring in main()
PaymentService paymentService = new PaymentService();
OrderService orderService = new OrderService(paymentService);
// Now understands: Dependencies injected via constructor
// Object lifecycle: PaymentService created first, then OrderService

// Step 2: Adopt Spring DI (framework)
@Service
public class OrderService {
    private final PaymentService paymentService;

    @Autowired  // Spring injects via constructor
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
// Now understands: @Autowired tells Spring to inject PaymentService
// Knows when injected: During Spring context initialization
// Can debug: Understands circular dependency errors (A needs B, B needs A)
// Can optimize: Uses constructor injection (immutable, testable)
```

**Why standard library first matters**: Manual dependency injection teaches object composition and lifecycle. When Spring reports circular dependency, developer visualizes constructor call chain (learned from manual wiring). Understands when to use interfaces vs concrete classes because manually composed dependencies. Can test without Spring because knows how to wire objects.
