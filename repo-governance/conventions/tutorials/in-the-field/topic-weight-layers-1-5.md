---
description: The topic-weight numbering ranges for the Foundation, Quality Foundation, Core Concepts, Security/Configuration, and Data Management layers.
when_to_use: Use when assigning a topic weight to a guide in the Foundation-through-Data-Management range.
---

# Topic Weight Layers 1-5

## 1. **Foundation Layer** (10000000-1000000X)

**What**: Essential tools, setup, and basic observability

**Why first**: Can't practice production patterns without basic infrastructure

**Domain examples**:

- **Programming languages**: Build tools, linting, logging
- **DevOps**: Version control, CI basics, monitoring fundamentals
- **Cloud platforms**: Account setup, CLI tools, basic resource management
- **Databases**: Installation, connection management, query basics

**Principle**: Master tools before techniques

## 2. **Quality Foundation** (1000000X-1000000Y)

**What**: Testing, validation, and quality practices

**Why second**: Establish quality mindset BEFORE writing production code

**Domain examples**:

- **Programming languages**: TDD, BDD, static analysis
- **DevOps**: Infrastructure testing, policy validation, smoke tests
- **Cloud platforms**: Resource validation, cost monitoring, compliance checks
- **Databases**: Data validation, integrity constraints, backup verification

**Principle**: Test-first mindset prevents technical debt

## 3. **Core Concepts** (1000000Y-1000000Z)

**What**: Fundamental patterns, principles, and best practices

**Why third**: Establish proper design before complex implementations

**Domain examples**:

- **Programming languages**: Design principles (SOLID), idioms, type systems
- **DevOps**: Infrastructure as Code principles, immutability, declarative config
- **Cloud platforms**: Well-Architected Framework, cost optimization, tagging strategies
- **Databases**: Normalization, indexing strategies, query optimization basics

**Principle**: Understand fundamentals before frameworks

## 4. **Security and Configuration** (1000000Z-1000000W)

**What**: Authentication, authorization, secrets management, externalized configuration

**Why fourth**: Never store data or deploy without proper security

**Domain examples**:

- **Programming languages**: Authentication flows, input validation, secret management
- **DevOps**: Secrets management, RBAC, policy enforcement
- **Cloud platforms**: IAM, encryption, network security, compliance
- **Databases**: User management, encryption at rest/transit, audit logging

**Principle**: Security before data and deployment

## 5. **Data Management** (1000000W-1000000V)

**What**: Persistence, state management, data flows

**Why fifth**: Data handling requires security foundation from previous layer

**Domain examples**:

- **Programming languages**: SQL databases, NoSQL, caching, state management
- **DevOps**: State backends, artifact storage, log aggregation
- **Cloud platforms**: Object storage, managed databases, data lakes
- **Databases**: Replication, sharding, partitioning, backup strategies

**Principle**: Secure first, then persist
