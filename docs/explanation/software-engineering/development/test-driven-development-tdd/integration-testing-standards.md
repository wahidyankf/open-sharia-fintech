---
title: "Integration Testing Standards"
description: OSE Platform standards for integration testing — mocked external I/O, in-memory repositories, MSW, and mockito patterns
category: explanation
subcategory: development
tags:
  - tdd
  - integration-testing
  - msw
  - wiremock
  - in-memory
principles:
  - automation-over-manual
  - reproducibility
created: 2026-02-09
---

# Integration Testing Standards

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding TDD By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/development/test-driven-development-tdd/by-example/) before using these standards.

**REQUIRED**: Read [Three-Tier Testing Model](./three-tier-testing.md) first. Integration tests are one of three distinct tiers. Understanding all three tiers before applying these standards is essential.

## Purpose

OSE Platform standards for integration tests — tests that verify multiple internal layers working
together while keeping all external I/O controlled via mocking and in-memory implementations.

## Core Rule

**REQUIRED**: Integration tests MUST mock all external I/O.

**PROHIBITED**: Real network calls, real databases, real external services in integration tests.

Integration tests prove the internal wiring is correct — routing, middleware, use cases, services,
and repositories all behave as specified — without depending on live infrastructure.

```
✅ Integration test boundary:
  [HTTP request] → [Router] → [Middleware] → [Use Case] → [In-Memory Repo]
                                                        ↑
                                           (real code, in-memory state)

❌ NOT this:
  [HTTP request] → [Router] → [Use Case] → [Real PostgreSQL]
                                         ↑
                              (real network = belongs in E2E)
```

## REQUIRED: In-Memory Repository Implementations

**REQUIRED**: Use in-memory repository implementations for integration tests.

**PROHIBITED**: Testcontainers, real databases, ORM connections in integration tests.

In-memory implementations are concrete classes that implement the same repository interface as
production implementations, using an in-memory data structure (Map, List) instead of a real
database. They behave realistically — CRUD operations, queries, relationship resolution — without
touching any infrastructure.

### TypeScript — In-Memory Repository

```typescript
// Production interface
interface MemberRepository {
  findAll(): Promise<Member[]>;
  findById(id: string): Promise<Member | null>;
  save(member: Member): Promise<void>;
  delete(id: string): Promise<void>;
}

// In-memory implementation for integration tests
export class InMemoryMemberRepository implements MemberRepository {
  private store = new Map<string, Member>();

  async findAll(): Promise<Member[]> {
    return Array.from(this.store.values());
  }

  async findById(id: string): Promise<Member | null> {
    return this.store.get(id) ?? null;
  }

  async save(member: Member): Promise<void> {
    this.store.set(member.id, member);
  }

  async delete(id: string): Promise<void> {
    this.store.delete(id);
  }
}

// Integration test usage
describe("MemberService (Integration)", () => {
  let service: MemberService;

  beforeEach(() => {
    const repository = new InMemoryMemberRepository();
    service = new MemberService(repository);
  });

  it("should list all members", async () => {
    await service.addMember({ name: "Alice Johnson", role: "admin" });
    await service.addMember({ name: "Bob Smith", role: "viewer" });

    const members = await service.listMembers();

    expect(members).toHaveLength(2);
    expect(members.map((m) => m.name)).toContain("Alice Johnson");
  });
});
```

### Rust — In-Memory Repository

