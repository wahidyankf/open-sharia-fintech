---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

> **Owner-operated lab only.** This course teaches the control plane, network, storage, TLS, GitOps, and
> recovery duties a cloud provider normally performs. Its examples print a plan, render local YAML, or use
> client-side dry runs; they do not download software, contact a cluster, alter a router, or include a
> credential, public IP, hostname, token, or real image digest. Run a real operation only in an isolated lab
> you own after a reviewed change record, backup, and rollback decision.

## Prerequisites

[Containers and Orchestration](../containers-and-orchestration/overview.md) supplies Kubernetes object and
reconciliation fluency. [CI/CD and Release Engineering](../cicd-and-release-engineering/overview.md) supplies
artifact provenance and promotion discipline. This course also assumes Linux, SSH-console recovery, and a
deliberately designed VM or bare-metal lab; it does not teach cloud provisioning or the virtual-machine
substrate.

## Why this exists

A self-managed cluster is not a cheaper managed Kubernetes service. You own control-plane quorum, node
maintenance, CNI enforcement, bare-metal addresses, persistent storage, ingress, certificate issuance,
Git reconciliation, secret boundaries, and recovery evidence. The durable model is declared desired state:
controllers reconcile it, Git reviews it, and restore drills prove it can survive loss.

## Scope and safety boundary

This is the deeper successor to [Self-Hosting Essentials](../self-hosting-essentials/overview.md), which
stops at one host and service. It consumes the VM or hardware layer from
[Bare-Metal Virtualization](../bare-metal-virtualization/overview.md), then operates a production-shaped
cluster: k3s or kubeadm, with k0s and Talos as alternatives; CNI, NetworkPolicy, MetalLB, Longhorn,
ingress and cert-manager; and Argo CD or Flux with Kustomize, Helm, secret delivery, Velero, and DR.

## Factual, licensing, and citation notes

