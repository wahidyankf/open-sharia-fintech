---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

## Intermediate: on-prem network, storage, ingress, and TLS

These examples model cluster add-ons and render harmless placeholder YAML. They require no installed chart,
custom resource, router, DNS zone, certificate authority, storage device, or live Kubernetes context.

### Example 31: CNI Is Required

_ex-31 · exercises co-16_

A kubeadm-style node remains incomplete until a CNI implements pod networking. CNI readiness is evidence that
the network model can work, not proof that policy or application connectivity is correct.

```sh
# => Prints the dependency; it does not install a CNI.
printf '%s\n' 'CNI supplies pod networking; without it, node readiness and Pod networking are incomplete'
```

**Verification**: The statement identifies CNI as a platform prerequisite.

**Key takeaway**: Install and validate a CNI before treating a new cluster as usable.

**Why it matters**: Workloads cannot reliably communicate while the cluster network is absent or unhealthy.
Making CNI ownership explicit prevents operators from diagnosing every networking symptom as an application
failure and creates a clear readiness gate for later policy and service tests.

### Example 32: Kubernetes Network Model

_ex-32 · exercises co-16_

Kubernetes expects Pods to reach other Pods without user-managed NAT. The CNI implements addressing, routing,
and often policy enforcement across nodes.

```sh
# => States the model locally; no packets are transmitted.
printf '%s\n' 'pod-to-pod connectivity is a CNI responsibility across the declared cluster network'
```

**Verification**: The model separates Pod networking from an external load balancer.

**Key takeaway**: CNI choice defines a major part of cluster connectivity behavior.

**Why it matters**: Incorrect assumptions about routing or NAT lead to fragile service designs and bad incident
triage. The network model lets an operator test the correct boundary: node health, Pod reachability, DNS,
NetworkPolicy, or external exposure.

### Example 33: Plan a Cilium Install

_ex-33 · exercises co-17_

Cilium is a CNI option with networking, observability, and policy capabilities. Select a current supported
version and configuration only after reviewing kernel, Kubernetes, and ownership compatibility.

```sh
# => Prints a review gate; it does not fetch a chart or modify a cluster.
printf '%s\n' 'review Cilium compatibility, policy needs, observability, rollback, and current official docs'
```

**Verification**: The plan does not claim a generic Helm command is safe for every cluster.

**Key takeaway**: CNI installation is a compatibility and recovery decision.

**Why it matters**: The CNI is on the data path for every workload, so an incompatible or unmanaged rollout can
isolate an entire cluster. Current primary-source guidance and a rollback plan reduce that systemic blast
radius.

### Example 34: CNI Decision

_ex-34 · exercises co-17_

Compare Cilium, Calico, and Flannel by policy, observability, datapath, operations, and support—not popularity.
Flannel's simple overlay model does not automatically provide every policy capability a design expects.

```sh
# => Prints evaluation dimensions only.
printf '%s\n' 'compare CNI policy enforcement, observability, datapath, operations, and support'
```

**Verification**: The criteria are requirements rather than product rankings.

**Key takeaway**: The selected CNI must enforce the security and operations model you claim.

**Why it matters**: Networking decisions become difficult to reverse after workloads depend on their semantics.
A written comparison exposes feature gaps early, particularly when a policy manifest would otherwise exist but
have no enforcing implementation.

### Example 35: Flannel VXLAN

_ex-35 · exercises co-17_

Flannel can use a VXLAN overlay to carry Pod traffic across nodes. The model adds encapsulation and MTU
considerations that must be tested in the actual underlay.

```sh
# => Prints an overlay reminder; it does not create a tunnel.
printf '%s\n' 'VXLAN overlays pod traffic; verify underlay MTU, routing, and failure behavior in the lab'
```

**Verification**: The statement calls for evidence instead of assuming all networks have suitable MTU.

**Key takeaway**: Overlay simplicity still depends on an intentional physical network.

**Why it matters**: MTU mismatch and underlay routing faults can appear as intermittent application failures.
Testing the complete path keeps network debugging at the correct layer and avoids treating the CNI as a magic
abstraction over unmanaged switches and routes.

### Example 36: NetworkPolicy Default Open

_ex-36 · exercises co-18_

Pods are generally non-isolated until a matching NetworkPolicy is enforced by the CNI. A policy object without
an enforcing CNI is documentation, not traffic control.

