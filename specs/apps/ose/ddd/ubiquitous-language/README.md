# Ubiquitous Language — OSE

Platform-agnostic glossary of OSE Application bounded contexts. OSE Platform Web has no
bounded contexts.

## Index

| Context             | Glossary                                       |
| ------------------- | ---------------------------------------------- |
| `health`            | [health.md](./health.md)                       |
| `regulatory-source` | [regulatory-source.md](./regulatory-source.md) |
| `internal-policy`   | [internal-policy.md](./internal-policy.md)     |
| `gap-analysis`      | [gap-analysis.md](./gap-analysis.md)           |
| `ai-orchestration`  | [ai-orchestration.md](./ai-orchestration.md)   |
| `config`            | [config.md](./config.md)                       |

## Authoring rules

1. One file per bounded context.
2. Glossary updates ride with the code change that introduces them.
3. Code identifiers match the Rust type/module name verbatim.
4. Forbidden synonyms must be explicit.

- [Ubiquitous Language — db](./db.md)
- [Ubiquitous Language — messaging](./messaging.md)
