---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- [Just Enough Bash](../just-enough-bash/learning/overview.md) for commands, variables, and exit status.
- [Backend Essentials](../backend-essentials/learning/overview.md) for the service the capstone describes.
- [Containers and Orchestration](../containers-and-orchestration/learning/overview.md) for a workload to deploy.
- Docker, LocalStack, and Terraform or OpenTofu. The course uses LocalStack and a local backend, so no paid cloud account or real credential is required.

## Why this exists

Hand-built infrastructure is difficult to review, reproduce, and recover. Infrastructure as code
replaces a sequence of console clicks with a declared target state. Terraform or OpenTofu compares
that target with tracked state and proposes the operations needed to converge it. Keep one warning
close: state can contain sensitive values, so treat it as protected operational data.

## Scope boundaries

This course teaches cloud service mental models, Terraform/OpenTofu workflows, and security/cost
discipline. It does not teach container construction, Kubernetes workload operation, or paid-cloud
account administration. LocalStack emulates selected AWS APIs for learning; production systems still
need provider-specific design, review, and controls.

## Course map

- **Foundations** introduces service models, responsibility boundaries, cloud primitives, HCL, and the lifecycle.
- **State, networks, and operations** builds reuse, state safety, drift control, virtual networking, and replaceable infrastructure.
- **Secure systems** applies least privilege, secret boundaries, cost accountability, GitOps, and observability.
- **Capstone** provisions tagged dev and stage service resources from one local module, verifies convergence, then destroys them.

## Safety notes

Use only LocalStack endpoints and example values in this course. Do not create a real `.env` file,
paste a credential into a variable file, or commit a generated state file. Terraform is licensed
under Business Source License 1.1; OpenTofu is MPL-2.0. Their core configuration workflow is similar
enough here that you can use either command by setting `IAC=tofu` or `IAC=terraform` locally.

Next: [Learning Overview](./learning/overview.md) →
