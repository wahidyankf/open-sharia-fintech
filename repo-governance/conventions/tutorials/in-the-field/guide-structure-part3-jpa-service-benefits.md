---
description: Why JPA/Hibernate is chosen over raw JDBC for production persistence.
when_to_use: Use when justifying JPA/Hibernate's use over standard-library JDBC.
---

# Guide Structure Part 3: JPA/Hibernate Benefits

**WHY JPA/HIBERNATE**:

- Automatic resource management (no connection leaks)
- Object-relational mapping (no manual ResultSet parsing)
- Query composition (Criteria API, JPQL)
- Multi-level caching (L1: EntityManager, L2: SessionFactory, query cache)
- Dirty checking (automatic UPDATE on entity changes)
- Lazy loading (load related entities on-demand)
- Database portability (same code for PostgreSQL, MySQL, Oracle)
- Trade-off: Learning curve, magic behaviour, N+1 query risk
