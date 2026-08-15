---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## 1. Recall: name the layers

From bottom to top, name the physical-host, hypervisor, storage, guest, and workload layers. Then explain the
isolation trade-off between a KVM guest and an LXC container without claiming that a container is a VM.

## 2. Judgment: choose the smallest safe substrate

For one low-criticality internal service, decide whether a managed platform, one self-hosted VM, a ZFS-backed
Proxmox host, or a three-node Ceph cluster is justified. State the recovery objective and operational owner.
Reject Ceph if its host/network budget cannot meet the failure model it promises.

## 3. Code: validate rather than operate

Run `sh ../learning/code/validate-skeleton.sh`. Read each placeholder in the capstone HCL/YAML/shell files.
Confirm that no endpoint, token, SSH private key, disk path, or production hostname is supplied by the repo.

## 4. Transfer: write a change record

For an owner-approved lab migration, record source/target node, CPU compatibility, shared-storage condition,
quorum state, backup snapshot, success probe, rollback decision, and person responsible. Do not substitute a
live command for this record until the change window approves it.

## 5. Self-check: prove recoverability

Before calling a substrate ready, ask: does quorum survive the intended fault; do replicas span the intended
failure domain; can a guest be rebuilt from image plus cloud-init; has a PBS restore booted; and are tokens
absent from git and state? A missing answer is an unfinished operational control.
