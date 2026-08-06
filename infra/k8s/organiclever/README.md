# OrganicLever Kubernetes boundary

This directory reserves the staging and production locations for a future
OrganicLever Kubernetes deployment. It does not currently contain deployable
manifests, so it is not a place to run kubectl apply or to begin local
development. 🛑

## What to use instead

| Your goal                                  | Start here                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| Explore or develop the local-first web app | [OrganicLever web app](../../../apps/organiclever-app-web/README.md)      |
| Work on the current backend service        | [OrganicLever backend](../../../apps/organiclever-be/README.md)           |
| Understand expected product behavior       | [OrganicLever specifications](../../../specs/apps/organiclever/README.md) |

The [staging](./staging/README.md) and
[production](./production/README.md) directories document their status and
the conditions needed before a manifest may be added.

## Safe boundary

Kubernetes configuration can affect shared environments. Keep secrets out of
Git, do not infer missing manifests from this directory structure, and do not
treat placeholders as an operational runbook. A future deployment change needs
a reviewed, secret-safe implementation plan and validated manifests before this
directory becomes executable.
