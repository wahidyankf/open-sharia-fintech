# 75 · Windows App Development ◆ (By Example, C# †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · C# † · Learn 175 / Drill 275 ·
Nvim-ready Partial · VSCode-ready Partial. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: `◆` app-domain — building a real Windows desktop app: .NET fundamentals, WinUI/WPF (XAML +
data binding + MVVM), async on the UI thread (dispatcher/cancellation), local persistence, packaging
intuition (MSIX), and applied testing. **Tooling note (DD-17)**: Visual Studio / the .NET SDK is the
practical baseline for WinUI/WPF; the topic favours the `dotnet` CLI for build/test/run where possible.

## Why this exists · the big idea

- **The problem before the solution**: a desktop UI freezes the instant you do real work on the thread
  that paints it, and business logic tangled into the view is untestable and unshippable — Windows app
  development exists to keep the UI responsive and the logic maintainable across the .NET/WinUI/packaging
  stack.
- **Keep-this-if-you-forget-everything**: MVVM plus `async`/`await` — never block the UI thread, and keep
  view, view-model, and model separable so long work runs off-thread while the logic stays testable
  without ever opening a window.
- **Big ideas touched**: `coupling-vs-cohesion` — MVVM splits view, state, and logic so each changes
  independently and the view-model is verifiable headless; `layering-and-leaks` — your app rides WinUI →
  Windows App SDK → Win32 → the OS, and the dispatcher/UI-thread rule is exactly where that layering
  bleeds into your code.

## Prerequisites

- **Prior topics**: [topic 74 Just Enough C#](./74-just-enough-csharp.md) (the language + `async`/`await`),
  [topic 14 Frontend Essentials](./14-frontend-essentials.md) (component + state UI, MVVM intuition), and
  [topic 47 Advanced Frontend](./47-advanced-frontend.md) (data binding, state management).
- **Tools & environment**: a **Windows** machine with **Visual Studio** / the **.NET SDK** (WinUI/WPF
  workloads); `dotnet` from the CLI where possible. (WinUI/WPF are Windows-only.)
- **Assumed knowledge**: C# syntax + `async`/`await` (topic 74); MVVM + data-binding thinking (topics
  14/47); local file/DB persistence (topic 10).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: WinUI 3 / WPF / WinForms (XAML, data binding, MVVM) remain actively-supported
  Windows desktop UI stacks; MSIX is still Microsoft's standard packaging format; `dotnet` CLI + xUnit/NUnit
  via `dotnet test`, and SQLite-on-.NET (Microsoft.Data.Sqlite) are current/unchanged.
- 2026-07-12 — verified (TIME-SENSITIVE, re-check at authoring): the **Windows App SDK** (platform under
  WinUI 3) is mid-transition from the 1.x line to 2.x (**2.2.0** released 2026-06-09), licensed **MIT**.
  This moves fast — avoid pinning a specific SDK version in authored content; re-pull at authoring time.
  (github.com/microsoft/WindowsAppSDK)

### DD-35 primary-source citations (fetched-and-read)

Per DD-35, every version/API/framework claim below traces to a primary source fetched and read during
grounding; anything not directly confirmed is flagged `[Needs Verification]` for the authoring pass.

- **WinUI 3 / Windows App SDK** — `[Verified]` WinUI 3 is Microsoft's current native Windows UI framework,
  shipped as part of the Windows App SDK (unified desktop app platform); MIT-licensed
  (learn.microsoft.com/windows/apps/winui/winui3, github.com/microsoft/WindowsAppSDK). Windows App SDK
  version is **`[Needs Verification]` at authoring** — moves fast (2.2.0 seen 2026-06-09); do NOT pin a
  version in authored content; re-pull from the GitHub releases page at authoring time.
- **WPF / WinForms** — `[Verified]` both remain supported .NET desktop UI stacks on Windows; WPF uses XAML
  - data binding, WinForms is the older designer-driven stack (learn.microsoft.com/dotnet/desktop). Both
    are Windows-only.
