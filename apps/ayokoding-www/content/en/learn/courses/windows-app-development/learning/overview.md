---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

## The working model

Every example keeps one rule in view: the view renders state, the view-model owns presentation logic,
and services own I/O. A UI thread is a constrained resource, so long work reports progress and honors
cancellation; background results cross back through the dispatcher rather than mutating UI state directly.

## Concept register

- **co-01 · dotnet-project-model** — a desktop app is a Windows-targeted .NET project that the dotnet CLI can build and run.
- **co-02 · nuget-packages** — NuGet restores the packages that a desktop project declares.
- **co-03 · ui-stack-choice** — WinUI 3, WPF, and WinForms trade modern platform integration, XAML, and designer-first workflows.
- **co-04 · windows-app-sdk** — WinUI 3 is delivered through the Windows App SDK.
- **co-05 · xaml-markup** — XAML declares a visual tree that the host renders.
- **co-06 · layout-panels** — StackPanel and Grid arrange controls instead of leaving coordinates scattered through code.
- **co-07 · controls** — controls such as Button, TextBox, and ListView provide the interactive surface.
- **co-08 · data-binding** — Binding and x:Bind connect properties to presentation state.
- **co-09 · inotifypropertychanged** — PropertyChanged tells bindings that an observable value changed.
- **co-10 · mvvm-pattern** — MVVM separates view, presentation logic, and domain state.
- **co-11 · commands** — ICommand turns an interaction into testable intent and can gate execution.
- **co-12 · observable-collection** — ObservableCollection reports list mutations to bound controls.
- **co-13 · ui-thread-dispatcher** — only the UI thread may update UI-owned state.
- **co-14 · async-await-ui** — await keeps work from freezing a responsive desktop UI.
- **co-15 · dispatcher-marshalling** — a dispatcher returns background results to the UI thread safely.
- **co-16 · cancellation** — CancellationToken makes long work cooperatively stoppable.
- **co-17 · progress-reporting** — IProgress reports incremental work without coupling a service to a view.
- **co-18 · file-io** — System.IO provides local file read and write boundaries.
- **co-19 · app-settings** — settings persist small preferences across launches.
- **co-20 · sqlite-persistence** — SQLite stores structured local data behind a repository boundary.
- **co-21 · app-lifecycle** — startup and activation establish the app's first state; suspend/resume preserve it.
- **co-22 · window-management** — a desktop application owns and configures its OS window.
- **co-23 · resources-styles** — resources, styles, and templates centralize visual decisions.
- **co-24 · dependency-injection** — a composition root provides services to view-models rather than constructing them ad hoc.
- **co-25 · msix-packaging** — MSIX declares a Windows app's package identity and installation boundary.
- **co-26 · unit-testing-viewmodel** — headless unit tests validate view-model behavior with dotnet test.
- **co-27 · ui-testing** — a narrow UI smoke test confirms the assembled, user-visible path.
- **co-28 · error-handling-ui** — a view-model surfaces recoverable errors as bound state instead of crashing.
- **co-29 · winforms-survey** — WinForms provides an event-driven, designer-oriented comparison point.
- **co-30 · deployment** — dotnet publish creates framework-dependent or self-contained distribution output.

## Run the examples

Each `learning/code/ex-NN-<slug>/Program.cs` is a file-based .NET 10 console probe. From that
directory, run `dotnet run Program.cs`. The probe validates the example's state or command contract;
when the example names a desktop host, complete its window-level step on Windows. The capstone is the
one multi-file project and runs through `dotnet test` plus its WPF host.

## Examples by Level

### Beginner (Examples 1–26)

