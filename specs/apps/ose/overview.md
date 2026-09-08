# OSE — Product Overview

## OSE Application (`ose-app-*`)

AI-assisted gap analysis between regulator-published rule documents and company internal
policies. Target users: compliance officers and risk teams.

### Scope (ose-app)

- Regulatory document ingestion and storage
- Internal policy document ingestion and storage
- AI-assisted gap analysis between regulatory corpus and policy corpus
- Traceable GapItem records linking regulatory clause to missing policy area

## OSE Platform Web (`ose-web`)

Marketing and updates site for the Open Sharia Enterprise platform. Showcases the platform
vision, publishes development updates, and provides a searchable content library.

### Who uses it (ose-web)

- **Visitors** — potential contributors, adopters, and community members
- **Content authors** — the platform maintainer publishing markdown update posts

### What ships today (ose-web)

- Landing page with hero block and social links
- Update post listing at `/updates/` and individual update articles
- Full-text search via FlexSearch
- RSS feed at `/feed.xml`
- SEO: sitemap, robots.txt, per-route metadata
- Health probe at `health.check` tRPC procedure

### What is deferred (ose-web)

- Authenticated contributor portal
- Dynamic content management (CMS integration)
- Multi-language support (English-only today)

## OSE LMS (`ose-lms-*`)

The learning-management backend for the platform. Today it is a scaffold: a proven
request-to-response path, a liveness probe, and an operator health endpoint, standing on the
toolchain every later LMS feature will use.

### Who uses it (ose-lms)

- **Orchestrators and operators** — they need a liveness signal before routing traffic
- **LMS feature authors** — they need one working endpoint to copy rather than a blank project

### What ships today (ose-lms)

- `GET /api/v1/health` returning the contracted health payload
- `GET /api/v1/hello` as the reference request-to-response path
- `GET /actuator/health` for operator tooling, with no other Actuator endpoint exposed
- Listener port resolution: explicit flag, then `OSE_LMS_BE_PORT`, then the default `8303`

### What is deferred (ose-lms)

- Every LMS domain concept — courses, enrolments, learners, assessments
- Persistence: the service owns no datastore and no local resource boundary
- Authentication and authorization
- Any localized content; the service returns no localized values today
