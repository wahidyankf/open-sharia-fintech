---
title: "Advanced Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

## Advanced: GitOps, promotion, secrets, and recovery

All artifacts are safe local models. Do not bootstrap a controller, access a repository, decrypt a secret, contact object storage, or restore data without an owner-approved environment and current primary documentation.

### Example 58: GitOps Model

_ex-58 · exercises co-25_

GitOps treats a reviewed repository as desired state and a controller continuously reconciles the cluster toward it.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'reviewed Git desired state → controller reconciliation → observed cluster state'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: GitOps treats a reviewed repository as desired state and a controller continuously reconciles the cluster toward it.

**Why it matters**: Git history supplies review, provenance, rollback, and a recovery baseline. Controller status also exposes drift, so operations become observable convergence rather than undocumented terminal actions.

### Example 59: Plan an Argo CD Install

_ex-59 · exercises co-26_

Argo CD is privileged platform infrastructure and needs current compatibility, RBAC, repository trust, monitoring, and rollback review.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'review Argo CD compatibility, RBAC, repo trust, monitoring, and rollback'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Argo CD is privileged platform infrastructure and needs current compatibility, RBAC, repository trust, monitoring, and rollback review.

**Why it matters**: A reconciler can change many workloads from one source. Least privilege and source validation prevent delivery automation from becoming an unreviewed cluster-wide change channel.

### Example 60: Argo CD Application

_ex-60 · exercises co-26_

An Argo CD Application binds one reviewed source path to a destination; real repository URLs and destinations belong to owner-approved inputs.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'Application is a reviewed source-to-destination reconciliation contract'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: An Argo CD Application binds one reviewed source path to a destination; real repository URLs and destinations belong to owner-approved inputs.

**Why it matters**: A wrong destination or broad credential can make one source path affect the wrong cluster. Explicit contracts and RBAC constrain scope while giving clear evidence of controller ownership.

### Example 61: Argo CD Sync Status

_ex-61 · exercises co-26_

OutOfSync means live state differs from desired target; Synced means the controller comparison converged. Neither proves usable service health.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'OutOfSync: live differs; Synced: target comparison converged; health still needs evidence'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: OutOfSync means live state differs from desired target; Synced means the controller comparison converged.

**Why it matters**: A workload can be Synced yet crash or fail readiness. Pair controller status with deployment, endpoint, probe, and client evidence before deciding a promotion is successful.

### Example 62: Argo CD ApplicationSet

_ex-62 · exercises co-26_

An ApplicationSet generates declared application instances such as dev, staging, and production. Its expansion must remain finite and reviewable.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'ApplicationSet generation is environment delivery policy'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: An ApplicationSet generates declared application instances such as dev, staging, and production.

**Why it matters**: A generator mistake can create or target many applications. Reviewable environment lists and destination controls prevent automation from expanding beyond intended clusters or namespaces.

### Example 63: Argo CD Auto-Sync

_ex-63 · exercises co-26_

Automated sync and self-heal reconcile approved Git and revert drift. Enable them only with protected sources, scoped destinations, health gates, and rollback practice.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'auto-sync requires protected Git, scope, health gates, and rollback'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Automated sync and self-heal reconcile approved Git and revert drift.

**Why it matters**: Automatic correction limits drift but can rapidly reapply a bad commit. Protected branches and known rollback revisions keep automatic convergence safer than manual editing.

### Example 64: Plan Flux Bootstrap

_ex-64 · exercises co-27_

Flux bootstrap binds a cluster controller to a Git source. Review its identity, repository authority, branch policy, destination scope, and recovery.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'review Flux identity, repository authority, branch policy, scope, and recovery'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Flux bootstrap binds a cluster controller to a Git source.

**Why it matters**: A bootstrap identity can continuously modify cluster state. Narrow scope, rotation, and repository protection prevent one leaked credential or branch write becoming a platform incident.

### Example 65: Flux Kustomization

_ex-65 · exercises co-27_

A Flux Kustomization continuously reconciles one source path. Its path, dependencies, prune behavior, and target namespace must be narrow and reviewed.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'Kustomization is a continuous path-to-cluster contract'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: A Flux Kustomization continuously reconciles one source path.

