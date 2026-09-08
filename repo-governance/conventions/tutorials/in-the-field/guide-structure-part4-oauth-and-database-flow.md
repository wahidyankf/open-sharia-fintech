---
description: Mermaid diagrams for OAuth2/OIDC authentication and the JDBC-to-HikariCP-to-JPA database persistence progression.
when_to_use: Use when building an OAuth2 authentication or database-persistence-progression diagram.
---

# Guide Structure Part 4: OAuth and Database Flow Diagrams

**Example 2c: Authentication Flow - Production (OAuth2 OIDC)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    C1[Client App] -->|1. Redirect to login| C2[Identity Provider<br/>Keycloak/Auth0]
    C2 -->|2. User authenticates| C2
    C2 -->|3. Authorization code| C1
    C1 -->|4. Code + client secret| C2
    C2 -->|5. Access token + ID token| C1
    C1 -->|6. Access token in header| C3[Resource Server<br/>Your API]
    C3 -->|7. Validates token with IdP| C2
    C2 -->|8. Token valid| C3
    C3 -->|9. Protected resource| C1

    style C1 fill:#029E73,stroke:#000,color:#fff
    style C2 fill:#029E73,stroke:#000,color:#fff
    style C3 fill:#029E73,stroke:#000,color:#fff
```

**Production benefit**: Centralized identity management, single sign-on (SSO), third-party integrations, token refresh flows.

**Example 3a: Database Persistence - Standard Library (JDBC)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    A1[Application] -->|DriverManager.getConnection| A2[Single Connection]
    A2 -->|PreparedStatement| A3[Database]
    A3 -->|ResultSet| A2
    A2 -->|Manual mapping<br/>rs.getString| A1
    A2 -->|close| A3
    A1 -->|New request<br/>creates new connection| A2

    style A1 fill:#0173B2,stroke:#000,color:#fff
    style A2 fill:#0173B2,stroke:#000,color:#fff
    style A3 fill:#0173B2,stroke:#000,color:#fff
```

**Limitation**: Each request creates new database connection, causing connection overhead.

**Example 3b: Database Persistence - Framework (HikariCP Connection Pool)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    B1[Application] -->|dataSource.getConnection| B2[Connection Pool<br/>10 connections]
    B2 -->|Reuse connection| B3[Database]
    B3 -->|ResultSet| B2
    B2 -->|Manual mapping| B1
    B1 -->|close returns to pool| B2
    B2 -->|Pool maintains connections| B3

    style B1 fill:#DE8F05,stroke:#000,color:#fff
    style B2 fill:#DE8F05,stroke:#000,color:#fff
    style B3 fill:#DE8F05,stroke:#000,color:#fff
```

**Improvement**: Connection pooling eliminates connection creation overhead, but still requires manual object mapping.

**Example 3c: Database Persistence - Production (JPA/Hibernate with Caching)**

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC
graph TD
    C1[Application] -- entityManager.find --> C2[L1 Cache<br/>EntityManager]
    C2 -- Cache miss --> C3[L2 Cache<br/>SessionFactory]
    C3 -- Cache miss --> C4[HikariCP Pool]
    C4 -- SQL query --> C5[Database]
    C5 -- ResultSet --> C6[Return Object]
    C2 -.-> note1[L1 hit: no DB query]

    style C1 fill:#029E73,stroke:#000,color:#fff
    style C2 fill:#029E73,stroke:#000,color:#fff
    style C3 fill:#029E73,stroke:#000,color:#fff
    style C4 fill:#029E73,stroke:#000,color:#fff
    style C5 fill:#029E73,stroke:#000,color:#fff
    style C6 fill:#029E73,stroke:#000,color:#fff
    style note1 fill:#CC78BC,stroke:#000,color:#fff
```

**Production benefit**: Multi-level caching (L1, L2) + connection pooling + automatic ORM mapping.
