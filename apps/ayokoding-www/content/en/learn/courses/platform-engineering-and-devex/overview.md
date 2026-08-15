---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Platform engineering makes the repeated operational work of delivery teams available as a useful
internal product. Its job is not to centralize every technical choice. Its job is to give
stream-aligned teams a self-service, safe, and genuinely easier path through common work such as
creating a service, obtaining infrastructure, delivering a change, and understanding ownership.

This is a leadership **no-code** Annotated-concept course. The fictional **Harbor** organization
used throughout has several product teams and a small platform team. You will create decision
artifacts—charters, contracts, service-catalog entries, guard-rail rules, and metric policies—not
software. There is no `code/` directory and no runnable artifact.

## Prerequisites

- [Containers and Orchestration](/en/learn/courses/containers-and-orchestration.md.md) supplies a runtime
  substrate the platform can hide behind a simpler interface.
- [Cloud and IaC](/en/learn/courses/cloud-and-iac.md.md) supplies the provisioned infrastructure a
  self-service capability can safely expose.
- [CI/CD and Release Engineering](/en/learn/courses/cicd-and-release-engineering.md.md) supplies the
  delivery practices a golden path can compose.

## The mental model

Treat the platform as a product for internal customers. Learn their recurring friction, offer a
small capability with opinionated safe defaults, document its contract and escape hatch, and test
whether it improves flow. A golden path should be easier than its DIY alternative; otherwise it is
a toll booth. The platform supplies mechanisms such as a template or managed database request;
product teams retain policy choices about their product where those choices are not shared safety
boundaries.

The course progresses from organization design and product discovery, through golden paths and
self-service, to measurement and improvement. Team Topologies distinguishes platform,
stream-aligned, enabling, and complicated-subsystem teams, as well as collaboration,
X-as-a-service, and facilitating interaction modes. [Team Topologies key concepts](https://teamtopologies.com/key-concepts)
The CNCF platform white paper similarly frames platforms as curated capabilities and experiences
for internal customers, with cognitive-load reduction as a key benefit. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

## Scope boundary

This course designs the internal product and its adoption model. It does not teach the full
implementation of a Kubernetes cluster, cloud estate, CI pipeline, or portal. It also does not use
delivery metrics to assess individual performance. DORA cautions against competing with metrics and
against applying them across incomparable contexts. [DORA delivery metrics guide](https://dora.dev/guides/dora-metrics/)

## How verification works

Each scenario has an observable artifact check. A platform contract has an owner, inputs, defaults,
service expectation, and escape hatch. A catalog record identifies a service owner. A metric policy
prohibits individual ranking and pairs a signal with a review question. These checks test whether a
platform practice is usable and accountable, rather than whether a command succeeds.

## Primary-source reading

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) — platform
  purpose, capabilities, and internal-customer framing.
- [Team Topologies key concepts](https://teamtopologies.com/key-concepts) — team types,
  interaction modes, and cognitive load.
- [DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/) — current
  delivery-measurement guidance and metric misuse pitfalls.
- [The SPACE of Developer Productivity](https://queue.acm.org/detail.cfm?id=3454124) — the
  multidimensional framework for developer productivity.
- [Backstage on CNCF](https://www.cncf.io/projects/backstage/) — an example open developer portal;
  the course remains tool-agnostic.
