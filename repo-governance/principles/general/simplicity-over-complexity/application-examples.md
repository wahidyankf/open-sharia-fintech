---
description: Three worked examples (dark mode, API errors, utilities) contrasting over-engineered and minimal solutions.
when_to_use: Use when you need a worked feature-request example.
---

# Application Examples

## Example 1: Feature Request - "Add a dark mode toggle"

**FAIL: Over-engineered**:

```typescript
// 200+ lines with theme system, configuration, persistence, animation...
interface ThemeConfig {
  mode: "light" | "dark" | "auto";
  customColors?: ColorPalette;
  transitionDuration?: number;
  persistenceStrategy?: "localStorage" | "cookie" | "api";
}

class ThemeManager {
  // Complex abstraction for a simple boolean toggle
}
```

**PASS: Minimal solution**:

```typescript
// 20 lines - just what was asked
const [isDark, setIsDark] = useState(false);

return (
  <button onClick={() => setIsDark(!isDark)}>
    Toggle {isDark ? 'Light' : 'Dark'} Mode
  </button>
);
```

## Example 2: API Error Handling

**FAIL: Defensive for impossible scenarios**:

```typescript
async function getUser(id: string) {
  if (!id) throw new Error("ID required"); // ID is required by type system
  if (typeof id !== "string") throw new Error("ID must be string"); // TypeScript guarantees this
  if (id.length === 0) throw new Error("ID cannot be empty"); // Already checked above

  try {
    const response = await api.get(`/users/${id}`);
    if (!response) throw new Error("No response"); // Fetch never returns undefined
    if (!response.data) throw new Error("No data"); // API contract guarantees data
    return response.data;
  } catch (error) {
    // Complex retry logic, fallbacks, logging that wasn't requested
  }
}
```

**PASS: Validate at boundaries only**:

```typescript
async function getUser(id: string) {
  // Trust internal code - TypeScript and API contract guarantee correctness
  const response = await api.get(`/users/${id}`);
  return response.data;

  // Handle errors at system boundary (API call)
  // Let framework handle network errors
}
```

## Example 3: Utility Functions

**FAIL: Premature abstraction**:

```typescript
// Created utility for one use case
function formatUserDisplay(user: User, options?: DisplayOptions): string {
  const { includeEmail, includeRole, separator = " - " } = options || {};
  const parts = [user.name];
  if (includeEmail) parts.push(user.email);
  if (includeRole) parts.push(user.role);
  return parts.join(separator);
}

// Used once
const display = formatUserDisplay(user, { includeEmail: true });
```

**PASS: Inline for single use**:

```typescript
// Just write it inline
const display = `${user.name} - ${user.email}`;

// If needed multiple times later, THEN extract
```
