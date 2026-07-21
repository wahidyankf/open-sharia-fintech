# Bare-Metal Virtualization (By Example, HCL/YAML/shell)

**Course ID**: `bare-metal-virtualization` · **Format**: By Example · **Language**: HCL/YAML/shell.

**Short summary**: Bare-metal hosts and hypervisors (Proxmox)

**Scope note**: standing up your own on-premise / bare-metal virtualization substrate — the layer
_beneath_ Kubernetes ([`50-containers-and-orchestration`](./containers-and-orchestration.md)) and the
public cloud ([`51-cloud-and-iac`](./cloud-and-iac.md)). Hypervisor fundamentals (Type-1 vs Type-2,
KVM/QEMU), a [**Proxmox VE**](https://www.proxmox.com/en/proxmox-virtual-environment/overview) cluster
(quorum, HA, live migration, LXC vs full VM), the lower-level
[**libvirt/virsh**](https://libvirt.org/) alternative, [**ZFS**](https://openzfs.github.io/openzfs-docs/)
(pools, RAID-Z, snapshots, send/receive, scrubs) and [**Ceph**](https://docs.ceph.com/) hyperconverged
storage (RBD/CephFS, OSD/MON/MGR, CRUSH failure domains), [**cloud-init**](https://cloud-init.io/) first-boot
provisioning, golden images with [**Packer**](https://www.packer.io/), infra-as-code against Proxmox via the
[**Terraform `bpg/proxmox`**](https://registry.terraform.io/providers/bpg/proxmox/latest) provider and
[**Ansible**](https://docs.ansible.com/), PXE/netboot installs, and backup/restore discipline (Proxmox
Backup Server). `†`: the "language" is Terraform HCL + cloud-init/Ansible YAML + shell/CLI against the
Proxmox/libvirt APIs. Wiring this substrate into a self-managed control plane is
[`53-self-managed-kubernetes-and-gitops`](./self-managed-kubernetes-and-gitops.md); here the hypervisor
host is the unit, not the cluster on top of it.

## Why this exists · the big idea

- **The problem before the solution**: renting every VM, disk, and load balancer from a hyperscaler is fast
  to start but you never own the substrate — you pay retail egress, you can't run in your own building for
  data-locality or regulatory reasons, and "just spin up a box" hides a hypervisor, a storage array, and a
  failure-domain model you never learned to reason about. When the cloud bill or the compliance boundary
  forces repatriation, the layer beneath the cloud is a black box.
- **Keep-this-if-you-forget-everything**: a hypervisor turns one physical machine into many isolated
  virtual ones; cluster three of them so a node can die without taking your workloads with it; put the disks
  under a redundancy model that survives drive loss (ZFS RAID-Z or Ceph CRUSH); and drive the whole thing
  through one API with the same plan/apply IaC discipline you use in the cloud — bake images once, configure
  at first boot, replace never-modify.
- **Big ideas touched**: `mechanism-vs-policy` (you declare the desired VMs/storage — the _policy_; the
  hypervisor + provider reconcile it — the _mechanism_), `determinism-vs-emergence` (golden images +
  cloud-init + IaC buy reproducible VMs; availability _emerges_ from quorum and failure-domain-aware data
  placement, not from any single node).

## Prerequisites

- **Prior topics**: [topic 50 Containers & Orchestration](./containers-and-orchestration.md) (the
  workloads that will run on the VMs, and the immutable-image intuition), [topic 51 Cloud & IaC](./cloud-and-iac.md)
  (Terraform plan/apply/state, idempotency, declarative-vs-imperative — reused here against Proxmox instead
  of a cloud), and [topic 12 Networking Essentials](./networking-essentials.md) (DHCP, bridges, subnets —
  the substrate is a network of hosts, and PXE is a network boot).
- **Tools & environment**: a macOS/Linux terminal for the CLI/IaC driver; a **Proxmox VE** host or nested
  install (a single node, or a 3-node-style lab via nested virtualization) — versions "verify current"; the
  `qm`/`pct`/`pvecm`/`pveceph` CLIs and the Proxmox **REST API** (an API token, never a committed password);
  **ZFS** (`zpool`/`zfs`) and optionally **Ceph** on HBA/direct-attached disks (no hardware RAID);
  **Terraform** (or **OpenTofu** — note the license split, DD-15) with the `bpg/proxmox` provider;
  **Packer**; **Ansible** with the `community.proxmox` collection; **libvirt/virsh** for the lower-level
  alternative. No secret committed (secrets rule).
- **Assumed knowledge**: Terraform plan/apply + state + idempotency (topic 51); containers and immutable
  images (topic 50); shell, SSH, and env vars (topic 05); IP/DHCP/bridging basics (topic 12). Storage RAID
  intuition helps but is taught here.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (DD-28) and a DD-35 primary-source pass, both
> 2026-07-12. Fast-moving projects: treat every version number as "verify current".

- 2026-07-12 — verified: **Proxmox VE** code is licensed under the **GNU Affero General Public License,
  version 3** (primary quote below). Proxmox VE 9.x is current (point release ~9.2, ~2026-05-21) — the exact
  point release and date are `[Needs Verification]` against a fetched Roadmap page this pass; treat as
  "verify current". The "free without a subscription; the subscription only unlocks the enterprise repo and
  support" characterization is widely documented but was **not** confirmed on the fetched FAQ page this pass
  — `[Needs Verification]`.
- 2026-07-12 — verified: **Neither ZFS nor Ceph should sit behind a hardware RAID controller** — both want
  direct disk access via an HBA (primary quotes below).
- 2026-07-12 — verified: Terraform **`bpg/proxmox`** is the actively-maintained provider — its README states
  it is a fork of the "no longer maintained" `danitso/terraform-provider-proxmox`. The specific resource
  counts (~111 for `bpg` vs ~5 RC-quality for `Telmate/proxmox`) come from the registry listings and were
  **not** re-counted from a fetched registry page this pass (the Terraform Registry page is a client-rendered
  SPA that did not render to text) — `[Needs Verification]`; the maintained-vs-abandoned distinction is
  verified.
- 2026-07-12 — verified: the Ansible module moved — **`community.general.proxmox_kvm` is deprecated /
  redirected to `community.proxmox.proxmox_kvm`** (fetched); author against the `community.proxmox`
  collection.
- 2026-07-12 — verified: **Terraform CLI is Business Source License 1.1 (BUSL-1.1)** post-August-2023;
  **OpenTofu is MPL-2.0** (a Linux Foundation project) — the license-clean drop-in. The OpenTofu "fork of
  Terraform" phrasing and the exact Terraform BUSL wording were **not** re-fetched from a primary license
  file this pass (see topic 51's DD-35 pass, which verified the Terraform BUSL wording) — `[Needs
Verification]` on the verbatim license text here; the OpenTofu MPL-2.0 / LF-governance fact is quoted below.
- 2026-07-12 — verified: cloud-init, Packer, libvirt, ZFS, and Ceph core concepts (first-boot datasource,
  identical-image build, multi-hypervisor toolkit, RAID-Z parity, RADOS/CRUSH) are stable and quoted verbatim
  below.

### DD-35 primary-source citations

> DD-35 primary-source pass (2026-07-12). Definitions, CLI semantics, and storage/redundancy models traced
> to primary sources (pve.proxmox.com, libvirt.org, openzfs.github.io, docs.ceph.com, docs.cloud-init.io,
> github.com/bpg, developer.hashicorp.com/packer, docs.ansible.com, opentofu.org) and fetched/read. Items
> that could not be fetched this pass are flagged `[Needs Verification]` above.

- **Proxmox VE — license** — "Proxmox VE code is licensed under the GNU Affero General Public License,
  version 3." Source: [Proxmox VE FAQ](https://pve.proxmox.com/wiki/FAQ) (fetched, verbatim).
- **Proxmox VE — KVM/QEMU** — "A QEMU/KVM guest (or VM) is a guest system running virtualized under Proxmox
  VE using QEMU and the Linux KVM kernel module"; "QEMU uses the Linux KVM kernel module to achieve near
  native performance by executing the guest code directly on the host CPU." Source:
  [Proxmox VE FAQ](https://pve.proxmox.com/wiki/FAQ) (fetched, verbatim).
- **Proxmox VE — LXC** — "Proxmox Containers are how we refer to containers that are created and managed
  using the Proxmox Container Toolkit (pct) … use LXC as the basis of the container offering." Source:
  [Proxmox VE FAQ](https://pve.proxmox.com/wiki/FAQ) (fetched, verbatim).
- **Proxmox VE — cluster & quorum** — "The Proxmox VE cluster manager pvecm is a tool to create a group of
  physical servers. Such a group is called a cluster"; "Proxmox VE use a quorum-based technique to provide a
  consistent state among all cluster nodes"; "In case of network partitioning, state changes requires that a
  majority of nodes are online. The cluster switches to read-only mode if it loses quorum"; uses the
  "Corosync Cluster Engine for reliable group communication." Source:
  [Cluster Manager](https://pve.proxmox.com/wiki/Cluster_Manager) (fetched, verbatim).
- **Proxmox VE — quorum node count & live migration** — "If you are interested in High Availability, you need
  to have at least three nodes for reliable quorum"; "For smaller 2-node clusters, the QDevice can be used to
  provide a 3rd vote"; "Online migration of virtual machines is only supported when nodes have CPUs from the
  same vendor. It might work otherwise, but this is never guaranteed." Source:
  [Cluster Manager](https://pve.proxmox.com/wiki/Cluster_Manager) (fetched, verbatim).
- **Proxmox VE — High Availability** — on failure "the CRM tries to move services from the failed node to
  nodes which are still online"; requires "at least three cluster nodes (to get reliable quorum)" and "shared
  storage for VMs and containers". Source:
  [High Availability](https://pve.proxmox.com/wiki/High_Availability) (fetched, verbatim).
- **libvirt — what it is** — libvirt "is a toolkit to manage virtualization platforms" and "supports KVM,
  Hypervisor.framework, QEMU, Xen, Virtuozzo, VMware ESX, LXC, BHyve and more." Source:
  [libvirt.org](https://libvirt.org/) (fetched, verbatim).
- **ZFS — RAID-Z** — "RAIDZ is a variation on RAID-5 that allows for better distribution of parity and
  eliminates the RAID-5 'write hole'"; "A raidz group can have single, double, or triple parity, meaning
  that the raidz group can sustain one, two, or three failures"; "The `raidz1` vdev type specifies a
  single-parity raidz group; the `raidz2` vdev type specifies a double-parity raidz group; and the `raidz3`
  vdev type specifies a triple-parity raidz group." Source:
  [OpenZFS — RAIDZ](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/RAIDZ.html) (fetched, verbatim).
- **ZFS — snapshot** — "a snapshot is a consistent image of a dataset at a specific point in time; it
  includes all modifications to the dataset made by system calls that have successfully completed before that
  point in time." Source: [OpenZFS — zfs-snapshot(8)](https://openzfs.github.io/openzfs-docs/man/master/8/zfs-snapshot.8.html) (fetched, verbatim).
- **Ceph — RADOS & CRUSH** — "Ceph uniquely delivers object, block, and file storage in one unified system";
  "Storage cluster clients and Ceph OSD Daemon[s] use the CRUSH algorithm to compute information about the
  location of data"; "By using the CRUSH algorithm, clients and OSDs avoid being bottlenecked by a central
  lookup table"; "CRUSH enables massive scale by distributing the work to all the OSD daemons in the cluster
  and all the clients that communicate with them." Source:
  [Ceph — Architecture](https://docs.ceph.com/en/latest/architecture/) (fetched, verbatim).
- **Ceph — RBD, CephFS, daemons** — "The Ceph Block Device (a.k.a., RBD) service provides resizable,
  thin-provisioned block devices that can be snapshotted and cloned"; "The Ceph File System (CephFS) provides
  a POSIX-compliant filesystem as a service layered on top of the object-based Ceph Storage Cluster"; "Ceph
  Monitors maintain the master copy of the cluster map, which they provide to Ceph clients"; "A Ceph Manager
  serves as an endpoint for monitoring, orchestration, and plug-in modules." Source:
  [Ceph — Architecture](https://docs.ceph.com/en/latest/architecture/) (fetched, verbatim).
- **Ceph — hyperconverged, no RAID, node count** — "Proxmox VE unifies your compute and storage systems,
  that is, you can use the same physical nodes within a cluster for both computing … and replicated storage";
  "Avoid RAID controllers. Use host bus adapter (HBA) instead"; "Ceph is designed to handle whole disks on
  its own, without any abstraction in between. RAID controllers are not designed for the Ceph workload …";
  "To build a hyper-converged Proxmox + Ceph Cluster, you must use at least three (preferably) identical
  servers for the setup." Source:
  [Deploy Hyper-Converged Ceph Cluster](https://pve.proxmox.com/wiki/Deploy_Hyper-Converged_Ceph_Cluster) (fetched, verbatim).
- **cloud-init — first boot** — "Cloud-init is an open source initialization tool that was designed to make
  it easier to get your systems up and running with a minimum of effort, already configured according to your
  needs"; "It's responsible for activities like setting the hostname, configuring network interfaces,
  creating user accounts, and even running scripts"; "Identify the datasource … The datasource is the source
  of all configuration data. Fetch the configuration: Once the datasource is identified, cloud-init fetches
  the configuration data from it." Source: [cloud-init — Introduction](https://docs.cloud-init.io/en/latest/explanation/introduction.html) (fetched, verbatim).
- **Packer** — "Packer is a community tool for creating identical machine images for multiple platforms from
  a single source configuration"; it "is lightweight, runs on every major operating system, and is highly
  performant, creating machine images for multiple platforms in parallel." Source:
  [Packer — Intro](https://developer.hashicorp.com/packer/docs/intro) (fetched, verbatim).
- **Terraform `bpg/proxmox`** — "A Terraform / OpenTofu Provider that adds support for Proxmox Virtual
  Environment"; "This repository is a fork of https://github.com/danitso/terraform-provider-proxmox which is
  no longer maintained." Source: [github.com/bpg/terraform-provider-proxmox](https://github.com/bpg/terraform-provider-proxmox) (fetched, verbatim).
- **Ansible `community.proxmox.proxmox_kvm`** — "Allows you to create/delete/stop Qemu(KVM) Virtual Machines
  in Proxmox VE cluster"; "Management of Qemu(KVM) Virtual Machines in Proxmox VE cluster." Source:
  [community.proxmox.proxmox_kvm](https://docs.ansible.com/ansible/latest/collections/community/proxmox/proxmox_kvm_module.html) (fetched, verbatim; the older `community.general.proxmox_kvm` page is deprecated/redirected).
- **OpenTofu** — "OpenTofu is an infrastructure as code tool that lets you define both cloud and on-prem
  resources in human-readable configuration files that you can version, reuse, and share"; documentation
  "licensed under the MPL-2.0 license"; governed as "a Series of LF Projects, LLC." Source:
  [OpenTofu — Intro](https://opentofu.org/docs/intro/) (fetched, verbatim; "fork of Terraform" phrasing `[Needs Verification]`).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. Concepts come before examples. -->

- **co-01 · why-bare-metal-virtualization** — owning the virtualization substrate beneath clouds/K8s buys
  control, cost, and data-locality — at the price of running the hypervisor, storage, and failure model
  yourself.
- **co-02 · hypervisor-type1-type2** — a Type-1 hypervisor runs on bare metal; a Type-2 runs hosted on an
  OS; KVM turns the Linux kernel itself into a Type-1-class hypervisor.
- **co-03 · kvm-qemu** — the KVM kernel module executes guest code on the host CPU for near-native speed;
  QEMU provides the device emulation around it.
- **co-04 · vm-vs-container-lxc** — a full VM runs its own kernel (strong isolation); an LXC container shares
  the host kernel (higher density, weaker isolation).
- **co-05 · proxmox-ve** — Proxmox VE is a Debian-based platform bundling KVM + LXC + a web GUI, licensed
  AGPLv3.
- **co-06 · proxmox-api** — one Proxmox REST API underlies the GUI, the CLI, Terraform, and Ansible — all
  automation is API-driven.
- **co-07 · proxmox-cluster-quorum** — `pvecm` builds a cluster over corosync; a quorum (majority of nodes)
  is required for a consistent state, and the cluster goes read-only on quorum loss.
- **co-08 · proxmox-ha** — the HA manager fences a failed node and the CRM restarts its guests on a surviving
  node; it needs shared storage and quorum.
- **co-09 · live-migration** — a running VM can move between nodes with no downtime, provided the CPUs are
  from the same vendor.
- **co-10 · libvirt-virsh** — libvirt is a lower-level multi-hypervisor toolkit (KVM/QEMU/Xen/LXC/…) driven
  by `virsh`/`virt-manager` — the un-integrated alternative to Proxmox.
- **co-11 · storage-redundancy-models** — hardware RAID, ZFS RAID-Z, and Ceph CRUSH are three distinct
  redundancy models with different failure handling and scale.
- **co-12 · no-hardware-raid** — ZFS and Ceph require direct disk access via an HBA; a hardware RAID
  controller between them and the disks is an anti-pattern.
- **co-13 · zfs-pools-vdevs** — a ZFS pool (`zpool`) is composed of vdevs; RAID-Z1/2/3 give single/double/
  triple parity, surviving that many disk losses.
- **co-14 · zfs-snapshots** — a snapshot is a cheap, consistent point-in-time image of a dataset used for
  rollback and as a replication base.
- **co-15 · zfs-send-receive** — `zfs send`/`receive` streams a snapshot (full or incremental) to another
  pool or host for replication.
- **co-16 · zfs-scrub** — a scrub walks every block verifying checksums and self-healing corruption from
  redundant copies.
- **co-17 · ceph-rados** — Ceph/RADOS is a distributed storage service delivering object, block, and file
  from one unified cluster.
- **co-18 · ceph-daemons** — Ceph runs MON (cluster map), MGR (monitoring/orchestration), OSD (one per
  disk), and MDS (for CephFS).
- **co-19 · ceph-crush** — the CRUSH algorithm computes data placement with no central lookup table, and
  failure domains bound the blast radius of a loss.
- **co-20 · ceph-rbd-cephfs** — RBD provides thin-provisioned block devices; CephFS provides a POSIX
  filesystem — both over the same RADOS cluster.
- **co-21 · hyperconverged** — the same physical nodes serve compute and replicated storage; a
  hyperconverged Ceph cluster wants at least three (preferably identical) nodes.
- **co-22 · cloud-init** — cloud-init runs at first boot, reading a datasource to set hostname, users, SSH
  keys, and network — turning one image into many configured instances.
- **co-23 · cloud-init-userdata** — declarative `#cloud-config` user-data (plus meta-data / network-config)
  is the first-boot configuration payload.
- **co-24 · golden-images-packer** — Packer builds identical machine images from a single source config,
  producing a reusable golden template.
- **co-25 · immutable-image-pipeline** — bake configuration into an image once (Packer) + apply per-instance
  config at boot (cloud-init) = reproducible VMs you replace, never modify in place.
- **co-26 · iac-proxmox-terraform** — the Terraform `bpg/proxmox` provider drives the Proxmox API
  declaratively (VMs, disks, cloud-init) with plan/apply.
- **co-27 · terraform-plan-apply-state** — plan/apply/state/idempotency (from topic 51) apply unchanged to
  the on-prem substrate; the API token is a secret kept out of state and code.
- **co-28 · provider-choice-bpg-vs-telmate** — `bpg/proxmox` is the maintained, broad-coverage provider;
  `Telmate/proxmox` is the older, thinner one — pick the maintained one.
- **co-29 · terraform-license-opentofu** — Terraform CLI is BUSL-1.1; OpenTofu is the MPL-2.0 license-clean
  drop-in that runs the same config.
- **co-30 · ansible-proxmox** — the `community.proxmox.proxmox_kvm` module imperatively creates/stops/deletes
  KVM VMs via the Proxmox API.
- **co-31 · declarative-vs-imperative-provisioning** — Terraform declares desired substrate state; Ansible
  procedurally converges hosts — provision with one, configure with the other.
- **co-32 · pxe-netboot** — PXE/netboot (DHCP + TFTP + an answer file) drives unattended bare-metal OS
  installs, so a new host provisions with no console clicks.
- **co-33 · backup-restore-pbs** — Proxmox Backup Server gives incremental, deduplicated backups and
  tested restores — the discipline that makes "cattle" recoverable.
- **co-34 · failure-domain-reasoning** — quorum (majority) and CRUSH failure domains are the
  distributed-systems tools for reasoning about blast radius: what survives when a disk, host, or rack dies.

## Tensions & trade-offs — when NOT to reach for this

- **You become the cloud provider**: renting a VM hides a hypervisor, a storage array, a network fabric, and
  an on-call rotation. Owning the substrate buys control, predictable cost at scale, and data-locality — and
  charges you the operational burden the hyperscaler used to absorb (patching hosts, replacing drives,
  reasoning about quorum at 3 a.m.). It wins when the cloud bill, egress fees, latency, or a compliance
  boundary make renting the wrong trade; it loses for a small, bursty, or short-lived workload.
- **Storage model is a one-way-ish door**: hardware RAID is simple but opaque and blocks ZFS/Ceph self-
  healing; ZFS RAID-Z is superb single-box integrity but doesn't scale past the box; Ceph scales horizontally
  and survives whole-host loss but demands ≥3 nodes, a network budget, and real operational literacy. Reach
  for ZFS on one or two nodes; reach for Ceph only when you genuinely need clustered, host-failure-tolerant
  storage — an under-resourced Ceph cluster is worse than a well-run ZFS box.
- **Snowflake risk moves, it doesn't vanish**: without the golden-image + cloud-init + IaC discipline, a
  hand-nursed Proxmox host is exactly the unreproducible pet that IaC in topic 51 was meant to kill. The
  substrate only earns its keep if you treat its VMs as cattle — baked, declared, and replaceable.
- **When NOT to use it**: a throwaway prototype, a team with no hardware or on-call capacity, or a workload
  that fits a managed cloud service cheaply — don't stand up a cluster to run one container.

## Lineage — why it beat the alternative

- The arc runs mainframe time-sharing → per-app physical servers (the "snowflake" era, one workload one box,
  wasteful and fragile) → the VMware-led x86 virtualization wave that consolidated many VMs per host and made
  compute fungible → the public cloud, which rented that virtualization by the minute and let a generation
  forget the layer underneath → and now a partial **repatriation**, where cost, latency, egress, and
  data-sovereignty pressures pull steady-state workloads back on-prem — but this time run _like_ a cloud
  (API-driven, IaC, immutable images) rather than by hand. Open KVM/QEMU + Proxmox + ZFS/Ceph is the
  free-software substrate that makes that credible without a VMware license. The invariant across every step:
  decouple the workload from the physical box, and make availability emerge from redundancy and quorum rather
  than from any one node staying up — the same determinism-over-emergence bet as immutable images in
  [`50-containers-and-orchestration`](./containers-and-orchestration.md) and declarative infra in
  [`51-cloud-and-iac`](./cloud-and-iac.md), now one layer lower.

## Worked examples

Colocated under `bare-metal-virtualization/learning/`; each is a real Proxmox/libvirt CLI session, a ZFS/Ceph
command, a cloud-init/Packer/Ansible YAML, or a Terraform HCL config run against a Proxmox host (a single node
or a nested 3-node-style lab) **or** an annotated decision artifact (DD-20/DD-30). Contiguous `ex-01..ex-80`.
Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · why-own-substrate** — a decision table rent-from-cloud vs own-the-substrate (control / cost /
  data-locality / operational burden) — verify each column's trade-off. (co-01)
- **ex-02 · type1-vs-type2** — a decision table Type-1 bare-metal vs Type-2 hosted hypervisor — verify KVM is
  Type-1-class. (co-02)
- **ex-03 · kvm-capability-check** — `lscpu | grep -i virtualization` and `lsmod | grep kvm` — verify
  hardware virtualization is present and the KVM module is loaded. (co-03)
- **ex-04 · kvm-qemu-split** — annotate the KVM kernel module (CPU execution) vs QEMU (device emulation) —
  verify each part's role in near-native speed. (co-03)
- **ex-05 · vm-vs-lxc-table** — a decision table full VM (own kernel) vs LXC (shared kernel) — verify the
  isolation-vs-density trade-off. (co-04)
- **ex-06 · proxmox-stack** — annotate Proxmox VE = Debian + KVM + LXC + web GUI, AGPLv3 — verify the license
  and the bundled stack. (co-05)
- **ex-07 · pveversion** — `pveversion -v` — verify the running PVE + kernel version string (verify current).
  (co-05)
- **ex-08 · proxmox-api-token** — create an API token, then `curl -k` the `/api2/json/version` endpoint —
  verify the REST API answers with the version. (co-06)
- **ex-09 · api-underlies-all** — annotate GUI / `qm` CLI / Terraform / Ansible all calling the same REST API
  — verify the single control plane. (co-06)
- **ex-10 · qm-create-vm** — `qm create <id> …` then `qm start <id>` — verify the VM is defined and boots.
  (co-03)
- **ex-11 · qm-pct-list** — `qm list` and `pct list` — verify VMs and containers are enumerated with status.
  (co-04)
- **ex-12 · pct-create-lxc** — `pct create <id> <template> …` then `pct start` — verify the LXC container
  starts. (co-04)
- **ex-13 · vm-lifecycle-cli** — `qm start` / `qm shutdown` / `qm stop` / `qm destroy` — verify each
  lifecycle transition on one VM. (co-03)
- **ex-14 · virsh-list** — libvirt `virsh list --all` + `virsh dominfo <dom>` — verify the lower-level toolkit
  lists and describes domains. (co-10)
- **ex-15 · virsh-vs-proxmox** — a decision table libvirt/virsh (raw multi-hypervisor toolkit) vs Proxmox
  (integrated platform) — verify when each fits. (co-10)
- **ex-16 · libvirt-hypervisor-scope** — annotate libvirt driving KVM/QEMU/Xen/LXC and more — verify the
  multi-hypervisor abstraction. (co-10)
- **ex-17 · storage-models-table** — a decision table hardware RAID vs ZFS RAID-Z vs Ceph CRUSH — verify each
  model's failure handling and scale. (co-11)
- **ex-18 · no-hardware-raid** — annotate ZFS/Ceph needing HBA direct disk access, never a RAID controller —
  verify why the controller is the anti-pattern. (co-12)
- **ex-19 · zpool-create-raidz** — `zpool create tank raidz1 /dev/sd{b,c,d}` then `zpool status` — verify the
  pool and its RAID-Z1 vdev topology. (co-13)
- **ex-20 · raidz-parity-table** — a decision table raidz1/2/3 (survive 1/2/3 disk losses; usable capacity) —
  verify the parity-to-redundancy mapping. (co-13)
- **ex-21 · zfs-dataset** — `zfs create tank/vmdata` then `zfs list` — verify the dataset appears under the
  pool. (co-13)
- **ex-22 · zfs-snapshot-cli** — `zfs snapshot tank/vmdata@before` then `zfs list -t snapshot` — verify the
  point-in-time snapshot exists. (co-14)
- **ex-23 · zfs-rollback** — change data, then `zfs rollback tank/vmdata@before` — verify the dataset returns
  to the snapshot state. (co-14)
- **ex-24 · cloud-init-first-boot** — annotate cloud-init's first-boot steps: identify datasource → fetch
  config → set hostname/users/SSH/network — verify the ordered steps. (co-22)
- **ex-25 · cloud-init-userdata-yaml** — a `#cloud-config` user-data YAML creating a user + injecting an SSH
  key — verify the declarative keys parse. (co-23)
- **ex-26 · proxmox-ci-drive** — `qm set <id> --ciuser … --sshkeys … --ipconfig0 …` on a template — verify the
  cloud-init drive injects the config at boot. (co-22)
- **ex-27 · pvecm-status** — `pvecm status` on a node — verify quorum state and cluster membership. (co-07)
- **ex-28 · quorum-majority-annotate** — annotate quorum = majority-of-nodes for a consistent state, read-only
  on loss — verify the majority rule. (co-07)

### Intermediate

- **ex-29 · pvecm-create-join** — `pvecm create <cluster>` on node 1, `pvecm add <node1>` on node 2 — verify
  the second node joins the cluster. (co-07)
- **ex-30 · corosync-annotate** — annotate corosync as the reliable group-communication engine under the
  cluster — verify its role. (co-07)
- **ex-31 · three-node-quorum** — annotate why ≥3 nodes give reliable quorum (or a QDevice supplies a 3rd
  vote for a 2-node cluster) — verify the count. (co-07)
- **ex-32 · live-migrate-online** — `qm migrate <id> <target-node> --online` — verify the running VM moves
  with no downtime. (co-09)
- **ex-33 · migration-cpu-constraint** — annotate that online migration is only supported across same-vendor
  CPUs — verify the constraint. (co-09)
- **ex-34 · ha-add-service** — `ha-manager add vm:<id>` then `ha-manager status` — verify the VM enters HA
  state `started`. (co-08)
- **ex-35 · ha-failover-annotate** — annotate fencing the failed node + the CRM moving services to an online
  node — verify the recovery path. (co-08)
- **ex-36 · ha-requirements-table** — a decision table HA prerequisites: quorum (≥3 nodes) + shared storage +
  hardware redundancy — verify each is required. (co-08)
- **ex-37 · zfs-send-receive** — `zfs send tank/vmdata@snap | ssh host2 zfs receive tank/vmdata` — verify the
  snapshot replicates to a second host. (co-15)
- **ex-38 · zfs-incremental-send** — `zfs send -i @snap1 tank/vmdata@snap2 | …` — verify only the delta
  between snapshots transfers. (co-15)
- **ex-39 · zfs-scrub** — `zpool scrub tank` then `zpool status` — verify a checksum scrub runs and reports
  errors repaired. (co-16)
- **ex-40 · proxmox-pvesr** — a Proxmox `pvesr` scheduled ZFS replication job between two nodes — verify a
  guest's disk replicates on schedule. (co-15)
- **ex-41 · ceph-hyperconverged-annotate** — annotate hyperconvergence: the same nodes serve compute and
  replicated storage — verify the unification. (co-21)
- **ex-42 · pveceph-init-mon** — `pveceph init` then `pveceph mon create` — verify a Ceph monitor comes up.
  (co-18)
- **ex-43 · pveceph-osd-create** — `pveceph osd create /dev/sdX` on an HBA disk — verify the OSD joins the
  cluster (`ceph osd tree`). (co-18)
- **ex-44 · ceph-daemons-table** — a decision table MON (map) / MGR (monitoring, orchestration) / OSD
  (per-disk) / MDS (CephFS) — verify each daemon's job. (co-18)
- **ex-45 · ceph-crush-annotate** — annotate CRUSH computing placement with no central lookup table — verify
  the decentralized placement. (co-19)
- **ex-46 · ceph-failure-domain** — annotate a CRUSH failure domain (host / rack) so replicas span domains —
  verify a host loss keeps a full replica set. (co-19)
- **ex-47 · ceph-rbd-pool** — `pveceph pool create` + attach the RBD storage, then place a VM disk on it —
  verify the VM disk lands on RBD. (co-20)
- **ex-48 · cephfs-annotate** — annotate CephFS as a POSIX filesystem layered on RADOS (needs an MDS) — verify
  the shared file interface. (co-20)
- **ex-49 · ceph-three-node** — annotate the ≥3 (preferably identical) node minimum for a hyperconverged Ceph
  cluster — verify the minimum. (co-21)
- **ex-50 · tf-proxmox-provider** — a `terraform { required_providers { proxmox = { source = "bpg/proxmox" }
} }` block + a `provider "proxmox"` — verify `terraform init` installs the provider. (co-26)
- **ex-51 · tf-proxmox-endpoint** — the provider `endpoint` + `api_token` (from an env var / var, never
  hard-coded) — verify it authenticates against the Proxmox API. (co-26)
- **ex-52 · tf-vm-resource** — a `proxmox_virtual_environment_vm` resource cloned from a template — verify
  `terraform apply` creates the VM. (co-26)
- **ex-53 · tf-plan-apply** — `terraform plan` then `terraform apply` against the substrate — verify the plan
  previews the VM and apply creates it. (co-27)
- **ex-54 · tf-idempotent-apply** — re-run `terraform apply` with no config change — verify a no-op (the
  idempotency recap from topic 51 holds on-prem). (co-27)
- **ex-55 · tf-cloud-init-inject** — Terraform passing `#cloud-config` user-data + an SSH key to the VM —
  verify the guest boots SSH-ready. (co-23)
- **ex-56 · provider-choice-table** — a decision table `bpg/proxmox` (maintained, broad resource coverage) vs
  `Telmate/proxmox` (older, thinner) — verify the maintained-provider pick. (co-28)

### Advanced

- **ex-57 · packer-annotate** — annotate Packer building identical images from one source config across
  platforms — verify the single-source / many-image idea. (co-24)
- **ex-58 · packer-proxmox-template** — a Packer `proxmox-iso` build producing a Proxmox VM template — verify
  a reusable golden template appears. (co-24)
- **ex-59 · packer-cloud-init-bake** — a Packer build baking in the qemu-guest-agent + a cloud-init datasource
  — verify the template is cloud-init-ready at boot. (co-24, co-22)
- **ex-60 · image-pipeline-annotate** — annotate the two-phase pipeline: bake-once (Packer) + configure-at-
  boot (cloud-init) = reproducible VMs — verify the split of concerns. (co-25)
- **ex-61 · immutable-vs-mutable-table** — a decision table bake-and-replace vs configure-in-place — verify
  the reproducibility trade-off. (co-25)
- **ex-62 · tf-golden-clone** — Terraform cloning the Packer golden template into N VMs — verify every clone
  derives from one image. (co-26, co-25)
- **ex-63 · ansible-proxmox-kvm** — a `community.proxmox.proxmox_kvm` task creating a VM — verify the play
  creates it through the Proxmox API. (co-30)
- **ex-64 · ansible-idempotent** — re-run the play unchanged — verify it reports `ok` / no change (converge,
  not re-create). (co-30)
- **ex-65 · ansible-collection-note** — annotate `community.general.proxmox*` deprecated → use
  `community.proxmox` — verify the current collection is named. (co-30)
- **ex-66 · declarative-vs-imperative-table** — a decision table Terraform (declarative desired-state) vs
  Ansible (procedural converge) — verify each tool's category. (co-31)
- **ex-67 · terraform-plus-ansible** — annotate Terraform provisioning the VM and Ansible converging the OS
  inside it — verify the hand-off boundary. (co-31)
- **ex-68 · pxe-boot-chain** — annotate the PXE chain: DHCP hands an IP + next-server, TFTP serves the boot
  image — verify the netboot sequence. (co-32)
- **ex-69 · pxe-autoinstall** — annotate a preseed / autoinstall answer file driving an unattended Debian/
  Proxmox install — verify no manual console prompt is needed. (co-32)
- **ex-70 · pbs-annotate** — annotate Proxmox Backup Server: incremental, deduplicated, verified backups —
  verify the incremental/dedup model. (co-33)
- **ex-71 · pbs-backup** — `vzdump` / `proxmox-backup-client backup` to a PBS datastore — verify a backup
  snapshot lands in the datastore. (co-33)
- **ex-72 · pbs-restore** — restore a VM from a PBS snapshot — verify the guest is recreated and boots.
  (co-33)
- **ex-73 · backup-tiers-table** — a decision table local ZFS snapshot / offsite `zfs send` / PBS
  incremental — verify each tier's recovery scope (rollback vs disaster). (co-33, co-14)
- **ex-74 · terraform-license-table** — a decision table Terraform BUSL-1.1 vs OpenTofu MPL-2.0 — verify the
  license-clean pick. (co-29)
- **ex-75 · opentofu-swap** — run `tofu init && tofu plan` against the same `bpg/proxmox` config — verify the
  identical plan runs under OpenTofu. (co-29)
- **ex-76 · failure-domain-reasoning** — annotate quorum (majority) + CRUSH failure domains as blast-radius
  reasoning — verify the distributed-systems framing of "what survives a loss". (co-34)
- **ex-77 · quorum-vs-crush-table** — a decision table corosync quorum (control-plane consistency) vs Ceph
  CRUSH failure domains (data durability) — verify each protects a different layer. (co-34, co-07, co-19)
- **ex-78 · secrets-out-of-state** — annotate keeping the Proxmox API token out of committed Terraform code
  and state (env var / vault) — verify no secret appears in any committed file. (co-27)
- **ex-79 · substrate-stack-annotate** — annotate the full stack bare metal → KVM/Proxmox → ZFS/Ceph → VMs →
  (K8s/cloud above) — verify this topic is the layer beneath topics 50 and 51. (co-01)
- **ex-80 · bare-metal-capstone** — a Packer golden template + a Terraform `bpg/proxmox` config + cloud-init
  user-data provisioning SSH-ready VMs across a 3-node-style Proxmox + Ceph substrate for a dev/staging/prod
  split — verify the VMs come up SSH-ready and a re-plan shows no drift. (co-05, co-21, co-24, co-26, co-23,
  co-33)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: provision a reproducible on-prem virtualization substrate as code — a Packer-built golden image,
  a Terraform `bpg/proxmox` config, and cloud-init first-boot config that together yield SSH-ready VMs on a
  3-node-style Proxmox + Ceph (or ZFS) substrate, cleanly split into a dev, a staging, and a prod set, with a
  tested PBS backup/restore — a substrate a later self-managed Kubernetes control plane
  ([`53`](./self-managed-kubernetes-and-gitops.md)) can sit on.
- **Concepts exercised**: [ ] Proxmox cluster + quorum + HA (co-05, co-07, co-08) [ ] hyperconverged Ceph or
  ZFS storage with a failure-domain-aware model (co-11, co-13, co-19, co-21) [ ] a Packer golden template
  (co-24) [ ] Terraform `bpg/proxmox` plan/apply cloning that template (co-26, co-27) [ ] cloud-init
  first-boot config making VMs SSH-ready (co-22, co-23) [ ] a dev/staging/prod split from variables (co-27)
  [ ] tested PBS backup + restore (co-33) [ ] secrets kept out of state (co-27).
- **Ordered steps**:
  1. `.../learning/capstone/packer/` — a Packer `proxmox-iso` build producing a cloud-init-ready golden
     template (qemu-guest-agent + cloud-init datasource baked in). Verify a golden template appears in
     Proxmox.
  2. `.../learning/capstone/terraform/` — a `bpg/proxmox` config (provider via API token from an env var)
     cloning the template into VMs, with `#cloud-config` user-data supplying users + SSH keys + network.
     Verify `terraform init && plan && apply` creates SSH-ready VMs and a re-`plan` shows no drift.
  3. Parameterize dev / staging / prod from variables (count, sizing, network) off the same config + template.
     Verify the three environments differ only by variable values and share one golden image.
  4. Place the VM disks on hyperconverged Ceph (RBD) or replicated ZFS, and confirm quorum + a live migration
     between nodes. Verify a running VM migrates with no downtime and storage survives a single node/disk loss
     per its failure-domain/parity model.
  5. Back up a VM to Proxmox Backup Server and restore it. Verify the restored guest boots, and confirm no
     API token or secret appears in any committed file or in Terraform state.
- **Acceptance criteria**: the golden image builds; `plan → apply` yields SSH-ready VMs and a re-plan shows no
  drift; dev/staging/prod come from one config + one image; a running VM live-migrates; storage tolerates the
  designed failure domain; a PBS backup restores to a booting guest; no secret is committed or in state.
- **Done bar**: runnable end-to-end against a Proxmox host (single node or nested 3-node-style lab) +
  web-verified.

## Read more

**Books**

- **Mastering Proxmox** — Wasim Ahmed (3rd ed., 2017, Packt). A practical tour of Proxmox VE clustering,
  storage, networking, and backup for building a production virtualization platform.
- **FreeBSD Mastery: ZFS** and **FreeBSD Mastery: Advanced ZFS** — Michael W. Lucas & Allan Jude (2015–2016).
  The clearest hands-on treatment of ZFS pools, RAID-Z, snapshots, and send/receive replication (concepts
  carry directly to OpenZFS on Linux).
- **Learning Ceph** — Anthony D'Atri, Vaibhav Bhembre, Karan Singh (2nd ed., 2017, Packt). A working
  introduction to RADOS, CRUSH, OSD/MON/MGR roles, RBD, and CephFS for hyperconverged storage.

**Papers & articles**

- **CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data** — Sage Weil et al. (2006, SC).
  The foundational paper behind Ceph's failure-domain-aware, lookup-table-free data placement.
  <https://ceph.io/assets/pdfs/weil-crush-sc06.pdf>
- **Proxmox VE Administration Guide** — Proxmox Server Solutions (ongoing). The canonical reference for
  cluster (pvecm), HA, live migration, storage, and backup. <https://pve.proxmox.com/pve-docs/>
- **cloud-init Documentation** — Canonical / cloud-init authors (ongoing). The authoritative reference for
  first-boot datasources, user-data, and network configuration. <https://docs.cloud-init.io/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Scale, cloud & platform ops — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 10 · Scale, cloud & platform ops.

> _Content originated in the now-closed FS-SE plan (topic 52); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
