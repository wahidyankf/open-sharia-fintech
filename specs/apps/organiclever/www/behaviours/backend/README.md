# organiclever-www Backend Applicability

`organiclever-www` is a static marketing site. It owns no tRPC route handlers,
REST endpoints, or other backend public boundary, so a backend corpus and a
`organiclever-www-be-e2e` project are inapplicable and intentionally omitted.

Do not add placeholder scenarios or no-op targets to fill this absent role.
Frontend behaviour remains owned by `organiclever-www` Unit tests and
`organiclever-www-fe-e2e` browser tests.

## Related

- **Frontend corpus**: [organiclever-www behaviour specs](../frontend/README.md)
- **Parent**: [behaviour specs](../../README.md)
