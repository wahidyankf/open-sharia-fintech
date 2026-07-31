---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Mental model

Cloud is a pool of remotely operated capabilities with a moving control boundary. IaC makes that
boundary explicit in versioned configuration: providers implement resource types, resources describe
the desired objects, and state connects those declarations to objects that exist. A plan is a review
artifact, not permission to skip review.

## Local runtime setup

Run LocalStack in one terminal. This uses a disposable container and never needs a cloud account.

```bash
# => Runs the AWS-compatible learning endpoint only on this machine.
docker run --rm --name cloud-iac-localstack -p 4566:4566 localstack/localstack:4.10
# => Keep this terminal open while examples that call LocalStack are running.
# => Stop it with Ctrl-C when the local learning session is finished.
```

Complete runnable artifact: [`setup-localstack/run.sh`](./code/setup-localstack/run.sh).

Install Terraform or OpenTofu from its official distribution, then run `terraform` below as `tofu`
if you chose OpenTofu. Use the capstone commands only from its directory. Generated `.terraform/`,
`terraform.tfstate*`, and plan files are local operational artifacts, not course deliverables.

## Worked-example progression

The examples move from cloud vocabulary to declared resources, then from state and networks to
operational security. HCL, YAML, command, decision-table, and diagram media appear where each best
explains the concept. Code-bearing examples keep line-by-line annotations; diagrams use labels,
shapes, and the accessible palette so meaning does not rely on colour.

Next: [Cloud and Terraform Foundations](./beginner.md) →
