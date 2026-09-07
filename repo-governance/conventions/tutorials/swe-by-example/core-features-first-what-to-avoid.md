---
description: "Catalogs premature abstraction/extension anti-patterns for languages, frameworks, and platforms, with paired FAIL/PASS code examples."
when_to_use: "Read when writing or reviewing a beginner example to check it does not prematurely introduce a framework, library, or auto-magic tool."
---

# Core Features First: What to Avoid Initially

**FAIL: Premature abstraction/extension introduction**:

**Programming Languages**:

- External frameworks requiring dependency installation (Spring, React, Django, Flask)
- Third-party libraries not in standard distribution (Jackson, Gson, Requests, OkHttp)
- Platform-specific extensions beyond core language (Android SDK when teaching Java)
- Build tool configurations (Maven, Gradle) until necessary for production patterns

**Frameworks**:

- Third-party state management before framework primitives (Redux before React's useState/Context)
- Third-party form libraries before native form handling
- Third-party routing before understanding framework navigation
- Third-party styling solutions before CSS basics

**Platforms**:

- Third-party abstractions before understanding platform capabilities
- Convenience wrappers before core APIs
- Auto-magic tools before manual configuration

**Anti-pattern examples**:

**Programming Language (Java)**:

```java
// FAIL: Teaching JSON with Jackson in beginner section
import com.fasterxml.jackson.databind.ObjectMapper;  // External dependency

ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(person);
```

```java
// PASS: Teaching JSON with standard library first
import java.util.Map;
import java.io.StringWriter;
import javax.json.Json;                               // Standard library (Java 11+)

var writer = new StringWriter();
Json.createWriter(writer).write(personMap);
String json = writer.toString();
```

**React Framework**:

```jsx
// FAIL: Teaching state management with Redux before React primitives
import { useDispatch, useSelector } from "react-redux"; // External dependency

function Counter() {
  const count = useSelector((state) => state.count); // Redux abstraction
  const dispatch = useDispatch(); // Redux abstraction
  return <button onClick={() => dispatch({ type: "INCREMENT" })}>Count: {count}</button>;
}
```

```jsx
// PASS: Teaching state management with React primitives first
import { useState } from "react"; // Built-in React

function Counter() {
  const [count, setCount] = useState(0); // React primitive
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

**Spring Framework**:

```java
// FAIL: Teaching dependency injection with Spring Boot auto-configuration
@SpringBootApplication                                   // Spring Boot magic
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);  // Auto-configuration hides DI
    }
}
```

```java
// PASS: Teaching dependency injection with Spring Core first
@Configuration                                           // Explicit Spring Core
public class AppConfig {
    @Bean
    public UserService userService() {                   // Explicit bean definition
        return new UserService(userRepository());        // Manual dependency wiring
    }
    @Bean
    public UserRepository userRepository() {
        return new UserRepository();
    }
}
```

**Node.js Platform**:

```javascript
// FAIL: Teaching HTTP servers with Express before understanding http module
const express = require("express"); // External framework
const app = express();
app.get("/", (req, res) => res.send("Hello"));
app.listen(3000);
```

```javascript
// PASS: Teaching HTTP servers with built-in http module first
const http = require("http"); // Built-in Node.js
const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Hello");
});
server.listen(3000);
```
