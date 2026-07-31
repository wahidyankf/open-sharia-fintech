---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

This spaced-repetition companion uses recall, scenario judgment, hands-on repetition, automaticity,
and explanation to reinforce CI/CD and release engineering. Attempt every prompt before expanding
an answer.

## Recall Q&A

**Q1 (co-01).** What two practices define continuous integration?

<details>
<summary>Answer</summary>

Frequent shared-mainline integration and an automated self-testing build.

</details>

**Q2 (co-02–co-06).** How do delivery, deployment, pipeline stages, fail-fast checks, and acceptance
gates work together?

<details>
<summary>Answer</summary>

Continuous delivery keeps a candidate releasable, continuous deployment ships a green candidate
automatically, and ordered fast-to-slow gates stop an unqualified candidate before production.

</details>

**Q3 (co-07–co-08).** When does a simpler branch flow beat GitFlow?

<details>
<summary>Answer</summary>

When continuous delivery needs a shared trunk and long-lived role branches add coordination delay.

</details>

**Q4 (co-09–co-13).** Name GitHub Actions building blocks that make CI reusable and fast.

<details>
<summary>Answer</summary>

Triggers, jobs, runners, steps, matrices, dependencies, caches, and artifacts.

</details>

**Q5 (co-14–co-18).** What do checks, environments, secrets, OIDC, and reusable automation protect?

<details>
<summary>Answer</summary>

They protect merge quality, production approval, sensitive inputs, cloud identity, and duplicated logic.

</details>

**Q6 (co-19–co-22).** How do commits become a published release?

<details>
<summary>Answer</summary>

SemVer and Conventional Commits provide intent; automation creates release metadata and publishing
sends a verified artifact to a registry.

</details>

**Q7 (co-23–co-26).** How do blue-green, canary, toggles, and rollback reduce release risk?

<details>
<summary>Answer</summary>

They limit or control exposure and preserve a defined recovery route when evidence turns bad.

</details>

**Q8 (co-27–co-29).** Why version pipelines and verify provenance?

<details>
<summary>Answer</summary>

A versioned pipeline is reviewable, while signature and provenance evidence let a deployer verify a
candidate's source and identity.

</details>

**Q9 (co-30–co-34).** What do DORA, runner policy, affected CI, and automated canaries optimize?

<details>
<summary>Answer</summary>

They optimize delivery observability, execution trust, feedback speed, and safe progressive exposure.

</details>

## Scenario Judgment

1. A lint gate is red. Should deployment start?
2. A canary error rate crosses its threshold. Should traffic expand?
3. A fork pull request requests a self-hosted runner. Is that a safe default?
4. A release breaks a public API. Which SemVer component changes?

<details>
<summary>Answer</summary>

No; no; no, prefer hosted or strongly isolated execution; and MAJOR changes.

</details>

## Hands-On Repetition

1. Run the Python artifact in the Example 60 directory.
2. Run the capstone rollout with a healthy signal.
3. Run the capstone rollout with an unhealthy signal.
4. Write one feature and one fix Conventional Commit.
5. Sketch a pipeline whose deploy job depends on test.

## Automaticity Checklist

- I can distinguish a cache from an artifact.
- I can state why a protected environment is a deployment boundary.
- I can choose rollback or fix forward from the current blast radius.
- I can explain why OIDC improves on a stored cloud credential.
- I can compute the DORA measures from a small deployment log.
- I can choose blue-green, canary, or a feature flag from the release constraint.

## Why / Why Not

Why promote one immutable artifact instead of rebuilding for production? Why can a redundant gate become
a warning? Why might automatic rollback beat a manual response during a canary? Why is a short-lived
OIDC token preferable to a stored cloud token? Answer with evidence, blast radius, and recovery rather
than tool preference alone.
