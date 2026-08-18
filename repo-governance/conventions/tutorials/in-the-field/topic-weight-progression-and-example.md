---
title: "Topic Weight Progression, Customization, and Java Example"
description: The pedagogical rationale behind the ten-layer progression, how to customize it per domain, and a full worked Java weight assignment.
when_to_use: Use when adapting the topic-weight scheme to a new language or reviewing a complete worked example.
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

# Topic Weight Progression, Customization, and Java Example

**Layer Dependencies** (can't skip):

```
Foundation → Quality → Core → Security → Data → Integration → Advanced → Deploy → Optimize → Meta
```

**Key Insights**:

1. **Can't skip layers**: Need foundation before quality, security before data
2. **Security early**: Always before persistence and deployment
3. **Simple before complex**: Core patterns before advanced patterns
4. **Deploy after build**: Infrastructure knowledge after having working code
5. **Optimize last**: Performance tuning after correct, tested implementation

## Domain-Specific Customization

When creating in-the-field content for a new domain:

1. **Identify domain foundation**: What tools/setup are prerequisite?
2. **Map quality practices**: How does testing/validation work in this domain?
3. **Extract core concepts**: What are fundamental patterns/principles?
4. **Define security requirements**: Authentication, authorization, secrets
5. **Specify data patterns**: How is state/data managed?
6. **Outline integration**: How do systems communicate?
7. **Advanced scenarios**: Domain-specific complex patterns
8. **Deployment approach**: How to get to production?
9. **Optimization targets**: Performance, cost, resource optimization
10. **Common mistakes**: Domain-specific anti-patterns

## Example: Java Programming Language

See actual implementation in `/apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/java/in-the-field/`:

```yaml
# Foundation Layer (10000000-10000003)
overview.md:                    weight: 10000000  # What is in-the-field
build-tools.md:                 weight: 10000001  # Maven/Gradle
linting-and-formatting.md:      weight: 10000002  # Code quality
logging.md:                     weight: 10000003  # Observability

# Quality Foundation (10000004-10000005)
test-driven-development.md:     weight: 10000004
behavior-driven-development.md: weight: 10000005

# Core Concepts (10000006-10000009)
design-principles.md:           weight: 10000006  # SOLID, DRY, YAGNI
best-practices.md:              weight: 10000007  # Java idioms
type-safety.md:                 weight: 10000008
functional-programming.md:      weight: 10000009

# Core Patterns (10000010-10000012)
dependency-injection.md:        weight: 10000010
domain-driven-design.md:        weight: 10000011
finite-state-machines.md:       weight: 10000012

# Security and Configuration (10000013-10000015)
configuration.md:               weight: 10000013
authentication.md:              weight: 10000014
security-practices.md:          weight: 10000015

# Data Management (10000016-10000017)
sql-database.md:                weight: 10000016
nosql-databases.md:             weight: 10000017

# Integration Patterns (10000018-10000021)
web-services.md:                weight: 10000018
json-and-api-integration.md:    weight: 10000019
messaging.md:                   weight: 10000020
caching.md:                     weight: 10000021

# Advanced Patterns (10000022-10000024)
concurrency-and-parallelism.md: weight: 10000022
reactive-programming.md:        weight: 10000023
resilience-patterns.md:         weight: 10000024

# Deployment and Operations (10000025-10000027)
docker-and-kubernetes.md:       weight: 10000025
ci-cd.md:                       weight: 10000026
cloud-native-patterns.md:       weight: 10000027

# Optimization (10000028-10000029)
performance.md:                 weight: 10000028
cli-app.md:                     weight: 10000029

# Meta Topics (10000030)
anti-patterns.md:               weight: 10000030
```

This Java example follows universal principles while adapting to language-specific concerns.