Version numbers and package-install recipes change quickly, so none are pinned here. Confirm commands,
compatibility, certificates, networking ranges, current releases, and licenses from the relevant primary
source before a real deployment: [Kubernetes](https://kubernetes.io/docs/home/),
[k3s](https://docs.k3s.io/), [kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/),
[Talos Linux](https://www.talos.dev/latest/), [Cilium](https://docs.cilium.io/),
[MetalLB](https://metallb.io/), [Longhorn](https://longhorn.io/docs/),
[cert-manager](https://cert-manager.io/docs/), [Argo CD](https://argo-cd.readthedocs.io/),
[Flux](https://fluxcd.io/), and [Velero](https://velero.io/docs/). The original operational scope and
concept mapping are preserved in the [course syllabus](../../../../../../../plans/done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/self-managed-kubernetes-and-gitops.md).

## How the course is organized

- [Learning](./learning/overview.md) has 82 annotated YAML/CLI examples: control-plane and node duties,
  then network/storage/TLS, then GitOps and recovery.
- [Drilling](./drilling/overview.md) converts the model into recall, review gates, and safe local checks.
- [Capstone](./learning/capstone/overview.md) is a reviewable, non-operating acceptance plan for the whole
  platform; an owner supplies real infrastructure inputs outside Git.

## Examples by Level

### Beginner (Examples 1–30)

- [Example 1: Why Self-Managed Kubernetes](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-1-why-self-managed-kubernetes)
- [Example 2: Control Plane and Workers](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-2-control-plane-and-workers)
- [Example 3: Control Plane Components](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-3-control-plane-components)
- [Example 4: Declarative Reconciliation](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-4-declarative-reconciliation)
- [Example 5: Etcd and Raft](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-5-etcd-and-raft)
- [Example 6: Quorum Math](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-6-quorum-math)
- [Example 7: Plan a k3s Server Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-7-plan-a-k3s-server-install)
- [Example 8: k3s Single Binary](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-8-k3s-single-binary)
- [Example 9: Plan k3s Kubeconfig Access](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-9-plan-k3s-kubeconfig-access)
- [Example 10: k3s SQLite Default](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-10-k3s-sqlite-default)
- [Example 11: k3s Embedded Etcd](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-11-k3s-embedded-etcd)
- [Example 12: Odd Server HA](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-12-odd-server-ha)
- [Example 13: Plan Three k3s Servers](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-13-plan-three-k3s-servers)
- [Example 14: Plan kubeadm Init](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-14-plan-kubeadm-init)
- [Example 15: Plan kubeadm Join](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-15-plan-kubeadm-join)
- [Example 16: kubeadm Bootstrap Scope](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-16-kubeadm-bootstrap-scope)
- [Example 17: Plan k0s Controller](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-17-plan-k0s-controller)
- [Example 18: Talos Immutable Boundary](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-18-talos-immutable-boundary)
- [Example 19: Talos Machine Configuration](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-19-talos-machine-configuration)
- [Example 20: Distribution Decision](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-20-distribution-decision)
- [Example 21: Immutable Node Updates](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-21-immutable-node-updates)
- [Example 22: Read a Node Inventory](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-22-read-a-node-inventory)
- [Example 23: Plan Worker Join](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-23-plan-worker-join)
- [Example 24: Cordon a Node](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-24-cordon-a-node)
- [Example 25: Drain a Node](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-25-drain-a-node)
- [Example 26: Uncordon a Node](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-26-uncordon-a-node)
- [Example 27: Plan an Etcd Snapshot](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-27-plan-an-etcd-snapshot)
- [Example 28: Plan an Etcd Restore](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-28-plan-an-etcd-restore)
- [Example 29: Upgrade Sequencing](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-29-upgrade-sequencing)
- [Example 30: Plan a k3s Upgrade](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/beginner#example-30-plan-a-k3s-upgrade)

### Intermediate (Examples 31–57)

- [Example 31: CNI Is Required](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-31-cni-is-required)
- [Example 32: Kubernetes Network Model](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-32-kubernetes-network-model)
- [Example 33: Plan a Cilium Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-33-plan-a-cilium-install)
- [Example 34: CNI Decision](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-34-cni-decision)
- [Example 35: Flannel VXLAN](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-35-flannel-vxlan)
- [Example 36: NetworkPolicy Default Open](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-36-networkpolicy-default-open)
- [Example 37: Deny Ingress by Default](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-37-deny-ingress-by-default)
- [Example 38: Allow Frontend to Database](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-38-allow-frontend-to-database)
- [Example 39: Plan a MetalLB Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-39-plan-a-metallb-install)
- [Example 40: MetalLB Address Pool](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-40-metallb-address-pool)
- [Example 41: LoadBalancer Assignment](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-41-loadbalancer-assignment)
- [Example 42: Layer 2 Advertisement](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-42-layer-2-advertisement)
- [Example 43: Layer 2 and BGP](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-43-layer-2-and-bgp)
- [Example 44: BGP Peering Plan](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-44-bgp-peering-plan)
- [Example 45: Plan a Longhorn Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-45-plan-a-longhorn-install)
- [Example 46: Longhorn Replication](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-46-longhorn-replication)
- [Example 47: Local Path Provisioning](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-47-local-path-provisioning)
- [Example 48: StorageClass and PVC](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-48-storageclass-and-pvc)
- [Example 49: Storage Decision](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-49-storage-decision)
- [Example 50: Ingress Controller Choice](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-50-ingress-controller-choice)
- [Example 51: Traefik Default](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-51-traefik-default)
- [Example 52: Ingress Manifest](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-52-ingress-manifest)
- [Example 53: Plan a cert-manager Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-53-plan-a-cert-manager-install)
- [Example 54: ClusterIssuer Contract](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-54-clusterissuer-contract)
- [Example 55: Certificate Resource](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-55-certificate-resource)
- [Example 56: Ingress TLS Automation](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-56-ingress-tls-automation)
- [Example 57: ACME HTTP-01 Flow](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/intermediate#example-57-acme-http-01-flow)

### Advanced (Examples 58–82)

- [Example 58: GitOps Model](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-58-gitops-model)
- [Example 59: Plan an Argo CD Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-59-plan-an-argo-cd-install)
- [Example 60: Argo CD Application](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-60-argo-cd-application)
- [Example 61: Argo CD Sync Status](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-61-argo-cd-sync-status)
- [Example 62: Argo CD ApplicationSet](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-62-argo-cd-applicationset)
- [Example 63: Argo CD Auto-Sync](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-63-argo-cd-auto-sync)
- [Example 64: Plan Flux Bootstrap](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-64-plan-flux-bootstrap)
- [Example 65: Flux Kustomization](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-65-flux-kustomization)
- [Example 66: Flux HelmRelease](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-66-flux-helmrelease)
- [Example 67: Argo CD and Flux](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-67-argo-cd-and-flux)
- [Example 68: Kustomize Base and Overlay](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-68-kustomize-base-and-overlay)
- [Example 69: Production Overlay Patch](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-69-production-overlay-patch)
- [Example 70: Helm Values Per Environment](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-70-helm-values-per-environment)
- [Example 71: Build Once Promote](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-71-build-once-promote)
- [Example 72: Promotion Through Git](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-72-promotion-through-git)
- [Example 73: Secrets Are Not Git Data](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-73-secrets-are-not-git-data)
- [Example 74: SealedSecret Contract](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-74-sealedsecret-contract)
- [Example 75: ExternalSecret Contract](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-75-externalsecret-contract)
- [Example 76: Secret Delivery Decision](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-76-secret-delivery-decision)
- [Example 77: Plan a Velero Install](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-77-plan-a-velero-install)
- [Example 78: Velero Backup](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-78-velero-backup)
- [Example 79: Velero Schedule](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-79-velero-schedule)
- [Example 80: RPO and RTO](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-80-rpo-and-rto)
- [Example 81: Restore Drill](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-81-restore-drill)
- [Example 82: Self-Managed Kubernetes Capstone](/en/learn/courses/self-managed-kubernetes-and-gitops/learning/advanced#example-82-self-managed-kubernetes-capstone)
