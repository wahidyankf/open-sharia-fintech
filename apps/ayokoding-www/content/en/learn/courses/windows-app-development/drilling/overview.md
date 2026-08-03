---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This companion uses active recall and small repairs. Answer before opening an answer; each kata is a
self-contained .NET file and has an intentional broken version beside a repaired one.

## Recall Q&A

**Q1 (co-01 — dotnet-project-model).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The project file declares a Windows target framework, output type, and SDK references so the CLI and desktop host agree on the executable boundary.

</details>

**Q2 (co-02 — nuget-packages).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

A PackageReference identifies a versioned dependency; restore resolves it into the project assets that compilation and the running desktop app use.

</details>

**Q3 (co-03 — ui-stack-choice).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Choose the stack from the product constraints: WinUI 3 for current Windows App SDK features, WPF for mature XAML desktop applications, or WinForms for a designer-oriented event model.

</details>

**Q4 (co-04 — windows-app-sdk).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The Windows App SDK reference supplies WinUI 3 APIs and deployment support independently from the base Windows SDK, so the project must declare a compatible package version.

</details>

**Q5 (co-05 — xaml-markup).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The root window, panels, and controls form a declarative tree; code-behind should configure host-specific behavior rather than recreate the tree imperatively.

</details>

**Q6 (co-06 — layout-panels).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Use StackPanel for sequential flow and Grid for aligned rows and columns, keeping resizing behavior in layout declarations instead of hard-coded pixel coordinates.

</details>

**Q7 (co-07 — controls).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Each control exposes input, command, and display properties that bind to presentation state; keep the control event thin and let the view-model own the resulting behavior.

</details>

**Q8 (co-08 — data-binding).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

One-way binding projects state to the view, two-way binding accepts editing input, and typed x:Bind gives compile-time access to the declared source member.

</details>

**Q9 (co-09 — inotifypropertychanged).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

A model or view-model raises PropertyChanged with the changed property name after its backing value changes so every bound control can refresh.

</details>

**Q10 (co-10 — mvvm-pattern).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The view renders XAML and forwards interactions, the view-model exposes bindable state and commands, and services or models own durable domain and persistence behavior.

</details>

**Q11 (co-11 — commands).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

A command packages an action and CanExecute predicate so a button can disable itself while work is unavailable or already running.

</details>

**Q12 (co-12 — observable-collection).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Add, remove, and replace operations raise collection notifications, allowing a bound ListView to update its items without reconstructing the whole list.

</details>

**Q13 (co-13 — ui-thread-dispatcher).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Controls and UI-affine collections must be changed on their owning dispatcher thread; background work returns data rather than touching visual state directly.

</details>

**Q14 (co-14 — async-await-ui).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Await asynchronous I/O instead of blocking with Result or Wait, allowing the message loop to continue handling paint, input, and cancellation.

</details>

**Q15 (co-15 — dispatcher-marshalling).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

After background work completes, enqueue the state mutation through the host dispatcher so the result is applied on the thread that owns the controls.

</details>

**Q16 (co-16 — cancellation).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Pass the token to every cancellable operation and check or throw from the work loop; cancellation becomes a normal completion path rather than a forced thread stop.

</details>

**Q17 (co-17 — progress-reporting).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

A worker reports percentages through IProgress while the view-model translates them into a bindable value for a progress indicator.

</details>

**Q18 (co-18 — file-io).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

File reads and writes belong behind an explicit persistence boundary, use asynchronous APIs for UI responsiveness, and handle absent or malformed files as recoverable input.

</details>

**Q19 (co-19 — app-settings).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Store compact user preferences such as the last filter in JSON settings, read them on startup, and write the user-selected value without treating settings as a task database.

</details>

**Q20 (co-20 — sqlite-persistence).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The repository opens connections and maps rows to task records, leaving the view-model unaware of SQL, connection lifetime, and database-specific failures.

</details>

