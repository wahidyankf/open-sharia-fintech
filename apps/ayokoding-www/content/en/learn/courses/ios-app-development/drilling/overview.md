---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to the learning track. Answer before opening an answer, then
repair each kata without looking at the solution. The point is choosing the right owner for state,
work, data, and a platform outcome.

## Recall Q&A

**Q1 (co-01).** Why are a deployment target and build SDK separate decisions?

<details><summary>Answer</summary>The deployment target sets the oldest OS the app supports. The build SDK supplies APIs and submission compliance for the compiler. A current SDK does not force an app to drop older deployment targets.</details>

**Q2 (co-02).** What owns an iOS scene lifecycle?

<details><summary>Answer</summary>The system manages scenes. `@main App` declares them and a view can observe `scenePhase`; neither replaces durable persistence for data that must survive relaunch.</details>

**Q3 (co-05, co-06).** When should a child receive a binding?

<details><summary>Answer</summary>Only when the child edits state owned by its parent or model. A read-only child should receive a value, which keeps mutation authority visible.</details>

**Q4 (co-07, co-08).** What does `@Bindable` add to an `@Observable` model?

<details><summary>Answer</summary>It creates bindings to observable properties for controls such as `TextField`. The model remains the state owner; the view merely gets a controlled editing path.</details>

**Q5 (co-18, co-19).** Why model loading, content, and failure as an enum?

<details><summary>Answer</summary>The enum prevents contradictory states and makes rendering exhaustive. Tests can name every legitimate screen condition without inferring meaning from `nil`.</details>

**Q6 (co-21–24).** Why should a view model receive a service and use `@MainActor`?

<details><summary>Answer</summary>Injection lets tests provide a fake and keeps transport out of the view model. Main-actor isolation makes UI-state mutation explicit while awaited service work can suspend safely.</details>

**Q7 (co-23, co-25).** What does an actor guarantee, and what does it not guarantee?

<details><summary>Answer</summary>An actor serializes access to its own mutable state. It does not make arbitrary external work safe, eliminate cancellation, or replace a model of ownership.</details>

**Q8 (co-26).** What data should a navigation path carry?

<details><summary>Answer</summary>Carry a stable, small value such as a note ID. Resolve mutable detail data from state or storage so restoration has a narrow boundary.</details>

**Q9 (co-28).** How should a permission denial appear in the app?

<details><summary>Answer</summary>As a normal rendered state with an explanation and alternate route where possible. The app must never assume a declaration or earlier grant guarantees access now.</details>

**Q10 (co-29, co-30).** What distinguishes unit testing from UI testing here?

<details><summary>Answer</summary>Unit tests prove model transitions with a fake service. UI tests prove that a running app exposes the intended accessible controls and flow.</details>

## Applied problems

**AP1.** A request finishes after a view disappears. Where should cancellation and the visible result be
decided?

<details><summary>Answer</summary>Start view-related work with `.task` or an owned task and model the result in a `@MainActor` view model. Check cancellation in long operations; do not let an unowned callback mutate a discarded screen.</details>

**AP2.** The network fails but an actor cache has notes. What should the reader see?

<details><summary>Answer</summary>Keep useful cached content visible, expose a non-blocking refresh failure, and offer retry. Do not replace meaningful content with a blank generic error.</details>

**AP3.** A test needs to prove decoded data changes screen state. Which boundary should it use first?

<details><summary>Answer</summary>Unit-test the `@MainActor` view model with a deterministic fake `NoteService`. Add UI tests only for the user-visible rendering and interaction that model tests cannot prove.</details>

## Code katas

### Kata 1: A child mutates copied state

**Symptom**: A child receives `String` and tries to own a second editing value, so parent and child
diverge. Repair it by giving the child an explicit `@Binding`.

### Kata 2: The view constructs `URLSession` work

**Symptom**: A button decodes network data directly, making failure and tests opaque. Move the
operation behind an injected service and an observable view model.

### Kata 3: A cache is a shared mutable dictionary

**Symptom**: Concurrent tasks read and write a global dictionary. Encapsulate it in an actor and
make access `await`-visible.

### Kata 4: Permission denial crashes the feature

**Symptom**: A feature assumes the system prompt grants access. Render a denied state with a safe
alternative instead.

### Kata 5: Navigation passes a full mutable model

**Symptom**: The path serializes or stores a whole note. Pass the stable ID and resolve current data
in the destination.

## Self-check checklist

- [ ] I can keep a SwiftUI view a function of explicit state and events.
- [ ] I can choose `@State`, `@Binding`, `@Observable`, and `@Bindable` by ownership.
- [ ] I can make loading, content, empty, and failed UI states distinct.
- [ ] I can inject a `URLSession`-backed service and replace it with a fake in a test.
- [ ] I can explain actor isolation, main-actor isolation, task lifetime, and cancellation separately.
- [ ] I can use a stable navigation value and persist durable data with SwiftData.
- [ ] I can choose XCTest or XCUITest based on the claim each test must prove.
