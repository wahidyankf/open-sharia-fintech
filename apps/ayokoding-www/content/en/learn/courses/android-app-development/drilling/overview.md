---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to the learning track. Answer each question before opening its
answer, then repair the katas without looking at the after file. The aim is not keyword recall; it
is choosing the correct owner for state, work, data, and a platform event.

## Recall Q&A

**Q1 (co-01).** What does the Gradle wrapper provide that a machine-wide Gradle install does not?

<details><summary>Answer</summary>A project-controlled Gradle version and repeatable entry point. Use ./gradlew so the project, not a shell default, selects the build tool.</details>

**Q2 (co-02).** What belongs in AndroidManifest.xml?

<details><summary>Answer</summary>Declarations the build tools, Android OS, and Play need: components, permissions, and required features. It is not a place for mutable screen state.</details>

**Q3 (co-03).** Which lifecycle callbacks run on a normal launch?

<details><summary>Answer</summary>The visible launch path is onCreate, onStart, then onResume. A stopped Activity returns through onRestart before onStart. The system can later destroy the Activity, and process death can discard all in-memory state without a final callback, so durable data must be persisted.</details>

**Q4 (co-04).** When does an explicit intent beat an implicit intent?

<details><summary>Answer</summary>Use an explicit intent for an in-app component you own. Use an implicit intent when you request a general action, such as opening a URL, and let another app handle it.</details>

**Q5 (co-05).** What does @Composable promise to Compose?

<details><summary>Answer</summary>It marks a function as one that turns inputs into UI. Compose can invoke it again when observed inputs change.</details>

**Q6 (co-06).** What is recomposition not?

<details><summary>Answer</summary>It is not imperative mutation of an existing view tree. Compose recalculates affected UI from current state; it may skip a call only when that call is eligible and its stable inputs are unchanged. Skipping is an optimization, not a correctness contract.</details>

**Q7 (co-07).** What survives recomposition but not process relaunch with remember?

<details><summary>Answer</summary>The object remembered in the current Composition survives recomposition. It is not durable process or configuration-change storage by itself.</details>

**Q8 (co-08).** What two parameters identify a well-hoisted editable value?

<details><summary>Answer</summary>A current value and an event callback, conventionally value: T and onValueChange: (T) -> Unit. The caller owns the mutation.</details>

**Q9 (co-09).** Why does Modifier order matter?

<details><summary>Answer</summary>Each operation wraps or transforms the next one. Padding before a background can produce a different painted area than padding after it.</details>

**Q10 (co-10).** What is Preview for?

<details><summary>Answer</summary>Fast IDE rendering of a composable without launching the app. It complements, but cannot replace, emulator and device verification.</details>

**Q11 (co-11).** When should you choose Box over Column?

<details><summary>Answer</summary>Choose Box when children intentionally stack or overlay; use Column for vertical sequencing and Row for horizontal sequencing.</details>

**Q12 (co-12).** What job does Scaffold perform?

<details><summary>Answer</summary>It provides standard Material screen slots such as top bar, content, navigation, and floating action button while passing safe content padding.</details>

**Q13 (co-13).** Why does LazyColumn suit a large list?

<details><summary>Answer</summary>It composes items on demand around the viewport instead of eagerly building every row. It does not reuse a pool of View instances like RecyclerView, so use stable keys and keep meaningful item state in the appropriate owner.</details>

**Q14 (co-14).** What state should a ViewModel own?

<details><summary>Answer</summary>Screen-level UI state and related business logic that must survive configuration changes. It should not retain a View, Activity, or composable.</details>

**Q15 (co-15).** What does state flows down and events flow up mean?

<details><summary>Answer</summary>The ViewModel exposes a state snapshot to render; the UI sends user intent back through callbacks. The UI does not mutate a duplicate model.</details>

**Q16 (co-16).** Why expose StateFlow rather than MutableStateFlow?

<details><summary>Answer</summary>The ViewModel keeps mutation private while consumers observe an immutable stream. That preserves one state authority.</details>

**Q17 (co-17).** Why model loading, content, and error as a sealed hierarchy?

<details><summary>Answer</summary>It prevents invalid combinations and forces rendering code to account for every legitimate state.</details>

**Q18 (co-18).** What is a repository's contract?

<details><summary>Answer</summary>It is the application-facing boundary that hides whether a value came from cache, database, network, or a test fake.</details>

**Q19 (co-19).** What does Room generate from Entity, Dao, and Database declarations?

<details><summary>Answer</summary>A SQLite-backed persistence layer: entities describe tables, DAOs describe access, and the database exposes DAOs.</details>

**Q20 (co-20).** When should a Room DAO return Flow?

<details><summary>Answer</summary>When callers must observe ongoing table changes. Use a suspend DAO method for one immediate result or write.</details>

**Q21 (co-21).** Why prefer DataStore for new preference work?

<details><summary>Answer</summary>It uses coroutines and Flow for asynchronous preference storage and gives a migration direction away from SharedPreferences.</details>

**Q22 (co-22).** What does Retrofit create from an annotated interface?

<details><summary>Answer</summary>A type-safe HTTP implementation whose suspend methods fit naturally into coroutines.</details>

**Q23 (co-23).** Why is a JSON converter a boundary concern?

<details><summary>Answer</summary>It translates a remote representation into Kotlin values. Keeping it near the API boundary prevents transport details leaking into UI models.</details>

**Q24 (co-24).** Why launch screen work in viewModelScope?

<details><summary>Answer</summary>The scope is owned by the ViewModel and cancels automatically when that ViewModel clears, avoiding work that outlives its screen.</details>

**Q25 (co-25).** What is a Flow?

