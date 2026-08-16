# Inputs

The orchestrator (or user) provides:

1. **Endpoint / base URL** — one or more live targets (required). May be production, staging, preview,
   or a local dev server (e.g. `http://localhost:8202/...` for `organiclever-be`,
   `http://localhost:8302/...` for `ose-be`, or a tRPC/GraphQL endpoint).
2. **Goal** — the testing mission (required). Examples: "verify the activities REST endpoints honour
   the OpenAPI contract and reject bad payloads", "find auth-bypass and over-fetch defects in the
   GraphQL API", "audit pagination and error envelopes for consistency across all list endpoints".
3. **Protocol** — `rest` | `graphql` (optional). When omitted, **auto-detect**: an OpenAPI/Swagger
   document (`openapi`/`swagger` key) or many distinct paths → REST; a single endpoint answering an
   `__schema` introspection query, an SDL/`.graphql` file, or a `{ data, errors }` envelope → GraphQL.
   Record the detected protocol in the coverage map.
4. **Optional refinements**:
   - **Scope hints** — specific endpoints/operations/resources to focus on or avoid.
   - **Contract pointer** — the authoritative contract to test against: an OpenAPI 3.x spec
     (e.g. `specs/apps/organiclever/containers/contracts/openapi.yaml`), a GraphQL SDL file, or a live
     introspection/`/openapi.json` URL. Even when none is named, the agent discovers it — see
     _Contract & Specs as Ground Truth_.
   - **Auth context** — how to obtain a **non-privileged, synthetic** test credential (a test bearer
     token, an API key for a throwaway account). Never real production secrets or privileged
     credentials. If a flow needs auth the agent cannot synthesize, record it as "not exercised — no
     test credential" rather than using a real one.
   - **Depth** — `quick` (one charter, happy + obvious edges), `standard` (default; several charters
     across dimensions), or `thorough` (full operation sweep + deeper auth/perf/security passes).
5. **Output mode & destination** — `plan` (default) | `delivery` | `local-tmp`; see _Output Modes_.
   With `delivery`, also pass a **plan-path** (the existing plan whose `delivery.md` receives the
   findings); with `plan`, optionally pass `plan-stage: in-progress` to file directly into
   `plans/in-progress/`.

If the goal or target is missing, ask for it before testing — do not invent a target or a credential.