**Why it matters**: Broad paths and careless pruning can affect unexpected resources. Scoped paths and Git revisions make reconciliation understandable and reversible.

### Example 66: Flux HelmRelease

_ex-66 · exercises co-27_

A Flux HelmRelease reconciles a chart and its values. Pin versions and review source trust, values, and upgrade behavior.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'HelmRelease requires pinned chart, reviewed values, and rollback'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: A Flux HelmRelease reconciles a chart and its values.

**Why it matters**: Unpinned charts and values can change exposure or privileges. Controlled inputs give teams reproducible releases and a revision to restore when a chart update is unsafe.

### Example 67: Argo CD and Flux

_ex-67 · exercises co-28_

Argo CD is application and UI-centric; Flux is a composable controller toolkit. Both require governed Git authority and health evidence.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'Argo CD: application/UI; Flux: controllers; both require governance'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Argo CD is application and UI-centric; Flux is a composable controller toolkit.

**Why it matters**: Tool preference can obscure support and operational needs. A documented choice aligns policy, observability, and incident practice instead of creating an opaque second control plane.

### Example 68: Kustomize Base and Overlay

_ex-68 · exercises co-29_

Kustomize keeps common resources in a base and environment deltas in overlays, avoiding full manifest forks.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'base holds shared intent; overlays hold reviewed environment deltas'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Kustomize keeps common resources in a base and environment deltas in overlays, avoiding full manifest forks.

**Why it matters**: Forked manifests drift until fixes reach one environment but not another. Overlays preserve shared review while making capacity, hostname, and digest differences deliberate.

### Example 69: Production Overlay Patch

_ex-69 · exercises co-29_

A production overlay patch changes only the fields that differ from the base, such as capacity and resources.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'production patch should be narrow and evidence-backed'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: A production overlay patch changes only the fields that differ from the base, such as capacity and resources.

**Why it matters**: Small patches make review and rollback understandable. A copied production workload hides whether failure originates in shared code or an environment-specific divergence.

### Example 70: Helm Values Per Environment

_ex-70 · exercises co-29_

Per-environment Helm values override a pinned shared chart. Treat every values change as executable infrastructure input.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'values are reviewable promotion inputs'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Per-environment Helm values override a pinned shared chart.

**Why it matters**: Values can change capacity, permissions, exposure, and artifact identity. Separate files keep shared chart behavior while making overrides reproducible during incident response.

### Example 71: Build Once Promote

_ex-71 · exercises co-30_

Build one tested image and promote its immutable digest through environments rather than rebuilding each time.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'promote image@sha256:<documented-digest> without rebuilding'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Build one tested image and promote its immutable digest through environments rather than rebuilding each time.

**Why it matters**: Tags can move and rebuilds change inputs. Digest promotion supplies one artifact identity for tests, rollout evidence, rollback, and vulnerability response.

### Example 72: Promotion Through Git

_ex-72 · exercises co-30_

Promotion updates the next environment overlay to an already tested digest through a reviewed Git change.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'record digest, source revision, destination overlay, reviewer, health, rollback'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Promotion updates the next environment overlay to an already tested digest through a reviewed Git change.

**Why it matters**: Git history explains what changed and supports precise rollback. Combined with controller and application evidence, it turns release governance into an observable process.

### Example 73: Secrets Are Not Git Data

_ex-73 · exercises co-31_

Kubernetes Secret data is encoded, not automatically encrypted, and plaintext committed to Git persists in history.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'never commit plaintext Secret data; base64 is encoding; rotate exposure'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Kubernetes Secret data is encoded, not automatically encrypted, and plaintext committed to Git persists in history.

**Why it matters**: Git replication, forks, logs, and backups make accidental commits difficult to erase. A strict policy plus rotation and review limits credential exposure.

### Example 74: SealedSecret Contract

_ex-74 · exercises co-31_

Sealed Secrets encrypts a Secret-shaped value for the target-cluster controller. Plaintext and private keys must never appear in a lesson.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'SealedSecret means encrypted Git delivery, never plaintext exposure'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Sealed Secrets encrypts a Secret-shaped value for the target-cluster controller.

**Why it matters**: Encryption can make Git storage safer, but controller key scope and access still determine who can recover the value. Rotation and incident procedures remain necessary.

### Example 75: ExternalSecret Contract

