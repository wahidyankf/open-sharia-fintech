---
title: "Guide Structure Part 2: Standard Library First — HTTP Client Example"
description: The worked standard-library HTTP client example (java.net.http.HttpClient) and its production limitations.
when_to_use: Use when writing the standard-library HTTP client example for a Part 2 section.
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

# Guide Structure Part 2: Standard Library First — HTTP Client Example

**Example 2: HTTP Client with Standard Library**

```java
import java.net.URI;
// => URI class for parsing and validating URLs
import java.net.http.HttpClient;
// => HTTP client from Java 11+ standard library
import java.net.http.HttpRequest;
// => Immutable HTTP request builder
import java.net.http.HttpResponse;
// => HTTP response container
// => Java 11+ standard library
// => No external dependencies required
// => Supports HTTP/1.1 and HTTP/2

public class HttpExample {
    // => Standard library HTTP example
    // => Demonstrates basic GET request

    public static void main(String[] args) throws Exception {
        // => main() throws Exception for simplicity
        // => Production code should handle exceptions
        // => Synchronous blocking HTTP client

        HttpClient client = HttpClient.newHttpClient();
        // => Creates HTTP/2 client with default config
        // => Reusable for multiple requests
        // => Connection pooling built-in
        // => Thread-safe (share across application)

        HttpRequest request = HttpRequest.newBuilder()
            // => Builder pattern for request construction
            .uri(URI.create("https://api.example.com/users"))
            // => Validates URI format at runtime
            // => Supports HTTP/HTTPS protocols
            // => URI.create() throws IllegalArgumentException if invalid
            .header("Accept", "application/json")
            // => Sets Accept header for JSON response
            // => Multiple headers allowed
            .GET()
            // => HTTP GET method (also POST, PUT, DELETE)
            // => Default method if not specified
            .build();
        // => Builds immutable request object
        // => Cannot be modified after build()

        HttpResponse<String> response = client.send(
            request,
            HttpResponse.BodyHandlers.ofString()
        );
        // => Synchronous blocking call
        // => Blocks current thread until response received
        // => BodyHandlers.ofString() reads response as String
        // => Handles connection, reading, closing automatically
        // => Throws IOException on network error

        int statusCode = response.statusCode();
        // => statusCode is 200, 404, 500, etc.
        // => HTTP status code from server
        // => 2xx success, 4xx client error, 5xx server error

        String body = response.body();
        // => body is response body as String
        // => No automatic JSON parsing
        // => Must parse manually or use library
    }
    // => No connection cleanup needed
    // => HttpClient handles resource management
}
```

**Limitations for production HTTP**:

- No automatic retry (manual retry logic required)
- No circuit breaker (failures cascade to callers)
- Limited request/response interceptors (no logging, metrics)
- No reactive/async composition (only blocking or callbacks)
- Manual error handling (no declarative error policies)
- No connection pool tuning (uses default settings)
