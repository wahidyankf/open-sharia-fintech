---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 1
---

## Recall Q&A

**Q1.** What makes a module boundary useful?

<details>
<summary>Answer</summary>

It localizes a likely change and exposes a small contract. Its cost is indirection, which the team
must justify with a quality attribute or a real change pressure.

</details>

**Q2.** What is the dependency direction in clean architecture?

<details>
<summary>Answer</summary>

Source dependencies point inward toward policy. Runtime control may enter from a framework at the
edge, but the policy does not need to import the framework.

</details>

**Q3.** What does a fitness function protect?

<details>
<summary>Answer</summary>

It protects an architectural characteristic, such as no domain-to-infrastructure imports or no
cycle between modules, by making a violation fail continuously.

</details>

## Scenario judgment

A small team has one deployable application with order, catalog, and payment areas. It needs local
calls and simple operations today, but it expects provider APIs to change.

<details>
<summary>Reasoned answer</summary>

Choose a modular monolith with a payment port. The deployment remains simple, while the volatile
provider contract stays behind an adapter. Record the choice in an ADR and add an import-boundary check.

</details>

## Hands-on boundary exercise

Take a handler that calculates a value and calls a provider directly. Extract a pure calculation,
introduce a port for the provider capability, and write one test showing an in-memory adapter can
replace the real adapter. Then state the new boundary's cost.

## Automaticity checklist

- [ ] I can name the quality attribute a proposed boundary protects.
- [ ] I can distinguish source dependency direction from runtime control flow.
- [ ] I can write an ADR with context, decision, and consequences.
- [ ] I can turn one architecture rule into a failing fitness function.
- [ ] I can explain the cost of a modular-monolith or service boundary.
