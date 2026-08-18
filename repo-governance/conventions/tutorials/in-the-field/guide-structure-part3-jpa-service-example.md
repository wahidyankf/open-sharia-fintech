---
title: "Guide Structure Part 3: JPA Service Example"
description: The worked JPA/Hibernate @Service class example showing EntityManager-based find, save, and update operations.
when_to_use: Use when writing a JPA/Hibernate service-layer example.
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

# Guide Structure Part 3: JPA Service Example

Continued from [Guide Structure Part 3 — JPA Entity Example](./guide-structure-part3-jpa-entity-example.md).

```java
// Usage
@Service
// => Spring service component
// => Business logic layer (not controller, not repository)
public class UserService {
    // => Service encapsulates entity operations
    // => Transaction boundary (methods are transactional)

    @PersistenceContext
    // => Injects EntityManager from Spring
    // => Container-managed EntityManager
    // => Thread-safe (proxy to request-scoped EntityManager)
    private EntityManager entityManager;
    // => EntityManager is JPA interface
    // => Injected by Spring/container
    // => Manages entity lifecycle (persist, merge, remove, find)
    // => Provides L1 cache (persistence context)

    @Transactional
    // => @Transactional wraps in database transaction
    // => Commits on success, rolls back on exception
    // => Required for any database write operation
    public User findById(Long id) {
        // => Read operation (no transaction strictly required)
        // => @Transactional enables L1 cache for lazy loading
        // => Returns User with full data (including lazy fields)

        User user = entityManager.find(User.class, id);
        // => find() executes SELECT * FROM users WHERE id = ?
        // => Returns User object (automatic mapping)
        // => Caches result in L1 cache (EntityManager)
        // => Second find(id) hits cache (no SQL)
        // => Returns null if not found (not exception)

        return user;
        // => Transaction commits when method returns
        // => L1 cache cleared after commit
        // => User becomes detached (no longer tracked)
    }

    @Transactional
    // => Transaction required for write operations
    // => Rollback on RuntimeException
    public void save(User user) {
        // => Save new user to database
        // => INSERT operation

        entityManager.persist(user);
        // => persist() adds entity to persistence context
        // => INSERT executed on transaction commit (not immediately)
        // => Auto-generated ID populated after commit
        // => Entity becomes managed (tracked for changes)
        // => Flush happens before commit
    }

    @Transactional
    // => Transaction required for update
    public void update(User user) {
        // => Update existing user
        // => User is detached (from another request/session)

        User managed = entityManager.merge(user);
        // => merge() syncs detached entity with database
        // => Returns managed entity (tracked)
        // => Loads current state from DB, applies changes
        // => UPDATE executed on commit if fields changed
        // => Hibernate dirty checking detects changes
        // => Original user remains detached
    }
    // => EntityManager lifecycle managed by Spring
    // => No manual close() needed
    // => Connection returned to pool after transaction
}
```
