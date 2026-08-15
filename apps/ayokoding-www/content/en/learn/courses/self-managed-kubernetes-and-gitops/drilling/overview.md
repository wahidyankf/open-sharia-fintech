---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall

Explain why a three-server control plane can lose one server while a two-server control plane has no safe
majority. Then name which layer owns each failure: Kubernetes API state, pod networking, bare-metal service
addressing, PVC placement, TLS renewal, Git reconciliation, and backup recovery.

## Judgment

Choose k3s, kubeadm, k0s, or Talos for a stated ownership and recovery constraint. Choose Cilium, Calico,
or Flannel by required policy and observability—not brand familiarity. Reject MetalLB BGP when the router
owner cannot provide an approved peer configuration, and reject a replicated-storage promise that its failure
domain cannot meet.

## Safe local practice

Write a namespace, default-deny policy, explicit database allow rule, PVC, Kustomize overlay, and
SealedSecret-shaped placeholder with no real data. Use `kubectl apply --dry-run=client` where your local
client has the relevant schema; otherwise validate indentation and review the object fields without implying
that a local render proves a controller will run.

## Transfer

For a promotion, record source digest, destination overlay, reviewer, Git revision, health signal, expected
controller status, rollback revision, and backup point. For a maintenance window, record node, drain
exceptions, replica capacity, quorum condition, console access, and the condition that ends the window.

## Self-check

Before calling a self-managed platform ready, can you show: quorum survives its claimed fault; policy is
actually enforced; load-balancer addresses are owned and non-conflicting; storage's data-loss behavior is
known; TLS and secrets have trust boundaries; Git is the desired-state source; and a restore has recovered
the workload and its data? A missing proof is unfinished work.
