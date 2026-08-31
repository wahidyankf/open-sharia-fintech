# organiclever-www — Common Patterns

## Adding a Feature to an Existing Feature Context

```typescript
// 1. Add Gherkin scenario in specs/apps/organiclever/behavior/organiclever-www/gherkin/<bc>/<file>.feature

// 2. Add step implementation in test/unit/steps/<bc>/<file>.steps.tsx

// 3. Implement domain type (if new aggregate field)
// src/contexts/<bc>/domain/types.ts

// 4. Implement use-case in application layer
// src/contexts/<bc>/application/my-use-case.ts

// 5. Implement PGlite store operation in infrastructure
// src/contexts/<bc>/infrastructure/<bc>-store.ts

// 6. Expose via barrel
// src/contexts/<bc>/application/index.ts  ← add export

// 7. Add/update React hook or component in presentation
// src/contexts/<bc>/presentation/use-<bc>.ts
// src/contexts/<bc>/presentation/index.ts  ← add export

// 8. Consume in Next.js page (thin wrapper only)
// src/app/app/<screen>/page.tsx
import { SomeScreen } from "@/contexts/<bc>/presentation";
```

## Using web-ui Components

```typescript
import {
  Button,
  Alert,
  Input,
  Icon,
  Toggle,
  StatCard,
  TabBar,
  SideNav,
} from "@open-sharia-enterprise/web-ui";

<Button variant="teal">Primary action</Button>
<Button variant="sage" size="xl">Hero CTA</Button>
<Alert variant="success">Entry logged!</Alert>
<Icon name="dumbbell" size={24} />
<StatCard label="Streak" value={7} unit="days" hue="terracotta" icon="flame" />
```
