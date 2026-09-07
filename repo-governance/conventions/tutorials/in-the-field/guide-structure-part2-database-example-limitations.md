---
description: The production limitations of the standard-library JDBC approach shown in the database example.
when_to_use: Use when documenting why the JDBC standard-library approach is insufficient for production.
---

# Guide Structure Part 2: Database Example Limitations

**Limitations for production persistence**:

- Manual resource management (prone to leaks if exceptions occur)
- Verbose object mapping (repetitive code for each query)
- No query composition (string concatenation error-prone)
- No caching (every query hits database)
- No lazy loading (must load entire object graph)
- No transaction management (manual commit/rollback)
