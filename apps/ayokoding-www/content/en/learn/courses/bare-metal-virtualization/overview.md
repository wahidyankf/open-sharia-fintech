---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

> **Safe lab boundary.** Every command in this course either inspects local capability, prints a
> reviewable plan, or uses a disposable nested Proxmox lab that you own. Do not run storage, cluster,
> migration, or restore commands against production hardware until the change is reviewed, backed up,
> and scheduled. Never commit an API token, SSH private key, or recovered guest data.

## Prerequisites

- [Containers and Orchestration](../containers-and-orchestration/overview.md) supplies the workloads that
  later run on these VMs; [Networking Essentials](../networking-essentials/overview.md) supplies bridge,
  DHCP, and subnet vocabulary.
- Terraform or OpenTofu plan/apply/state fluency is assumed. Use a Proxmox VE host or a nested lab, direct
  HBA-attached disposable disks for ZFS/Ceph practice, and a POSIX shell. A single node is sufficient for
  inspection; quorum, HA, Ceph, and live migration require a deliberately built multi-node lab.

## Why this exists

A cloud VM is still a guest on somebody's physical substrate. This course exposes that substrate: KVM/QEMU
virtualization, Proxmox control-plane operations, storage failure models, image and first-boot provisioning,
and tested recovery. The durable model is: make hardware capacity programmable, keep guest configuration
reproducible, and design both control-plane and data-plane failures before production needs them.

## Scope boundary: the two altitudes

[Self-Hosting Essentials](../self-hosting-essentials/overview.md) is this course's **lighter-altitude
sibling**: it teaches one box or VM, a service, reverse proxy, TLS, firewall, and backup basics. This course
deliberately goes deeper into the Proxmox/KVM hypervisor layer that self-hosting-essentials excludes:
physical hosts, VM versus LXC isolation, cluster quorum and HA, live migration, ZFS/Ceph failure domains,
cloud-init templates, Proxmox API automation, PXE, and Proxmox Backup Server restores. It stops before
operating the Kubernetes control plane that consumes those VMs.

## Accuracy, licensing, and safety notes