```sh
# => Records the baseline without opening or testing any connection.
printf '%s\n' 'default traffic openness changes only when an enforcing CNI applies matching NetworkPolicy'
```

**Verification**: The output connects policy intent with CNI enforcement.

**Key takeaway**: A NetworkPolicy must be selected and enforced to change traffic behavior.

**Why it matters**: Teams may commit a default-deny manifest and assume isolation exists. Verification against
the actual CNI prevents a false security boundary and ensures incident responders know whether connectivity is
blocked by intended policy or another network fault.

### Example 37: Deny Ingress by Default

_ex-37 · exercises co-18_

A default-deny ingress policy selects all Pods in one namespace. The following documentation object is safe to
render locally and uses no application or environment identity.

```yaml
# => Selects all Pods in the chosen namespace when applied by an enforcing CNI.
spec:
  # => An empty selector means every Pod in that policy namespace.
  podSelector: {}
  # => The policy type closes ingress until an allow rule is added.
  policyTypes: [Ingress]
```

**Verification**: The object is intentionally incomplete until its namespace and CNI enforcement are reviewed.

**Key takeaway**: Default deny makes every allowed flow an explicit decision.

**Why it matters**: Explicit ingress policy limits lateral movement and exposes application dependencies. It
also creates migration work: every required caller must be modeled and tested, otherwise a correct security
control can become an unexpected availability failure.

### Example 38: Allow Frontend to Database

_ex-38 · exercises co-18_

An allow rule should name both source labels and destination port. This model permits a frontend role to reach
a database role without embedding a real namespace, IP, or credential.

```yaml
# => Describes an allowed caller identity rather than an address range.
from:
  # => The selector matches a reviewed frontend label contract.
  - podSelector: { matchLabels: { role: frontend } }
```

**Verification**: The source is label-based, so label governance becomes part of policy correctness.

**Key takeaway**: Least-privilege policy is an explicit, testable flow contract.

**Why it matters**: Label typos can deny legitimate traffic, while broad selectors can reopen the whole
namespace. Testing allowed and denied flows after policy changes makes security intent observable instead of
relying on a YAML review alone.

### Example 39: Plan a MetalLB Install

_ex-39 · exercises co-19_

MetalLB supplies `LoadBalancer` behavior on bare metal, but installation affects cluster and LAN ownership.
Review current controller requirements, reserved addresses, advertisement mode, router owner, and rollback.

```sh
# => Prints an install gate; it does not install a chart or announce an address.
printf '%s\n' 'review MetalLB compatibility, reserved addresses, mode, network owner, health, and rollback'
```

**Verification**: The plan requires LAN coordination before creating a Service.

**Key takeaway**: A bare-metal load balancer is a network integration, not only a Kubernetes add-on.

**Why it matters**: Advertising an unreserved address can collide with another host and create a network-wide
incident. Explicit pool ownership and routing review let the platform provide external services without
silently claiming addresses the cluster is not authorized to use.

### Example 40: MetalLB Address Pool

_ex-40 · exercises co-19_

An `IPAddressPool` declares addresses explicitly reserved for MetalLB. Documentation ranges must never be
copied into a real LAN without the network owner's approval and conflict check.

```yaml
# => Names a documentation-only pool; do not apply it to a real network.
spec:
  # => TEST-NET address space illustrates shape, not a usable LAN allocation.
  addresses: [192.0.2.10-192.0.2.20]
```

**Verification**: The range is documentation-only and has no real environment identity.

**Key takeaway**: Load-balancer addresses are an owned, finite network resource.

**Why it matters**: A pool is a contract between cluster and network operators. Reserving and documenting it
prevents address collisions, enables incident diagnosis, and makes clear which exposure paths should be
monitored, protected, and withdrawn during maintenance.

### Example 41: LoadBalancer Assignment

_ex-41 · exercises co-19_

A `LoadBalancer` Service requests an address from an installed, configured controller. A Service spec alone
does not guarantee that an address will be assigned or become reachable.

```yaml
# => Declares the requested service type without selecting a real workload.
spec:
  # => MetalLB may satisfy this only after its platform prerequisites are met.
  type: LoadBalancer
```

**Verification**: The object expresses intent; controller and network status supply evidence.

