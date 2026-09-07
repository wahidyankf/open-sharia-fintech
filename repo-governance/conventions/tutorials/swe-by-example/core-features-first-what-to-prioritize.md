---
description: "Lists which core/built-in features to prioritize for programming languages, frameworks, and platforms, with worked examples across React, Vue, Node.js, and Spring."
when_to_use: "Read when you need the concrete checklist of what counts as a core/built-in feature to teach first for a given language, framework, or platform."
---

# Core Features First: What to Prioritize

**PASS: Use core/built-in features**:

**For programming languages**:

- Built-in language syntax and semantics
- Standard library packages shipping with the language runtime
- Core APIs requiring no installation (Java: `java.util.*`, `java.io.*`, Python: `json`, `os`, `sys`)
- Platform-provided testing frameworks when part of standard toolchain

**For frameworks**:

- Core primitives and built-in features before third-party extensions
- Framework-provided state management before external libraries
- Native routing/navigation before routing libraries
- Built-in HTTP clients before external client libraries

**For platforms**:

- Built-in capabilities and native APIs before add-ons
- Platform-standard patterns before third-party abstractions
- Core tooling before convenience wrappers

**Examples**:

**Programming Languages**:

- JSON processing: Use `java.util.json` (Java 11+), `json` module (Python), `encoding/json` (Go)
- HTTP clients: Use `java.net.http.HttpClient` (Java 11+), `urllib` (Python), `net/http` (Go)
- Concurrency: Use `Thread`/`ExecutorService` (Java), `threading` (Python), goroutines (Go)
- Testing basics: Use assertions before frameworks (`assert` in Python, manual checks in Java before JUnit)

**React Framework**:

- State management: Use `useState`, `useReducer`, `Context API` before Zustand, Redux, Jotai
- Side effects: Use `useEffect` before external effect libraries
- Form handling: Use controlled components with `useState` before React Hook Form, Formik
- HTTP requests: Use `fetch` API with `useEffect` before React Query, SWR

**Vue Framework**:

- State management: Use `ref`, `reactive`, `computed` before Pinia, Vuex
- Composition: Use Vue Composition API before external composables libraries
- Routing: Use Vue Router (official) before third-party navigation libraries

**Node.js Platform**:

- HTTP servers: Use `http.createServer` before Express, Fastify, Koa
- File operations: Use `fs` module before third-party file libraries
- Path manipulation: Use `path` module before path utility libraries

**Spring Framework**:

- Dependency Injection: Use Spring Core `@Component`, `@Autowired` before Spring Boot auto-configuration
- Configuration: Use explicit `@Configuration` classes before `application.properties` magic
- Web: Understand `@Controller`, `@RequestMapping` before Spring Boot REST conventions