```rust
use std::collections::HashMap;

// Production trait
trait MemberRepository: Send + Sync {
    fn find_all(&self) -> Vec<Member>;
    fn find_by_id(&self, id: &MemberId) -> Option<Member>;
    fn save(&mut self, member: Member);
    fn delete(&mut self, id: &MemberId);
}

// In-memory implementation for integration tests
struct InMemoryMemberRepository {
    store: HashMap<MemberId, Member>,
}

impl InMemoryMemberRepository {
    fn new() -> Self {
        Self { store: HashMap::new() }
    }
}

impl MemberRepository for InMemoryMemberRepository {
    fn find_all(&self) -> Vec<Member> {
        self.store.values().cloned().collect()
    }

    fn find_by_id(&self, id: &MemberId) -> Option<Member> {
        self.store.get(id).cloned()
    }

    fn save(&mut self, member: Member) {
        self.store.insert(member.id.clone(), member);
    }

    fn delete(&mut self, id: &MemberId) {
        self.store.remove(id);
    }
}

// Integration test usage
#[cfg(test)]
mod member_service_integration_tests {
    use super::*;

    #[test]
    fn should_list_all_members() {
        let mut repository = InMemoryMemberRepository::new();
        repository.save(Member::create(MemberId::generate(), "Alice Johnson", Role::Admin));
        repository.save(Member::create(MemberId::generate(), "Bob Smith", Role::Viewer));

        let service = MemberService::new(repository);
        let members = service.list_members();

        assert_eq!(members.len(), 2);
        assert!(members.iter().any(|m| m.name == "Alice Johnson"));
    }
}
```

## REQUIRED: Mock External HTTP Services

**REQUIRED**: Intercept and mock all outbound HTTP calls in integration tests.

**PROHIBITED**: Real network calls to external APIs, payment gateways, notification services, or
any external HTTP endpoint.

### TypeScript — MSW (Mock Service Worker)

MSW intercepts HTTP calls at the network layer. Integration tests configure MSW handlers to control
what the application receives when it makes fetch/axios calls.

```typescript
// src/test/server.ts — shared MSW server for integration tests
import { setupServer } from "msw/node";
import { handlers } from "./handlers";

export const server = setupServer(...handlers);

// src/test/handlers.ts — default mock responses
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/members", () =>
    HttpResponse.json([
      { id: "1", name: "Alice Johnson", role: "admin" },
      { id: "2", name: "Bob Smith", role: "viewer" },
    ]),
  ),
  http.post("/api/members", async ({ request }) => {
    const body = await request.json() as { name: string; role: string };
    return HttpResponse.json({ id: "3", ...body }, { status: 201 });
  }),
];

// Integration test — MSW intercepts all HTTP in the rendered component
import { server } from "../server";
import { http, HttpResponse } from "msw";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it("should show error when API returns 500", async () => {
  server.use(
    http.get("/api/members", () => HttpResponse.json(null, { status: 500 })),
  );

  render(<MemberList />);

  expect(await screen.findByText("Failed to load members")).toBeInTheDocument();
});
```

### Rust — `mockito` HTTP Mock Server

`mockito` starts an in-process HTTP server on a dynamic port. Configure it per-test to control
what the application receives when it calls external services.

```rust
use mockito::{Server, Matcher};

#[tokio::test]
async fn should_send_notification_successfully() {
    let mut server = Server::new_async().await;

    let mock = server
        .mock("POST", "/notifications")
        .with_status(200)
        .with_body(r#"{"status": "sent"}"#)
        .expect(1)
        .create_async()
        .await;

    let client = HttpNotificationClient::new(server.url());
    let service = NotificationService::new(client);

    service
        .notify(MemberId::of("1"), "Welcome to OSE Platform")
        .await
        .expect("notification should succeed");

    mock.assert_async().await;
}

#[tokio::test]
async fn should_retry_when_notification_fails() {
    let mut server = Server::new_async().await;

    // First attempt fails
    let fail_mock = server
        .mock("POST", "/notifications")
        .with_status(503)
        .expect(1)
        .create_async()
        .await;

    // Second attempt succeeds
    let ok_mock = server
        .mock("POST", "/notifications")
        .with_status(200)
        .with_body(r#"{"status": "sent"}"#)
        .expect(1)
        .create_async()
        .await;

    let client = HttpNotificationClient::new(server.url());
    let service = NotificationService::new(client);
    service.notify(MemberId::of("1"), "Welcome").await.expect("should succeed on retry");

    fail_mock.assert_async().await;
    ok_mock.assert_async().await;
}
```

## REQUIRED: Separate Integration Tests from Unit Tests

**REQUIRED**: Integration tests MUST live in a dedicated directory separate from unit tests.

```
src/
  tests/
    unit/
      member_service_test.rs          # Pure unit tests — all dependencies mocked
      zakat_calculator_test.rs
    integration/
      member_list_integration_test.rs # Multiple layers wired + in-memory infra
      user_login_integration_test.rs
```