- **XAML + data binding + MVVM** — `[Verified]` `{Binding}` (runtime) and `{x:Bind}` (compiled) are the two
  binding markup extensions; `INotifyPropertyChanged` drives change notification; MVVM is Microsoft's
  documented desktop pattern (learn.microsoft.com/windows/apps/develop/data-binding). Exact per-control
  binding-mode defaults are `[Needs Verification]` — confirm against the control's reference page at
  authoring time (`{x:Bind}` defaults to OneTime; `{Binding}` defaults to OneWay for most).
- **Dispatcher / UI thread** — `[Verified]` UI updates must occur on the UI thread; `DispatcherQueue`
  (WinUI 3) / `Dispatcher` (WPF) marshal work back to it. `async`/`await` resumes on the captured context
  by default (learn.microsoft.com/windows/apps/design/threading). The exact `DispatcherQueue.TryEnqueue`
  vs `Dispatcher.Invoke` API surface is `[Needs Verification]` per chosen stack (WinUI 3 vs WPF).
- **Cancellation & progress** — `[Verified]` `CancellationToken`/`CancellationTokenSource` and `IProgress<T>`
  are the standard .NET async cancellation + progress primitives (learn.microsoft.com/dotnet/standard/
  parallel-programming/task-cancellation).
- **Persistence** — `[Verified]` `Microsoft.Data.Sqlite` is Microsoft's SQLite ADO.NET provider
  (learn.microsoft.com/dotnet/standard/data/sqlite). App-settings API differs by stack
  (`ApplicationData.Current.LocalSettings` for packaged apps vs config files) — `[Needs Verification]` per
  packaging model at authoring time.
- **MSIX packaging** — `[Verified]` MSIX is Microsoft's standard Windows app packaging format;
  `Package.appxmanifest` declares identity (learn.microsoft.com/windows/msix). Packaging depth kept at
  intuition level per the scope note.
- **Testing** — `[Verified]` xUnit / NUnit run via `dotnet test`; view-models are testable headless
  (learn.microsoft.com/dotnet/core/testing). UI-test intuition only — no specific UI-automation framework
  version is pinned.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · dotnet-project-model** — a .NET desktop app is a `.csproj` project scaffolded/built/run with the `dotnet` CLI (`new`/`build`/`run`) against a Windows target framework.
- **co-02 · nuget-packages** — desktop apps pull dependencies from NuGet via `dotnet add package`.
- **co-03 · ui-stack-choice** — WinUI 3, WPF, and WinForms are the three Windows desktop UI stacks; WinUI 3/WPF use XAML, WinForms is designer-driven (surveyed).
- **co-04 · windows-app-sdk** — WinUI 3 ships as part of the Windows App SDK, the unified modern desktop app platform.
- **co-05 · xaml-markup** — the UI is declared in XAML: a tree of elements the framework renders.
- **co-06 · layout-panels** — layout containers (`StackPanel`, `Grid`) arrange child controls.
- **co-07 · controls** — `Button`, `TextBox`, `ListView`, and other controls compose the interactive surface.
- **co-08 · data-binding** — `{Binding}` (runtime) and `{x:Bind}` (compiled) connect UI properties to a data source; a `DataContext` supplies it.
- **co-09 · inotifypropertychanged** — a model raises `PropertyChanged` (INotifyPropertyChanged) so bindings update the UI on change.
- **co-10 · mvvm-pattern** — MVVM separates View (XAML), ViewModel (state + presentation logic), and Model, keeping the ViewModel testable headless.
- **co-11 · commands** — `ICommand`/`RelayCommand` bind user actions to ViewModel methods, with `CanExecute` gating.
- **co-12 · observable-collection** — `ObservableCollection<T>` bound to a list control updates the UI as items are added/removed.
- **co-13 · ui-thread-dispatcher** — the UI may only be touched on the UI thread; violating this throws.
- **co-14 · async-await-ui** — `async`/`await` runs work without blocking the UI thread, keeping the app responsive.
- **co-15 · dispatcher-marshalling** — work on a background thread marshals updates back to the UI thread via the dispatcher (`DispatcherQueue`/`Dispatcher`).
- **co-16 · cancellation** — `CancellationToken`/`CancellationTokenSource` cancel in-flight async work cooperatively.
- **co-17 · progress-reporting** — `IProgress<T>` reports incremental progress from a long task to the UI.
- **co-18 · file-io** — `System.IO` reads and writes files for app data.
- **co-19 · app-settings** — app settings persist across launches (local settings / config).
- **co-20 · sqlite-persistence** — `Microsoft.Data.Sqlite` stores structured data in a local SQLite database.
- **co-21 · app-lifecycle** — an app has a startup/activation/suspend/resume lifecycle (`App.xaml`/`OnLaunched`).
- **co-22 · window-management** — the OS window (title, message loop) is a first-class object the app owns.
- **co-23 · resources-styles** — XAML resources, styles, and templates centralize and reuse visual definitions.
- **co-24 · dependency-injection** — a DI container registers services and injects them into ViewModels.
- **co-25 · msix-packaging** — MSIX is the Windows packaging format; `Package.appxmanifest` declares app identity (intuition level).
- **co-26 · unit-testing-viewmodel** — xUnit/NUnit tests run via `dotnet test` verify ViewModel logic without opening a window.
- **co-27 · ui-testing** — UI-automation smoke testing verifies the assembled UI flow (intuition level).
- **co-28 · error-handling-ui** — errors are caught and surfaced to the user (dialogs / bound error state) rather than crashing.
- **co-29 · winforms-survey** — WinForms is the older event-driven designer stack, surveyed for contrast.
- **co-30 · deployment** — `dotnet publish` (self-contained vs framework-dependent) produces a deployable app.

