# 85 · Enterprise Java & the JVM (By Example, Java †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · Java † · Learn 185 / Drill 285 · Nvim-ready
Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: enterprise Java as it is actually built and run — the Spring/Spring Boot ecosystem,
dependency injection as the organizing principle, and the JVM underneath (JIT, garbage collection, the
memory model). The primer [`84-just-enough-java`](./84-just-enough-java.md) gives you the language;
this topic gives you the framework conventions and the runtime that a large Java shop lives inside, with
the trade-offs of the heavyweight-framework approach made explicit rather than assumed. `†`: Java on a
current LTS JDK, Spring Boot, and a build tool (Maven/Gradle).

## Why this exists · the big idea

- **The problem before the solution**: wiring a large application by hand — constructing every service,
  passing every dependency, managing every lifecycle — collapses under its own weight; enterprise codebases
  needed a way to declare _what_ depends on _what_ and let the framework assemble it, plus a runtime that
  stays fast without manual memory management.
- **Keep-this-if-you-forget-everything**: inversion of control is the load-bearing idea — components declare
  their dependencies and the container supplies them, so wiring becomes configuration instead of code, and
  the JVM's managed runtime (JIT + GC) buys portability and speed at the cost of a warm-up and a tuning
  surface you must understand.
- **Big ideas touched**: `coupling-vs-cohesion` (dependency injection inverts control so modules couple to
  interfaces, not concrete constructors — the framework's whole reason to exist), `abstraction-and-its-cost`
  (Spring's auto-configuration hides enormous machinery; the leverage is real and so is the leak when the
  magic misfires).

## Prerequisites

- **Prior topics**: [topic 84 Just Enough Java](./84-just-enough-java.md) (the language, records, streams,
  the memory model at a glance) and [topic 42 Software Architecture](./42-software-architecture.md) (layering,
  boundaries, and where a DI container fits an architecture).
- **Tools & environment**: a macOS/Linux/Windows machine; a **JDK** pinned to a current LTS; **Spring Boot**
  via **Maven or Gradle**; `curl` for exercising endpoints; Neovim/VSCode with the Java LSP (DD-17). Keep the
  JDK and Spring Boot versions unpinned in prose — re-pull at authoring time.
- **Assumed knowledge**: classes/interfaces and generics (topic 84); collections/streams (topic 84);
  architectural layering and dependency direction (topic 42); building/serving an HTTP API (topic 11).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: dependency injection, Spring/Spring Boot's convention-over-configuration model,
  and the JVM's JIT + generational-GC design are evergreen and correctly left version-unpinned. Java's LTS
  cadence (a new LTS roughly every two years) means "current LTS JDK" and the matching Spring Boot line
  should be re-pulled at authoring time rather than pinned here.
- 2026-07-12 — verified: garbage-collector specifics (G1 as the default collector, ZGC as a low-pause
  alternative) are stable enough to name generically but move between JDK releases — describe them by role
  (throughput vs pause-time) rather than committing to a per-version default. (docs.oracle.com/en/java)

### DD-35 primary-source citations (fetched-and-read)

> Anti-hallucination (DD-35): every version/API below traces to a primary source a
> `web-researcher` fetched and read on 2026-07-12. Unverifiable claims are marked `[Needs Verification]`.

- **Spring versions** — current is **Spring Boot 4.1.0** on **Spring Framework 7.0.8+**, with a **Java 17
  baseline** (Java 25 LTS recommended); shipped prose keeps versions unpinned and re-pulls at authoring
  time. Verified against spring.io / the Spring Boot reference docs.
- **Test-mock annotation renamed** — `@MockBean` is **deprecated/removed in favor of `@MockitoBean`**
  (Spring Framework 6.2+ / Boot 3.4+). Cite `@MockitoBean`, never `@MockBean`, for mocking beans in slice
  tests. Verified against the Spring Framework docs.
- **Jackson 3 is the default** — Spring Boot 4 defaults JSON (de)serialization to **Jackson 3**
  (`tools.jackson`), not Jackson 2 — note the package move if quoting APIs.
- **JUnit 6** — Spring Boot 4's test starter uses **JUnit 6** (`org.junit.jupiter`), not JUnit 5.
- **JVM runtime** — DI/IoC, the JIT (interpret → tiered-compile → optimize) + warm-up, and generational GC
  are evergreen; **G1 is the default collector**, **ZGC** the low-pause alternative — described by role
  (throughput vs pause), not a per-version default (docs.oracle.com/en/java).

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · dependency-injection** — components declare their dependencies and the container supplies them, so wiring becomes configuration.
- **co-02 · inversion-of-control** — the IoC container owns object construction and lifecycle instead of the code.
- **co-03 · constructor-injection** — constructor injection is the preferred, immutable, testable form of DI.
- **co-04 · beans** — `@Component`/`@Service`/`@Repository` register beans the container manages and can `@Qualifier`-disambiguate.
- **co-05 · bean-lifecycle** — beans have a lifecycle and scopes (singleton by default, prototype per-request).
- **co-06 · configuration** — `@Configuration` classes with `@Bean` methods declare beans explicitly.
- **co-07 · autoconfiguration** — Spring Boot auto-configures beans from the classpath (convention over configuration).
- **co-08 · starters** — Spring Boot starters bundle coherent dependency sets (e.g. `spring-boot-starter-web`).
- **co-09 · application-properties** — `application.yml`/`.properties` externalize configuration, injectable with `@Value`.
- **co-10 · profiles** — `@Profile`/active profiles select environment-specific beans and properties.
- **co-11 · rest-controller** — `@RestController` maps HTTP requests to handler methods returning JSON.
- **co-12 · request-mapping** — `@GetMapping`/`@PostMapping` bind path variables, request params, and bodies.
- **co-13 · service-layer** — a `@Service` layer holds business logic between controller and repository.
- **co-14 · repository-layer** — a Spring Data repository abstracts persistence behind an interface.
- **co-15 · validation** — `@Valid` + Bean Validation constraints (`@NotNull`/`@Size`) reject bad input.
- **co-16 · error-handling** — `@ControllerAdvice`/`@ExceptionHandler` map exceptions to a structured error envelope.
- **co-17 · jpa-entity** — `@Entity` maps an object to a relational table.
- **co-18 · jpa-repository** — `JpaRepository` provides CRUD, derived queries, and pagination.
- **co-19 · transactions** — `@Transactional` defines an atomic boundary that commits or rolls back.
- **co-20 · n-plus-one** — the N+1 query trap in an ORM, diagnosed and fixed with a fetch join.
- **co-21 · json-serialization** — Jackson (de)serializes objects/DTOs to and from JSON.
- **co-22 · actuator** — Actuator exposes health and metrics endpoints for operations.
- **co-23 · testing-spring** — `@SpringBootTest` and slice tests (`@WebMvcTest`/`@DataJpaTest`) test layers in isolation or whole.
- **co-24 · mock-bean** — `@MockitoBean` replaces a bean with a Mockito mock in a test context.
- **co-25 · jvm-classloading** — the JVM loads classes lazily via class loaders.
- **co-26 · jit** — the JIT interprets then tier-compiles hot code, so performance improves after warm-up.
- **co-27 · gc-generational** — generational GC collects short-lived young objects cheaply and old objects rarely.
- **co-28 · gc-collectors** — the collector is chosen by role: G1 (default, throughput) vs ZGC (low-pause).
- **co-29 · memory-model** — heap growth and GC pauses under load are observable and tunable.
- **co-30 · packaging** — Spring Boot packages a self-contained runnable fat jar (`java -jar`).

## Tensions & trade-offs — when NOT to reach for this

- **Framework magic vs debuggability**: auto-configuration and classpath scanning assemble a working app
  with almost no code — until something wires wrong, and now you are debugging a graph you never wrote. The
  same leverage that speeds the happy path lengthens the failure path; the cost is a steep "what is actually
  happening" tax when the abstraction leaks.
- **Startup and footprint**: a JIT-warmed, reflection-heavy Spring app is superb for long-lived servers and
  poor for short-lived, cold-start workloads (serverless, CLIs) — where startup time and memory dominate, the
  heavyweight-framework approach is the wrong default; a lighter runtime or ahead-of-time compilation fits
  better.
- **When NOT to reach for it**: a small service, a script, or a latency-critical cold-start path does not
  need a DI container and an ORM. Reach for the enterprise stack when team size, longevity, and integration
  breadth make its conventions pay for their weight — not because Java implies Spring.

## Lineage — why it beat the alternative

- Enterprise Java's shape is a reaction to its own past. J2EE/EJB tried to standardize enterprise concerns
  but did so with heavyweight, ceremony-laden components; Spring won by inverting that — a lightweight IoC
  container plus POJOs, letting the framework wire plain objects instead of forcing them into an EJB mold.
  Spring Boot then removed the remaining XML-and-boilerplate friction with opinionated auto-configuration, so
  "convention over configuration" became the enterprise default. Underneath, the JVM's write-once-run-anywhere
  bargain plus a maturing JIT made managed-runtime performance acceptable for server workloads. What this
  hands forward: the DI + layered-service discipline reinforces [`42-software-architecture`](./42-software-architecture.md),
  and the managed-runtime intuition (JIT, GC, memory model) is the counterweight to the manual-memory world
  of the systems-programming topics.

## Worked examples

Colocated under `enterprise-java-and-the-jvm/learning/code/`; each runnable via Maven/Gradle and exercised
from the CLI with `curl` (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it
exercises. Concepts come before examples.

### Beginner

- **ex-01 · spring-boot-app** — a `@SpringBootApplication` starts — verify startup. (co-07)
- **ex-02 · component-bean** — a `@Component` registered as a bean — verify it's in the context. (co-04)
- **ex-03 · constructor-inject** — constructor injection of a dependency — verify the wiring. (co-03, co-01)
- **ex-04 · service-annotation** — a `@Service` bean — verify it's injectable. (co-04, co-13)
- **ex-05 · ioc-container** — the container assembling the graph — verify no manual wiring. (co-02)
- **ex-06 · bean-singleton** — a singleton-scoped bean — verify one instance. (co-05)
- **ex-07 · configuration-bean** — `@Configuration` + `@Bean` — verify a manually declared bean. (co-06)
- **ex-08 · starter-dependency** — a `spring-boot-starter-web` dependency — verify it builds. (co-08)
- **ex-09 · application-yml** — read a value from `application.yml` (`@Value`) — verify injection. (co-09)
- **ex-10 · profile-dev** — a `dev`-profile bean — verify profile activation. (co-10)
- **ex-11 · rest-controller** — a `@RestController` GET — verify a JSON response via `curl`. (co-11)
- **ex-12 · get-mapping** — `@GetMapping` with a path variable — verify routing. (co-12)
- **ex-13 · post-mapping** — `@PostMapping` with a body — verify it accepts JSON. (co-12)
- **ex-14 · request-param** — a `@RequestParam` — verify query binding. (co-12)
- **ex-15 · json-response** — a record/POJO serialized to JSON — verify the shape. (co-21)
- **ex-16 · json-request** — JSON deserialized to an object — verify the binding. (co-21)
- **ex-17 · service-called-by-controller** — a controller → service call — verify the layering. (co-13, co-11)
- **ex-18 · actuator-health** — the Actuator `/health` endpoint — verify `UP` via `curl`. (co-22)
- **ex-19 · actuator-metrics** — an Actuator metrics endpoint — verify a metric. (co-22)
- **ex-20 · package-jar** — build a runnable jar — verify `java -jar` runs it. (co-30)
- **ex-21 · run-jar** — run the packaged app — verify it serves. (co-30)
- **ex-22 · prototype-scope** — a prototype-scoped bean — verify a new instance per request. (co-05)
- **ex-23 · qualifier** — `@Qualifier` disambiguating beans — verify the right one is injected. (co-04)
- **ex-24 · property-override** — override a property per profile — verify the value. (co-09, co-10)
- **ex-25 · component-scan** — component scanning finding a bean — verify auto-registration. (co-04, co-07)
- **ex-26 · injected-list** — inject a `List` of beans — verify all are collected. (co-01)

### Intermediate

- **ex-27 · controller-service-repo** — a controller → service → repository stack — verify the flow. (co-11, co-13, co-14)
- **ex-28 · jpa-entity** — an `@Entity` mapped to a table — verify persistence. (co-17)
- **ex-29 · jpa-repository-crud** — `JpaRepository` save/`findById` — verify CRUD. (co-18)
- **ex-30 · jpa-derived-query** — a derived query method (`findByName`) — verify the query. (co-18)
- **ex-31 · save-via-curl** — a POST persists an entity — verify it's stored. (co-14, co-11)
- **ex-32 · read-via-curl** — a GET reads an entity — verify the JSON. (co-14, co-11)
- **ex-33 · update-delete** — update + delete a resource — verify the state change. (co-18)
- **ex-34 · validation-valid** — `@Valid` on a valid body — verify it passes. (co-15)
- **ex-35 · validation-invalid** — an invalid body → 400 — verify the rejection. (co-15)
- **ex-36 · constraint-annotations** — `@NotNull`/`@Size` constraints — verify enforcement. (co-15)
- **ex-37 · error-envelope** — `@ControllerAdvice` mapping errors to a JSON envelope — verify no stack trace. (co-16)
- **ex-38 · exception-handler** — `@ExceptionHandler` for a custom exception — verify the mapped status. (co-16)
- **ex-39 · not-found-404** — a missing resource → 404 with an envelope — verify the response. (co-16)
- **ex-40 · transaction-commit** — a `@Transactional` multi-step write commits — verify persistence. (co-19)
- **ex-41 · transaction-rollback** — a failure mid-transaction rolls back — verify no partial write. (co-19)
- **ex-42 · n-plus-one-observe** — observe an N+1 query in the logs — verify the query count. (co-20)
- **ex-43 · n-plus-one-fix** — a fetch join fixes N+1 — verify the count drops. (co-20)
- **ex-44 · dto-mapping** — an entity → DTO mapping — verify the API shape. (co-21, co-17)
- **ex-45 · pagination** — a paged repository query — verify a page. (co-18)
- **ex-46 · springboot-test** — a `@SpringBootTest` loading the context — verify it starts. (co-23)
- **ex-47 · web-mvc-test** — a `@WebMvcTest` slice test — verify a controller in isolation. (co-23)
- **ex-48 · data-jpa-test** — a `@DataJpaTest` slice — verify the repository. (co-23, co-18)
- **ex-49 · mockito-bean** — `@MockitoBean` mocking a service dependency — verify the mock. (co-24)
- **ex-50 · mock-return-stub** — stub a mocked bean's return — verify the stubbed value. (co-24)
- **ex-51 · mockmvc-request** — a MockMvc request assertion — verify status + body. (co-23, co-11)
- **ex-52 · integration-persist-test** — an integration test persisting + reading — verify the round-trip. (co-23, co-18)

### Advanced

- **ex-53 · classloading** — observe class loading of a class — verify it's loaded. (co-25)
- **ex-54 · jit-warmup** — observe JIT warm-up (interpret → compile) — verify the post-warm-up speedup. (co-26)
- **ex-55 · jit-tiered** — tiered compilation levels — verify the progression. (co-26)
- **ex-56 · gc-generational** — a young/old generation collection — verify the GC logs. (co-27)
- **ex-57 · gc-g1-default** — G1 as the default collector — verify it's active. (co-28)
- **ex-58 · gc-zgc-lowpause** — the ZGC low-pause alternative — verify pause behaviour. (co-28)
- **ex-59 · gc-throughput-vs-pause** — compare G1 vs ZGC throughput/pause — verify the trade-off. (co-28)
- **ex-60 · heap-under-load** — heap growth under load — verify the allocation behaviour. (co-29)
- **ex-61 · gc-log-reading** — read a GC log — verify pause times. (co-29, co-27)
- **ex-62 · load-warmup-curve** — a warm-up latency curve under load — verify it flattens. (co-26, co-29)
- **ex-63 · profile-prod-config** — a `prod` profile with tuned GC flags — verify the config. (co-10, co-28)
- **ex-64 · actuator-under-load** — Actuator metrics during load — verify the live metrics. (co-22, co-29)
- **ex-65 · transaction-isolation** — a transaction isolation setting — verify the behaviour. (co-19)
- **ex-66 · lazy-vs-eager-fetch** — lazy vs eager JPA fetch — verify the difference. (co-20, co-17)
- **ex-67 · validation-group** — a validation group — verify conditional validation. (co-15)
- **ex-68 · global-error-model** — a consistent global error model across endpoints — verify uniformity. (co-16)
- **ex-69 · full-crud-service** — a full CRUD service with validation + errors — verify all paths. (co-11, co-14, co-15, co-16)
- **ex-70 · di-graph-inspect** — inspect the bean dependency graph — verify the wiring. (co-01, co-02)
- **ex-71 · packaged-runnable** — the packaged runnable artifact serves — verify `java -jar`. (co-30)
- **ex-72 · test-suite-green** — the full test suite (JUnit 6) passes — verify green. (co-23, co-24)
- **ex-73 · service-under-load-clean** — the service stable under sustained load — verify no leak. (co-29)
- **ex-74 · n-plus-one-then-fix** — N+1 observed then fixed end-to-end — verify the query count drops. (co-20)
- **ex-75 · jit-gc-observed** — JIT warm-up + GC behaviour both observed under load — verify both. (co-26, co-27)
- **ex-76 · full-spring-slice** — DI + web + JPA + transaction + validation + Actuator in one service — verify the whole. (co-01, co-11, co-18, co-19, co-22)
- **ex-77 · integration-runtime-observed** — the whole service tested + run under load with JIT/GC observed — verify it. (co-23, co-26, co-28)
- **ex-78 · capstone-spring-service** — a Spring Boot service: constructor-injected layers, JPA persistence with a transaction, validation + error envelope, health/metrics endpoints, then run under load observing JIT + GC — verify the app starts and serves, DI is explicit, persistence + transaction + validation are correct, N+1 is resolved, and JIT/GC behaviour + the collector trade-off are observed. (co-01, co-19, co-22, co-26, co-28)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small but idiomatic Spring Boot service — constructor-injected layers, JPA persistence
  with a transaction boundary, validation and an error model, and health/metrics endpoints — then exercise
  it under load and observe the JVM's JIT and GC behaviour, demonstrating both the framework conventions and
  the runtime beneath them.
- **Concepts exercised**: [ ] constructor dependency injection (co-01, co-03) [ ] Spring Boot
  auto-configuration + profiles (co-07, co-10) [ ] controller/service/repository layering (co-11, co-13, co-14)
  [ ] JPA persistence with a transaction (co-17, co-18, co-19) [ ] validation + error envelope (co-15, co-16)
  [ ] health/metrics endpoint (co-22) [ ] JIT warm-up + GC observation under load (co-26, co-27, co-28).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a Spring Boot app with constructor-injected service + repository beans
     and an Actuator-style health/metrics endpoint. Verify the app starts and `curl` of the health endpoint
     returns healthy.
  2. Add a controller → service → JPA-repository CRUD path with validation and a structured error response.
     Verify a valid write persists (`curl`) and an invalid one returns the error envelope, not a stack trace.
  3. Wrap a multi-step write in a transaction and reproduce/fix an N+1 query. Verify the transaction rolls
     back on failure and the N+1 is gone (query count drops).
  4. Drive the service under a small load; capture JIT warm-up and GC behaviour, then swap the collector.
     Verify warm-up is observable and the throughput/pause trade-off between collectors is visible.
- **Acceptance criteria**: the app starts and serves; DI wiring is explicit (constructor injection);
  persistence + transaction + validation behave correctly; N+1 is resolved; JIT/GC behaviour is observed and
  the collector trade-off is demonstrated.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Java Concurrency in Practice** — Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes,
  Doug Lea (2006). The definitive treatment of the Java Memory Model and concurrent programming, essential
  for correct enterprise JVM code.
- **Spring in Action** — Craig Walls (6th ed., 2022). The long-running, most widely used introduction to the
  Spring Framework and Spring Boot ecosystem.
- **Java Performance** — Scott Oaks (2nd ed., 2020). Authoritative, in-depth guide to JVM tuning, garbage
  collection, and profiling for production Java systems.
- **Optimizing Java** — Benjamin J. Evans, James Gough, Chris Newland (2018). Practical JVM
  performance-engineering techniques by well-known JVM/Java Champions.

**Papers & articles**

- **The Java Virtual Machine Specification, Java SE 21 Edition** — Oracle America, Inc. (2023). The official
  normative reference for JVM bytecode, the class-file format, and execution semantics.
  <https://docs.oracle.com/javase/specs/jvms/se21/jvms21.pdf>

---

← Previous: [84 · Just Enough Java](./84-just-enough-java.md) · Next: [86 · Lisp](./86-lisp.md) →