- Proxmox VE documents its KVM/QEMU guests, LXC containers, cluster quorum, HA, and backup tooling in its
  [official documentation](https://pve.proxmox.com/pve-docs/). Verify current release and command details
  against that documentation before changing a real host.
- ZFS RAID-Z parity and snapshots are documented by [OpenZFS](https://openzfs.github.io/openzfs-docs/);
  Ceph's MON, MGR, OSD, RBD, CephFS, and CRUSH concepts are documented by [Ceph](https://docs.ceph.com/en/latest/architecture/).
  Use direct disks via an HBA for ZFS/Ceph rather than hiding disks behind hardware RAID.
- [cloud-init](https://docs.cloud-init.io/) configures an instance at first boot;
  [Packer](https://developer.hashicorp.com/packer/docs/intro) builds repeatable images; and the maintained
  [bpg/proxmox](https://github.com/bpg/terraform-provider-proxmox) provider exposes Proxmox to Terraform or
  OpenTofu. Terraform's post-2023 license and OpenTofu's MPL-2.0 license differ: make the tool choice
  deliberately and verify its current terms.

## How the course is organized

- [Learning](./learning/overview.md) contains 80 annotated, safe examples: fundamentals and local models,
  then clustering/storage/IaC, then repeatable images, PXE, recovery, and failure-domain reasoning.
- [Drilling](./drilling/overview.md) turns the vocabulary into recall, judgment, local validation, transfer,
  and self-review.
- [Capstone](./learning/capstone/overview.md) provides a non-secret skeleton for an image, cloud-init,
  Terraform/OpenTofu, and recovery decision trail. It requires an owner-provided isolated lab before apply.

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Why Own the Substrate](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-1-why-own-the-substrate)
- [Example 2: Type 1 and Type 2 Hypervisors](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-2-type-1-and-type-2-hypervisors)
- [Example 3: Check KVM Capability](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-3-check-kvm-capability)
- [Example 4: Split KVM from QEMU](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-4-split-kvm-from-qemu)
- [Example 5: Compare a VM and LXC](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-5-compare-a-vm-and-lxc)
- [Example 6: Read the Proxmox Stack](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-6-read-the-proxmox-stack)
- [Example 7: Inspect a Proxmox Version](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-7-inspect-a-proxmox-version)
- [Example 8: Model a Proxmox API Token](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-8-model-a-proxmox-api-token)
- [Example 9: Trace the Shared API](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-9-trace-the-shared-api)
- [Example 10: Plan a VM Lifecycle](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-10-plan-a-vm-lifecycle)
- [Example 11: List VM and LXC Inventory](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-11-list-vm-and-lxc-inventory)
- [Example 12: Plan an LXC Lifecycle](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-12-plan-an-lxc-lifecycle)
- [Example 13: Separate VM Lifecycle Actions](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-13-separate-vm-lifecycle-actions)
- [Example 14: Inspect Libvirt Domains](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-14-inspect-libvirt-domains)
- [Example 15: Compare Libvirt and Proxmox](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-15-compare-libvirt-and-proxmox)
- [Example 16: Name Libvirt Hypervisors](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-16-name-libvirt-hypervisors)
- [Example 17: Compare Storage Models](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-17-compare-storage-models)
- [Example 18: Avoid Hardware RAID](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-18-avoid-hardware-raid)
- [Example 19: Plan a RAID Z Pool](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-19-plan-a-raid-z-pool)
- [Example 20: Choose RAID Z Parity](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-20-choose-raid-z-parity)
- [Example 21: Plan a ZFS Dataset](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-21-plan-a-zfs-dataset)
- [Example 22: Plan a ZFS Snapshot](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-22-plan-a-zfs-snapshot)
- [Example 23: Rehearse a ZFS Rollback](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-23-rehearse-a-zfs-rollback)
- [Example 24: Trace Cloud Init First Boot](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-24-trace-cloud-init-first-boot)
- [Example 25: Write Cloud Init User Data](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-25-write-cloud-init-user-data)
- [Example 26: Plan a Proxmox Cloud Init Drive](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-26-plan-a-proxmox-cloud-init-drive)
- [Example 27: Inspect Cluster Quorum](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-27-inspect-cluster-quorum)
- [Example 28: Calculate a Quorum Majority](/en/learn/courses/bare-metal-virtualization/learning/beginner#example-28-calculate-a-quorum-majority)

### Intermediate (Examples 29–56)

- [Example 29: Plan a Cluster Join](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-29-plan-a-cluster-join)
- [Example 30: Name Corosync's Job](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-30-name-corosyncs-job)
- [Example 31: Design Three Node Quorum](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-31-design-three-node-quorum)
- [Example 32: Plan a Live Migration](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-32-plan-a-live-migration)
- [Example 33: Check Migration CPU Compatibility](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-33-check-migration-cpu-compatibility)
- [Example 34: Plan an HA Service](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-34-plan-an-ha-service)
- [Example 35: Trace HA Failover](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-35-trace-ha-failover)
- [Example 36: Check HA Prerequisites](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-36-check-ha-prerequisites)
- [Example 37: Plan ZFS Send Receive](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-37-plan-zfs-send-receive)
- [Example 38: Plan Incremental ZFS Send](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-38-plan-incremental-zfs-send)
- [Example 39: Plan a ZFS Scrub](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-39-plan-a-zfs-scrub)
- [Example 40: Plan Proxmox Replication](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-40-plan-proxmox-replication)
- [Example 41: Model Hyperconvergence](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-41-model-hyperconvergence)
- [Example 42: Plan a Ceph Monitor](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-42-plan-a-ceph-monitor)
- [Example 43: Plan a Ceph OSD](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-43-plan-a-ceph-osd)
- [Example 44: Assign Ceph Daemon Jobs](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-44-assign-ceph-daemon-jobs)
- [Example 45: Trace CRUSH Placement](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-45-trace-crush-placement)
- [Example 46: Design a Ceph Failure Domain](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-46-design-a-ceph-failure-domain)
- [Example 47: Plan an RBD Pool](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-47-plan-an-rbd-pool)
- [Example 48: Name CephFS](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-48-name-cephfs)
- [Example 49: Size a Three Node Ceph Lab](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-49-size-a-three-node-ceph-lab)
- [Example 50: Declare a Proxmox Provider](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-50-declare-a-proxmox-provider)
- [Example 51: Keep a Provider Token External](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-51-keep-a-provider-token-external)
- [Example 52: Declare a VM Clone](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-52-declare-a-vm-clone)
- [Example 53: Review Plan Then Apply](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-53-review-plan-then-apply)
- [Example 54: Check an Idempotent Apply](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-54-check-an-idempotent-apply)
- [Example 55: Inject Cloud Init Through IaC](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-55-inject-cloud-init-through-iac)
- [Example 56: Choose a Maintained Provider](/en/learn/courses/bare-metal-virtualization/learning/intermediate#example-56-choose-a-maintained-provider)

### Advanced (Examples 57–80)

- [Example 57: Describe Packer's Image Contract](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-57-describe-packers-image-contract)
- [Example 58: Skeleton a Proxmox Template Build](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-58-skeleton-a-proxmox-template-build)
- [Example 59: Bake Cloud Init Readiness](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-59-bake-cloud-init-readiness)
- [Example 60: Split Image and First Boot Work](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-60-split-image-and-first-boot-work)
- [Example 61: Compare Immutable and Mutable Guests](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-61-compare-immutable-and-mutable-guests)
- [Example 62: Clone a Golden Template](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-62-clone-a-golden-template)
- [Example 63: Skeleton an Ansible VM Task](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-63-skeleton-an-ansible-vm-task)
- [Example 64: Check Ansible Convergence](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-64-check-ansible-convergence)
- [Example 65: Select the Proxmox Collection](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-65-select-the-proxmox-collection)
- [Example 66: Compare Terraform and Ansible](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-66-compare-terraform-and-ansible)
- [Example 67: Define the Provision Configure Handoff](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-67-define-the-provision-configure-handoff)
- [Example 68: Trace the PXE Boot Chain](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-68-trace-the-pxe-boot-chain)
- [Example 69: Plan an Unattended Install](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-69-plan-an-unattended-install)
- [Example 70: Describe PBS Backups](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-70-describe-pbs-backups)
- [Example 71: Plan a PBS Backup](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-71-plan-a-pbs-backup)
- [Example 72: Rehearse a PBS Restore](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-72-rehearse-a-pbs-restore)
- [Example 73: Compare Recovery Tiers](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-73-compare-recovery-tiers)
- [Example 74: Compare Terraform and OpenTofu Licenses](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-74-compare-terraform-and-opentofu-licenses)
- [Example 75: Plan an OpenTofu Swap](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-75-plan-an-opentofu-swap)
- [Example 76: Reason About Failure Domains](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-76-reason-about-failure-domains)
- [Example 77: Compare Quorum and CRUSH](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-77-compare-quorum-and-crush)
- [Example 78: Keep Secrets out of State](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-78-keep-secrets-out-of-state)
- [Example 79: Locate the Substrate Layer](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-79-locate-the-substrate-layer)
- [Example 80: Assemble the Bare Metal Capstone](/en/learn/courses/bare-metal-virtualization/learning/advanced#example-80-assemble-the-bare-metal-capstone)

## Legacy relation

Superseded by: this canonical course replaces the overlapping legacy Proxmox virtualization material;
the historical material remains available during the transition.
