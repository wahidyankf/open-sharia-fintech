---
description: "Shows worked PASS/FAIL comparisons of core-features-first vs framework-first teaching for JSON processing and React state management."
when_to_use: "Read when you need worked PASS/FAIL comparison snippets for teaching JSON processing or React state management progressively."
---

# Core Features First: Comparison for JSON Processing and State Management

## Comparison: Core Features vs External Tools

**Teaching JSON Processing (Language)**:

```markdown
## PASS: Progressive Approach

### Example 15: JSON with Standard Library (Beginner)

Use Java 11+ `javax.json` for basic JSON operations...

### Example 42: JSON with Jackson (Intermediate)

When you need advanced features like polymorphic deserialization, Jackson provides...
Note: Requires Maven dependency `com.fasterxml.jackson.core:jackson-databind:2.15.0`
Builds on JSON fundamentals from Example 15.
```

```markdown
## FAIL: Framework-First Approach

### Example 15: JSON with Jackson (Beginner)

Jackson is the industry standard for JSON in Java...
(Learner must install dependencies, understand Maven, before learning JSON!)
```

**Teaching State Management (React)**:

```markdown
## PASS: Progressive Approach

### Example 12: Local State with useState (Beginner)

React's `useState` hook manages component-local state...

### Example 35: Global State with Context API (Intermediate)

Context API shares state across components without prop drilling...
Builds on `useState` (Example 12) by adding global state capability.

### Example 58: Redux for Complex State (Advanced)

When state logic becomes complex with many actions and async flows, Redux provides...
Note: Requires `npm install redux react-redux`
Compare Redux overhead vs Context API (Example 35) - Redux justified when >10 state slices.
```

```markdown
## FAIL: Framework-First Approach

### Example 12: Redux for State Management (Beginner)

Redux is the industry standard for React state...
(External dependency before showing React's built-in state primitives!)
```
