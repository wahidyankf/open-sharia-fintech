---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

The 28 concepts below are deliberately small enough for a productive JVM on-ramp. Every example
ex-01 through ex-80 is listed in the accompanying progression and has a colocated original source
artifact under [learning/code](./code/README.md).

## Concepts

1. **co-01 · jdk-build-tool** — Maven or Gradle compiles, runs, and tests a project.
2. **co-02 · main-method** — public static void main(String[]) is the classic entry point.
3. **co-03 · primitives** — primitives, wrappers, autoboxing, and String model basic values.
4. **co-04 · classes-objects** — classes define fields, constructors, and methods; new instantiates.
5. **co-05 · interfaces** — interfaces, including default methods, supply polymorphic contracts.
6. **co-06 · inheritance** — extends and Override express subtype behavior.
7. **co-07 · records** — records are concise immutable data carriers with value semantics.
8. **co-08 · sealed-types** — sealed hierarchies constrain permitted variants.
9. **co-09 · enums** — enums model a fixed typed set, optionally with data and methods.
10. **co-10 · instanceof-pattern** — pattern matching binds a tested value to a typed variable.
11. **co-11 · switch-pattern** — pattern switches dispatch over known variants.
12. **co-12 · exhaustive-switch** — a sealed hierarchy can make a switch exhaustive without default.
13. **co-13 · generics** — generic classes and methods preserve compile-time type information.
14. **co-14 · bounded-generics** — bounds and wildcards express safe constraints and variance.
15. **co-15 · collections-list** — lists preserve ordered, indexed values.
16. **co-16 · collections-map** — maps associate unique keys with values.
17. **co-17 · collections-set** — sets model uniqueness.
18. **co-18 · streams-map-filter** — streams compose lazy transformations and selection.
19. **co-19 · streams-collect** — collectors materialize or group a stream result.
20. **co-20 · streams-reduce** — reductions aggregate many values to one.
21. **co-21 · lambdas** — lambdas implement functional interfaces inline.
22. **co-22 · method-references** — method references abbreviate a simple forwarding lambda.
23. **co-23 · optional** — Optional models an intentionally possibly absent value.
24. **co-24 · exceptions** — checked/unchecked exceptions and explicit handling model failure.
25. **co-25 · jvm-memory** — stack, heap, GC eligibility, identity, and equality are different ideas.
26. **co-26 · junit-test** — a JUnit Jupiter test is executed by the build tool.
27. **co-27 · single-file-source-run** — java Hello.java launches one source file directly.
28. **co-28 · compact-source-and-instance-main** — Java 25 compact source and instance main reduce
    ceremonial startup code.

Read the examples in order, then complete the capstone before moving to enterprise JVM material.
