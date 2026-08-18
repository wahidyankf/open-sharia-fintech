---
title: "Guide Structure Part 3: OkHttp Client Setup"
description: The worked OkHttp production HTTP client example - imports, fields, and the retry/logging-interceptor constructor.
when_to_use: Use when writing the setup/configuration half of an OkHttp production example.
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

# Guide Structure Part 3: OkHttp Client Setup

**Example 2: Production HTTP with OkHttp**

```java
import okhttp3.*;
// => OkHttp HTTP client library (external dependency)
// => Industry standard for resilient HTTP
// => Supports HTTP/1.1, HTTP/2, WebSocket
// => Maven: com.squareup.okhttp3:okhttp:4.12.0

import java.util.concurrent.TimeUnit;
// => For timeout configuration
// => Java standard library time unit enum

import java.io.IOException;
// => Exception for network errors

public class HttpClient {
    // => Production HTTP client wrapper
    // => Encapsulates OkHttp configuration

    private final OkHttpClient client;
    // => OkHttpClient is thread-safe
    // => Share single instance across application
    // => Manages connection pool internally

    public HttpClient() {
        // => Constructor configures production client
        // => Called once at application startup
        // => Creates configured singleton

        this.client = new OkHttpClient.Builder()
            // => Builder pattern for configuration
            // => Immutable after build()
            .addInterceptor(new RetryInterceptor(3))
            // => Automatic retry up to 3 attempts
            // => Exponential backoff between retries
            // => Prevents cascading failures
            // => Custom interceptor (implements Interceptor)
            .addInterceptor(new LoggingInterceptor())
            // => Logs all requests/responses
            // => Interceptors run in order (retry → logging)
            // => Useful for debugging production issues
            .connectTimeout(10, TimeUnit.SECONDS)
            // => Connection timeout (prevents hanging)
            // => Throws SocketTimeoutException after 10s
            // => Applies to TCP handshake phase
            .readTimeout(30, TimeUnit.SECONDS)
            // => Read timeout for slow responses
            // => Applies to response body reading
            // => 30s for large payloads
            .build();
        // => Builds configured client
        // => Connection pooling enabled by default
        // => Max 5 idle connections, 5 minute keep-alive
    }
```

_(Continued in [OkHttp GET Method and Benefits](./guide-structure-part3-okhttp-get-method-and-benefits.md).)_