**Key takeaway**: `LoadBalancer` is a request whose fulfillment depends on platform integration.

**Why it matters**: Cloud experience can hide the controller and network dependencies behind a provider API.
On bare metal, observing assignment, advertisement, and client reachability separately prevents a YAML object
from being mistaken for an externally working service.

### Example 42: Layer 2 Advertisement

_ex-42 · exercises co-20_

MetalLB Layer 2 mode advertises service addresses through local address discovery, with one node owning an
address at a time. Its failover and network behavior belong in the owner-approved lab test plan.

```sh
# => Prints the Layer 2 model without sending ARP or NDP traffic.
printf '%s\n' 'Layer 2 mode advertises a service address locally; one node owns it at a time'
```

**Verification**: The model distinguishes address ownership from multi-node active forwarding.

**Key takeaway**: Layer 2 mode is simple but has a single active address owner.

**Why it matters**: The mode can fit a controlled LAN while still requiring failure testing and switch-aware
operations. Stating ownership semantics prevents teams from promising load distribution or router behavior that
Layer 2 advertisement does not provide.

### Example 43: Layer 2 and BGP

_ex-43 · exercises co-20_

Layer 2 uses local ARP/NDP advertisement; BGP peers with routers controlled by the network owner. Choose the
mode by topology, approval, operational competence, and desired failure behavior.

```sh
# => Prints a comparison; it does not configure a peer or router.
printf '%s\n' 'Layer 2: local discovery and one owner; BGP: reviewed router peering and route advertisement'
```

**Verification**: The alternatives have distinct prerequisites and no universal winner.

**Key takeaway**: Advertisement mode is a joint cluster-and-network design choice.

**Why it matters**: BGP can offer routing behavior that Layer 2 cannot, but it expands the change boundary to
routers and peer policy. An explicit comparison keeps operators from deploying a network protocol they cannot
observe, recover, or obtain approval to run.

### Example 44: BGP Peering Plan

_ex-44 · exercises co-20_

BGP peering needs a router owner, peer identity, allowed prefixes, authentication handling, monitoring, and
withdrawal/rollback procedure. Never publish a tutorial peer address, autonomous-system number, or secret.

```sh
# => Prints BGP change controls; it does not open a routing session.
printf '%s\n' 'record peer owner, prefixes, authentication, monitoring, route withdrawal, and rollback'
```

**Verification**: The plan has operational ownership and route-withdrawal evidence.

**Key takeaway**: BGP is a coordinated routing change, not a cluster-local toggle.

**Why it matters**: Incorrect advertised routes can affect traffic far beyond one application. Review with the
network owner and rehearse withdrawal so a failed service, node, or controller does not leave stale or
unintended reachability in the surrounding network.

### Example 45: Plan a Longhorn Install

_ex-45 · exercises co-21_

Longhorn supplies distributed block storage and needs compatible nodes, disks, replication settings, and an
operating owner. Recheck current prerequisites from Longhorn documentation before installing it in any lab.

```sh
# => Prints a storage gate; it does not touch a disk or fetch a chart.
printf '%s\n' 'review Longhorn node, disk, replica, failure-domain, backup, monitoring, and rollback requirements'
```

**Verification**: The plan treats storage as a data-safety system, not merely a PVC provider.

**Key takeaway**: Replicated storage needs explicit disks, failure domains, and recovery evidence.

**Why it matters**: Storage configuration determines both availability and data-loss behavior. A convenient
install that ignores disks, replicas, and backup ownership can present a bound PVC while failing the recovery
promise applications and operators believe it provides.

### Example 46: Longhorn Replication

_ex-46 · exercises co-21_

Replicated volume storage aims to retain data through a defined node failure when replicas span suitable
failure domains. Replica count alone cannot protect against shared rack, power, or disk-controller failure.

```sh
# => Prints a replication condition; no volume is created.
printf '%s\n' 'replicas protect only failures they do not share; map disks, nodes, racks, power, and backup'
```

**Verification**: The statement ties replication to the actual fault model.

**Key takeaway**: Replication is a topology promise, not a number in a values file.

**Why it matters**: Multiple replicas on one shared failure domain can disappear together. Mapping placement and
backup behavior gives teams a realistic recovery claim and prevents a storage dashboard's healthy status from
masking correlated infrastructure risk.

