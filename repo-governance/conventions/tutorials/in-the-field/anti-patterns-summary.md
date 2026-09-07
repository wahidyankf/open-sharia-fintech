---
description: The consolidated summary of why standard-library-first prevents the five documented anti-patterns.
when_to_use: Use when you need the closing summary argument for the standard-library-first principle.
---

# Anti-Patterns Summary: Standard Library First Prevents Production Disasters

| Anti-Pattern                          | Production Consequence                   | Standard Library Foundation                  |
| ------------------------------------- | ---------------------------------------- | -------------------------------------------- |
| JUnit without assertions              | Can't debug test failures                | `assert` keyword teaches testing             |
| Hibernate without JDBC                | N+1 queries, connection pool exhaustion  | JDBC teaches SQL and connections             |
| Spring Boot without HTTP fundamentals | Wrong status codes, security holes       | HttpClient teaches HTTP protocol             |
| Reactive Streams without threads      | CPU thrashing, deadlocks                 | ExecutorService teaches concurrency          |
| Spring DI without manual wiring       | Circular dependencies, unclear lifecycle | Manual DI teaches object composition         |
| Jackson without standard library JSON | Can't debug parsing errors               | javax.json teaches JSON structure            |
| OkHttp without HttpClient             | Over-engineering simple use cases        | HttpClient teaches when complexity justified |

**Key insight**: Framework magic becomes comprehensible when you've implemented similar functionality with standard library. Debugging, optimization, and informed decision-making all require foundational understanding.
