---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Shell fluency**: [Just Enough Bash](../just-enough-bash/learning/overview.md). You should be
  comfortable reading commands, variables, pipes, and exit statuses before operating containers.
- **Prior topic**: [Backend Essentials](../backend-essentials/learning/overview.md). The capstone
  treats its HTTP service as an already-working application.
- **Data fluency**: [SQL Essentials](../sql-essentials/learning/overview.md). Compose exercises
  use PostgreSQL connections and a small `SELECT 1` readiness query.
- **Tools and environment**: Docker Engine with Compose, a registry account for push/pull exercises,
  `kubectl`, and a local Kubernetes cluster such as kind, minikube, or Docker Desktop Kubernetes.
- **Assumed knowledge**: reading a shell command, HTTP ports, environment variables, and a basic
  service health endpoint. The course uses YAML and CLI commands rather than a programming language.

## Why this exists -- the big idea

An application that only runs on its author's machine is not yet deployable. Containers package a
process with its runtime dependencies, while Kubernetes continuously drives a declared fleet of
containers toward the state you asked for. Keep this mental model: build an immutable image, run it
with explicit configuration and storage, then let a declarative controller maintain the desired
number of healthy instances.

The important trade-offs recur throughout the course: image convenience versus size and attack
surface, mutable tags versus reproducible digests, local bind mounts versus managed volumes, and
rapid delivery versus availability and resource controls. Docker teaches the process package;
Kubernetes teaches the control loop around that package.

## Scope boundaries

This is an application-container and Kubernetes-workload course. It does not teach
[Self-Hosting Essentials](../self-hosting-essentials/overview.md), which covers operating applications
on self-managed hosts; production Kubernetes control-plane operations; `cloud-and-iac` (a pending
course) for cloud-account architecture and infrastructure as code; or `bare-metal-virtualization`
(a pending course) for physical-server and virtual-machine provisioning. Those concerns decide where
a cluster lives; this course teaches how to build, configure, expose, and operate the application
workload that runs on it.

## How this course is organized

- **[Learning](./learning/overview.md)** contains 83 annotated examples. Beginner establishes
  images, Dockerfiles, networking, and image distribution; Intermediate builds multi-service
  Compose stacks and Kubernetes workload/network/configuration primitives; Advanced covers health,
  resources, autoscaling, specialized workloads, reconciliation, Podman, and the integrated
  capstone.
- **[Capstone](./learning/capstone/overview.md)** packages a small HTTP service into a non-root,
  multi-stage image, runs it with Compose, then deploys the same image using Kubernetes manifests.
- **[Drilling](./drilling/overview.md)** turns the course's command vocabulary and operational
  decisions into recall prompts, incident drills, and a deployment checklist.

## Accuracy and safety notes

- A container is process isolation, not a virtual machine or a security boundary by itself. Treat
  an image as executable supply-chain input; use trusted registries and review updates.
- Tags are mutable labels. A digest identifies exact image content, but digest pinning also means
  you must deliberately update the digest when security fixes are released.
- Kubernetes `Secret` values use base64 encoding in manifests; base64 is not encryption. Avoid
  committing real credentials, and configure encryption, least privilege, and an external secret
  workflow for production.
- An Ingress resource needs an installed Ingress controller. Kubernetes recommends Gateway API for
  new traffic-management investments, while many existing clusters still use Ingress.

Next: [Learning Overview](./learning/overview.md) →
