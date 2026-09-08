---
description: The production consequences (wrong status codes, security holes) of using a REST framework without HTTP fundamentals.
when_to_use: Use when explaining the risk of teaching a REST framework before HTTP basics.
---

# Anti-Pattern: REST Framework Without HTTP Fundamentals

**FAIL: Starting with Spring Boot without understanding HTTP**

```java
// Developer jumps directly to Spring Boot
@RestController
public class UserController {
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
// What HTTP method is this?
// What status code for not found?
// How to return 404 vs 500?
// What are HTTP headers?
```

**Problems**:

- Doesn't understand HTTP status codes (returns 200 when should return 404)
- Can't debug network issues (doesn't know HTTP headers, request/response cycle)
- Security vulnerabilities (doesn't validate input, allows injection)
- When API fails: Can't read HTTP logs (doesn't understand request structure)

**PASS: Learning HttpClient first, then Spring Boot**

```java
// Step 1: Understand java.net.http.HttpClient (standard library)
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users/1"))
    .header("Accept", "application/json")
    .GET()
    .build();
HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
int statusCode = response.statusCode();  // 200, 404, 500
// Now understands: HTTP method, headers, status codes, request/response

// Step 2: Adopt Spring Boot (framework)
@GetMapping("/users/{id}")
public ResponseEntity<User> getUser(@PathVariable Long id) {
    return userService.findById(id)
        .map(ResponseEntity::ok)           // 200 OK
        .orElse(ResponseEntity.notFound()  // 404 Not Found
                .build());
}
// Now understands: ResponseEntity sets status code (200/404)
// Knows when to return 404: User not found (learned from HTTP fundamentals)
// Can debug: Reads request headers, status codes in logs
// Can optimize: Uses appropriate status codes (201 Created, 204 No Content)
```

**Why standard library first matters**: HttpClient teaches HTTP protocol fundamentals. When Spring Boot endpoint returns wrong status code, developer knows to check ResponseEntity mapping. Understands security implications because learned about headers (authentication, CORS). Can debug API issues by reading HTTP logs.
