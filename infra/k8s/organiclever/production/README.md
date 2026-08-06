# OrganicLever production Kubernetes placeholder

There are no production Kubernetes manifests in this directory yet. This is a
reservation for a future, reviewed production deployment—not an instruction to
create, apply, or infer configuration. 🛑

## Before this becomes deployable

A production-ready change must provide, at minimum:

- reviewed manifests that match the active OrganicLever applications;
- a secret-safe configuration contract with no real values in Git;
- health, rollback, and observability behavior that can be verified; and
- an operational plan approved through the repository’s delivery workflow.

Until then, use the [OrganicLever web README](../../../../apps/organiclever-app-web/README.md)
for product exploration and the [OrganicLever backend README](../../../../apps/organiclever-be/README.md)
for server-side development. Product intent belongs in the
[OrganicLever specifications](../../../../specs/apps/organiclever/README.md).