**Q21 (co-21 — app-lifecycle).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Activation arguments select the initial route or task, while suspend persists enough state to recreate a useful session when the application resumes.

</details>

**Q22 (co-22 — window-management).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The host creates the window, sets title and size, and keeps it alive; application behavior remains in the view-model so it can be tested without opening that window.

</details>

**Q23 (co-23 — resources-styles).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Resource dictionaries share colors and values, styles share property sets, and control templates redefine a control's visual structure without changing its behavior.

</details>

**Q24 (co-24 — dependency-injection).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Register repository and settings implementations at startup, then inject their interfaces into the view-model so tests can substitute focused fakes.

</details>

**Q25 (co-25 — msix-packaging).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

The manifest names the package identity, entry point, and assets; MSIX then provides a predictable install, update, and uninstall boundary for the desktop application.

</details>

**Q26 (co-26 — unit-testing-viewmodel).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Unit tests create the view-model with fake repositories and settings, invoke commands or async methods, and assert bindable state without needing a Windows UI session.

</details>

**Q27 (co-27 — ui-testing).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

A smoke test should locate the rendered controls, perform one representative action, and verify the visible outcome while leaving detailed logic coverage to headless tests.

</details>

**Q28 (co-28 — error-handling-ui).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Catch expected persistence or validation failures, preserve useful user input, and set a bindable ErrorMessage that the view can show with a retry path.

</details>

**Q29 (co-29 — winforms-survey).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

WinForms favors forms, controls, and event handlers; it is useful when that mature model fits the product, while MVVM-oriented XAML stacks separate presentation state more directly.

</details>

**Q30 (co-30 — deployment).** What is the boundary this concept protects?

<details>
<summary>Answer</summary>

Framework-dependent publishing relies on an installed compatible runtime, while self-contained publishing includes the runtime and trades a larger package for fewer machine prerequisites.

</details>

## Applied Scenarios

1. A Load button freezes the window. Move blocking work behind an awaited service call and bind an
   IsBusy state so the command can disable itself.
2. A worker thread changes a bound collection. Marshal the mutation through the UI dispatcher instead
   of letting the worker touch a UI-owned object.
3. A preference disappears after restart. Store only the preference in settings and put repeatable
   task records behind the SQLite repository.
4. A Save command crashes after a locked database error. Surface a friendly ErrorMessage state and
   retain the unsaved input for a retry.
5. A view-model constructs a concrete database itself. Move construction to the composition root and
   inject an interface so the view-model test can use a fake.

## Hands-on Katas

Run each before file, describe the failure, then compare it with after. Use `dotnet run kata.cs`.

- [Kata 1: Blocking load](./code/kata-01-blocking-load/before/kata.cs)
- [Kata 2: Missing PropertyChanged](./code/kata-02-missing-propertychanged/before/kata.cs)
- [Kata 3: Command ignores CanExecute](./code/kata-03-command-ignores-canexecute/before/kata.cs)
- [Kata 4: Cancellation swallowed](./code/kata-04-cancellation-swallowed/before/kata.cs)
- [Kata 5: Persistence error crashes](./code/kata-05-persistence-error-crashes/before/kata.cs)

## Self-Check Checklist

- [ ] I can choose WinUI 3, WPF, or WinForms for a stated constraint without claiming they are identical.
- [ ] I can explain why bindings need PropertyChanged and collections need collection notifications.
- [ ] I can keep slow work awaited, cancellable, progress-reporting, and off the UI thread.
- [ ] I can test view-model behavior without opening a window.
- [ ] I can distinguish small settings from structured SQLite-backed data and package a Windows app intentionally.

## Elaborative Interrogation

1. Why does MVVM reduce the cost of changing a screen without making all code abstract by default?
2. Why is a dispatcher boundary a platform leak worth acknowledging rather than hiding?
3. Why must cancellation be cooperative rather than a forced thread stop?
4. Why should an error be bound as state instead of displayed only through an exception dialog?
5. Why does packaging belong in the application design rather than the last release checklist?