_ex-75 · exercises co-31_

External Secrets synchronizes approved external-secret values into Kubernetes runtime Secrets. Review identity, path scope, refresh, audit, and failure behavior.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'ExternalSecret moves trust to a governed external authority'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: External Secrets synchronizes approved external-secret values into Kubernetes runtime Secrets.

**Why it matters**: Runtime delivery avoids plaintext Git but adds identity and availability dependencies. Least privilege and tested failure policy prevent a vault problem becoming a service or security incident.

### Example 76: Secret Delivery Decision

_ex-76 · exercises co-31_

Choose encrypted Git delivery or runtime vault synchronization by trust boundary, operations, and recovery needs. Both require rotation and access review.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'Sealed Secrets: encrypted Git; External Secrets: runtime sync'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Choose encrypted Git delivery or runtime vault synchronization by trust boundary, operations, and recovery needs.

**Why it matters**: Secret tooling changes where authority and failure live, not whether values are sensitive. A deliberate choice prevents accidental plaintext and unobservable dependencies.

### Example 77: Plan a Velero Install

_ex-77 · exercises co-32_

Velero backup infrastructure needs compatibility, protected object storage, encryption, retention, monitoring, and restore tests.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'review Velero compatibility, storage authority, encryption, retention, alerts, restore'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: Velero backup infrastructure needs compatibility, protected object storage, encryption, retention, monitoring, and restore tests.

**Why it matters**: A successful controller deployment does not prove recoverable data. Object-store ownership and restore procedures protect the chain from cluster objects to operator action.

### Example 78: Velero Backup

_ex-78 · exercises co-32_

A backup needs defined scope, status, volume policy, retention, and restore expectation. Do not include a real namespace or bucket in reusable content.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'backup scope, object status, PV policy, retention, alert, and restore evidence'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: A backup needs defined scope, status, volume policy, retention, and restore expectation.

**Why it matters**: Object and volume recovery can have different paths. Defining both prevents a green backup job from masking missing data, wrong scope, expired retention, or inaccessible storage.

### Example 79: Velero Schedule

_ex-79 · exercises co-32_

A backup schedule expresses RPO only if every run completes and retention works. Set cadence from stated recovery objectives.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'schedule cadence must be justified by RPO and restore evidence'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: A backup schedule expresses RPO only if every run completes and retention works.

**Why it matters**: A six-hour interval may suit one service and fail another. Alerts and restore drills ensure the configured cadence actually supports the promise made to users.

### Example 80: RPO and RTO

_ex-80 · exercises co-32_

RPO is tolerated data loss; RTO is tolerated recovery time. They determine backup, staffing, and restore-test design.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'RPO: data-loss window; RTO: time to restore service'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: RPO is tolerated data loss; RTO is tolerated recovery time.

**Why it matters**: A platform cannot claim recoverability without measurable objectives. Mapping them to cadence and drills turns aspirational targets into operational evidence.

### Example 81: Restore Drill

_ex-81 · exercises co-33_

A restore drill recovers objects and data into a controlled target, then verifies client-visible application health.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'record target, backup identity, timing, objects, PV data, health, gaps, owner'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: A restore drill recovers objects and data into a controlled target, then verifies client-visible application health.

**Why it matters**: Restore procedures fail through permissions, incompatible versions, untested data, and unclear ownership. Rehearsal exposes gaps before a real outage depends on the runbook.

### Example 82: Self-Managed Kubernetes Capstone

_ex-82 · exercises co-06, co-08, co-19, co-21, co-24, co-26, co-29, co-30_

The capstone combines quorum, platform add-ons, Git reconciliation, digest promotion, and restore evidence into one owner-operated acceptance plan.

```sh
# => Prints a safe review model; it contacts no external system.
printf '%s\\n' 'quorum → platform add-ons → Git reconciliation → digest promotion → restore evidence'
```

**Verification**: The example has no real endpoint, credential, repository, or live cluster target.

**Key takeaway**: The capstone combines quorum, platform add-ons, Git reconciliation, digest promotion, and restore evidence into one owner-operated acceptance plan.

**Why it matters**: Individual controllers can look healthy while the service cannot survive loss, drift, certificate failure, or restore. End-to-end evidence makes the operational claim credible.
