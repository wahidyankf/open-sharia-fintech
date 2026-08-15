---
title: "Capstone: Task Board Report"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build and test a deliberately small task-board report. The project proves the primer surface:
a record models immutable task data, a sealed state hierarchy is rendered by exhaustive switch,
a generic list owns tasks, a stream creates the open-task report, and JUnit verifies the result.

## Run

    cd code
    mvn test
    mvn -q exec:java -Dexec.mainClass=org.ayokoding.java.TaskBoard

The Maven project declares Java 21 because its sealed-switch syntax is final there. JUnit is only a
test dependency; no application framework is introduced.

## Acceptance checks

- Task value equality works through its record components.
- The sealed state hierarchy has no default switch branch.
- Open task names are filtered and sorted through a stream pipeline.
- The JUnit test suite passes under Maven.

## Why this stays small

Spring, persistence, dependency injection, and server wiring would conceal the language choices the
course is meant to make visible. This capstone proves readiness for those next layers without
claiming to teach them.
