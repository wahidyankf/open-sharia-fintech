# OSE Application BE — Gherkin Scenarios

Backend (HTTP-semantic) Gherkin scenarios for `ose-be`. Consumed by xUnit + TickSpec.

## Feature files

| Feature file                                                           | Domain            |
| ---------------------------------------------------------------------- | ----------------- |
| [health/health.feature](./health/health.feature)                       | health            |
| [regulatory-source/](./regulatory-source/)                             | regulatory-source |
| [internal-policy/](./internal-policy/)                                 | internal-policy   |
| [gap-analysis/](./gap-analysis/)                                       | gap-analysis      |
| [ai-orchestration/](./ai-orchestration/)                               | ai-orchestration  |
| [db/migrations.feature](./db/migrations.feature)                       | db                |
| [messaging/nats-connect.feature](./messaging/nats-connect.feature)     | messaging         |
| [messaging/nats-config.feature](./messaging/nats-config.feature)       | messaging         |
| [messaging/jetstream-demo.feature](./messaging/jetstream-demo.feature) | messaging         |
| [config/env-tier-loading.feature](./config/env-tier-loading.feature)   | config            |

- [ai-orchestration — ose-be Gherkin Domain](./ai-orchestration/README.md)
- [config — ose-be Gherkin Domain](./config/README.md)
- [db — ose-be Gherkin Domain](./db/README.md)
- [gap-analysis — ose-be Gherkin Domain](./gap-analysis/README.md)
- [health — ose-be Gherkin Domain](./health/README.md)
- [internal-policy — ose-be Gherkin Domain](./internal-policy/README.md)
- [messaging — ose-be Gherkin Domain](./messaging/README.md)
- [regulatory-source — ose-be Gherkin Domain](./regulatory-source/README.md)
