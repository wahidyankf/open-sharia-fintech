---
title: "Guide Structure Part 3: OkHttp GET Method and Benefits"
description: The OkHttp client's get() method implementation and the rationale for choosing OkHttp over the standard library.
when_to_use: Use when writing the request/response half of an OkHttp example or justifying OkHttp's use.
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

# Guide Structure Part 3: OkHttp GET Method and Benefits

_(Continuing the `HttpClient` class from [OkHttp Client Setup](./guide-structure-part3-okhttp-client-setup.md).)_

```java
    public String get(String url) throws IOException {
        // => Synchronous GET request
        // => Throws IOException on network error
        // => Blocks calling thread until response

        Request request = new Request.Builder()
            // => Builder pattern for request construction
            .url(url)
            // => Validates URL format
            // => Throws IllegalArgumentException if invalid
            .header("Accept", "application/json")
            // => Sets Accept header
            // => Tells server we want JSON response
            .build();
        // => Builds immutable request
        // => Cannot be modified after build()

        try (Response response = client.newCall(request).execute()) {
            // => try-with-resources auto-closes response body
            // => execute() is synchronous (blocks until response)
            // => newCall creates Call object (request executor)
            // => Response must be closed to release connection
            // => Connection returns to pool on close

            if (!response.isSuccessful()) {
                // => Checks status code (200-299 is successful)
                // => isSuccessful() returns false for 4xx, 5xx
                throw new IOException("Unexpected code " + response);
                // => Non-2xx throws IOException
                // => Production: log error, trigger circuit breaker
            }

            return response.body().string();
            // => Reads entire response body as String
            // => body() returns ResponseBody (closeable)
            // => string() consumes and closes body
            // => Entire response loaded into memory
        }
        // => response auto-closed by try-with-resources
        // => Connection returned to pool for reuse
    }
    // => No cleanup needed (OkHttpClient manages resources)
    // => Connection pool evicts idle connections automatically
}
```

**WHY OKHTTP**:

- Automatic retry with exponential backoff (prevents cascading failures)
- Request/response interceptors (logging, auth, metrics)
- Connection pooling (reuses connections, better performance)
- HTTP/2 support (multiplexing, server push)
- WebSocket support (full-duplex communication)
- Trade-off: External dependency (500KB) vs resilience features
