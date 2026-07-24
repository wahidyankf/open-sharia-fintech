# Containers and Orchestration (By Example, YAML/CLI)

**Course ID**: `containers-and-orchestration` · **Format**: By Example · **Language**: YAML/CLI.

**Short summary**: Docker containers and Kubernetes orchestration

**Scope note**: packaging and running services with containers and Kubernetes — images, Dockerfiles,
Compose for local multi-service, then K8s objects (Pods/Deployments/Services/Ingress), config/secrets,
and health/scaling — plus the daemonless/rootless alternative (Podman + Quadlet) alongside Docker.
`†`: the "language" is Dockerfiles + YAML + the `docker`/`podman`/`kubectl` CLIs against a
real app (the [`11-backend-essentials`](./backend-essentials.md) service). Ingress-vs-Gateway-API is
handled with the license/standards-awareness lens (DD-15). Cloud provisioning is
[`51-cloud-and-iac`](./cloud-and-iac.md).

## Why this exists · the big idea

- **The problem before the solution**: "works on my machine" and hand-run servers fail the moment you need
  reproducibility, many identical copies, and automatic recovery — manual ops don't scale and drift silently.
- **Keep-this-if-you-forget-everything**: package the app with its environment into an immutable image, then
  declare the desired state and let the orchestrator's control loops continuously reconcile reality to it —
  you describe _what you want_, not the steps to get there.
- **Big ideas touched**: `mechanism-vs-policy` (you declare desired state; the orchestrator is the
  reconciling mechanism), `determinism-vs-emergence` (immutable images buy reproducibility; self-healing
  emerges from control loops).

## Prerequisites

- **Prior topics**: [topic 11 Backend Essentials](./backend-essentials.md) (an app to containerize),
  [topic 5 Just Enough Bash](./just-enough-bash.md) (CLI fluency), and
  [topic 10 SQL Essentials](./sql-essentials.md) (a DB to run as a companion service).
- **Tools & environment**: a macOS/Linux terminal; **Docker** (or a compatible engine) + `docker compose`;
  a local Kubernetes (kind/minikube/k3d) + `kubectl`; the backend app + a DB image. Images pinned by
  digest where practical (DD-15/supply-chain).
- **Assumed knowledge**: running a service locally + env-based config (topic 11); shell basics (topic 05);
  reading YAML.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **Ingress is frozen; Gateway API is the recommendation.** kubernetes.io states
  verbatim "The Ingress API has been frozen" and "recommends using Gateway instead of Ingress" — Ingress
  stays GA/stable with no removal planned but takes no further changes. (kubernetes.io/docs/concepts/services-networking/ingress)
- 2026-07-12 — verified: **`docker compose` (v2 CLI plugin, space not hyphen)** is current; v1
  (`docker-compose`) is EOL. Use `compose.yaml` with **no `version:` key** (the current recommended form).
  (docs.docker.com/compose/release-notes)
- 2026-07-12 — verified: file stays version-agnostic on K8s object versions (good) — current stable is
  Kubernetes v1.36.2 (2026-06-09), v1.37.0 due 2026-08-26; keep it unpinned. Multi-stage builds, non-root
  users, `.dockerignore`, digest-pinned images remain current supply-chain best practice.

> DD-35 primary-source pass (2026-07-12). Kernel mechanisms, Dockerfile/CLI syntax, OCI specs, and K8s
> object field defaults traced to primary sources (man7.org man-pages, docs.docker.com, opencontainers.org
> GitHub specs, kubernetes.io) and fetched/read. Numeric defaults and spec versions flagged as version-sensitive.

