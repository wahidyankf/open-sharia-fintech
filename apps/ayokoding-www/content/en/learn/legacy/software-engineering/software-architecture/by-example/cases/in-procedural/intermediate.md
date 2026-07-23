---
title: "Intermediate"
weight: 10000004
date: 2026-05-24T00:00:00+07:00
draft: false
description: "Guides 7–14: Postgres adapter, in-memory test double, domain event publisher with outbox, cross-context Anti-Corruption Layer, database migrations, integration test harness, observability, and multi-adapter configuration — production hexagonal wiring for the procurement domain"
tags:
  [
    "hexagonal-architecture",
    "ports-and-adapters",
    "postgres",
    "testing",
    "domain-events",
    "outbox",
    "acl",
    "observability",
    "tutorial",
    "in-the-field",
    "procedural",
    "go",
    "rust",
    "intermediate",
  ]
---

This intermediate guide set extends the beginner hexagonal application — one context, in-memory adapters, composition root — with production-grade adapter implementations. Each guide adds one adapter or wiring concern: Postgres persistence, test doubles, domain event publishing via outbox, Anti-Corruption Layer for cross-context translation, database migrations, integration test harness, structured logging, and multi-environment configuration.

**Running domain**: `procurement-platform-be` (PurchaseOrder bounded context). All guides extend the same application skeleton built in the beginner tier.

## Guide 7 — PostgreSQL Adapter for PurchaseOrder Repository

The in-memory repository from the beginner tier is a test double — production needs a real database. This guide implements `PostgresPORepository` that satisfies `PurchaseOrderRepository` (the domain port). Go uses pgx v5; Rust uses sqlx with the postgres feature and compile-time query macros. The adapter never imports domain logic — it only translates between SQL rows and domain structs. Production persistence must be explicit about query semantics and transaction isolation rather than relying on ORM magic.

### Why It Matters

Persistence bugs discovered in production are expensive and often silent — corrupted data survives for weeks before anyone notices the inconsistency. Implementing the adapter with real pgx/sqlx calls (rather than ORM magic) gives explicit control over query performance, transaction isolation, and JSONB serialization behavior.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => PostgresPORepository satisfies the PurchaseOrderRepository port
type PostgresPORepository struct {
    pool *pgxpool.Pool // => pgxpool manages connection pool; pool is safe for concurrent use
}

// => NewPostgresPORepository creates the adapter; pool is injected (hexagonal: no direct DB config here)
func NewPostgresPORepository(pool *pgxpool.Pool) *PostgresPORepository {
    return &PostgresPORepository{pool: pool}
}

// => Save upserts the PO — INSERT OR UPDATE based on primary key conflict
func (r *PostgresPORepository) Save(ctx context.Context, po *PurchaseOrder) error {
    // => JSONB column stores line_items — avoids a separate table for this read pattern
    lineItemsJSON, err := json.Marshal(po.LineItems)
    if err != nil {
        return fmt.Errorf("marshal line items: %w", err)
    }
    // => ON CONFLICT (id) DO UPDATE makes Save idempotent — safe to retry
    _, err = r.pool.Exec(ctx, `
        INSERT INTO purchase_orders (id, supplier_id, status, line_items, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (id) DO UPDATE SET
            status = EXCLUDED.status,
            line_items = EXCLUDED.line_items,
            updated_at = EXCLUDED.updated_at
    `, po.Id, po.SupplierId, po.Status.String(), lineItemsJSON, po.CreatedAt, po.UpdatedAt)
    return err
}

// => FindById maps DB row back to domain PurchaseOrder
func (r *PostgresPORepository) FindById(ctx context.Context, id PurchaseOrderId) (*PurchaseOrder, error) {
    row := r.pool.QueryRow(ctx, `
        SELECT id, supplier_id, status, line_items, created_at, updated_at
        FROM purchase_orders WHERE id = $1
    `, id)
    var po PurchaseOrder
    var statusStr string
    var lineItemsJSON []byte
    // => Scan into local variables; domain struct populated after scan
    if err := row.Scan(&po.Id, &po.SupplierId, &statusStr, &lineItemsJSON, &po.CreatedAt, &po.UpdatedAt); err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return nil, nil // => nil, nil = not found; caller decides if missing is an error
        }
        return nil, fmt.Errorf("scan: %w", err)
    }
    po.Status = POStatusFromString(statusStr) // => string → enum; unknown string → Draft (safe default)
    if err := json.Unmarshal(lineItemsJSON, &po.LineItems); err != nil {
        return nil, fmt.Errorf("unmarshal line items: %w", err)
    }
    return &po, nil
}
```

{{< /tab >}}
{{< tab >}}

```rust
// => PostgresPORepository holds a sqlx connection pool; Clone is cheap (Arc internally)
pub struct PostgresPORepository {
    pool: sqlx::PgPool, // => PgPool is Send+Sync; safe to share across async tasks
}

