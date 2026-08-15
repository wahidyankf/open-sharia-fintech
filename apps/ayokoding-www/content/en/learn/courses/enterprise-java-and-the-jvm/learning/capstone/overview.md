---
title: "Capstone: Catalog Service"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

The capstone is a small Spring Boot catalog service with explicit constructor injection, JPA
persistence, validation, an error envelope, transaction boundary, and Actuator health. It uses
Spring Boot 4.1.0 because that is the official current release documented when this course was
authored; update the version deliberately when refreshing the course.

## Run

    cd code
    mvn test
    mvn spring-boot:run

Then request GET /actuator/health. POST a valid JSON catalog item to /items, and POST a blank name
to observe the structured validation response.

## JVM observation

Run the packaged jar with JVM logging only after the functional tests pass. Compare workload
warm-up and GC pause observations under a measured workload; do not claim a collector is universally
better without workload evidence.