<details><summary>Answer</summary>A cold asynchronous stream that starts producing when collected and can be transformed before lifecycle-aware collection by the UI.</details>

**Q26 (co-26).** What owns destinations in Navigation Compose?

<details><summary>Answer</summary>A NavHost declares destinations and a NavController performs route and back-stack operations.</details>

**Q27 (co-27).** What must a runtime-permission UI do after denial?

<details><summary>Answer</summary>Keep functioning safely at reduced capability, explain the consequence where useful, and offer a recovery path rather than crashing or looping prompts.</details>

**Q28 (co-28).** How do rememberSaveable and ViewModel differ?

<details><summary>Answer</summary>rememberSaveable preserves small UI state through recreation; ViewModel owns screen data and business logic through configuration change. Neither replaces durable storage.</details>

**Q29 (co-29).** What changes when a ViewModel receives a repository rather than creates one?

<details><summary>Answer</summary>Construction moves to a composition root or DI container, so tests can supply a fake and production can choose the real implementation.</details>

**Q30 (co-30).** What test layers does this course use?

<details><summary>Answer</summary>Local JVM unit tests for pure logic, instrumented tests on an emulator/device for Android integration, and Compose UI tests for rendered behaviour.</details>

## Applied problems

**AP1.** A user rotates while a list refresh is in flight. Where should the list and coroutine live?

<details><summary>Answer</summary>Keep screen data and the refresh in the ViewModel and viewModelScope. The composable collects immutable state; it does not restart the request just because the Activity recreates.</details>

**AP2.** A detail screen needs an item selected from a list. What belongs in a navigation route?

<details><summary>Answer</summary>Pass a stable ID, not a serialized screen object. Resolve the current item through the ViewModel or repository so saved state and process recreation have a narrow, durable boundary.</details>

**AP3.** The network is down but Room contains yesterday's list. What should the user see?

<details><summary>Answer</summary>Render the cached list immediately, surface refresh state or a non-blocking error, and provide retry. Do not replace useful cached content with a blank error screen.</details>

**AP4.** A camera feature is denied. How does the app remain honest and usable?

<details><summary>Answer</summary>Render the denied state, explain the unavailable capability, and offer a settings or alternate-input route. Never assume permission based only on the manifest declaration.</details>

**AP5.** A test needs to verify a state transition after a network response. Which layer should it target first?

<details><summary>Answer</summary>Unit-test the ViewModel with a fake repository and test dispatcher. Add emulator or UI tests only for Android wiring and user-visible rendering that the local test cannot prove.</details>

## Code katas

### Kata 1: UI mutates repository data directly

**Symptom**: A composable owns a mutable list and writes it directly, making rotation and tests unreliable.

Repair drilling/code/kata-01-state-in-composable/before/kata.kt before reading after/kata.kt.

### Kata 2: Detached coroutine outlives the screen

**Symptom**: A click handler launches work without an owner, so cancellation and error delivery are unclear.

Repair drilling/code/kata-02-unscoped-coroutine/before/kata.kt by using an owner-aware scope.

### Kata 3: Room work runs on the main thread

**Symptom**: A DAO result is read synchronously during rendering, blocking the UI and violating Room's contract.

Repair drilling/code/kata-03-room-main-thread/before/kata.kt with a suspend or Flow boundary.

### Kata 4: Permission is treated as already granted

**Symptom**: Camera use starts unconditionally, so denial becomes a crash or broken workflow.

Repair drilling/code/kata-04-permission-assumed/before/kata.kt so denied permission is a rendered state.

### Kata 5: Route argument is stored only in local state

**Symptom**: The selected ID disappears after recreation or back-stack restoration.

Repair drilling/code/kata-05-navigation-lost-state/before/kata.kt with a stable route argument and ViewModel state.

### Kata 6: Error is represented by nullable data only

**Symptom**: A null value cannot distinguish loading, empty, and failed conditions.

Repair drilling/code/kata-06-nonexhaustive-ui-state/before/kata.kt with a sealed UI state.

## Self-check checklist

- [ ] I can explain the manifest, activity, and Compose roles without treating them as one owner.
- [ ] I can make a composable stateless with a value and event callback.
- [ ] I can expose immutable StateFlow from a ViewModel and collect it lifecycle-aware.
- [ ] I can distinguish a repository boundary from a Room DAO and a Retrofit service.
- [ ] I can choose suspend versus Flow for a data operation.
- [ ] I can preserve the right state across recomposition, rotation, navigation, and process loss.
- [ ] I can make permission denial, loading, empty content, and network failure distinct UI states.
- [ ] I can choose local, instrumented, and Compose UI tests for the claim each layer can prove.

## Elaborative interrogation and self-explanation

**Why is a ViewModel not a place to store an Activity or composable reference?**

<details><summary>Answer</summary>The ViewModel can outlive a configuration-specific UI object. Retaining one couples durable state to a destroyed screen and risks leaks; expose state and events instead.</details>

**Why does an offline-first repository improve both speed and failure behaviour?**

<details><summary>Answer</summary>It can render known local data immediately while network refresh proceeds separately. A refresh failure then becomes a visible condition layered over useful data rather than a reason to discard the screen.</details>

**Why does a sealed UI state reduce testing work?**

<details><summary>Answer</summary>It makes the permitted screen cases finite and explicit. Tests can name each case, and the compiler points to renderers that need updating when a new case is introduced.</details>

**Why should permission denial be a designed state rather than an exception path?**

<details><summary>Answer</summary>Users can deny, revoke, or never grant a dangerous permission. Treating denial as normal lets the app offer an accessible alternative instead of failing at the platform boundary.</details>
