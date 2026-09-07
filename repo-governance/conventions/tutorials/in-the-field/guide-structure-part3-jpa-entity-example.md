---
description: The worked JPA/Hibernate @Entity class example mapping a User to a database table.
when_to_use: Use when writing a JPA entity-mapping example.
---

# Guide Structure Part 3: JPA Entity Example

**Example 3: Production Persistence with JPA/Hibernate**

```java
import javax.persistence.*;
// => JPA annotations (Java Persistence API)
// => Standard interface, Hibernate is implementation
// => javax.persistence package (JPA 2.x)
// => Maven: org.hibernate:hibernate-core:5.6.15.Final

@Entity
// => @Entity marks JPA entity (database-mapped class)
// => Hibernate scans classpath for @Entity classes
// => Creates table schema on startup (auto-DDL)
@Table(name = "users")
// => @Table specifies table name (defaults to class name)
// => Optional if table name matches class name
// => Can specify schema, catalog, unique constraints
public class User {
    // => Entity class represents database table row
    // => Must have no-arg constructor (required by JPA)
    // => Fields map to table columns

    @Id
    // => @Id marks primary key field
    // => Required for all JPA entities
    // => Can be composite (multiple @Id fields)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    // => @GeneratedValue auto-increment strategy
    // => IDENTITY uses database auto-increment
    // => Database generates value on INSERT
    // => Alternative: SEQUENCE, TABLE, AUTO
    private Long id;
    // => Primary key type: Long (nullable wrapper)
    // => null before persist, populated after INSERT

    @Column(nullable = false, unique = true, length = 50)
    // => Column constraints enforced by Hibernate
    // => nullable = false: NOT NULL constraint
    // => unique = true: UNIQUE constraint
    // => length = 50: VARCHAR(50)
    // => Schema generation creates these constraints
    private String username;
    // => username field maps to username column
    // => @Column optional if field name matches column

    @Column(nullable = false, unique = true, length = 100)
    // => Email column with constraints
    // => length = 100: larger than username (email longer)
    private String email;
    // => email field maps to email column

    // Constructors, getters, setters omitted for brevity
    // => No-arg constructor required by JPA
    // => Getters/setters required for property access
}
```

Continued in [Guide Structure Part 3 — JPA Service Example](./guide-structure-part3-jpa-service-example.md).
