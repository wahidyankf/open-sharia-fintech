---
title: "Topic Weight Layers 6-10"
description: The topic-weight numbering ranges for the Integration Patterns, Advanced Patterns, Deployment, Optimization, and Meta Topics layers.
when_to_use: Use when assigning a topic weight to a guide in the Integration-Patterns-through-Meta-Topics range.
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

# Topic Weight Layers 6-10

## 6. **Integration Patterns** (1000000V-1000000U)

**What**: System communication, APIs, messaging, inter-service patterns

**Why sixth**: Integration builds on data management and core patterns

**Domain examples**:

- **Programming languages**: REST APIs, messaging queues, API clients, caching
- **DevOps**: Service mesh, API gateways, event-driven pipelines
- **Cloud platforms**: Load balancers, API Gateway, event buses, service discovery
- **Databases**: Federation, change data capture (CDC), ETL pipelines

**Principle**: Internal correctness before external integration

## 7. **Advanced Patterns** (1000000U-1000000T)

**What**: Complex scenarios, async patterns, advanced architectures

**Why seventh**: Advanced patterns require solid grasp of fundamentals

**Domain examples**:

- **Programming languages**: Concurrency, reactive programming, resilience patterns
- **DevOps**: GitOps, progressive delivery, chaos engineering
- **Cloud platforms**: Multi-region, disaster recovery, auto-scaling strategies
- **Databases**: Distributed transactions, eventual consistency, CQRS

**Principle**: Complexity after simplicity

## 8. **Deployment and Operations** (1000000T-1000000S)

**What**: Containerization, orchestration, CI/CD, production deployments

**Why eighth**: Deploy after having correct, tested code to deploy

**Domain examples**:

- **Programming languages**: Docker, Kubernetes, CI/CD pipelines, blue-green deployment
- **DevOps**: Container orchestration, deployment strategies, rollback procedures
- **Cloud platforms**: Compute services, container registries, serverless deployments
- **Databases**: Migration strategies, zero-downtime deployments, rollback procedures

**Principle**: Build correctly, then deploy reliably

## 9. **Optimization and Observability** (1000000S-1000000R)

**What**: Performance tuning, monitoring, profiling, cost optimization

**Why ninth**: Optimize after correct implementation (premature optimization is evil)

**Domain examples**:

- **Programming languages**: Profiling, JVM tuning, memory optimization, benchmarking
- **DevOps**: Pipeline optimization, resource right-sizing, cost analysis
- **Cloud platforms**: Cost optimization, performance insights, reserved instances
- **Databases**: Query optimization, index tuning, connection pooling

**Principle**: Make it work, make it right, make it fast (in that order)

## 10. **Meta Topics** (1000000R+)

**What**: Anti-patterns, common mistakes, lessons learned, best practices synthesis

**Why last**: Learn from mistakes after understanding correct patterns

**Domain examples**:

- **Programming languages**: Anti-patterns, code smells, refactoring strategies
- **DevOps**: Pipeline anti-patterns, configuration drift pitfalls
- **Cloud platforms**: Common architectural mistakes, cost pitfalls, security gotchas
- **Databases**: Performance anti-patterns, schema design mistakes

**Principle**: Understand correct patterns before recognizing incorrect ones
