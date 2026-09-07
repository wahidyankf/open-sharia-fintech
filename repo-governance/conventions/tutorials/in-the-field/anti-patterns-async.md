---
description: The production consequences (CPU thrashing, deadlocks) of using async frameworks without threading fundamentals.
when_to_use: Use when explaining the risk of teaching async frameworks before threading basics.
---

# Anti-Pattern: Async Frameworks Without Threading Knowledge

**FAIL: Starting with Reactive Streams without understanding Threads**

```java
// Developer jumps directly to Project Reactor
Flux.fromIterable(items)
    .flatMap(item -> processAsync(item))
    .subscribe(result -> System.out.println(result));
// What thread executes this?
// How many threads in pool?
// Why is CPU at 100%?
// How to control concurrency?
```

**Problems**:

- Doesn't understand thread scheduling (CPU thrashing from too many threads)
- Can't control concurrency (overwhelms downstream services)
- Deadlocks and race conditions (doesn't understand thread safety)
- When debugging: Can't read thread dumps (doesn't know thread states)

**PASS: Learning ExecutorService first, then Reactor**

```java
// Step 1: Understand ExecutorService (standard library)
ExecutorService executor = Executors.newFixedThreadPool(10);
for (Item item : items) {
    executor.submit(() -> {
        Result result = process(item);
        System.out.println(result);
    });
}
executor.shutdown();
// Now understands: Thread pool, task submission, concurrency limits

// Step 2: Adopt Project Reactor (framework)
Flux.fromIterable(items)
    .flatMap(item -> Mono.fromCallable(() -> process(item))
        .subscribeOn(Schedulers.boundedElastic()), 10)  // Concurrency: 10
    .subscribe(result -> System.out.println(result));
// Now understands: flatMap concurrency parameter limits parallel execution
// Knows why CPU at 100%: Too many parallel operations (learned from thread pool sizing)
// Can optimize: Sets appropriate concurrency based on CPU cores (learned from ExecutorService)
// Can debug: Reads thread dumps, recognizes scheduler thread pools
```

**Why standard library first matters**: ExecutorService teaches thread pool fundamentals and concurrency control. When Reactor app has performance issues, developer knows to check flatMap concurrency and scheduler configuration. Understands backpressure because learned about bounded queues in ExecutorService. Can optimize thread pool size based on workload type (CPU-bound vs I/O-bound).
