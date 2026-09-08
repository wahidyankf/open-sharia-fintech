---
description: "How to use Immer for deep nested updates and Object.freeze for runtime immutability enforcement."
when_to_use: "Use when a nested object update is too deep for spread syntax, or you need to enforce immutability at runtime."
---

# Immutability Patterns — Immer and Object.freeze

## Using Immer for Complex Updates

**Deep nested updates with Immer**:

```typescript
import { produce } from "immer";

interface State {
  users: Array<{
    id: string;
    profile: {
      name: string;
      settings: {
        theme: string;
        notifications: boolean;
      };
    };
  }>;
}

const state: State = {
  users: [
    {
      id: "1",
      profile: {
        name: "Ahmad",
        settings: { theme: "dark", notifications: true },
      },
    },
  ],
};

// PASS: Immer - write like mutation, get immutability
const newState = produce(state, (draft) => {
  draft.users[0].profile.settings.theme = "light";
});

// Original unchanged, newState has update
```

## Object.freeze for Runtime Immutability

**Prevent mutations at runtime**:

```typescript
interface Config {
  apiUrl: string;
  timeout: number;
}

const config: Readonly<Config> = Object.freeze({
  apiUrl: "https://api.example.com",
  timeout: 5000,
});

// FAIL: Mutation fails in strict mode
config.timeout = 10000; // Error in strict mode

// PASS: Create new object instead
const updatedConfig = { ...config, timeout: 10000 };
```