impl PostgresPORepository {
    pub fn new(pool: sqlx::PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl PORepository for PostgresPORepository {
    async fn save(&self, po: &PurchaseOrder) -> Result<(), RepoError> {
        // => serde_json::to_value for JSONB column
        let line_items = serde_json::to_value(&po.line_items)?;
        // => sqlx::query! macro verifies SQL at compile time against DB schema
        sqlx::query!(
            r#"INSERT INTO purchase_orders (id, supplier_id, status, line_items, created_at, updated_at)
               VALUES ($1, $2, $3, $4, $5, $6)
               ON CONFLICT (id) DO UPDATE SET
                 status = EXCLUDED.status,
                 line_items = EXCLUDED.line_items,
                 updated_at = EXCLUDED.updated_at"#,
            po.id.0,
            po.supplier_id.0,
            po.status.to_string(),
            line_items,
            po.created_at,
            po.updated_at
        )
        .execute(&self.pool)
        .await?;
        Ok(())
    }

    async fn find_by_id(&self, id: &PurchaseOrderId) -> Result<Option<PurchaseOrder>, RepoError> {
        // => sqlx::query! maps row to anonymous record; then convert to domain type
        let row = sqlx::query!(
            "SELECT id, supplier_id, status, line_items, created_at, updated_at FROM purchase_orders WHERE id = $1",
            id.0
        )
        .fetch_optional(&self.pool) // => fetch_optional returns None for not-found
        .await?;
        Ok(row.map(|r| PurchaseOrder {
            id: PurchaseOrderId(r.id),
            supplier_id: SupplierId(r.supplier_id),
            status: POStatus::from_str(&r.status).unwrap_or(POStatus::Draft),
            // => unknown status string → Draft (safe default; never panics)
            line_items: serde_json::from_value(r.line_items).unwrap_or_default(),
            created_at: r.created_at,
            updated_at: r.updated_at,
        }))
    }
}
```

{{< /tab >}}
{{< /tabs >}}

Guide 8 shows how to use the in-memory repository as a test double alongside this Postgres adapter, enabling the entire application service layer to be tested at unit-test speed.

## Guide 8 — In-Memory Repository as a Hexagonal Test Double

The hexagonal architecture's payoff is that the entire application service layer can be tested against an in-memory adapter at unit-test speed — no Docker, no migrations, no ports. This guide implements and uses `InMemoryPORepository` as a drop-in test double for `PostgresPORepository`. Both adapters satisfy the same `PurchaseOrderRepository` port; the composition root decides which one to wire at startup. The test uses the in-memory adapter directly without any mocking framework.

### Why It Matters

A test suite that requires a running database is fragile and slow. The in-memory adapter enables fast feedback in CI without mocking application service internals — the application service under test runs exactly as it would in production, just with a different adapter behind the port.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => InMemoryPORepository satisfies the same PurchaseOrderRepository port as PostgresPORepository
type InMemoryPORepository struct {
    mu    sync.RWMutex
    store map[PurchaseOrderId]*PurchaseOrder
}

func NewInMemoryPORepository() *InMemoryPORepository {
    return &InMemoryPORepository{store: make(map[PurchaseOrderId]*PurchaseOrder)}
}

func (r *InMemoryPORepository) Save(_ context.Context, po *PurchaseOrder) error {
    r.mu.Lock()
    defer r.mu.Unlock()
    // => Deep copy on save: prevents external mutation of stored state
    cloned := *po
    cloned.LineItems = append([]LineItem(nil), po.LineItems...)
    r.store[po.Id] = &cloned
    return nil
}

func (r *InMemoryPORepository) FindById(_ context.Context, id PurchaseOrderId) (*PurchaseOrder, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    po, ok := r.store[id]
    if !ok {
        return nil, nil // => nil, nil = not found; consistent with PostgresPORepository behaviour
    }
    // => Return a copy; caller cannot mutate stored state through the returned pointer
    cloned := *po
    return &cloned, nil
}

// => Unit test using InMemoryPORepository — no database required
func TestCreatePOHandler_Success(t *testing.T) {
    repo := NewInMemoryPORepository()
    bus := NewInMemoryEventBus()
    handler := NewCreatePOHandler(repo, bus)

    id, err := handler.Handle(context.Background(), CreatePOCommand{
        SupplierID: "SUP-001",
        LineItems: []CreateLineItemInput{
            {Description: "Paper A4", Qty: 100, Unit: "each", UnitPriceCents: 500, Currency: "USD"},
        },
    })
    // => After Handle, PO should be findable in the repo
    require.NoError(t, err)
    po, err := repo.FindById(context.Background(), id)
    require.NoError(t, err)
    assert.Equal(t, POStatusDraft, po.Status)
    assert.Len(t, po.LineItems, 1)
}
```

{{< /tab >}}
{{< tab >}}

```rust
pub struct InMemoryPORepository {
    // => RwLock allows concurrent reads; Mutex would serialize all access
    store: std::sync::RwLock<std::collections::HashMap<PurchaseOrderId, PurchaseOrder>>,
}

impl InMemoryPORepository {
    pub fn new() -> Self {
        Self {
            store: Default::default(),
        }
    }
}

#[async_trait]
impl PORepository for InMemoryPORepository {
    async fn save(&self, po: &PurchaseOrder) -> Result<(), RepoError> {
        self.store.write().unwrap().insert(po.id.clone(), po.clone());
        // => .clone() ensures stored value is independent of caller's PO
        Ok(())
    }
    async fn find_by_id(&self, id: &PurchaseOrderId) -> Result<Option<PurchaseOrder>, RepoError> {
        Ok(self.store.read().unwrap().get(id).cloned())
        // => .cloned() returns owned copy; caller cannot affect stored state
    }
}

#[tokio::test]
async fn test_create_po_handler() {
    let repo = Arc::new(InMemoryPORepository::new());
    let bus = Arc::new(InMemoryEventBus::new());
    let handler = CreatePOHandler::new(repo.clone(), bus.clone());
    // => wire handler with in-memory adapters — no database, no network
    let id = handler
        .handle(CreatePOCommand {
            supplier_id: SupplierId("SUP-001".into()),
            ..Default::default()
        })
        .await
        .unwrap();
    let po = repo.find_by_id(&id).await.unwrap().unwrap();
    assert_eq!(po.status, POStatus::Draft);
    // => status is Draft immediately after creation
}
```

{{< /tab >}}
{{< /tabs >}}

Guide 9 shows how to publish domain events reliably using the outbox pattern, ensuring events are never lost even if the application crashes after saving the aggregate.

## Guide 9 — Domain Event Publisher with Outbox Pattern

Domain events emitted by aggregates must be published reliably — if the application crashes after saving the aggregate but before publishing, events are lost. The outbox pattern stores events in the same DB transaction as the aggregate, then a separate publisher polls and forwards them. Go uses pgx transactions explicitly; Rust uses a sqlx `Transaction` handle passed through the same async task. Both implementations follow the same structural pattern: one atomic write, one background poller.

### Why It Matters

Lost events cause silent data inconsistency across bounded contexts — Finance never knows a PO was approved; supplier notification is never sent. The outbox pattern provides at-least-once delivery without distributed transactions, making it the production-grade default for domain event publishing.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => OutboxEntry stored in the same DB transaction as the aggregate
type OutboxEntry struct {
    ID          string
    AggregateId string
    EventType   string
    Payload     []byte     // => JSON-serialized event
    PublishedAt *time.Time // => nil = unpublished
    RetryCount  int
    CreatedAt   time.Time
}

// => OutboxRepository is a port; same pgx transaction passed to both repo saves
type OutboxRepository interface {
    Save(ctx context.Context, tx pgx.Tx, entry OutboxEntry) error
    FindUnpublished(ctx context.Context, limit int) ([]OutboxEntry, error)
    MarkPublished(ctx context.Context, id string) error
    IncrementRetry(ctx context.Context, id string) error
}

// => CreatePOWithOutbox saves PO + outbox entries in one DB transaction
func CreatePOWithOutbox(ctx context.Context, pool *pgxpool.Pool, poRepo *PostgresPORepository, outboxRepo PostgresOutboxRepository, po *PurchaseOrder) error {
    tx, err := pool.Begin(ctx)
    if err != nil {
        return err
    }
    defer tx.Rollback(ctx) // => deferred rollback is no-op after commit
    // => Save PO within transaction
    if err := poRepo.SaveTx(ctx, tx, po); err != nil {
        return err
    }
    // => Save each domain event as outbox entry within SAME transaction
    for _, event := range po.DomainEvents() {
        payload, _ := json.Marshal(event)
        entry := OutboxEntry{
            ID:          uuid.New().String(),
            AggregateId: string(po.Id),
            EventType:   event.EventType(),
            Payload:     payload,
            CreatedAt:   time.Now(),
        }
        if err := outboxRepo.Save(ctx, tx, entry); err != nil {
            return err
        }
    }
    po.ClearEvents()
    return tx.Commit(ctx) // => atomic: PO + outbox entries committed together
}

// => OutboxPublisher polls unpublished entries and forwards to event bus
type OutboxPublisher struct {
    outboxRepo OutboxRepository
    bus        DomainEventBus
    eventReg   EventRegistry // => maps event type string → concrete event struct
    interval   time.Duration
}

func (p *OutboxPublisher) Run(ctx context.Context) {
    ticker := time.NewTicker(p.interval)
    defer ticker.Stop()
    for {
        select {
        case <-ticker.C:
            p.publishBatch(ctx)
        case <-ctx.Done():
            return
        }
    }
}

func (p *OutboxPublisher) publishBatch(ctx context.Context) {
    entries, _ := p.outboxRepo.FindUnpublished(ctx, 100) // => process up to 100 at a time
    for _, entry := range entries {
        event := p.eventReg.Deserialize(entry.EventType, entry.Payload)
        if err := p.bus.Publish(ctx, event); err != nil {
            p.outboxRepo.IncrementRetry(ctx, entry.ID) // => failed entries retried next poll
            continue
        }
        p.outboxRepo.MarkPublished(ctx, entry.ID)
    }
}
```

{{< /tab >}}
{{< tab >}}

```rust
// => OutboxEntry mirrors Go version; serde for JSON serialization
#[derive(Debug, sqlx::FromRow)]
pub struct OutboxEntry {
    pub id: Uuid,
    pub aggregate_id: String,
    pub event_type: String,
    pub payload: serde_json::Value, // => JSONB column maps to serde_json::Value
    pub published_at: Option<DateTime<Utc>>,
    pub retry_count: i32,
    pub created_at: DateTime<Utc>,
}

// => save_po_with_outbox uses sqlx::Transaction for atomicity
pub async fn save_po_with_outbox(
    pool: &sqlx::PgPool,
    po: &PurchaseOrder,
    events: &[Box<dyn DomainEvent>],
) -> Result<(), RepoError> {
    let mut tx = pool.begin().await?; // => begin transaction
    // => save PO inside transaction
    save_po_tx(&mut tx, po).await?;
    // => save each domain event to outbox inside same transaction
    for event in events {
        let payload = serde_json::to_value(event)?;
        sqlx::query!(
            "INSERT INTO outbox (id, aggregate_id, event_type, payload, created_at) VALUES ($1, $2, $3, $4, NOW())",
            Uuid::new_v4(),
            po.id.0,
            event.event_type(),
            payload
        )
        .execute(&mut *tx)
        .await?;
    }
    tx.commit().await?; // => atomic commit: PO + all outbox entries
    Ok(())
}

// => OutboxPublisher polls via tokio interval
pub struct OutboxPublisher {
    pool: sqlx::PgPool,
    bus: Arc<dyn DomainEventBus + Send + Sync>,
    interval: Duration,
}

impl OutboxPublisher {
    pub async fn run(&self) {
        let mut ticker = tokio::time::interval(self.interval);
        // => interval fires immediately on first tick; subsequent ticks at self.interval
        loop {
            ticker.tick().await;
            self.publish_batch().await;
        }
    }

    async fn publish_batch(&self) {
        let entries = sqlx::query_as!(
            OutboxEntry,
            "SELECT * FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100"
        )
        .fetch_all(&self.pool)
        .await
        .unwrap_or_default();
        // => unwrap_or_default: transient DB error skips batch; retried next interval
        for entry in entries {
            // => deserialize and publish; mark published or increment retry on failure
            let _ = self.try_publish_entry(&entry).await;
        }
    }
}
```

{{< /tab >}}
{{< /tabs >}}

Guide 10 shows how to translate external supplier data through an Anti-Corruption Layer before it enters the domain model, keeping ERP naming conventions out of the bounded context.

## Guide 10 — Cross-Context Anti-Corruption Layer (ACL)

The procurement context consumes supplier data from an ERP system that uses a different model — "Vendor" with a "VendorCode" instead of "Supplier" with a "SupplierCode". The Anti-Corruption Layer (ACL) translates at the boundary, keeping the ERP model out of the procurement domain. The ACL is implemented as a separate package (`adapter/out/erpacl/`) that depends on an `ExternalVendorClient` port — the domain never imports the HTTP client or ERP DTOs directly. Translation happens at the edge; domain structs always carry procurement vocabulary.

### Why It Matters

Without an ACL, ERP naming conventions and data shapes leak into the domain model. A refactor in the ERP triggers domain code changes — tight coupling that makes the bounded context meaningless. The ACL acts as a semantic firewall: ERP changes are contained to the translator, not scattered across the domain.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => ExternalVendorDTO represents the ERP's vendor model — not the domain's Supplier
type ExternalVendorDTO struct {
    VendorCode       string // => ERP uses "VendorCode" not "SupplierCode"
    LegalName        string
    PaymentTermsDays int
    BankIBAN         string
    ActiveFlag       int // => ERP uses 1/0 instead of bool
}

// => ExternalVendorClient is a port — the ACL depends on this interface, not on the HTTP client directly
type ExternalVendorClient interface {
    FetchVendor(ctx context.Context, vendorCode string) (ExternalVendorDTO, error)
}

// => SupplierACL translates ERP vendor data to domain Supplier
type SupplierACL struct {
    client ExternalVendorClient // => injected port
}

func NewSupplierACL(client ExternalVendorClient) *SupplierACL {
    return &SupplierACL{client: client}
}

// => FetchSupplierByCode fetches from ERP and translates to domain Supplier
func (acl *SupplierACL) FetchSupplierByCode(ctx context.Context, code SupplierCode) (*Supplier, error) {
    // => Call ERP using its VendorCode — same format as SupplierCode in domain
    dto, err := acl.client.FetchVendor(ctx, string(code))
    if err != nil {
        return nil, fmt.Errorf("ERP vendor fetch: %w", err)
    }
    return acl.translate(dto)
}

// => translate maps ERP DTO to domain Supplier — this is the ACL's core responsibility
func (acl *SupplierACL) translate(dto ExternalVendorDTO) (*Supplier, error) {
    code, err := ParseSupplierCode(dto.VendorCode)
    // => Validation at translation time: invalid ERP data never enters domain
    if err != nil {
        return nil, fmt.Errorf("invalid vendor code %q: %w", dto.VendorCode, err)
    }
    return &Supplier{
        Id:        SupplierId(uuid.New().String()), // => domain generates its own ID
        Name:      dto.LegalName,
        Code:      code,
        Active:    dto.ActiveFlag == 1, // => int → bool translation
        CreatedAt: time.Now(),
    }, nil
}
```

{{< /tab >}}
{{< tab >}}

```rust
// => ExternalVendorDto mirrors the ERP API response
#[derive(Debug, Deserialize)]
pub struct ExternalVendorDto {
    pub vendor_code: String,
    pub legal_name: String,
    pub payment_terms_days: u32,
    pub bank_iban: String,
    pub active_flag: u8, // => ERP sends 0 or 1
}

// => ExternalVendorClient is a port (trait); ACL never imports the HTTP client directly
#[async_trait]
pub trait ExternalVendorClient: Send + Sync {
    async fn fetch_vendor(&self, vendor_code: &str) -> Result<ExternalVendorDto, ClientError>;
}

pub struct SupplierAcl {
    client: Arc<dyn ExternalVendorClient>, // => injected; swappable in tests
}

impl SupplierAcl {
    pub fn new(client: Arc<dyn ExternalVendorClient>) -> Self {
        Self { client }
    }

    pub async fn fetch_by_code(&self, code: &SupplierCode) -> Result<Supplier, AclError> {
        let dto = self.client.fetch_vendor(&code.0).await?;
        // => fetch from ERP using ERP vocabulary; translate immediately
        self.translate(dto)
    }

    fn translate(&self, dto: ExternalVendorDto) -> Result<Supplier, AclError> {
        // => Parse and validate at translation boundary — invalid ERP data never enters domain
        let code = SupplierCode::parse(&dto.vendor_code)
            .map_err(|e| AclError::InvalidVendorCode(e.to_string()))?;
        Ok(Supplier {
            id: SupplierId(Uuid::new_v4().to_string()), // => domain generates its own ID
            name: dto.legal_name,
            code,
            active: dto.active_flag != 0, // => u8 → bool translation
            created_at: Utc::now(),
        })
    }
}
```

{{< /tab >}}
{{< /tabs >}}

Guides 11–14 cover database migrations, integration test harness, structured logging, and production wiring that ties all adapters together under environment-based configuration.

## Guide 11 — Database Migrations

The Postgres schema for `purchase_orders` and `outbox` tables must be created and versioned before any adapter can run. Go uses [goose](https://github.com/pressly/goose) v3; Rust uses sqlx's built-in `sqlx::migrate!` macro pointing at a `migrations/` folder. Both tools track applied migrations in a version table and apply only the delta on startup. Migrations run once at application boot before the composition root constructs repositories — this guarantees the schema is always at the expected version when adapters start.

### Why It Matters

Migrations without version control cause schema drift between environments — staging runs schema version 5 but production is at version 3, and the deployment fails silently with cryptic column-not-found errors. Goose and sqlx-migrate keep all environments synchronized by treating migrations as checked-in artifacts, not manual scripts.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => migrations/001_create_purchase_orders.sql (goose format)
// -- +goose Up
// => Up migration: create the purchase_orders table
// CREATE TABLE purchase_orders (
//     id          TEXT PRIMARY KEY,
//     supplier_id TEXT NOT NULL,
//     status      TEXT NOT NULL DEFAULT 'draft',
//     line_items  JSONB NOT NULL DEFAULT '[]',
//     created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//     updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
// );
// -- +goose Down
// => Down migration: rollback drops the table
// DROP TABLE IF EXISTS purchase_orders;

// => migrations/002_create_outbox.sql
// -- +goose Up
// CREATE TABLE outbox (
//     id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//     aggregate_id TEXT NOT NULL,
//     event_type   TEXT NOT NULL,
//     payload      JSONB NOT NULL,
//     published_at TIMESTAMPTZ,
//     retry_count  INT NOT NULL DEFAULT 0,
//     created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
// );
// => partial index: only unpublished entries; keeps the poller query fast
// CREATE INDEX idx_outbox_unpublished ON outbox (created_at) WHERE published_at IS NULL;
// -- +goose Down
// DROP TABLE IF EXISTS outbox;

// => RunMigrations applies all pending migrations at startup
func RunMigrations(ctx context.Context, db *sql.DB, migrationsDir string) error {
    // => goose.SetDialect must be called once; "postgres" maps to pgx-compatible SQL
    goose.SetDialect("postgres")
    // => goose.Up applies all unapplied migrations in ascending version order
    if err := goose.Up(db, migrationsDir); err != nil {
        return fmt.Errorf("run migrations: %w", err)
    }
    return nil
}

// => In main.go: call RunMigrations before constructing repositories
// => db, _ := sql.Open("pgx", cfg.DatabaseURL)
// => require.NoError(t, RunMigrations(ctx, db, "../../migrations"))
```

{{< /tab >}}
{{< tab >}}

```rust
// => migrations/ folder contains timestamped .sql files
// => 20260524000001_create_purchase_orders.sql:
// CREATE TABLE purchase_orders (
//     id          TEXT PRIMARY KEY,
//     supplier_id TEXT NOT NULL,
//     status      TEXT NOT NULL DEFAULT 'draft',
//     line_items  JSONB NOT NULL DEFAULT '[]'::jsonb,
//     created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//     updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
// );
//
// => 20260524000002_create_outbox.sql:
// CREATE TABLE outbox (
//     id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//     aggregate_id TEXT NOT NULL,
//     event_type   TEXT NOT NULL,
//     payload      JSONB NOT NULL,
//     published_at TIMESTAMPTZ,
//     retry_count  INT NOT NULL DEFAULT 0,
//     created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
// );
// CREATE INDEX idx_outbox_unpublished ON outbox (created_at) WHERE published_at IS NULL;

// => apply_migrations runs all pending migrations at startup
pub async fn apply_migrations(pool: &sqlx::PgPool) -> Result<(), sqlx::migrate::MigrateError> {
    // => sqlx::migrate! macro embeds migration files at compile time from ./migrations
    sqlx::migrate!("./migrations")
        .run(pool) // => applies all pending migrations in timestamp order
        .await
}

// => In main(): apply_migrations(&pool).await?; before constructing repos
// => sqlx tracks applied migrations in _sqlx_migrations table automatically
```

{{< /tab >}}
{{< /tabs >}}

Guide 12 builds on the migration setup to create a full integration test harness using Testcontainers, running real Postgres in Docker for each test run.

## Guide 12 — Integration Test Harness with Testcontainers

Integration tests need a real Postgres instance. Testcontainers spins up a Docker Postgres container per test run — isolated, reproducible, and automatically cleaned up after the test. Go uses [testcontainers-go](https://github.com/testcontainers/testcontainers-go); Rust uses [testcontainers-rs](https://github.com/testcontainers/testcontainers-rs). Both start the container, wait for the port, run migrations, then return a live connection pool. Cleanup is registered with the test runner so no manual teardown is needed.

### Why It Matters

Testing against a mock database validates application logic, not database behavior. Real Postgres integration tests catch constraint violations, index performance issues, and JSONB query bugs that mock tests miss entirely — including the `ON CONFLICT` upsert behavior from Guide 7.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => setupTestDB creates a Postgres container and returns a pgxpool for integration tests
func setupTestDB(t *testing.T) *pgxpool.Pool {
    t.Helper()
    ctx := context.Background()
    // => testcontainers starts a real Postgres 16 container
    req := testcontainers.ContainerRequest{
        Image:        "postgres:16-alpine",
        ExposedPorts: []string{"5432/tcp"},
        Env: map[string]string{
            "POSTGRES_USER":     "test",
            "POSTGRES_PASSWORD": "test",
            "POSTGRES_DB":       "testdb",
        },
        WaitingFor: wait.ForListeningPort("5432/tcp"),
        // => WaitingFor blocks until Postgres is ready to accept connections
    }
    container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: req,
        Started:          true,
    })
    require.NoError(t, err)
    // => t.Cleanup ensures container is stopped after test regardless of pass/fail
    t.Cleanup(func() { container.Terminate(ctx) })

    host, _ := container.Host(ctx)
    port, _ := container.MappedPort(ctx, "5432")
    dsn := fmt.Sprintf("postgres://test:test@%s:%s/testdb", host, port.Port())

    pool, err := pgxpool.New(ctx, dsn)
    require.NoError(t, err)
    // => Run migrations against the test container before any test assertions
    db, _ := sql.Open("pgx", dsn)
    require.NoError(t, RunMigrations(ctx, db, "../../migrations"))
    return pool
}

// => Integration test using real Postgres via testcontainers
func TestPostgresPORepository_SaveAndFind(t *testing.T) {
    pool := setupTestDB(t)
    repo := NewPostgresPORepository(pool)
    po := NewPurchaseOrder(PurchaseOrderId("po-test-001"), SupplierId("sup-001"))
    po.AddLineItem(LineItem{
        Id:          "li-001",
        Description: "Printer paper",
        Qty:         Quantity{Amount: 10, Unit: UnitEach},
        UnitPrice:   Money{AmountCents: 500, Currency: "USD"},
    })
    // => Save PO to real Postgres; exercises ON CONFLICT upsert path
    require.NoError(t, repo.Save(context.Background(), po))
    found, err := repo.FindById(context.Background(), po.Id)
    require.NoError(t, err)
    require.NotNil(t, found)
    assert.Equal(t, po.Status, found.Status)
    assert.Len(t, found.LineItems, 1)
    // => line_items round-trips through JSONB without data loss
}
```

{{< /tab >}}
{{< tab >}}

```rust
// => integration_test.rs uses testcontainers-rs to start a real Postgres container
#[cfg(test)]
mod tests {
    use testcontainers::{clients, images::postgres::Postgres};

    // => setup_db starts a Postgres container and returns a PgPool with migrations applied
    async fn setup_db() -> sqlx::PgPool {
        let docker = clients::Cli::default();
        // => Postgres::default() pulls postgres:latest; pin to 16-alpine for reproducibility
        let pg = docker.run(Postgres::default());
        let port = pg.get_host_port_ipv4(5432);
        // => container is dropped at end of test function; Docker removes it automatically
        let dsn = format!("postgres://postgres:postgres@127.0.0.1:{}/postgres", port);
        let pool = sqlx::PgPool::connect(&dsn).await.unwrap();
        // => Apply migrations before test assertions
        sqlx::migrate!("./migrations").run(&pool).await.unwrap();
        pool
    }

    #[tokio::test]
    async fn test_postgres_repo_save_and_find() {
        let pool = setup_db().await;
        let repo = PostgresPORepository::new(pool);
        // => create a minimal PO for the save round-trip
        let po = PurchaseOrder::new(
            PurchaseOrderId("po-001".into()),
            SupplierId("sup-001".into()),
        );
        repo.save(&po).await.unwrap();
        // => find_by_id exercises the SELECT + JSONB unmarshal path
        let found = repo.find_by_id(&po.id).await.unwrap().unwrap();
        assert_eq!(found.status, POStatus::Draft);
        // => status survives round-trip through TEXT column
    }
}
```

{{< /tab >}}
{{< /tabs >}}

Guide 13 adds structured logging as a port-and-adapter, giving application services observability without importing a concrete logger.

## Guide 13 — Structured Logging Adapter

Production applications need structured logs — key-value pairs that log aggregation systems (Datadog, Loki, CloudWatch) can query and alert on. The logging adapter is a port: domain and application layers never import the concrete logger directly. Go uses the standard library `slog` (Go 1.21+) wrapped behind a thin `Logger` interface; Rust uses the `tracing` crate wrapped behind a `Logger` trait. Both expose the same `With(fields)` / `Info` / `Error` surface so application services remain independent of the log backend.

### Why It Matters

Unstructured log strings like `"PO 1234 approved by alice"` cannot be queried or alerted on — they require fragile regex parsing. Structured logs with discrete fields power dashboards, on-call alerts, and distributed trace correlation without any post-processing.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => Logger is the domain-level logging port — no slog import in domain/app packages
type Logger interface {
    Info(msg string, args ...any)
    Error(msg string, args ...any)
    With(args ...any) Logger // => With returns a child logger pre-set with fields
}

// => SlogAdapter wraps Go 1.21 slog.Logger as the Logger port implementation
type SlogAdapter struct {
    inner *slog.Logger
}

func NewSlogAdapter(inner *slog.Logger) *SlogAdapter {
    return &SlogAdapter{inner: inner}
}

func (l *SlogAdapter) Info(msg string, args ...any) {
    l.inner.Info(msg, args...) // => slog.Info is structured: alternating key-value pairs
}

func (l *SlogAdapter) Error(msg string, args ...any) {
    l.inner.Error(msg, args...)
}

func (l *SlogAdapter) With(args ...any) Logger {
    // => slog.Logger.With creates a child logger; returned as Logger port
    return &SlogAdapter{inner: l.inner.With(args...)}
}

// => Usage in application service: enrich logger with request-scoped fields
func (h *CreatePOHandler) Handle(ctx context.Context, cmd CreatePOCommand) (PurchaseOrderId, error) {
    log := h.logger.With("command", "CreatePO", "supplier_id", cmd.SupplierId)
    // => every log line from here carries command + supplier_id automatically
    log.Info("handling command")
    id, err := h.createPO(ctx, cmd)
    if err != nil {
        log.Error("command failed", "error", err)
        return "", err
    }
    log.Info("PO created", "po_id", id)
    return id, nil
}
```

{{< /tab >}}
{{< tab >}}

```rust
// => Logger trait as port — application layer imports only this trait
pub trait Logger: Send + Sync {
    fn info(&self, msg: &str, fields: &[(&str, &str)]);
    fn error(&self, msg: &str, fields: &[(&str, &str)]);
    fn with(&self, fields: &[(&str, &str)]) -> Box<dyn Logger>;
    // => with() returns a child logger pre-enriched with context fields
}

// => TracingAdapter wraps the tracing crate (de facto standard in Rust async)
pub struct TracingAdapter {
    context: Vec<(String, String)>, // => pre-set context fields from .with() calls
}

impl TracingAdapter {
    pub fn new() -> Self {
        Self { context: vec![] }
    }
}

impl Logger for TracingAdapter {
    fn info(&self, msg: &str, fields: &[(&str, &str)]) {
        // => tracing::info! macro emits structured events consumed by tracing-subscriber
        let all: Vec<String> = self
            .context
            .iter()
            .chain(fields.iter().map(|(k, v)| (k.to_string(), v.to_string())).collect::<Vec<_>>().iter())
            .map(|(k, v)| format!("{}={}", k, v))
            .collect();
        tracing::info!("{} {}", msg, all.join(" "));
    }
    fn error(&self, msg: &str, fields: &[(&str, &str)]) {
        let all: Vec<String> = fields.iter().map(|(k, v)| format!("{}={}", k, v)).collect();
        tracing::error!("{} {}", msg, all.join(" "));
    }
    fn with(&self, fields: &[(&str, &str)]) -> Box<dyn Logger> {
        let mut ctx = self.context.clone();
        ctx.extend(fields.iter().map(|(k, v)| (k.to_string(), v.to_string())));
        Box::new(TracingAdapter { context: ctx })
        // => child logger carries both parent context and new fields
    }
}

// => In main: initialize tracing-subscriber with JSON format for production log aggregators
// tracing_subscriber::fmt().json().init();
```

{{< /tab >}}
{{< /tabs >}}

Guide 14 ties all adapters together in the composition root, selecting concrete implementations based on the `APP_ENV` environment variable.

## Guide 14 — Multi-Adapter Configuration (Test vs Production)

The composition root in `main.go`/`main.rs` wires concrete adapters together based on environment. `APP_ENV=test` uses in-memory adapters; `APP_ENV=production` uses Postgres and real external clients. Configuration is loaded from environment variables — no hardcoded values, no config files committed to source control. The `Wire` function is the single place that knows which adapter satisfies which port; application services and domain packages never see this decision.

### Why It Matters

Hardcoding adapter choices in the composition root makes environment-specific testing impossible. Environment-based wiring enables the same binary to run with test doubles in CI and real adapters in production, without any code changes between environments.

{{< tabs items="Go,Rust" >}}
{{< tab >}}

```go
// => AppConfig holds environment-specific configuration
type AppConfig struct {
    Env         string // => "test", "development", "production"
    DatabaseURL string
    ERPBaseURL  string
    LogLevel    string
}

// => LoadConfig reads from environment variables; defaults to "development"
func LoadConfig() AppConfig {
    return AppConfig{
        Env:         getEnv("APP_ENV", "development"),
        DatabaseURL: getEnv("DATABASE_URL", ""),
        ERPBaseURL:  getEnv("ERP_BASE_URL", ""),
        LogLevel:    getEnv("LOG_LEVEL", "info"),
    }
}

// => Wire builds the application with adapters chosen by config
func Wire(cfg AppConfig) (*Application, error) {
    var repo PurchaseOrderRepository
    var erpClient ExternalVendorClient

    switch cfg.Env {
    case "test":
        // => test env: in-memory adapters, no external dependencies
        repo = NewInMemoryPORepository()
        erpClient = NewMockVendorClient()
    default:
        // => production/development: Postgres + real HTTP client
        if cfg.DatabaseURL == "" {
            return nil, fmt.Errorf("DATABASE_URL required for env %s", cfg.Env)
        }
        pool, err := pgxpool.New(context.Background(), cfg.DatabaseURL)
        if err != nil {
            return nil, err
        }
        // => LoggingPORepository wraps PostgresPORepository — decorator pattern
        repo = NewLoggingPORepository(NewPostgresPORepository(pool), slog.Default())
        erpClient = NewHTTPVendorClient(cfg.ERPBaseURL)
    }

    supplierACL := NewSupplierACL(erpClient)
    bus := NewInMemoryEventBus()
    createPOHandler := NewCreatePOHandler(repo, bus)
    // => all ports wired; application struct holds only the handler surface
    return &Application{createPOHandler: createPOHandler, supplierACL: supplierACL}, nil
}
```

{{< /tab >}}
{{< tab >}}

```rust
// => AppConfig read from environment variables via envy crate
#[derive(Debug, serde::Deserialize)]
pub struct AppConfig {
    #[serde(default = "default_env")]
    pub app_env: String, // => "test" | "development" | "production"
    pub database_url: Option<String>,
    pub erp_base_url: Option<String>,
}

fn default_env() -> String {
    "development".to_string()
}

// => wire builds the application; returns trait objects for each port
pub async fn wire(cfg: AppConfig) -> Result<Application, WireError> {
    let (repo, erp_client): (
        Arc<dyn PORepository + Send + Sync>,
        Arc<dyn ExternalVendorClient + Send + Sync>,
    ) = if cfg.app_env == "test" {
        // => test: in-memory adapters — no Docker, no network
        (
            Arc::new(InMemoryPORepository::new()),
            Arc::new(MockVendorClient::new()),
        )
    } else {
        // => production: Postgres + HTTP; migrations run before constructing repo
        let dsn = cfg.database_url.ok_or(WireError::MissingDatabaseUrl)?;
        let pool = sqlx::PgPool::connect(&dsn).await?;
        sqlx::migrate!("./migrations").run(&pool).await?;
        // => migrations applied once at startup before any adapter is constructed
        (
            Arc::new(LoggingPORepository::new(PostgresPORepository::new(pool.clone()))),
            Arc::new(HttpVendorClient::new(
                cfg.erp_base_url.unwrap_or_default(),
            )),
        )
    };

    let supplier_acl = Arc::new(SupplierAcl::new(erp_client));
    let bus = Arc::new(InMemoryEventBus::new());
    let create_po_handler = CreatePOHandler::new(repo, bus);
    // => Application owns the handler surface; ports are hidden behind trait objects
    Ok(Application {
        create_po_handler,
        supplier_acl,
    })
}
```

{{< /tab >}}
{{< /tabs >}}

The advanced tier (Guides 15+) covers retry and circuit-breaker decorators, end-to-end domain event flow across four bounded contexts, OpenTelemetry observability, and the Kubernetes deployment topology.
