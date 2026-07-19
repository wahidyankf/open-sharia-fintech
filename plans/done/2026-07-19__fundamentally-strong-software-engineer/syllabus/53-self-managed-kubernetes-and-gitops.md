# 53 · Self-Managed Kubernetes & On-Prem GitOps (By Example, YAML/CLI †)

**prd row**: Pass 3 · Build for the Real World · By Example · YAML/CLI † · Learn 153 / Drill 253 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: standing up and operating a **production-grade Kubernetes cluster you fully own** — on
your own VMs or bare metal — then running dev/staging/prod on it via GitOps. Multi-node bring-up with
**k3s** and **kubeadm** (plus the **k0s** and immutable **Talos Linux** alternatives); node
join/cordon/drain, etcd backup/restore, upgrade sequencing; **CNI** selection (Cilium/Calico/Flannel) +
NetworkPolicy; bare-metal LoadBalancer via **MetalLB**; on-prem storage via **Longhorn** +
local-path; ingress + **cert-manager** ACME TLS; then the dev→staging→prod topology via **Argo CD** /
**Flux**, per-env Kustomize overlays / Helm values, secrets that can't live in Git (Sealed Secrets /
External Secrets), and backup/DR with **Velero**. `†`: the "language" is k3s/kubeadm/talosctl CLI +
Helm values + Kubernetes/Argo/Flux YAML manifests against real VMs. Local-dev K8s (kind/minikube/k3d)
and core K8s objects are [`50-containers-and-orchestration`](./50-containers-and-orchestration.md);
cloud-provider provisioning is [`51-cloud-and-iac`](./51-cloud-and-iac.md); the VMs underneath are
[`52-bare-metal-virtualization`](./52-bare-metal-virtualization.md). Here the cluster **you** operate is
the unit.

## Why this exists · the big idea

- **The problem before the solution**: a managed control plane (EKS/GKE/AKS) hides the hard parts — but
  the moment you must run on your own hardware (cost, data residency, air-gap, edge, learning), nobody
  provisions the control plane, the load balancer, the storage, or the TLS for you. Hand-running
  `kubectl apply` against a cluster no one bootstrapped, with secrets pasted into terminals and no
  backup, drifts and fails silently the first time a node dies.
- **Keep-this-if-you-forget-everything**: own the whole stack as **declared desired state that a
  reconciler drives reality toward** — bootstrap the control plane over a consensus datastore (etcd via
  Raft), install the missing on-prem pieces (CNI, LoadBalancer, storage, TLS) as reconciled add-ons,
  then make **Git the source of truth** so a promotion is a commit and the cluster continuously
  converges to it. You describe _what you want_ at every layer, from the node image to the running app.
