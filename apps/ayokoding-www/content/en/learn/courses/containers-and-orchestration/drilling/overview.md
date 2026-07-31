---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

Answer before looking anything up.

1. What is the distinction between an image, an image layer, and a container's writable layer?
   <details><summary>Answer</summary>An image is immutable metadata plus read-only layers; a running container adds one private writable layer above them.</details>
2. When do you choose an immutable digest over a tag, and what maintenance cost follows?
   <details><summary>Answer</summary>Choose a digest when exact deployment input matters; intentionally update and test that digest to receive security fixes.</details>
3. Which Dockerfile instruction establishes the executable and which supplies default arguments?
   <details><summary>Answer</summary>`ENTRYPOINT` establishes the executable; `CMD` supplies default arguments that a caller can replace.</details>
4. Why does copying dependency metadata before application source improve build-cache reuse?
   <details><summary>Answer</summary>A source-only edit then leaves the dependency-install layer unchanged, so the builder can reuse it.</details>
5. What differs between a Docker volume and a bind mount?
   <details><summary>Answer</summary>Docker manages a named volume independently of a container; a bind mount exposes a specified host path and its permissions.</details>
6. Which Kubernetes object maintains replica count, and which object gives those Pods stable DNS?
   <details><summary>Answer</summary>A Deployment manages the desired replica count through ReplicaSets; a Service selects those Pods and provides stable DNS.</details>
7. Why must a readiness failure normally remove traffic without restarting the container?
   <details><summary>Answer</summary>Readiness says an otherwise running process cannot serve now, so Kubernetes removes its endpoint; liveness is the restart signal.</details>
8. Why is a Kubernetes Secret not encrypted merely because its value is base64-encoded?
   <details><summary>Answer</summary>Base64 is reversible text encoding, not cryptography; storage encryption and access control are separate safeguards.</details>
9. Which workload has stable ordinal identity, and which runs once per eligible node?
   <details><summary>Answer</summary>A StatefulSet gives Pods stable ordinal identities; a DaemonSet reconciles one Pod on each eligible node.</details>
10. What controller action follows when a Deployment-managed Pod is deleted?
    <details><summary>Answer</summary>The ReplicaSet observes fewer actual Pods than desired and creates a replacement Pod.</details>

## Applied problems

- Write a two-stage Dockerfile for a service, then use `docker history` to explain which stage's
  build tools are absent from the final image.
- Create a Compose stack with an application and a database. Remove the application container and
  show which data survives using a named volume.
- Deploy a three-replica Deployment with a readiness probe. Make one replica unready and inspect
  EndpointSlices to explain why the Service stopped routing to it.
- Given a Pod that is `OOMKilled`, identify whether the fix belongs in a memory limit, workload
  behavior, autoscaling, or all three. Do not blindly raise the limit.

## Code katas

- Write a Dockerfile whose `ENTRYPOINT` remains fixed while a caller replaces its `CMD` arguments;
  prove both forms with `docker run`.
- Create a Pod manifest with a ConfigMap environment value and a readiness probe; use
  `kubectl describe` to explain why it is or is not an endpoint.
- Turn a one-container Pod into a two-replica Deployment and roll it back after changing its image.
- Write a rootless Quadlet `.container` for a pinned image, reload user systemd, then stop and remove it.

## Self-check checklist

- I can explain why a container shares the host kernel without calling it a virtual machine.
- I can build, tag, inspect, run, stop, and remove an image without losing named-volume data.
- I can read a Deployment, Service, ConfigMap, Secret, and probe configuration without guessing.
- I can distinguish a declarative reconciliation target from a one-off imperative command.
- I do not place real credentials in an image, a Compose file, or a Kubernetes manifest.

## Elaborative interrogation & self-explanation

- Why does a changed early Dockerfile layer make later layers rebuild, and how does dependency-first
  copying change that outcome?
- Why does a readiness failure remove traffic but normally not restart a container, whereas a liveness
  failure can restart it?
- Explain to a teammate why a Service remains stable while its selected Pods are replaced.
- Why is a rootless container safer than a root-privileged daemon without making a container escape harmless?

← Previous: [Capstone](../learning/capstone/overview.md)