- **Containers vs VMs** — a namespace "wraps a global system resource in an abstraction that makes it appear
  to the processes within the namespace that they have their own isolated instance"; cgroups "allow processes
  to be organized into hierarchical groups whose usage of various types of resources can then be limited and
  monitored." Docker: containers "share the OS kernel," VMs bundle "a full copy of an operating system."
  Sources: [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html), [cgroups(7)](https://man7.org/linux/man-pages/man7/cgroups.7.html), [Docker — What is a Container](https://www.docker.com/resources/what-container/) (fetched, verbatim).
- **Images & layers** — an image is "a standardized package that includes all of the files, binaries,
  libraries, and configurations to run a container … Once an image is created, it can't be modified"; layers
  are "stacked" with a copy-on-write "new writable layer on top." Sources: [Docker — What is an image](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/), [storage drivers](https://docs.docker.com/storage/storagedriver/) (fetched, verbatim).
- **Dockerfile** — `FROM` "initializes a new build stage and sets the base image"; `RUN` "will execute any
  commands to create a new layer"; `COPY` "copies new files or directories"; `CMD` "sets the command to be
  executed" (only the last takes effect); `ENTRYPOINT` "configure a container that will run as an
  executable" — "arguments to `docker run` will be appended after … an exec form `ENTRYPOINT`, and will
  override … `CMD`." Source: [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) (fetched, verbatim).
- **Build cache / multi-stage** — "If a layer changes, all other layers that come after it are also
  affected"; multi-stage: name stages with `AS <NAME>` and `COPY --from=build …`. Sources: [build cache](https://docs.docker.com/build/cache/), [multi-stage builds](https://docs.docker.com/build/building/multi-stage/) (fetched, verbatim).
- **Image size** — distroless images "contain only your application and its runtime dependencies … no
  package managers, shells or any other programs" (~2 MiB vs Alpine ~5 MiB, Debian ~124 MiB); `.dockerignore`
  excludes files "to avoid sending unwanted files … to the builder." Sources: [distroless](https://github.com/GoogleContainerTools/distroless), [best practices](https://docs.docker.com/build/building/best-practices/), [build context](https://docs.docker.com/build/building/context/#dockerignore-files) (fetched, verbatim).
- **OCI** — the OCI (launched June 22, 2015 by Docker, CoreOS et al. under the Linux Foundation) maintains
  the Image, Runtime, and Distribution specs. A digest is "a unique identifier created from a cryptographic
  hash of a Blob's content"; "A manifest digest may have zero, one, or many tags" (tags mutable, digests
  immutable). Versions at fetch: image-spec v1.1.1, runtime-spec v1.3.0 (**version-sensitive**). Sources:
  [OCI overview](https://opencontainers.org/about/overview/), [image-spec](https://github.com/opencontainers/image-spec/blob/main/spec.md), [distribution-spec](https://github.com/opencontainers/distribution-spec/blob/main/spec.md) (fetched, verbatim).
- **Registries / digests** — image name format `[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]` (defaults:
  `docker.io`, `library`, `latest`); pull-by-digest "specify exactly which version … 'pin' an image," with
  the caveat Docker "does therefore not pull updated versions … which may include security updates."
  Sources: [docker tag](https://docs.docker.com/reference/cli/docker/image/tag/), [image digests](https://docs.docker.com/dhi/core-concepts/digests/) (fetched, verbatim).
- **Networking / volumes** — drivers: bridge ("default network driver"), host ("Remove network isolation"),
  none ("Completely isolate"); `-p [IP:]hostPort:containerPort[/proto]` publishes ports (default bind
  `0.0.0.0`). Volumes are "created and managed by Docker"; bind mounts mount "a file or directory on the host
  machine … into a container." Sources: [Docker networking](https://docs.docker.com/engine/network/), [volumes](https://docs.docker.com/engine/storage/volumes/), [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/) (fetched, verbatim).
- **K8s architecture** — a cluster is "a control plane plus a set of worker machines, called nodes";
  kube-apiserver "is the front end for the Kubernetes control plane"; etcd is the "backing store for all
  cluster data"; kube-scheduler "watches for newly created Pods with no assigned node"; kubelet "makes sure
  that containers are running in a Pod"; kube-proxy implements "part of the … Service concept." Source:
  [K8s Components](https://kubernetes.io/docs/concepts/architecture/) (fetched, verbatim).
- **Pods** — "the smallest deployable units … a group of one or more containers, with shared storage and
  network resources"; sidecars are init containers with `restartPolicy: Always` (stable since v1.29).
  Sources: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/), [Sidecar containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) (fetched, verbatim).
- **Deployments / ReplicaSets** — a Deployment "provides declarative updates for Pods and ReplicaSets …
  changes the actual state to the desired state at a controlled rate"; rolling-update `maxSurge`/
  `maxUnavailable` "Defaults to 25%." A ReplicaSet maintains "a stable set of replica Pods." Sources:
  [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [Deployment API](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/), [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) (fetched, verbatim).
- **Services** — "a method for exposing a network application"; types `ClusterIP` (default), `NodePort`,
  `LoadBalancer`, `ExternalName`; NodePort default range `30000-32767` (`[Verified]` via WebSearch snippet of
  the live page — direct fetch truncated). Discovery via environment variables and DNS. Source:
  [Service](https://kubernetes.io/docs/concepts/services-networking/service/) (fetched; NodePort range corroborated).
- **ConfigMaps / Secrets** — a ConfigMap stores "non-confidential data in key-value pairs" (≤ 1 MiB); a
  Secret holds "a small amount of sensitive data," but "Kubernetes Secrets are, by default, stored
  unencrypted in the API server's underlying data store (etcd)" — base64 is **not** encryption. Sources:
  [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/), [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) (fetched, verbatim).
- **Namespaces / labels** — namespaces provide "a mechanism for isolating groups of resources"; labels are
  "key/value pairs … attached to objects … to specify identifying attributes"; equality (`=`/`==`/`!=`) and
  set-based (`in`/`notin`/`exists`) selectors, with "no logical OR." Sources: [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) (fetched, verbatim).
- **Ingress** — "exposes HTTP and HTTPS routes from outside the cluster"; "You must have an Ingress
  controller to satisfy an Ingress. Only creating an Ingress resource has no effect." Per the frozen-Ingress
  note above, Gateway API is the recommended successor. Source: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) (fetched, verbatim).
- **Probes** — liveness "determine when to restart a container"; readiness "determine when a container is
  ready to accept traffic"; startup "verify whether the application … is started." Shared `Probe` defaults:
  `periodSeconds` 10, `timeoutSeconds` 1, `successThreshold` 1, `failureThreshold` 3, `initialDelaySeconds` 0. Sources: [Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/), [Pod API — Probe](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#Probe) (fetched, verbatim).
- **Resources / QoS** — requests inform scheduling and reservation; limits are "enforced by the kernel with
  out of memory (OOM) kills"; QoS classes Guaranteed (limits == requests for all containers), Burstable (some
  request/limit), BestEffort (none); a memory-limit kill shows `STATUS: OOMKilled`, `exitCode: 137`. Sources:
  [Manage resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), [QoS](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/) (fetched, verbatim).
- **HPA / workloads** — HPA "automatically scaling capacity to match demand" via
  `ceil(currentReplicas × currentMetricValue / desiredMetricValue)`. StatefulSets maintain "a sticky
  identity for each of those Pods"; DaemonSets "ensure that all (or some) Nodes run a copy of a Pod"; Jobs
  "run to completion and then stop" (default `parallelism`/`completions` = 1, exact API sentence `[Needs Verification]`); CronJobs create Jobs "on a repeating schedule" (approximate — "two Jobs might be created,
  or no Job"). Sources: [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/), [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/), [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) (fetched, verbatim).
- **Reconciliation loop** — "controllers are control loops that watch the state of your cluster, then make or
  request changes … Each controller tries to move the current cluster state closer to the desired state"
  (thermostat analogy; desired state in `spec`). Source: [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/) (fetched, verbatim).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · containers-vs-vms** — containers are OS-level virtualization sharing the host kernel; VMs bundle
  a full guest OS.
- **co-02 · namespaces** — Linux kernel namespaces give a process an isolated view of a global resource
  (PID, net, mount, …).
- **co-03 · cgroups** — control groups limit and monitor a group of processes' resource usage.
- **co-04 · image-vs-container** — an image is an immutable package; a container is a running instance of
  one.
- **co-05 · image-layers** — images are stacked layers with a copy-on-write writable layer per container.
- **co-06 · dockerfile-instructions** — `FROM`/`RUN`/`COPY`/`CMD`/`ENTRYPOINT` build an image step by step.
- **co-07 · cmd-vs-entrypoint** — `ENTRYPOINT` sets the executable and `CMD` supplies default, overridable
  arguments.
- **co-08 · build-cache** — each instruction is a cached layer; a changed layer invalidates all layers after
  it.
- **co-09 · multi-stage-build** — named build stages and `COPY --from` produce a slim final image.
- **co-10 · dockerignore** — `.dockerignore` excludes files from the build context.
- **co-11 · image-optimization** — minimize layers and use a slim/distroless base to shrink the image.
- **co-12 · oci-specs** — the OCI Image, Runtime, and Distribution specs standardize container formats.
- **co-13 · registries-tags-digests** — registries store images; a tag is a mutable pointer, a digest an
  immutable content address.
- **co-14 · digest-pinning** — pinning an image by `@sha256:` digest makes a pull reproducible.
- **co-15 · container-networking** — bridge/host/none drivers and `-p` port publishing connect containers.
- **co-16 · volumes-bind-mounts** — a Docker-managed volume vs a host bind mount persists container data.
- **co-17 · docker-compose** — Compose (`compose.yaml`) runs a multi-service local stack.
- **co-18 · k8s-architecture** — the control plane (apiserver/etcd/scheduler/controller-manager) plus nodes
  (kubelet/kube-proxy) form a cluster.
- **co-19 · pods** — a Pod is the smallest deployable unit: one or more containers sharing network and
  storage.
- **co-20 · deployments-replicasets** — a Deployment declaratively manages ReplicaSets and rolling updates
  (`maxSurge`/`maxUnavailable`).
- **co-21 · services** — a Service (ClusterIP/NodePort/LoadBalancer) exposes Pods with stable DNS discovery.
- **co-22 · configmaps-secrets** — ConfigMaps hold non-confidential config; Secrets hold sensitive data
  (base64 is not encryption).
- **co-23 · namespaces-labels-selectors** — namespaces isolate resources; labels + selectors group and
  target objects.
- **co-24 · ingress** — an Ingress routes external HTTP(S) to Services and requires an Ingress controller
  (Ingress frozen; Gateway API recommended).
- **co-25 · probes** — liveness/readiness/startup probes drive restart, traffic-gating, and slow-start
  handling.
- **co-26 · resources-qos** — requests/limits schedule and cap Pods; QoS classes are Guaranteed/Burstable/
  BestEffort; over-limit memory is OOMKilled.
- **co-27 · hpa** — a HorizontalPodAutoscaler scales replica count to match demand.
- **co-28 · statefulsets** — StatefulSets give Pods sticky identities and stable per-Pod storage.
- **co-29 · daemonsets** — a DaemonSet runs one Pod copy per node.
- **co-30 · jobs-cronjobs** — Jobs run to completion; CronJobs run Jobs on a schedule.
- **co-31 · reconciliation-loop** — controllers continuously drive current state toward the declared desired
  state.
- **co-32 · kubectl-apply-declarative** — `kubectl apply` reconciles a declarative manifest, not imperative
  steps.
- **co-33 · podman-daemonless** — Podman is a daemonless, OCI-compatible engine: `podman run` fork-execs the
  OCI runtime as a child of the invoking process, so there is no long-running root daemon like `dockerd`.
- **co-34 · rootless-containers** — rootless is Podman's default and recommended mode; container UIDs map into
  the invoking user's subuid/subgid range, so a container escape lands as an unprivileged host user, not root
  (contrast Docker's root-privileged daemon). Images are interchangeable with Docker via the OCI spec.
- **co-35 · podman-compose-and-quadlet** — `podman compose` shells out to a compose provider
  (`docker-compose` or `podman-compose`); **Quadlet** `.container`/`.pod` unit files are the systemd-native
  way to run containers, replacing the deprecated `podman generate systemd`.

## Worked examples

Colocated under `containers-and-orchestration/learning/`; each is a real Dockerfile, Compose file, or K8s
manifest applied from the `docker`/`kubectl` CLI **or** an annotated decision artifact (DD-20/DD-30).
Contiguous `ex-01..ex-83`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · containers-vs-vms** — a decision table containers (share kernel) vs VMs (full guest OS) — verify
  the kernel-sharing distinction. (co-01)
- **ex-02 · namespaces-isolation** — annotate kernel namespaces isolating PID/net/mount — verify each gives
  an isolated view. (co-02)
- **ex-03 · cgroups-limits** — annotate cgroups limiting CPU/memory — verify usage is capped. (co-03)
- **ex-04 · image-vs-container** — annotate image (immutable) vs container (running instance) — verify the
  relationship. (co-04)
- **ex-05 · docker-run** — `docker run` an image into a container — verify the container starts. (co-04)
- **ex-06 · image-layers** — annotate the layered filesystem + writable layer — verify layers stack. (co-05)
- **ex-07 · copy-on-write** — annotate copy-on-write on first modify — verify a write copies the file up.
  (co-05)
- **ex-08 · dockerfile-from-run** — a Dockerfile with `FROM` + `RUN` — verify it builds. (co-06)
- **ex-09 · dockerfile-copy** — `COPY` files into the image — verify the file appears in the image. (co-06)
- **ex-10 · dockerfile-cmd** — a `CMD` default command — verify it runs on `docker run`. (co-06)
- **ex-11 · entrypoint-cmd-interaction** — `ENTRYPOINT` + `CMD` default-args — verify args override CMD but
  append to ENTRYPOINT. (co-07)
- **ex-12 · build-cache-order** — order instructions so deps cache before source — verify a source change
  reuses the deps layer. (co-08)
- **ex-13 · cache-invalidation** — annotate a change invalidating all subsequent layers — verify the cascade.
  (co-08)
- **ex-14 · multi-stage-build** — a multi-stage Dockerfile with `COPY --from` — verify the final image omits
  build tools. (co-09)
- **ex-15 · multi-stage-named** — named build stages (`AS build`) — verify the stage name resolves. (co-09)
- **ex-16 · dockerignore** — a `.dockerignore` excluding `node_modules`/`.git` — verify they leave the
  context. (co-10)
- **ex-17 · non-root-user** — a `USER` non-root final image — verify the process runs unprivileged. (co-11)
- **ex-18 · distroless-base** — annotate a distroless/alpine slim base — verify no shell/package manager.
  (co-11)
- **ex-19 · small-image-layers** — combine `RUN` + apt-cache cleanup in one layer — verify the cache isn't
  persisted. (co-11)
- **ex-20 · oci-specs** — annotate the OCI Image/Runtime/Distribution specs — verify each spec's role.
  (co-12)
- **ex-21 · docker-build-tag** — `docker build -t name:tag` — verify the tag is applied. (co-13)
- **ex-22 · registry-push-pull** — `docker push`/`docker pull` `name:tag` — verify a round-trip. (co-13)
- **ex-23 · tag-vs-digest** — annotate mutable tag vs immutable digest — verify the addressing difference.
  (co-13)
- **ex-24 · digest-pin** — `docker pull image@sha256:…` — verify the exact content is pinned. (co-14)
- **ex-25 · bridge-network** — run on the default bridge network — verify container connectivity. (co-15)
- **ex-26 · port-publish** — `-p 8080:80` publish a port — verify the host reaches the container. (co-15)
- **ex-27 · host-none-network** — annotate host vs none network drivers — verify their isolation levels.
  (co-15)

### Intermediate

- **ex-28 · named-volume** — a Docker-managed named volume — verify data survives container removal. (co-16)
- **ex-29 · bind-mount** — a host bind mount — verify host edits appear in the container. (co-16)
- **ex-30 · volume-vs-bind** — a decision table volume vs bind mount — verify when to use each. (co-16)
- **ex-31 · compose-two-services** — a `compose.yaml` app + DB — verify both start. (co-17)
- **ex-32 · compose-up** — `docker compose up` brings the stack up — verify all services run. (co-17)
- **ex-33 · compose-networks-depends** — service networking + `depends_on` — verify start ordering. (co-17)
- **ex-34 · compose-app-db-cache** — an app + DB + cache three-service stack — verify the app reaches both.
  (co-17)
- **ex-35 · k8s-architecture** — annotate control-plane + node components — verify each component's role.
  (co-18)
- **ex-36 · pod-manifest** — a single-container Pod manifest — verify it schedules and runs. (co-19)
- **ex-37 · multi-container-pod** — a Pod with a sidecar container — verify both share the network. (co-19)
- **ex-38 · deployment-manifest** — a Deployment with `replicas` — verify N Pods run. (co-20)
- **ex-39 · rolling-update** — annotate `maxSurge`/`maxUnavailable` rolling update — verify zero-downtime
  rollout. (co-20)
- **ex-40 · replicaset-owned** — annotate a ReplicaSet owning Pods via `ownerReferences` — verify ownership.
  (co-20)
- **ex-41 · kubectl-apply** — `kubectl apply -f` a manifest — verify the object is created. (co-32)
- **ex-42 · clusterip-service** — a ClusterIP Service — verify in-cluster reachability. (co-21)
- **ex-43 · nodeport-service** — a NodePort Service (30000–32767) — verify the node port routes in. (co-21)
- **ex-44 · loadbalancer-service** — a LoadBalancer Service — verify an external address is provisioned.
  (co-21)
- **ex-45 · service-dns-discovery** — annotate DNS-based service discovery — verify a service name resolves.
  (co-21)
- **ex-46 · configmap** — a ConfigMap consumed as env — verify the value reaches the container. (co-22)
- **ex-47 · secret** — a Secret injected into a Pod — verify the sensitive value is available. (co-22)
- **ex-48 · secret-not-encryption** — annotate the base64 ≠ encryption caveat — verify the etcd-plaintext
  warning. (co-22)
- **ex-49 · namespace** — a Namespace isolating resources — verify same-name objects coexist across
  namespaces. (co-23)
- **ex-50 · labels-selectors** — label a Pod and select it — verify the selector matches. (co-23)
- **ex-51 · set-based-selector** — a set-based (`in`/`notin`) selector — verify the set match. (co-23)
- **ex-52 · ingress-manifest** — an Ingress routing HTTP by path/host — verify the route reaches a Service.
  (co-24)
- **ex-53 · ingress-controller-required** — annotate that an Ingress needs a controller — verify no effect
  without one. (co-24)
- **ex-54 · ingress-frozen-gateway** — annotate Ingress frozen / Gateway API recommended — verify the
  successor status. (co-24)
- **ex-55 · liveness-probe** — a `livenessProbe` restarting on failure — verify a dead container restarts.
  (co-25)

### Advanced

- **ex-56 · readiness-probe** — a `readinessProbe` gating traffic — verify an unready Pod leaves the
  endpoints. (co-25)
- **ex-57 · startup-probe** — a `startupProbe` for a slow-start app — verify liveness waits for it. (co-25)
- **ex-58 · probe-defaults** — annotate probe defaults (`periodSeconds` 10, `failureThreshold` 3) — verify
  the shared defaults. (co-25)
- **ex-59 · resource-requests** — CPU/memory requests for scheduling — verify the scheduler reserves them.
  (co-26)
- **ex-60 · resource-limits** — CPU/memory limits enforced — verify over-limit is capped. (co-26)
- **ex-61 · qos-classes** — annotate Guaranteed/Burstable/BestEffort — verify each class's criteria. (co-26)
- **ex-62 · oomkilled** — annotate an OOMKilled (`exitCode 137`) memory-limit kill — verify the status.
  (co-26)
- **ex-63 · hpa-manifest** — a HorizontalPodAutoscaler on CPU — verify it scales under load. (co-27)
- **ex-64 · hpa-formula** — annotate the `ceil(currentReplicas × current/desired)` formula — verify the
  target-replica math. (co-27)
- **ex-65 · statefulset** — a StatefulSet with stable ordinal identity — verify `name-0`/`name-1` hostnames.
  (co-28)
- **ex-66 · statefulset-storage** — per-Pod persistent volume claims — verify each Pod keeps its volume.
  (co-28)
- **ex-67 · daemonset** — a DaemonSet one-Pod-per-node — verify one Pod per node. (co-29)
- **ex-68 · job** — a Job run-to-completion — verify it completes then stops. (co-30)
- **ex-69 · job-parallelism** — annotate `parallelism`/`completions` — verify parallel completions. (co-30)
- **ex-70 · cronjob** — a CronJob on a schedule — verify a Job is created per tick. (co-30)
- **ex-71 · cronjob-at-least-once** — annotate approximate/not-exactly-once scheduling — verify the caveat.
  (co-30)
- **ex-72 · reconciliation-loop** — annotate the controller current→desired loop — verify the thermostat
  analogy. (co-31)
- **ex-73 · self-heal-pod-kill** — `kubectl delete pod`, Deployment reschedules it — verify auto-recovery.
  (co-31)
- **ex-74 · declarative-vs-imperative** — a decision table `kubectl apply` vs imperative create — verify the
  reconciliation difference. (co-32)
- **ex-75 · scale-deployment** — `kubectl scale --replicas` — verify the Pod count changes. (co-20)
- **ex-76 · rollback-deployment** — `kubectl rollout undo` — verify the prior ReplicaSet is restored.
  (co-20)
- **ex-77 · configmap-volume-mount** — a ConfigMap mounted as a file — verify the file appears in the
  container. (co-22)
- **ex-78 · env-injection** — inject config as env vars into a container — verify the env is set. (co-22)
- **ex-79 · build-ship-run** — the full build → push → run CLI loop — verify an image goes from Dockerfile to
  running container. (co-13)
- **ex-80 · podman-rootless-run** — run the same image rootless under Podman — verify the process tree has no
  root daemon and the container UID maps to your unprivileged user. (co-33, co-34)
- **ex-81 · docker-podman-oci-parity** — build an image with Docker and run it under Podman (and the reverse)
  — verify the OCI image is interchangeable across engines. (co-33)
- **ex-82 · quadlet-systemd-unit** — a Quadlet `.container` unit managed by systemd — verify
  `systemctl --user start` runs it boot-persistently without a daemon. (co-35)
- **ex-83 · containers-capstone** — a hardened multi-stage image + Compose stack + K8s
  Deployment/Service/Ingress/ConfigMap/Secret/probes with self-healing — verify reachability, injected
  config, and pod-kill recovery. (co-09, co-17, co-20, co-21, co-25, co-31)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take the Backend-Essentials service and fully containerize + orchestrate it — a hardened
  multi-stage image, a Compose dev stack (app + DB + cache), then a Kubernetes deployment
  (Deployment/Service/Ingress + ConfigMap/Secret + liveness/readiness probes + resource limits) on a local
  cluster — proving reachability, config injection, and self-healing from the CLI.
- **Concepts exercised**: [ ] a multi-stage non-root Dockerfile (co-09, co-11) [ ] a Compose multi-service
  stack (co-17) [ ] K8s Deployment + Service + Ingress (co-20, co-21, co-24) [ ] ConfigMap + Secret injection
  (co-22) [ ] liveness/readiness probes (co-25) [ ] self-healing (pod kill → reschedule) (co-31) [ ] resource
  requests/limits (co-26).
- **Ordered steps**:
  1. `.../learning/capstone/Dockerfile` — a multi-stage, non-root image. Verify `docker build` succeeds and
     the running container serves the app.
  2. `compose.yaml` — app + DB + cache. Verify `docker compose up` brings all three up and the app reaches
     the DB.
  3. `k8s/` manifests — Deployment + Service + Ingress + ConfigMap + Secret + probes + limits, applied with
     `kubectl apply`. Verify the app is reachable through the Ingress and config comes from the ConfigMap.
  4. Delete a pod (`kubectl delete pod`). Verify the Deployment reschedules it and the app recovers with no
     manual step.
- **Acceptance criteria**: the image is multi-stage + non-root; Compose runs the full stack; the K8s app is
  reachable with injected config; killing a pod self-heals; secrets are injected (not baked into the image).
- **Done bar**: runnable end-to-end on a local cluster + web-verified.

## Read more

**Books**

- **Kubernetes: Up and Running** — Kelsey Hightower, Brendan Burns, Joe Beda (1st ed., 2017; 3rd ed. with Lachlan Evenson, 2022). Written by Kubernetes co-creators/maintainers; the standard introductory and reference text.
- **Docker Deep Dive** — Nigel Poulton (multiple editions). Widely used practical reference for Docker fundamentals and container runtime internals.
- **The Kubernetes Book** — Nigel Poulton (annual editions). Popular, frequently updated companion covering Kubernetes objects and operations.

**Papers & articles**

- **Large-scale cluster management at Google with Borg** — Abhishek Verma et al. (2015), EuroSys. Describes the internal Google system that directly inspired Kubernetes's design. <https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/>
- **Kubernetes Documentation** — Cloud Native Computing Foundation (ongoing). The official, canonical reference for Kubernetes concepts and APIs. <https://kubernetes.io/docs/home/>

## In which paths

- `interview-ready/software-engineer` — Phase 2 · Production-effective (web → cloud).
- `immediately-effective/software-engineer` — Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST.
- `fundamentally-strong/software-engineer` — Stage 10 · Scale, cloud & platform ops.

> _Content originated in the now-closed FS-SE plan (topic 50); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