- **Big ideas touched**: `mechanism-vs-policy` (you declare cluster + app desired state — the _policy_;
  the control plane and the GitOps controller are the reconciling _mechanisms_),
  `determinism-vs-emergence` (immutable/image-based nodes and content-addressed manifests buy
  reproducibility; self-healing and HA emerge from control loops over a quorum datastore),
  `taming-state` (etcd is the one stateful heart — its consensus, backup, and restore are the cluster's
  survival) — see [prd Cross-Cutting Big Ideas](../prd.md#cross-cutting-big-ideas-the-idea-spine-dd-33).

## Prerequisites

- **Prior topics**: [topic 50 Containers & Orchestration](./50-containers-and-orchestration.md) (images,
  Pods/Deployments/Services/Ingress, ConfigMaps/Secrets, the reconciliation loop, `kubectl apply` — this
  topic assumes you can already write and apply a manifest against a running cluster),
  [topic 52 Bare-Metal Virtualization](./52-bare-metal-virtualization.md) (the VMs/hosts the cluster
  nodes run on), and [topic 46 Distributed Systems](./46-distributed-systems.md) (consensus, quorum,
  replication, failure modes — the reasoning behind etcd/Raft and HA control planes).
- **Tools & environment**: a macOS/Linux terminal + `kubectl`, `helm`; **three or more Linux VMs/hosts**
  you can SSH into (from topic 52) reachable on a LAN; **k3s** (`curl` installer) and/or **kubeadm**;
  optionally **talosctl**/**k0s**; **Argo CD** or **Flux** CLI; **kubeseal** and/or the External Secrets
  Operator; **Velero** CLI + an S3-compatible object store (e.g. self-hosted MinIO) for backups. A Git
  repo of source-of-truth manifests. Versions are fast-moving — pin to current and re-verify.
- **Assumed knowledge**: writing and applying K8s YAML (topic 50); SSH + basic Linux networking and
  systemd (topics 05, 52); the idea of consensus/quorum and leader election (topic 46); reading YAML.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (DD-28) and a DD-35 primary-source pass, both
> 2026-07-12. Kubernetes and this ecosystem move fast — treat every version string as **version-
> sensitive** and re-verify current before authoring.

- 2026-07-12 — verified: **k3s** current release **v1.36.2+k3s1** (2026-06-24), tracking upstream
  Kubernetes **v1.36.2**; license **Apache-2.0**. **CNCF maturity nuance**: k3s is at the CNCF
  **Sandbox** level (accepted 2020-08-19) — it is **not** Incubating or Graduated. Separately, k3s is a
  **fully conformant** Kubernetes distribution (it appears in the `cncf/k8s-conformance` results). These
  are two distinct claims: "passes CNCF Kubernetes conformance" ≠ "CNCF-graduated project." State both
  accurately and never conflate them.
- 2026-07-12 — verified: **kubeadm** is part of `kubernetes/kubernetes` (an upstream bootstrapper, not a
  separate distro). **Talos Linux** (Sidero Labs) is an immutable, API-managed OS with **no SSH, no
  shell, no package manager**. **k0s** is a single-binary, CNCF-certified Kubernetes distribution.
- 2026-07-12 — verified: **Cilium** is CNCF **Graduated** (moved to Graduated 2023-10-11). **MetalLB** is
  CNCF Sandbox; its two modes are **Layer 2** (ARP/NDP) and **BGP** (FRR-K8s backend). **Longhorn** is a
  CNCF **Incubating** project.
- 2026-07-12 — verified: **Argo** (incl. Argo CD) is CNCF **Graduated** (2022-12-06); **Flux** is CNCF
  **Graduated**; **cert-manager** is CNCF **Graduated** (2024-09-29). All track fast-moving APIs — pin
  and re-verify.
- 2026-07-12 — verified: reverse-proxy / ingress licenses — **Traefik** MIT, **Caddy** Apache-2.0,
  **nginx** BSD-2-Clause. Confirm against each project's own `LICENSE` before asserting in a lesson;
  the exact SPDX identifiers here were corroborated by web search but not each re-fetched this pass —
  treat as `[Verified]` pending a per-project `LICENSE` read at authoring time.

> DD-35 primary-source pass (2026-07-12). Distro definitions, datastore/quorum rules, CNI/network model,
> LoadBalancer modes, storage, TLS automation, and GitOps semantics traced to primary sources (docs.k3s.io,
> cncf.io, kubernetes.io, siderolabs.com, docs.k0sproject.io, cilium.io, metallb.io, longhorn.io,
> etcd.io, argo-cd.readthedocs.io, fluxcd.io, cert-manager.io, external-secrets.io,
> github.com/bitnami-labs/sealed-secrets, velero.io) and fetched/read. Versions flagged version-sensitive above.

- **k3s — what it is** — "K3s is a fully compliant Kubernetes distribution with the following
  enhancements"; "Distributed as a single binary or minimal container image"; "Lightweight datastore
  based on sqlite3 as the default storage backend. etcd3, MySQL, and Postgres are also available."
  Source: [k3s docs](https://docs.k3s.io/) (fetched, verbatim).
- **k3s — CNCF maturity** — "k3s was accepted to CNCF on August 19, 2020 at the **Sandbox** maturity
  level." Source: [CNCF — k3s](https://www.cncf.io/projects/k3s/) (fetched, verbatim). License:
  "Apache License Version 2.0, January 2004." Source:
  [k3s LICENSE](https://github.com/k3s-io/k3s/blob/master/LICENSE) (fetched, verbatim).
- **k3s — HA embedded etcd & quorum** — "An HA K3s cluster with embedded etcd is composed of: Three or
  more **server nodes** that will serve the Kubernetes API and run other control plane services, as well
  as host the embedded etcd datastore"; "HA embedded etcd cluster must be comprised of an odd number of
  server nodes for etcd to maintain quorum"; "For a cluster with n servers, quorum is (n/2)+1." Source:
  [k3s — HA embedded etcd](https://docs.k3s.io/datastore/ha-embedded) (fetched, verbatim).
- **kubeadm — bootstrapper** — "a tool built to provide `kubeadm init` and `kubeadm join` as best-
  practice 'fast paths' for creating Kubernetes clusters"; "kubeadm performs the actions necessary to get
  a minimum viable cluster up and running. By design, it cares only about bootstrapping, not about
  provisioning machines." Source:
  [kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/) (fetched, verbatim).
- **Talos Linux — immutable & API-only** — the OS is built on "No SSH," "No shell," and "No package
  manager," with an "immutable root filesystem (read-only, ephemeral, RAM-resident)," a "declarative
  configuration model using YAML applied through an API rather than imperative commands," and "atomic A/B
  image swaps for updates with automatic rollback on failure"; it is "Built only for Kubernetes." Source:
  [Sidero Labs — Talos Linux](https://www.siderolabs.com/talos-linux/) (fetched, verbatim).
- **k0s — single-binary distro** — "an open source, all-inclusive Kubernetes distribution … packaged as
  a single binary"; "k0s is distributed as a single binary with zero host OS dependencies besides the
  host OS kernel"; it "drastically reduces the complexity of installing and running a CNCF certified
  Kubernetes distribution." Source: [k0s docs](https://docs.k0sproject.io/stable/) (fetched, verbatim).
- **etcd / Raft** — etcd is "a consistent key-value store for configuration management, service
  discovery, and coordinating distributed work" that "stores metadata in a consistent and fault-tolerant
  way" using the Raft consensus protocol; "The Kubernetes API server persists cluster state into etcd. It
  uses etcd's watch API to monitor the cluster and roll out critical configuration changes." Source:
  [etcd — Why etcd](https://etcd.io/docs/latest/learning/why/) (fetched, verbatim).
- **Kubernetes network model / CNI** — "The network model is implemented by the container runtime on each
  node. The most common container runtimes use Container Network Interface (CNI) plugins to manage their
  network and security capabilities"; Kubernetes "allocates non-overlapping IP addresses" for Pods,
  Services, and Nodes so pods communicate without NAT. Source:
  [Cluster Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) (fetched, verbatim).
- **NetworkPolicy** — "NetworkPolicies allow you to specify rules for traffic flow within your cluster,
  and also between Pods and the outside world"; by default a pod is "non-isolated for ingress" and
  "non-isolated for egress" (all connections allowed); "To use network policies, you must be using a
  networking solution which supports NetworkPolicy. Creating a NetworkPolicy resource without a
  controller that implements it will have no effect." Source:
  [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) (fetched, verbatim).
- **MetalLB — bare-metal LB & modes** — "MetalLB hooks into your Kubernetes cluster, and provides a
  network load-balancer implementation"; "It allows you to create Kubernetes services of type
  `LoadBalancer` in clusters that don't run on a cloud provider"; "In layer 2 mode, one machine in the
  cluster takes ownership of the service, and uses standard address discovery protocols (ARP for IPv4,
  NDP for IPv6) to make those IPs reachable"; "In BGP mode, all machines in the cluster establish BGP
  peering sessions with nearby routers that you control." Source:
  [MetalLB concepts](https://metallb.io/concepts/) (fetched, verbatim).
- **Longhorn** — "Cloud native distributed block storage for Kubernetes"; "Longhorn is a CNCF Incubating
  Project." Source: [Longhorn](https://longhorn.io/) (fetched, verbatim).
- **cert-manager — ACME TLS** — "cert-manager creates TLS certificates for workloads in your Kubernetes
  or OpenShift cluster and renews the certificates before they expire"; it can "obtain certificates from
  a variety of certificate authorities, including: Let's Encrypt, HashiCorp Vault …," storing "the
  private key and certificate … in a Kubernetes Secret." CNCF: "moved to the **Graduated** maturity level
  on September 29, 2024." Sources: [cert-manager docs](https://cert-manager.io/docs/),
  [CNCF — cert-manager](https://www.cncf.io/projects/cert-manager/) (fetched, verbatim).
- **Cilium — eBPF & CNCF** — "Cloud Native, eBPF-based Networking, Observability, and Security"; "Cilium
  was accepted to CNCF on October 13, 2021 at the **Incubating** maturity level and then moved to the
  **Graduated** maturity level on October 11, 2023." Sources: [Cilium](https://cilium.io/),
  [CNCF — Cilium](https://www.cncf.io/projects/cilium/) (fetched, verbatim).
- **Argo CD — GitOps** — "Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes"; it
  uses "Git repositories as the source of truth for defining the desired application state," and
  "continuously monitors running applications and compares the current, live state against the desired
  target state," marking an app `OutOfSync` "whose live state deviates from the target state." CNCF:
  "Argo … moved to the **Graduated** maturity level on December 6, 2022." Sources:
  [Argo CD](https://argo-cd.readthedocs.io/en/stable/), [CNCF — Argo](https://www.cncf.io/projects/argo/) (fetched, verbatim).
- **Flux — GitOps** — Flux is "a tool for keeping Kubernetes clusters in sync with sources of
  configuration (like Git repositories), and automating updates to configuration when there is new code
  to deploy," using **Kustomization** objects to sync configuration and **HelmRelease** objects to manage
  Helm deployments; it is a "CNCF Graduated project." Source: [Flux](https://fluxcd.io/flux/) (fetched, verbatim).
- **Kustomize — base/overlay** — "The kustomization file is a YAML specification of a Kubernetes Resource
  Model (KRM) object called a _Kustomization_. A kustomization describes how to generate or transform
  other KRM objects"; an "encapsulating kustomization can be called an _overlay_, and what it refers to
  can be called a _base_." Source:
  [Kustomization](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/) (fetched, verbatim).
- **Helm — charts & values** — "A chart is a collection of files that describe a related set of
  Kubernetes resources"; values come from a chart's `values.yaml` and a user-supplied file, and "when a
  user supplies custom values, these values will override the values in the chart's `values.yaml` file."
  Source: [Helm charts](https://helm.sh/docs/topics/charts/) (fetched, verbatim).
- **Sealed Secrets** — "Encrypt your Secret into a SealedSecret, which _is_ safe to store - even inside a
  public repository. The SealedSecret can be decrypted only by the controller running in the target
  cluster." Source: [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) (fetched, verbatim).
- **External Secrets Operator** — "External Secrets Operator is a Kubernetes operator that integrates
  external secret management systems like AWS Secrets Manager, HashiCorp Vault …"; "The operator reads
  information from external APIs and automatically injects the values into a Kubernetes Secret" via
  `ExternalSecret`, `SecretStore`, and `ClusterSecretStore` custom resources. Source:
  [External Secrets](https://external-secrets.io/latest/) (fetched, verbatim).
- **Velero — backup/DR** — each Velero operation "is a custom resource, defined with a Kubernetes Custom
  Resource Definition (CRD)"; a backup "Uploads a tarball of copied Kubernetes objects into cloud object
  storage" and "Calls the cloud provider API to make disk snapshots of persistent volumes, if
  specified"; "The restore operation allows you to restore all of the objects and persistent volumes from
  a previously created backup"; "Velero is ideal for the disaster recovery use case." Source:
  [How Velero works](https://velero.io/docs/main/how-velero-works/) (fetched, verbatim).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. Concepts come before examples. -->

- **co-01 · why-self-managed-k8s** — a self-managed cluster means _you_ bootstrap and operate the
  control plane, LoadBalancer, storage, and TLS that a cloud provider would otherwise supply.
- **co-02 · cluster-topology** — a cluster is control-plane (server) nodes plus worker (agent) nodes;
  `kubectl get nodes` shows them `Ready`.
- **co-03 · control-plane-components** — the API server, scheduler, controller-manager, and each node's
  kubelet cooperate over the etcd datastore.
- **co-04 · declarative-reconciliation** — you post desired state to the API server; controllers
  continuously drive live state toward it (not imperative steps).
- **co-05 · etcd-raft-quorum** — etcd is the consensus datastore (Raft); a cluster of `n` servers needs
  quorum `(n/2)+1`, so servers come in odd numbers.
- **co-06 · k3s-single-binary** — k3s is a fully-compliant single-binary distribution installed with one
  command, ideal for on-prem/edge.
- **co-07 · k3s-datastore-options** — k3s defaults to embedded SQLite; `--cluster-init` selects embedded
  etcd (or an external DB) for HA.
- **co-08 · ha-odd-servers** — an HA control plane needs three or more server nodes, always an odd count,
  to keep etcd quorum through a node loss.
- **co-09 · kubeadm-bootstrap** — kubeadm is the upstream bootstrapper: `kubeadm init` makes a
  control-plane node, `kubeadm join` adds nodes; it only bootstraps.
- **co-10 · k0s-distro** — k0s is another single-binary, zero-dependency CNCF-certified distribution.
- **co-11 · talos-immutable-api** — Talos Linux is an immutable, API-only OS (no SSH/shell/package
  manager) configured by applying declarative YAML machine config.
- **co-12 · distro-selection** — choose k3s (light/edge), kubeadm (upstream control), k0s (single-binary),
  or Talos (immutable) by operational needs.
- **co-13 · node-lifecycle** — nodes join with a token, and `cordon`/`drain`/`uncordon` safely remove and
  return a node for maintenance.
- **co-14 · etcd-backup-restore** — a periodic etcd snapshot is the cluster's lifeline; restore rebuilds
  state from it after a control-plane loss.
- **co-15 · upgrade-sequencing** — upgrade the control plane before workers, draining each node in turn,
  one minor version at a time.
- **co-16 · cni-network-model** — Kubernetes requires every pod to reach every pod without NAT; a CNI
  plugin implements that model (no CNI ⇒ nodes NotReady).
- **co-17 · cni-selection** — Cilium (eBPF), Calico, and Flannel (VXLAN overlay) are CNI choices trading
  performance, policy, and observability.
- **co-18 · network-policy** — pods are non-isolated by default; a NetworkPolicy (enforced by the CNI)
  restricts pod-to-pod and pod-to-world traffic.
- **co-19 · metallb-bare-metal-lb** — MetalLB provides `type: LoadBalancer` on bare metal by handing
  Services real IPs from a pool you declare.
- **co-20 · metallb-l2-vs-bgp** — MetalLB advertises those IPs in Layer 2 mode (ARP/NDP, one owner node)
  or BGP mode (peer with your routers).
- **co-21 · on-prem-storage** — Longhorn gives replicated distributed block storage; local-path-
  provisioner gives simple node-local volumes.
- **co-22 · storageclass-pvc** — a StorageClass + PVC dynamically provisions a PersistentVolume from the
  chosen storage backend.
- **co-23 · ingress-controller** — an ingress controller (Traefik, nginx, Caddy) is required to satisfy
  Ingress objects and route external HTTP(S).
- **co-24 · cert-manager-acme** — cert-manager issues and auto-renews TLS certs, obtaining them from
  Let's Encrypt via the ACME protocol into a Secret.
- **co-25 · gitops-model** — GitOps makes a Git repo the source of truth; a controller continuously
  reconciles the cluster to the committed manifests.
- **co-26 · argocd-application** — Argo CD's Application (and ApplicationSet) points at a Git path and
  syncs/self-heals it, reporting `Synced`/`OutOfSync`.
- **co-27 · flux-kustomization-helmrelease** — Flux reconciles Git via Kustomization (raw/kustomize) and
  HelmRelease (Helm chart) custom resources.
- **co-28 · argo-vs-flux** — Argo CD offers a UI-centric app model; Flux is a controller-set toolkit —
  both are CNCF-graduated GitOps engines.
- **co-29 · env-overlays** — dev/staging/prod differ via Kustomize base+overlays or per-env Helm values,
  not by forking the manifests.
- **co-30 · build-once-promote** — build an image once, then promote the _same_ digest through
  environments by a Git change, never rebuilding per env.
- **co-31 · secrets-not-in-git** — plaintext Secrets can't live in Git; Sealed Secrets encrypt them for
  Git, External Secrets sync them from a vault at runtime.
- **co-32 · velero-backup-dr** — Velero backs up cluster objects + PV snapshots to object storage, sizing
  the schedule to a target RPO/RTO.
- **co-33 · restore-drill** — a backup is only as good as a rehearsed restore; a periodic restore drill
  proves the DR path actually recovers.
- **co-34 · immutable-nodes** — image-based/immutable nodes (Talos, atomic A/B updates) make the OS
  reproducible and roll back on a failed update.

## Worked examples

Colocated under `self-managed-kubernetes-and-gitops/learning/`; each is a real k3s/kubeadm/talosctl CLI
run, a Helm values file, or a Kubernetes/Argo/Flux YAML manifest applied against multi-node VMs **or** an
annotated decision artifact (DD-20/DD-30). Contiguous `ex-01..ex-82`. Every example cites the `co-NN` it
exercises. Concepts come before examples.

### Beginner

- **ex-01 · why-self-managed** — a decision table cloud-managed (EKS/GKE) vs self-managed (you run the
  control plane, LB, storage, TLS) — verify what each side owns. (co-01)
- **ex-02 · control-plane-vs-workers** — annotate the server/agent node split — verify which node runs
  the API server vs the workloads. (co-02)
- **ex-03 · control-plane-components** — annotate apiserver/scheduler/controller-manager/kubelet over
  etcd — verify each component's job. (co-03)
- **ex-04 · reconciliation-loop** — annotate posting desired state, a controller converging live state —
  verify the declarative (not imperative) model. (co-04)
- **ex-05 · etcd-raft** — annotate etcd as the Raft-backed cluster datastore — verify the API server
  persists all state there. (co-05)
- **ex-06 · quorum-math** — annotate quorum `(n/2)+1` for `n` servers — verify why 3 tolerates 1 loss and
  even counts don't help. (co-05)
- **ex-07 · k3s-install-server** — `curl -sfL https://get.k3s.io | sh -` on the first VM — verify the
  server comes up and `kubectl get nodes` shows it Ready. (co-06)
- **ex-08 · k3s-single-binary** — annotate k3s as one fully-compliant binary bundling the control plane —
  verify one process serves the cluster. (co-06)
- **ex-09 · k3s-kubeconfig** — copy `/etc/rancher/k3s/k3s.yaml`, point `KUBECONFIG`, `kubectl get nodes`
  — verify remote access. (co-06)
- **ex-10 · k3s-datastore-sqlite** — annotate the default embedded SQLite backend on a single-server k3s
  — verify the default storage. (co-07)
- **ex-11 · k3s-embedded-etcd** — start the first server with `--cluster-init` — verify k3s selects
  embedded etcd for HA instead of SQLite. (co-07)
- **ex-12 · ha-odd-servers** — annotate the three-or-more, odd-count server rule — verify a two-server
  "HA" cluster has no fault tolerance. (co-08)
- **ex-13 · k3s-ha-three-servers** — join two more servers to the `--cluster-init` node with the token —
  verify a three-server HA control plane. (co-08)
- **ex-14 · kubeadm-init** — `kubeadm init --pod-network-cidr=…` on a fresh VM — verify a control-plane
  node and the printed join command. (co-09)
- **ex-15 · kubeadm-join** — run the `kubeadm join … --token …` on a worker — verify the node joins and
  reports Ready (after CNI). (co-09)
- **ex-16 · kubeadm-scope** — annotate that kubeadm only bootstraps (no machine provisioning, no add-ons)
  — verify what it deliberately leaves to you. (co-09)
- **ex-17 · k0s-single-binary** — `k0s install controller` + `k0s start` — verify a k0s single-binary
  control plane runs. (co-10)
- **ex-18 · talos-immutable** — annotate Talos's no-SSH/no-shell/immutable-rootfs model — verify why you
  can't `ssh` in to fix a node. (co-11)
- **ex-19 · talos-machineconfig** — `talosctl apply-config` a controlplane YAML machine config — verify
  the node configures itself from declarative YAML over the API. (co-11)
- **ex-20 · distro-decision** — a decision table k3s / kubeadm / k0s / Talos by weight, control, and
  immutability — verify the selection heuristic. (co-12)
- **ex-21 · immutable-nodes** — annotate Talos atomic A/B image updates with auto-rollback — verify a
  failed update reverts instead of leaving a broken node. (co-34)
- **ex-22 · kubectl-get-nodes** — `kubectl get nodes -o wide` on the multi-node cluster — verify all
  nodes are Ready with roles. (co-02)
- **ex-23 · add-worker-join** — join an agent with the node token/URL — verify the worker appears and
  schedules pods. (co-13)
- **ex-24 · node-cordon** — `kubectl cordon <node>` — verify it goes `SchedulingDisabled` and takes no new
  pods. (co-13)
- **ex-25 · node-drain** — `kubectl drain <node> --ignore-daemonsets` — verify pods evict and reschedule
  elsewhere. (co-13)
- **ex-26 · node-uncordon** — `kubectl uncordon <node>` — verify scheduling resumes on the node. (co-13)
- **ex-27 · etcd-snapshot-save** — `k3s etcd-snapshot save` — verify a timestamped snapshot file is
  written. (co-14)
- **ex-28 · etcd-snapshot-restore** — `k3s server --cluster-reset --cluster-reset-restore-path=…` — verify
  the cluster restores state from the snapshot. (co-14)
- **ex-29 · upgrade-sequencing** — annotate control-plane-first, one-minor-at-a-time, drain-each-node
  upgrade order — verify the safe sequence. (co-15)
- **ex-30 · k3s-upgrade** — re-run the k3s installer pinned to a newer `INSTALL_K3S_VERSION` (or the
  system-upgrade-controller) — verify the version rolls forward. (co-15)

### Intermediate

- **ex-31 · cni-required** — annotate fresh kubeadm nodes stuck `NotReady` until a CNI is installed —
  verify the CNI is what makes them Ready. (co-16)
- **ex-32 · k8s-network-model** — annotate the every-pod-reaches-every-pod-without-NAT requirement —
  verify the flat pod-IP model. (co-16)
- **ex-33 · install-cilium** — `helm install cilium cilium/cilium` — verify eBPF-based pod networking
  brings nodes Ready. (co-17)
- **ex-34 · cni-decision** — a decision table Cilium (eBPF) / Calico / Flannel (VXLAN) — verify each CNI's
  trade-off. (co-17)
- **ex-35 · flannel-vxlan** — annotate Flannel's VXLAN overlay encapsulating pod traffic — verify the
  overlay path between nodes. (co-17)
- **ex-36 · netpol-default-open** — annotate that pods accept all ingress/egress by default — verify the
  open baseline before any policy. (co-18)
- **ex-37 · netpol-deny-ingress** — a default-deny NetworkPolicy selecting a namespace — verify traffic to
  those pods is now blocked. (co-18)
- **ex-38 · netpol-allow-frontend** — an ingress rule allowing only `role: frontend` on port 6379 —
  verify only the frontend reaches the db. (co-18)
- **ex-39 · metallb-install** — install MetalLB via Helm/manifests — verify the controller and speaker
  pods run. (co-19)
- **ex-40 · metallb-ipaddresspool** — an `IPAddressPool` CR carving a LAN range — verify the pool is
  registered. (co-19)
- **ex-41 · loadbalancer-gets-ip** — a `type: LoadBalancer` Service — verify MetalLB assigns it an
  external IP from the pool (no cloud provider). (co-19)
- **ex-42 · metallb-l2advertisement** — an `L2Advertisement` CR — verify the IP is reachable on the LAN
  via ARP from one owner node. (co-20)
- **ex-43 · metallb-l2-vs-bgp** — a decision table Layer 2 (ARP, single-owner) vs BGP (router peering,
  true balancing) — verify each mode's fit. (co-20)
- **ex-44 · metallb-bgp** — a `BGPPeer` + `BGPAdvertisement` peering with a router — verify routes are
  advertised over BGP. (co-20)
- **ex-45 · longhorn-install** — install Longhorn via Helm — verify the Longhorn StorageClass and
  manager pods appear. (co-21)
- **ex-46 · longhorn-replicated** — annotate Longhorn replicating a volume across nodes — verify a
  replica survives a node loss. (co-21)
- **ex-47 · local-path-provisioner** — use the k3s-bundled `local-path` StorageClass — verify a
  node-local PV is provisioned. (co-21)
- **ex-48 · storageclass-pvc** — a PVC referencing a StorageClass — verify a PV is dynamically bound to
  the claim. (co-22)
- **ex-49 · storage-decision** — a decision table Longhorn (replicated/HA) vs local-path (simple/node-
  bound) — verify when to use each. (co-22)
- **ex-50 · ingress-controller-choice** — a decision table Traefik / nginx / Caddy ingress controllers —
  verify each's trade-off and license. (co-23)
- **ex-51 · traefik-default** — annotate the Traefik ingress controller k3s bundles by default — verify
  Ingress objects are satisfied out of the box. (co-23)
- **ex-52 · ingress-manifest** — an Ingress routing a host/path to a Service — verify external HTTP
  reaches the app through the controller. (co-23)
- **ex-53 · cert-manager-install** — install cert-manager via Helm — verify its CRDs and controller run.
  (co-24)
- **ex-54 · clusterissuer-acme** — a `ClusterIssuer` for Let's Encrypt ACME — verify the issuer is Ready.
  (co-24)
- **ex-55 · certificate-resource** — a `Certificate` requesting a host cert — verify cert-manager writes
  the signed cert into a TLS Secret. (co-24)
- **ex-56 · ingress-tls-auto** — an Ingress annotated `cert-manager.io/cluster-issuer` — verify the TLS
  cert is issued and renewed automatically. (co-24)
- **ex-57 · acme-http01** — annotate the ACME HTTP-01 challenge cert-manager solves via a temporary
  ingress route — verify the domain-validation flow. (co-24)

### Advanced

- **ex-58 · gitops-model** — annotate Git as the single source of truth with a controller reconciling the
  cluster to it — verify the pull-based model vs `kubectl apply`. (co-25)
- **ex-59 · argocd-install** — install Argo CD into the cluster — verify the API/UI and repo-server pods
  run. (co-26)
- **ex-60 · argocd-application** — an `Application` pointing at a Git repo path — verify Argo CD syncs the
  manifests into the cluster. (co-26)
- **ex-61 · argocd-sync-status** — change the Git manifest, watch the app — verify it flips `OutOfSync`
  then `Synced` on reconcile. (co-26)
- **ex-62 · argocd-applicationset** — an `ApplicationSet` generating one Application per env from a
  list/git generator — verify dev/staging/prod apps appear. (co-26)
- **ex-63 · argocd-auto-sync** — enable automated sync + self-heal — verify a manual cluster edit is
  reverted back to Git. (co-26)
- **ex-64 · flux-bootstrap** — `flux bootstrap git` against a repo — verify Flux installs itself and
  commits its own manifests. (co-27)
- **ex-65 · flux-kustomization** — a Flux `Kustomization` CR reconciling a path — verify the manifests
  apply on the sync interval. (co-27)
- **ex-66 · flux-helmrelease** — a `HelmRelease` CR installing a chart with values — verify Flux releases
  and upgrades it from Git. (co-27)
- **ex-67 · argo-vs-flux** — a decision table Argo CD (app/UI-centric) vs Flux (controller toolkit) —
  verify when to reach for each. (co-28)
- **ex-68 · kustomize-base-overlay** — a `base/` + `overlays/{dev,staging,prod}/` layout — verify each
  overlay hydrates the shared base. (co-29)
- **ex-69 · overlay-patch** — a prod overlay patch bumping `replicas` and resources — verify only prod
  differs from the base. (co-29)
- **ex-70 · helm-values-per-env** — per-env `values-{dev,staging,prod}.yaml` overriding a chart — verify
  each env renders distinct config. (co-29)
- **ex-71 · build-once-promote** — annotate promoting one image digest dev→staging→prod (no rebuild) —
  verify identical bits ship to every env. (co-30)
- **ex-72 · promotion-via-git** — annotate a promotion as a Git commit/PR bumping the digest in the next
  overlay — verify the audit trail. (co-30)
- **ex-73 · secrets-not-in-git** — annotate why a plaintext (base64) Secret must never be committed —
  verify the leak risk of Git history. (co-31)
- **ex-74 · sealed-secret** — `kubeseal` a Secret into a `SealedSecret` committed to Git — verify only the
  in-cluster controller can decrypt it. (co-31)
- **ex-75 · external-secrets** — an `ExternalSecret` + `SecretStore` syncing from a vault — verify the
  operator materializes a Secret at runtime. (co-31)
- **ex-76 · secrets-decision** — a decision table Sealed Secrets (encrypt-in-Git) vs External Secrets
  (sync-from-vault) — verify each model's fit. (co-31)
- **ex-77 · velero-install** — install Velero pointing at an S3/MinIO bucket — verify the backup location
  is Available. (co-32)
- **ex-78 · velero-backup** — `velero backup create` a namespace with PVs — verify the tarball + PV
  snapshot land in object storage. (co-32)
- **ex-79 · velero-schedule** — a `Schedule` backing up on a cron — verify the RPO the interval implies.
  (co-32)
- **ex-80 · rpo-rto** — annotate RPO (data-loss window = backup interval) vs RTO (time-to-recover) — verify
  how the schedule sizes each. (co-32)
- **ex-81 · restore-drill** — `velero restore` a backup into a fresh cluster — verify the app + data come
  back, proving the DR path. (co-33)
- **ex-82 · self-managed-capstone** — bootstrap a three-server k3s HA cluster with MetalLB + Longhorn +
  cert-manager, then drive one app dev→staging→prod through Argo CD from a Git repo — verify a Git commit
  promotes the app and the cluster self-heals. (co-06, co-08, co-19, co-21, co-24, co-26, co-29, co-30)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: bootstrap and operate a **self-managed production-style k3s cluster** on your own VMs, install
  the on-prem essentials (bare-metal LoadBalancer, replicated storage, automatic TLS), then run one app
  through a **dev→staging→prod GitOps promotion** driven by Argo CD from a Git repo of source-of-truth
  manifests — proving a promotion is a commit, secrets never sit in Git in plaintext, and the cluster
  self-heals and can be restored.
- **Concepts exercised**: [ ] a three-server HA k3s cluster with embedded etcd + quorum (co-06, co-07,
  co-08) [ ] a CNI + a NetworkPolicy (co-16, co-18) [ ] MetalLB `type: LoadBalancer` on bare metal
  (co-19, co-20) [ ] Longhorn storage via StorageClass/PVC (co-21, co-22) [ ] ingress + cert-manager ACME
  TLS (co-23, co-24) [ ] Argo CD Application/ApplicationSet with Kustomize overlays (co-26, co-29) [ ]
  build-once-promote across envs (co-30) [ ] a SealedSecret or ExternalSecret (co-31) [ ] a Velero backup
  - restore drill (co-32, co-33).
- **Ordered steps**:
  1. `.../learning/capstone/cluster/` — bring up server 1 with `--cluster-init`, join servers 2–3 and a
     worker; install a CNI. Verify three servers form an HA control plane (`kubectl get nodes` all Ready,
     etcd quorum holds when one server is stopped).
  2. `.../learning/capstone/platform/` — install MetalLB (IPAddressPool + L2Advertisement), Longhorn, and
     cert-manager (ClusterIssuer). Verify a `type: LoadBalancer` Service gets a LAN IP, a PVC binds a
     Longhorn PV, and an Ingress serves auto-issued TLS.
  3. `.../learning/capstone/gitops/` — a Git repo with `base/` + `overlays/{dev,staging,prod}/`, wired to
     Argo CD via an ApplicationSet; secrets committed as SealedSecrets. Verify Argo CD syncs all three
     envs and the sealed secret decrypts only in-cluster.
  4. Promote: bump the image digest in `overlays/staging` then `overlays/prod` via a Git commit. Verify
     Argo CD rolls the _same_ digest forward per env and reports `Synced`; delete a pod and verify
     self-heal.
  5. `.../learning/capstone/dr/` — a Velero scheduled backup, then a `velero restore` drill. Verify the
     app + its Longhorn data recover from the backup.
- **Acceptance criteria**: the control plane is HA (survives one server loss); a bare-metal Service gets a
  real IP; storage is replicated; TLS is auto-issued and renewed; a Git commit promotes the app across
  envs with no rebuild; no plaintext secret is in Git; a restore drill recovers app + data.
- **Done bar**: runnable end-to-end on your own multi-node VMs + web-verified.

## Read more

**Books**

- **Kubernetes: Up and Running** — Kelsey Hightower, Brendan Burns, Joe Beda (3rd ed. with Lachlan
  Evenson, 2022, O'Reilly). By Kubernetes co-creators/maintainers; the standard reference for the objects
  and control-plane model this topic operates.
- **Cloud Native DevOps with Kubernetes** — John Arundel, Justin Domingus (2nd ed., 2022, O'Reilly). A
  practical operator's view — clusters, storage, networking, secrets, and continuous deployment.
- **GitOps and Kubernetes** — Billy Yuen, Alexander Matyushentsev, Todd Ekenstam, Jesse Suen (2021,
  Manning). Written partly by Argo CD maintainers; the declarative-promotion / reconciliation model this
  topic's second half builds on.

**Papers & articles**

- **In Search of an Understandable Consensus Algorithm (Raft)** — Diego Ongaro, John Ousterhout (2014,
  USENIX ATC). The consensus algorithm behind etcd — the quorum reasoning under every HA control plane.
  <https://raft.github.io/raft.pdf>
- **Kubernetes Documentation** — Cloud Native Computing Foundation (ongoing). The canonical reference for
  the network model, storage, and cluster administration. <https://kubernetes.io/docs/home/>
- **Argo CD & Flux Documentation** — CNCF (ongoing). The two graduated GitOps engines' own reconciliation
  and Application/Kustomization semantics. <https://argo-cd.readthedocs.io/> · <https://fluxcd.io/flux/>

---

← Previous: [52 · Bare-Metal Virtualization](./52-bare-metal-virtualization.md) · Next: [54 · Build Automation & Task Runners](./54-build-automation-and-task-runners.md) →