### Example 47: Local Path Provisioning

_ex-47 · exercises co-21_

Local-path provisioning creates node-local volumes and is useful for simple or disposable workloads. It does
not supply the node-independent durability that a replicated storage design claims.

```sh
# => Records the locality boundary without provisioning storage.
printf '%s\n' 'local-path volume follows one node; plan workload placement and recovery accordingly'
```

**Verification**: The output identifies locality as the decisive availability trade-off.

**Key takeaway**: Local storage is simple, but its data and scheduling are node-bound.

**Why it matters**: A workload may reschedule while its local data cannot follow it. Choosing local-path
deliberately for cache or low-criticality data avoids accidental dependence on node-local state where the
application's recovery objective requires replication or restore.

### Example 48: StorageClass and PVC

_ex-48 · exercises co-22_

A PVC requests storage through a named StorageClass. The resulting PV behavior depends on the selected
provisioner, access mode, capacity, topology, reclaim policy, and controller health.

```yaml
# => Requests a documentation-only class; this is not applied.
spec:
  # => The class name must exist and be approved in a real cluster.
  storageClassName: documented-storage-class
```

**Verification**: The object references a contract rather than promising a volume will bind.

**Key takeaway**: A PVC is a request; the storage class defines its fulfillment behavior.

**Why it matters**: Bound status is necessary but insufficient evidence for data safety. StorageClass semantics
affect placement, retention, and recovery, so application owners must understand the provisioner contract
before relying on persistent data across node maintenance or disaster recovery.

### Example 49: Storage Decision

_ex-49 · exercises co-22_

Compare replicated Longhorn-style storage with simple local-path storage by RPO, RTO, topology, performance,
operational budget, and workload data value. Do not use a storage backend as a substitute for backups.

```sh
# => Prints decision factors; it does not select a StorageClass.
printf '%s\n' 'compare durability, locality, failure domain, restore path, performance, and operations'
```

**Verification**: The factors include recovery and operational costs.

**Key takeaway**: Storage selection follows the data recovery promise.

**Why it matters**: Replication, snapshots, and backups solve different failure modes. A clear decision record
prevents teams from buying more storage complexity than they can operate or, worse, expecting local data to
survive failures it was never designed to tolerate.

### Example 50: Ingress Controller Choice

_ex-50 · exercises co-23_

Ingress objects require a controller such as Traefik, ingress-nginx, or Caddy-compatible implementation to
make routes real. Confirm current project licensing, support, and compatibility from primary sources.

```sh
# => Prints choice criteria; no controller is installed.
printf '%s\n' 'compare controller compatibility, routing needs, TLS integration, operations, and current license'
```

**Verification**: The plan separates an API object from the controller that serves it.

**Key takeaway**: Ingress intent needs an installed and operated data-plane controller.

**Why it matters**: A valid Ingress YAML can have no effect when no matching controller watches it. Selecting
and observing the controller makes external routing a testable platform capability rather than a quiet
assumption hidden behind an object definition.

### Example 51: Traefik Default

_ex-51 · exercises co-23_

k3s may bundle Traefik by default depending on current installation choices. Verify actual installed state
before relying on it, and disable or replace it only through a reviewed distribution-specific procedure.

```sh
# => Prints the verification question; no cluster is queried.
printf '%s\n' 'verify the installed ingress controller and class before assuming a bundled default exists'
```

**Verification**: The wording avoids a version-insensitive guarantee.

**Key takeaway**: Inspect the deployed platform; do not rely on remembered defaults.

**Why it matters**: Distribution options and releases can change bundled components. Checking live evidence
before defining routes prevents duplicate controllers, mismatched IngressClass names, and incident-time
confusion about which data plane owns traffic.

### Example 52: Ingress Manifest

_ex-52 · exercises co-23_

An Ingress maps host/path intent to a Service. Use a documentation host and validate object shape locally; a
real hostname, controller class, Service, and TLS policy belong in an approved environment overlay.

```yaml
# => Uses a reserved documentation hostname and cannot route public traffic.
spec:
  # => Route behavior is fulfilled only by the selected controller.
  rules: [{ host: app.example.invalid }]
```

**Verification**: The hostname is explicitly non-routable documentation data.

**Key takeaway**: Ingress defines routing intent; the controller and environment make it reachable.

