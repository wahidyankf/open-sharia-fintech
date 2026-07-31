---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What makes cloud computing more than remote hosting?
   <details><summary>Answer</summary>NIST describes on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service.</details>
2. What shifts between IaaS, PaaS, and SaaS?
   <details><summary>Answer</summary>The customer control boundary descends from operating system and application toward data and account configuration.</details>
3. What does Terraform state connect?
   <details><summary>Answer</summary>It maps configuration addresses to real provider objects and their tracked attributes.</details>
4. Why is a plan not harmless output?
   <details><summary>Answer</summary>It may reveal sensitive values and it can propose replacement or deletion that needs review.</details>
5. What is the safe response to a state lock held by an active apply?
   <details><summary>Answer</summary>Wait and inspect the owner; do not force unlock an active writer.</details>
6. What does a NAT gateway allow that a private subnet otherwise lacks?
   <details><summary>Answer</summary>Outbound-initiated access while retaining no unsolicited inbound initiation path.</details>
7. Why use a workload role?
   <details><summary>Answer</summary>It delivers temporary credentials without distributing a long-lived key.</details>
8. What are the three OpenTelemetry signals?
   <details><summary>Answer</summary>Metrics measure, logs record events, and traces show request paths.</details>

## Applied problems

- Write a responsibility matrix for a managed database and identify who tests restore.
- Given a plan that replaces a production bucket, identify whether the address, name, or lifecycle caused it before applying.
- Design two subnets across zones and explain which failure each design survives.
- Review an IAM policy containing `Action: "*"`; reduce it to one observed workload operation.

## Code katas

- Add a typed `environment` variable and a bucket-name output to a small local module.
- Create dev and stage callers for one module, then show the exact plan difference.
- Run `terraform plan -refresh-only` after a controlled LocalStack change and explain what source change follows.
- Add four required tags through `locals`, rather than repeating them in each resource.

## Self-check checklist

- I can explain provider, resource, module, state, and backend without treating them as synonyms.
- I review a plan for destructive actions and unknown values before applying it.
- I keep secret values out of source, variable files, and committed state.
- I can distinguish a security group from IAM and a NAT path from a load balancer.
- I can destroy a local environment after verifying the configuration is reproducible.

## Elaborative interrogation

- Why does a remote backend improve collaboration while increasing the importance of access control?
- Why does an immutable-server workflow need externalized data and configuration?
- Explain why GitOps continuous reconciliation can both improve recovery and undo an emergency console change.
- Which signal would you inspect first for a slow function invocation, and what would the other two add?

← Previous: [Capstone](../learning/capstone/overview.md)