- [Example 1: Dotnet New WinUI](/en/learn/courses/windows-app-development/learning/beginner#example-1-dotnet-new-winui)
- [Example 2: Project File](/en/learn/courses/windows-app-development/learning/beginner#example-2-project-file)
- [Example 3: Dotnet Run Window](/en/learn/courses/windows-app-development/learning/beginner#example-3-dotnet-run-window)
- [Example 4: Add NuGet](/en/learn/courses/windows-app-development/learning/beginner#example-4-add-nuget)
- [Example 5: Stack Choice](/en/learn/courses/windows-app-development/learning/beginner#example-5-stack-choice)
- [Example 6: Windows App SDK Reference](/en/learn/courses/windows-app-development/learning/beginner#example-6-windows-app-sdk-reference)
- [Example 7: XAML Window](/en/learn/courses/windows-app-development/learning/beginner#example-7-xaml-window)
- [Example 8: XAML Hierarchy](/en/learn/courses/windows-app-development/learning/beginner#example-8-xaml-hierarchy)
- [Example 9: StackPanel](/en/learn/courses/windows-app-development/learning/beginner#example-9-stackpanel)
- [Example 10: Grid Layout](/en/learn/courses/windows-app-development/learning/beginner#example-10-grid-layout)
- [Example 11: Button Click](/en/learn/courses/windows-app-development/learning/beginner#example-11-button-click)
- [Example 12: TextBox](/en/learn/courses/windows-app-development/learning/beginner#example-12-textbox)
- [Example 13: ListView](/en/learn/courses/windows-app-development/learning/beginner#example-13-listview)
- [Example 14: One-Way Binding](/en/learn/courses/windows-app-development/learning/beginner#example-14-one-way-binding)
- [Example 15: Two-Way Binding](/en/learn/courses/windows-app-development/learning/beginner#example-15-two-way-binding)
- [Example 16: XBind](/en/learn/courses/windows-app-development/learning/beginner#example-16-xbind)
- [Example 17: DataContext](/en/learn/courses/windows-app-development/learning/beginner#example-17-datacontext)
- [Example 18: Static Resource](/en/learn/courses/windows-app-development/learning/beginner#example-18-static-resource)
- [Example 19: Style](/en/learn/courses/windows-app-development/learning/beginner#example-19-style)
- [Example 20: Read File](/en/learn/courses/windows-app-development/learning/beginner#example-20-read-file)
- [Example 21: Write File](/en/learn/courses/windows-app-development/learning/beginner#example-21-write-file)
- [Example 22: App Startup](/en/learn/courses/windows-app-development/learning/beginner#example-22-app-startup)
- [Example 23: Window Title](/en/learn/courses/windows-app-development/learning/beginner#example-23-window-title)
- [Example 24: WinForms Form](/en/learn/courses/windows-app-development/learning/beginner#example-24-winforms-form)
- [Example 25: Error Dialog](/en/learn/courses/windows-app-development/learning/beginner#example-25-error-dialog)
- [Example 26: Test Project](/en/learn/courses/windows-app-development/learning/beginner#example-26-test-project)

### Intermediate (Examples 27–54)

- [Example 27: INPC Model](/en/learn/courses/windows-app-development/learning/intermediate#example-27-inpc-model)
- [Example 28: Bind INPC](/en/learn/courses/windows-app-development/learning/intermediate#example-28-bind-inpc)
- [Example 29: ViewModel](/en/learn/courses/windows-app-development/learning/intermediate#example-29-viewmodel)
- [Example 30: MVVM Wiring](/en/learn/courses/windows-app-development/learning/intermediate#example-30-mvvm-wiring)
- [Example 31: RelayCommand](/en/learn/courses/windows-app-development/learning/intermediate#example-31-relaycommand)
- [Example 32: Command CanExecute](/en/learn/courses/windows-app-development/learning/intermediate#example-32-command-canexecute)
- [Example 33: Button Command Bind](/en/learn/courses/windows-app-development/learning/intermediate#example-33-button-command-bind)
- [Example 34: Observable Collection](/en/learn/courses/windows-app-development/learning/intermediate#example-34-observable-collection)
- [Example 35: Collection Mutation](/en/learn/courses/windows-app-development/learning/intermediate#example-35-collection-mutation)
- [Example 36: Async Load](/en/learn/courses/windows-app-development/learning/intermediate#example-36-async-load)
- [Example 37: Async Command](/en/learn/courses/windows-app-development/learning/intermediate#example-37-async-command)
- [Example 38: Dispatcher Enqueue](/en/learn/courses/windows-app-development/learning/intermediate#example-38-dispatcher-enqueue)
- [Example 39: UI Thread Violation](/en/learn/courses/windows-app-development/learning/intermediate#example-39-ui-thread-violation)
- [Example 40: Background to UI](/en/learn/courses/windows-app-development/learning/intermediate#example-40-background-to-ui)
- [Example 41: Settings Write](/en/learn/courses/windows-app-development/learning/intermediate#example-41-settings-write)
- [Example 42: Settings Read](/en/learn/courses/windows-app-development/learning/intermediate#example-42-settings-read)
- [Example 43: SQLite Open](/en/learn/courses/windows-app-development/learning/intermediate#example-43-sqlite-open)
- [Example 44: SQLite Insert](/en/learn/courses/windows-app-development/learning/intermediate#example-44-sqlite-insert)
- [Example 45: SQLite Query](/en/learn/courses/windows-app-development/learning/intermediate#example-45-sqlite-query)
- [Example 46: DI Register](/en/learn/courses/windows-app-development/learning/intermediate#example-46-di-register)
- [Example 47: DI ViewModel](/en/learn/courses/windows-app-development/learning/intermediate#example-47-di-viewmodel)
- [Example 48: Resource Dictionary](/en/learn/courses/windows-app-development/learning/intermediate#example-48-resource-dictionary)
- [Example 49: Control Template](/en/learn/courses/windows-app-development/learning/intermediate#example-49-control-template)
- [Example 50: VM Unit Test](/en/learn/courses/windows-app-development/learning/intermediate#example-50-vm-unit-test)
- [Example 51: Command Unit Test](/en/learn/courses/windows-app-development/learning/intermediate#example-51-command-unit-test)
- [Example 52: Error Surface](/en/learn/courses/windows-app-development/learning/intermediate#example-52-error-surface)
- [Example 53: Activation Args](/en/learn/courses/windows-app-development/learning/intermediate#example-53-activation-args)
- [Example 54: WinForms Async](/en/learn/courses/windows-app-development/learning/intermediate#example-54-winforms-async)

### Advanced (Examples 55–78)

- [Example 55: Cancellation Token](/en/learn/courses/windows-app-development/learning/advanced#example-55-cancellation-token)
- [Example 56: Cancel Button](/en/learn/courses/windows-app-development/learning/advanced#example-56-cancel-button)
- [Example 57: Cancellation Exception](/en/learn/courses/windows-app-development/learning/advanced#example-57-cancellation-exception)
- [Example 58: IProgress](/en/learn/courses/windows-app-development/learning/advanced#example-58-iprogress)
- [Example 59: Progress Bar](/en/learn/courses/windows-app-development/learning/advanced#example-59-progress-bar)
- [Example 60: Progress Plus Cancel](/en/learn/courses/windows-app-development/learning/advanced#example-60-progress-plus-cancel)
- [Example 61: Dispatcher Progress](/en/learn/courses/windows-app-development/learning/advanced#example-61-dispatcher-progress)
- [Example 62: Non-Blocking Proof](/en/learn/courses/windows-app-development/learning/advanced#example-62-non-blocking-proof)
- [Example 63: SQLite Round Trip](/en/learn/courses/windows-app-development/learning/advanced#example-63-sqlite-round-trip)
- [Example 64: Settings Plus DB](/en/learn/courses/windows-app-development/learning/advanced#example-64-settings-plus-db)
- [Example 65: Lifecycle Suspend](/en/learn/courses/windows-app-development/learning/advanced#example-65-lifecycle-suspend)
- [Example 66: MSIX Manifest](/en/learn/courses/windows-app-development/learning/advanced#example-66-msix-manifest)
- [Example 67: MSIX Package](/en/learn/courses/windows-app-development/learning/advanced#example-67-msix-package)
- [Example 68: Deploy Self-Contained](/en/learn/courses/windows-app-development/learning/advanced#example-68-deploy-self-contained)
- [Example 69: Deploy Framework Dependent](/en/learn/courses/windows-app-development/learning/advanced#example-69-deploy-framework-dependent)
- [Example 70: WinForms vs WinUI](/en/learn/courses/windows-app-development/learning/advanced#example-70-winforms-vs-winui)
- [Example 71: DI Full App](/en/learn/courses/windows-app-development/learning/advanced#example-71-di-full-app)
- [Example 72: VM Async Test](/en/learn/courses/windows-app-development/learning/advanced#example-72-vm-async-test)
- [Example 73: UI Test Intuition](/en/learn/courses/windows-app-development/learning/advanced#example-73-ui-test-intuition)
- [Example 74: Error Recovery](/en/learn/courses/windows-app-development/learning/advanced#example-74-error-recovery)
- [Example 75: Templated List](/en/learn/courses/windows-app-development/learning/advanced#example-75-templated-list)
- [Example 76: Full MVVM Slice](/en/learn/courses/windows-app-development/learning/advanced#example-76-full-mvvm-slice)
- [Example 77: Integration Persistence Slice](/en/learn/courses/windows-app-development/learning/advanced#example-77-integration-persistence-slice)
- [Example 78: Capstone Desktop App](/en/learn/courses/windows-app-development/learning/advanced#example-78-capstone-desktop-app)