## Worked examples

Colocated under `windows-app-development/learning/code/`; each runnable/testable via `dotnet` (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · dotnet-new-winui** — scaffold a WinUI/WPF app with `dotnet new` — verify it builds. (co-01, co-04)
- **ex-02 · project-file** — inspect the `.csproj` target framework — verify the Windows TFM. (co-01)
- **ex-03 · dotnet-run-window** — `dotnet run` the app — verify a window appears. (co-01, co-22)
- **ex-04 · add-nuget** — `dotnet add package` a library — verify it restores. (co-02)
- **ex-05 · stack-choice** — scaffold WinUI/WPF/WinForms templates — verify each builds. (co-03)
- **ex-06 · windows-app-sdk-ref** — reference the Windows App SDK — verify the package resolves. (co-04)
- **ex-07 · xaml-window** — a XAML window with a `TextBlock` — verify the text renders. (co-05)
- **ex-08 · xaml-hierarchy** — nested XAML elements — verify the visual tree. (co-05)
- **ex-09 · stackpanel** — a `StackPanel` of controls — verify vertical layout. (co-06)
- **ex-10 · grid-layout** — a `Grid` with rows/columns — verify placement. (co-06)
- **ex-11 · button-click** — a `Button` with a `Click` handler — verify it fires. (co-07)
- **ex-12 · textbox** — a `TextBox` — verify input. (co-07)
- **ex-13 · listview** — a `ListView` of items — verify rendering. (co-07)
- **ex-14 · oneway-binding** — `{Binding}` a property to a `TextBlock` — verify display. (co-08)
- **ex-15 · twoway-binding** — two-way bind a `TextBox` — verify the round-trip. (co-08)
- **ex-16 · xbind** — `{x:Bind}` compiled binding — verify it resolves. (co-08)
- **ex-17 · datacontext** — set a `DataContext` — verify bindings pick it up. (co-08)
- **ex-18 · static-resource** — a XAML resource + `StaticResource` — verify reuse. (co-23)
- **ex-19 · style** — a `Style` targeting a control — verify it applies. (co-23)
- **ex-20 · read-file** — read a text file — verify the contents. (co-18)
- **ex-21 · write-file** — write a text file — verify persistence. (co-18)
- **ex-22 · app-startup** — `App.xaml` `OnLaunched` — verify startup runs. (co-21)
- **ex-23 · window-title** — set the window title — verify it shows. (co-22)
- **ex-24 · winforms-form** — a WinForms `Form` with a button — verify it runs. (co-29)
- **ex-25 · error-dialog** — show a `ContentDialog` on error — verify it appears. (co-28)
- **ex-26 · test-project** — `dotnet new xunit` test project — verify `dotnet test` green. (co-26)

### Intermediate

- **ex-27 · inpc-model** — a model implementing `INotifyPropertyChanged` — verify `PropertyChanged` fires. (co-09)
- **ex-28 · bind-inpc** — bind to an INPC property + mutate it — verify the UI updates. (co-09, co-08)
- **ex-29 · viewmodel** — a ViewModel class exposing state — verify it's separable from the View. (co-10)
- **ex-30 · mvvm-wiring** — wire View→ViewModel via `DataContext` — verify binding. (co-10, co-08)
- **ex-31 · relaycommand** — an `ICommand`/`RelayCommand` — verify `Execute` fires. (co-11)
- **ex-32 · command-canexecute** — `CanExecute` gating a button — verify it enables/disables. (co-11)
- **ex-33 · button-command-bind** — bind a `Button.Command` — verify the command runs. (co-11, co-08)
- **ex-34 · observable-collection** — an `ObservableCollection` bound to a `ListView` — verify an add updates the UI. (co-12)
- **ex-35 · collection-mutation** — add/remove items — verify the live UI. (co-12)
- **ex-36 · async-load** — an async `Task` load in the ViewModel — verify it awaits. (co-14)
- **ex-37 · async-command** — an async command handler — verify the UI stays responsive. (co-14, co-11)
- **ex-38 · dispatcher-enqueue** — `DispatcherQueue.TryEnqueue` back to the UI — verify marshalling. (co-15, co-13)
- **ex-39 · ui-thread-violation** — a cross-thread update without dispatch — verify it throws. (co-13)
- **ex-40 · background-to-ui** — update a bound property from a background task via the dispatcher — verify the UI reflects it. (co-15)
- **ex-41 · settings-write** — write an app setting — verify persistence. (co-19)
- **ex-42 · settings-read** — read a setting back on relaunch — verify the round-trip. (co-19)
- **ex-43 · sqlite-open** — open a `Microsoft.Data.Sqlite` connection — verify it connects. (co-20, co-02)
- **ex-44 · sqlite-insert** — insert a row — verify it's stored. (co-20)
- **ex-45 · sqlite-query** — query rows into the ViewModel — verify results. (co-20)
- **ex-46 · di-register** — register services in a DI container — verify resolution. (co-24)
- **ex-47 · di-viewmodel** — inject a service into a ViewModel — verify it's used. (co-24, co-10)
- **ex-48 · resource-dictionary** — a merged `ResourceDictionary` — verify shared styles. (co-23)
- **ex-49 · control-template** — a `ControlTemplate` — verify custom visuals. (co-23)
- **ex-50 · vm-unit-test** — `dotnet test` a ViewModel's logic headless — verify no window is needed. (co-26, co-10)
- **ex-51 · command-unit-test** — unit-test an `ICommand`'s `CanExecute` — verify the logic. (co-26, co-11)
- **ex-52 · error-surface** — catch an exception in the ViewModel + expose an error property — verify the UI binds it. (co-28, co-08)
- **ex-53 · activation-args** — handle activation arguments — verify the lifecycle path. (co-21)
- **ex-54 · winforms-async** — a WinForms async event handler — verify it's non-blocking. (co-29, co-14)

### Advanced

- **ex-55 · cancellation-token** — pass a `CancellationToken` to async work — verify it plumbs through. (co-16)
- **ex-56 · cancel-button** — a cancel button triggering `CancellationTokenSource.Cancel` — verify the work stops. (co-16, co-11)
- **ex-57 · cancellation-exception** — handle `OperationCanceledException` — verify a graceful stop. (co-16)
- **ex-58 · iprogress** — report progress via `IProgress<T>` — verify updates arrive. (co-17)
- **ex-59 · progress-bar** — bind a `ProgressBar` to progress — verify it advances. (co-17, co-08)
- **ex-60 · progress-plus-cancel** — a long task with both progress and cancel — verify both work. (co-17, co-16)
- **ex-61 · dispatcher-progress** — marshal progress back to the UI thread — verify safe updates. (co-15, co-17)
- **ex-62 · non-blocking-proof** — the UI responds during a long async task — verify responsiveness. (co-14, co-13)
- **ex-63 · sqlite-round-trip** — write then read across relaunch — verify persistence survives. (co-20, co-18)
- **ex-64 · settings-plus-db** — persist settings + DB together — verify both survive relaunch. (co-19, co-20)
- **ex-65 · lifecycle-suspend** — handle suspend/resume — verify state is saved. (co-21)
- **ex-66 · msix-manifest** — inspect the `Package.appxmanifest` — verify app identity. (co-25)
- **ex-67 · msix-package** — packaging intuition via the manifest — verify the packaged identity. (co-25)
- **ex-68 · deploy-self-contained** — `dotnet publish` self-contained — verify the output runs standalone. (co-30, co-01)
- **ex-69 · deploy-framework-dependent** — a framework-dependent publish — verify the smaller output. (co-30)
- **ex-70 · winforms-vs-winui** — the same tiny app in WinForms vs WinUI — verify both run. (co-29, co-03)
- **ex-71 · di-full-app** — a DI-wired app resolving ViewModel + services — verify composition. (co-24, co-10)
- **ex-72 · vm-async-test** — unit-test an async ViewModel method with a fake service — verify the awaited result. (co-26, co-14)
- **ex-73 · ui-test-intuition** — a UI-automation smoke check — verify the flow. (co-27)
- **ex-74 · error-recovery** — recover from a persistence error + surface it — verify a graceful UI. (co-28, co-20)
- **ex-75 · templated-list** — an `ObservableCollection` + `DataTemplate` in a `ListView` — verify per-item visuals. (co-12, co-23)
- **ex-76 · full-mvvm-slice** — View + ViewModel + model + command + async load — verify they compose. (co-10, co-11, co-14)
- **ex-77 · integration-persistence-slice** — an MVVM ViewModel loading from SQLite with progress + cancel — verify end-to-end. (co-10, co-20, co-16, co-17)
- **ex-78 · capstone-desktop-app** — a WinUI/WPF MVVM app: data binding, async off-UI load with cancel + progress, SQLite + settings round-trip, covered by `dotnet test` — verify build/run on Windows + tests pass. (co-05, co-08, co-10, co-14, co-16, co-17, co-19, co-20, co-26)

## Capstone spec — intra-topic (subject → full runnable app)

- **Goal**: build a small but complete Windows desktop app — a WinUI/WPF XAML UI under MVVM with data
  binding, an async data load off the UI thread with cancellation + progress reporting, and a local
  SQLite/settings persistence round-trip — covered by xUnit/NUnit tests, buildable/testable via
  `dotnet`.
- **Concepts exercised**: [ ] XAML + data binding (co-05, co-08) [ ] MVVM + an observable model (co-10, co-12)
  [ ] `async`/`await` off the UI thread + the dispatcher (co-14, co-15) [ ] cancellation + progress reporting
  (co-16, co-17) [ ] a persistence + settings round-trip (co-20, co-19) [ ] `dotnet test` unit tests (co-26).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a XAML window under MVVM with data binding + a command. Verify the UI
     binds to the model and `dotnet test` runs.
  2. Add an async data load with cancellation + progress. Verify the UI stays responsive, progress updates,
     and a cancel stops the work (a unit test covers the view-model logic).
  3. Add a SQLite + settings persistence round-trip. Verify data + settings survive relaunch.
- **Acceptance criteria**: the app builds + runs on Windows; the UI binds via MVVM; async work is
  cancellable and non-blocking; persistence survives relaunch; `dotnet test` passes.
- **Done bar**: runnable end-to-end (Windows) + tests green + web-verified.

## Read more

**Books**

- **Programming Windows**, 5th ed. — Charles Petzold (1998, Microsoft Press). The classic Win32 API programming bible; foundational for understanding the Windows app model even as APIs evolved.
- **Windows via C/C++**, 5th ed. — Jeffrey Richter & Christophe Nasarre (2007, Microsoft Press). The canonical deep-dive into Windows process, thread, and memory primitives underlying desktop app frameworks.

**Papers & articles**

- **WinUI 3 documentation** — Microsoft, official (Microsoft Learn). The authoritative reference for Microsoft's current native Windows UI framework. <https://learn.microsoft.com/en-us/windows/apps/winui/winui3/>
- **Windows App SDK documentation** — Microsoft, official (Microsoft Learn). The canonical reference for the modern unified Windows desktop app platform. <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/>

---

← Previous: [74 · Just Enough C#](./74-just-enough-csharp.md) · Next: [76 · Linux App Development](./76-linux-app-development.md) →