**Why it matters**: Keeping real DNS outside generic examples prevents accidental exposure and makes
environment ownership clear. It also focuses verification on the complete path: controller readiness, service
endpoints, certificate state, DNS, and client health.

### Example 53: Plan a cert-manager Install

_ex-53 · exercises co-24_

cert-manager automates certificate resources but requires current compatible installation guidance, trusted
issuers, DNS/HTTP challenge ownership, secret access policy, monitoring, and renewal evidence.

```sh
# => Prints a platform gate; it does not install CRDs or contact a CA.
printf '%s\n' 'review cert-manager compatibility, issuer ownership, challenge path, secret policy, alerting'
```

**Verification**: The plan includes renewal and secret handling, not only installation.

**Key takeaway**: Certificate automation is a lifecycle and trust-boundary design.

**Why it matters**: TLS can fail at issuance, renewal, routing, or secret delivery. Explicit ownership of
challenge paths and monitoring turns cert-manager into a reliable platform control rather than a controller
whose failure is discovered only when a certificate expires.

### Example 54: ClusterIssuer Contract

_ex-54 · exercises co-24_

A ClusterIssuer represents issuer configuration and authority for certificate requests. Do not commit an ACME
account key, real email, DNS credential, or production issuer endpoint in a teaching artifact.

```yaml
# => Declares an issuer kind without credentials or a real service endpoint.
kind: ClusterIssuer
# => A real issuer's sensitive configuration belongs in an approved secret workflow.
metadata: { name: documented-issuer }
```

**Verification**: The contract has no external authority that could issue or revoke real certificates.

**Key takeaway**: Issuer configuration is security-sensitive infrastructure state.

**Why it matters**: Certificate issuers can affect every public route in a cluster. Separating sensitive issuer
inputs from Git protects account authority and allows a security review to examine who may request, renew, or
revoke certificates in each environment.

### Example 55: Certificate Resource

_ex-55 · exercises co-24_

A Certificate requests a named Secret that cert-manager manages after issuer approval. The Secret is sensitive
runtime state; inspect metadata and expiration evidence rather than printing private key material.

```yaml
# => Uses documentation names only; it cannot request a usable certificate.
spec:
  # => A controller would write certificate material only in an approved target cluster.
  secretName: documented-tls-secret
```

**Verification**: The resource contains no hostname, key, account, or live issuer reference.

**Key takeaway**: Certificate lifecycle ends in sensitive Secret delivery.

**Why it matters**: A certificate object is not proof of valid TLS until issuance, Secret creation, controller
reload, DNS, and client validation all succeed. Treating the secret as protected runtime data avoids turning
automation into accidental private-key distribution.

### Example 56: Ingress TLS Automation

_ex-56 · exercises co-24_

Ingress annotations can connect a route to a certificate issuer, but controller compatibility and challenge
reachability must be proven in the owner-approved environment. An annotation is neither a certificate nor DNS.

```yaml
# => Documents the integration point without naming an actual issuer.
metadata:
  # => The value is a placeholder and must not be applied as production configuration.
  annotations: { cert-manager.io/cluster-issuer: documented-issuer }
```

**Verification**: The object is intentionally non-operating and exposes the controller integration point.

**Key takeaway**: TLS automation spans issuer, challenge route, controller, Secret, and client verification.

**Why it matters**: One field can hide several dependencies that fail independently. Testing the complete
issuance and renewal path avoids false confidence from a rendered Ingress and gives responders clear evidence
when a route, issuer, or secret lifecycle breaks.

### Example 57: ACME HTTP-01 Flow

_ex-57 · exercises co-24_

HTTP-01 validation proves a domain challenge through reachable HTTP routing. It requires domain and ingress
ownership; it must never be tested against a domain a learner does not control.

```sh
# => Prints the trust flow; it does not expose a challenge route.
printf '%s\n' 'issuer requests challenge → controller serves proof → CA validates domain → certificate Secret'
```

**Verification**: The flow identifies external reachability and domain ownership as prerequisites.

**Key takeaway**: ACME validation is an externally visible authorization flow.

**Why it matters**: Misconfigured challenge routing can block issuance or accidentally expose an unintended
route. Requiring owner-controlled DNS and HTTP paths keeps the test ethical and lets the platform team monitor
the exact boundary that certificate automation depends on.