**TypeScript** (organiclever-app-web pattern):

```
src/
  test/
    integration/
      member-list.integration.test.tsx    # vitest-cucumber + MSW
      user-login.integration.test.tsx
    helpers/
      mock-data.ts                        # Shared test data
      auth-mock.ts                        # Auth state helpers
    server.ts                             # MSW server setup
    setup.ts                             # Global test setup
  components/
    Breadcrumb.unit.test.tsx             # Unit test co-located with source
```

## BDD Integration Tests (Gherkin-Driven)

Integration tests at OSE Platform use BDD Gherkin scenarios as the specification. The feature
files in `specs/` drive the integration test implementation.

### TypeScript — vitest-cucumber

```typescript
// src/test/integration/member-list.integration.test.tsx
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { render, screen } from "@testing-library/react/pure";
import { BASE_AUTH } from "../helpers/auth-mock";
import { server } from "../server";
import { MOCK_MEMBERS } from "../helpers/mock-data";
import { http, HttpResponse } from "msw";

const feature = await loadFeature("../../specs/apps/organiclever/members/member-list.feature");

describeFeature(feature, ({ Scenario }) => {
  Scenario("Viewing the member list as a logged-in user", ({ Given, When, Then }) => {
    Given("a user is logged in", () => {
      // Configure auth state — no real HTTP, cookie set in-memory
      document.cookie = `auth=${BASE_AUTH}`;
    });

    When("they navigate to the members page", () => {
      render(<MemberListPage />);
      // MSW intercepts GET /api/members and returns MOCK_MEMBERS
    });

    Then("they see all members in the list", async () => {
      for (const member of MOCK_MEMBERS) {
        expect(await screen.findByText(member.name)).toBeInTheDocument();
      }
    });
  });
});
```

### Rust — `cucumber` crate + in-memory router

```rust
// tests/integration/member_list_integration_test.rs
// Integration test — Axum router loaded, real DB replaced with in-memory repository
use axum::http::StatusCode;
use axum_test::TestServer;
use serde_json::json;

#[tokio::test]
async fn should_return_member_list() {
    // Build router with in-memory repository (no real DB)
    let mut repository = InMemoryMemberRepository::new();
    repository.save(Member::create(MemberId::generate(), "Alice Johnson", Role::Admin));
    repository.save(Member::create(MemberId::generate(), "Bob Smith", Role::Viewer));

    let app = build_router(repository);
    let server = TestServer::new(app).expect("failed to create test server");

    let response = server
        .get("/api/members")
        .add_header("Authorization", "Bearer test-token")
        .await;

    assert_eq!(response.status_code(), StatusCode::OK);
    let body: Vec<serde_json::Value> = response.json();
    assert_eq!(body.len(), 2);
    assert_eq!(body[0]["name"], json!("Alice Johnson"));
}
```

## Transaction Management

Integration tests must not leave state between test cases.

**TypeScript**: Reset MSW handlers after each test. Use `beforeEach` to reinitialize in-memory
repositories.

**Rust**: Reinitialize the in-memory repository at the start of each test function. Because each
`#[tokio::test]` is an independent async task with its own stack, state never leaks between tests
when the repository is constructed locally inside the function.

```rust
#[tokio::test]
async fn member_repository_integration_test() {
    let repository = InMemoryMemberRepository::new(); // Fresh state per test
    // … test body …
}
```

## What Does NOT Belong in Integration Tests

| Concern                               | Correct tier |
| ------------------------------------- | ------------ |
| Testcontainers / real PostgreSQL      | E2E          |
| Real HTTP to external payment gateway | E2E          |
| Real browser automation               | E2E          |
| Slow Docker container startup         | E2E          |
| Single-class business logic           | Unit         |
| Pure function calculation             | Unit         |

## Related Standards

- [Three-Tier Testing Model](./three-tier-testing.md) — authoritative tier definitions and the mocking boundary
- [Test Doubles Standards](./test-doubles-standards.md) — in-memory implementations vs. mocks
- [TypeScript Testing](../../programming-languages/typescript/testing.md) — TypeScript-specific integration patterns
