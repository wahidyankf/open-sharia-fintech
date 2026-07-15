# 15 · Software Testing (By Example, Python + TS)

**prd row**: Pass 1 · Core Foundations · By Example · Python + TS · Learn 115 / Drill 215 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: testing as a discipline across both stacks — unit through integration, test doubles, TDD,
property-based testing, and BDD / executable specifications (Gherkin + pytest-bdd/behave) folded in. Deep
CI wiring cross-refs
[`30-software-engineering-practices`](./30-software-engineering-practices.md). This topic underpins the
Regression Test Mandate the whole repo enforces.

## Why this exists · the big idea

- **The problem before the solution**: you cannot prove code works by re-reading it, and regressions
  creep back in silently as the system grows — a test is how you make "it works" durable and repeatable.
- **Keep-this-if-you-forget-everything**: a test encodes an expectation as executable truth; the pyramid
  (many fast unit tests, few slow end-to-end ones) trades breadth of confidence against speed of feedback.
- **Big ideas touched**: `correctness-vs-pragmatism` — coverage is a proxy, not proof; pyramid-vs-trophy
  and mutation testing are all judgments about how much verification a given risk actually earns.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md) and
  [topic 13 Just Enough TypeScript](./13-just-enough-typescript.md) (examples span both);
  [topic 11 Backend Essentials](./11-backend-essentials.md) provides the app the integration test targets.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with **pytest** + **Hypothesis**;
  **Node.js** with **Vitest**/Jest + **fast-check**; optional mutation tools (mutmut/Stryker).
- **Assumed knowledge**: reading/writing basic Python and TypeScript; running a program from the CLI.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring.

- 2026-07-12 — verified: **pytest 9.1.1**, **Hypothesis 6.156.6**, **Vitest 4.1.10**, **fast-check 4.9.0**
  — all current/CVE-clean. Pact contract testing is current (`pact-python` latest 2026-05-04; PactV3/V4 +
  Matchers V3). Mutation testing: **`mutmut` 3.6.0** (Python). (pypi.org / npmjs.com)
- 2026-07-12 — verified (CORRECTION): the JS/TS mutation tool is **`@stryker-mutator/core` 9.6.1** — the
  bare `stryker` npm package is abandoned (last publish 7 years ago); reference the scoped package only.
  (npmjs.com)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: PyPI/npm registries, `docs.pytest.org`,
> `docs.python.org/unittest.mock`, `hypothesis.readthedocs.io`, `coverage.readthedocs.io`, and primary
> author articles/publisher records. All version pins + API claims verified; 1 attribution corrected.

- **Version pins** — pytest **9.1.1** (MIT), Hypothesis **6.156.6** (MPL-2.0), Vitest **4.1.10**,
  fast-check **4.9.0**, mutmut **3.6.0** (BSD-3), `@stryker-mutator/core` **9.6.1** (bare `stryker`
  abandoned, ~7yr), pact-python **3.4.0** (2026-05-04, PactV3/V4) — all confirmed latest on
  [PyPI](https://pypi.org/project/pytest/)/[npm](https://registry.npmjs.org/vitest/latest).
- **pytest API (co-02..09/21, ex-01..28/53)** — [docs.pytest.org](https://docs.pytest.org/en/stable/):
  `test_*.py`/`test_*` discovery, assert rewriting, `pytest.raises(match=…)` (uses `re.search`),
  `@pytest.fixture` scopes + `yield` teardown, `@pytest.mark.parametrize`/`ids`, `pytest.approx`
  (`0.1+0.2 == approx(0.3)` verbatim), `skip`/`xfail`/`-k`/`-m`, `conftest.py`, "N passed" output; branch
  coverage `--branch` per [coverage.py](https://coverage.readthedocs.io/en/latest/branch.html).
- **Test doubles (co-11..16, ex-29..40/77)** — **corrected**: the dummy/stub/spy/mock/fake taxonomy is
  **Meszaros's** (_xUnit Test Patterns_, 2007), which Fowler's
  [_Mocks Aren't Stubs_](https://martinfowler.com/articles/mocksArentStubs.html) explicitly credits
  ("follow the vocabulary of Gerard Meszaros's book") — co-11/ex-77 re-attributed from "Fowler". API
  (`MagicMock`, `mock.patch`, `assert_called_once_with`, `side_effect`, `monkeypatch.setattr/setenv`)
  verbatim from [unittest.mock](https://docs.python.org/3/library/unittest.mock.html).
- **Pyramid / trophy (co-10, ex-61/62/79)** — pyramid credited to Mike Cohn (_Succeeding with Agile_, 2009) per [Fowler's TestPyramid bliki](https://martinfowler.com/bliki/TestPyramid.html); "testing
  trophy" is Kent C. Dodds (2018,
  [kentcdodds.com](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)) — both
  added to Read more.
- **Property-based (co-18..20, ex-43..50)** — [Hypothesis strategies](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html):
  `st.integers()`/`st.text()`, `@st.composite` + `draw`, `assume()`, `@example` all confirmed.
- **Read more** — Beck _TDD by Example_ (2002), Freeman & Pryce _GOOS_ (2009), Meszaros _xUnit Test
  Patterns_ (2007) — all author/year confirmed; Claessen & Hughes QuickCheck (ICFP 2000) URL swapped to
  durable [ACM DL](https://dl.acm.org/doi/10.1145/351240.351266) (was a course-archive mirror).
- **BDD fold (co-28..32, ex-81..86)** — added 2026-07-12. BDD term coined by **Dan North**
  ([_Introducing BDD_](https://dannorth.net/introducing-bdd/), 2006). Gherkin's
  `Feature`/`Scenario`/`Given`/`When`/`Then`/`And`/`But` grammar and `Scenario Outline` + `Examples`
  table are from the [Cucumber Gherkin reference](https://cucumber.io/docs/gherkin/reference/); Python
  runners [`pytest-bdd`](https://pytest-bdd.readthedocs.io/) (MIT) and
  [`behave`](https://behave.readthedocs.io/) (BSD-2). Concepts (Given/When/Then framing, step-definition
  binding, outline-over-examples, BDD/ATDD-vs-TDD placement) authored from established knowledge and
  confirmed accurate by the 2026-07-15 `web-researcher` verification sweep below — no corrections
  needed to the prose, only version/license/date pins.
- 2026-07-15 — verified (`web-researcher`, DD-35 resolution — the last remaining "to verify" line):
  **pytest-bdd 8.1.0** (MIT; released 2024-12-05 — actively maintained per continued GitHub
  commits/issues despite the ~19-month-stale release, no known CVEs) — `@given`/`@when`/`@then`
  decorators from `pytest_bdd` bind Gherkin steps to functions via pytest-fixture-style injection;
  `parsers.parse("...{n:d}...")`/`parsers.cfparse(...)` extract typed named parameters;
  `scenarios('features/')` auto-binds every scenario under a path, `@scenario('file.feature', 'Name')`
  binds one scenario to one test function; `target_fixture=` lets a step publish a fixture for later
  steps. **behave 1.3.3** (BSD-2; released 2025-09-04; Snyk "Healthy", no known CVEs) —
  `@given`/`@when`/`@then`/`@step` decorators from `behave` bind Gherkin text to functions taking
  `context` as the first argument; `context` carries state across a scenario's steps;
  `features/environment.py` supplies `before_all`/`after_all`/`before_feature`/`after_feature`/
  `before_scenario`/`after_scenario`/`before_step`/`after_step` hooks. **`@cucumber/cucumber`
  (Cucumber.js) 13.1.0** (MIT; released 2026-07-14, no known CVEs — an unrelated typosquat package
  named bare `cucumber-js` exists, not the scoped package used here) — `Given`/`When`/`Then` functions
  imported from `@cucumber/cucumber`; step-definition callbacks must be non-arrow `function`
  expressions to access the shared `World` instance via `this` (arrow functions cannot bind `this`).
  Sources: [PyPI pytest-bdd](https://pypi.org/project/pytest-bdd/),
  [pytest-bdd README](https://github.com/pytest-dev/pytest-bdd/blob/master/README.rst),
  [PyPI behave](https://pypi.org/project/behave/),
  [behave tutorial](https://behave.readthedocs.io/en/latest/tutorial/),
  [npm @cucumber/cucumber](https://registry.npmjs.org/@cucumber/cucumber/latest),
  [cucumber-js step-definitions docs](https://github.com/cucumber/cucumber-js/blob/main/docs/support_files/step_definitions.md).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · why-test-and-aaa** — a test encodes an expectation as executable truth, structured as
  arrange–act–assert so intent is legible.
- **co-02 · test-discovery-and-run** — `pytest` discovers `test_*.py` files and `test_*` functions and runs
  them from the CLI, including a single named test.
- **co-03 · assertions** — plain `assert` plus pytest's expression introspection reports the failing
  operands, no assertion-method zoo required.
- **co-04 · exception-testing** — `pytest.raises(Error, match=…)` asserts a block raises the expected
  exception (and message).
- **co-05 · fixtures** — `@pytest.fixture` provides reusable setup/teardown injected by parameter name, with
  scopes and yield-based cleanup.
- **co-06 · parametrization** — `@pytest.mark.parametrize` runs one test body over many input/expected rows,
  each reported as its own case.
- **co-07 · approx-and-floats** — `pytest.approx` compares floating-point values within tolerance rather
  than by exact equality.
- **co-08 · markers-and-selection** — markers (`skip`, `xfail`, custom) plus `-k`/`-m` select and label
  subsets of the suite.
- **co-09 · test-organization** — grouping tests in classes/modules and sharing fixtures via `conftest.py`
  keeps a suite navigable.
- **co-10 · test-pyramid-vs-trophy** — many fast unit tests and few slow e2e tests (pyramid) versus a
  trophy that weights integration; both are risk-driven judgments.
- **co-11 · test-doubles-taxonomy** — dummy, stub, spy, mock, and fake are distinct doubles for distinct
  needs (Meszaros taxonomy, popularized by Fowler's _Mocks Aren't Stubs_).
- **co-12 · stubbing** — a stub returns canned answers so the unit under test runs in isolation from a real
  collaborator.
- **co-13 · mocking-and-verification** — `unittest.mock`/`MagicMock` records calls so you can assert the
  interaction, not just the result.
- **co-14 · patching** — `monkeypatch`/`mock.patch` replaces a dependency at its use site for the duration
  of a test.
- **co-15 · spies** — a spy wraps a real object to record how it was called while still delegating to it.
- **co-16 · fakes** — a fake is a working lightweight implementation (e.g. an in-memory repository)
  substituted for the real one.
- **co-17 · tdd-red-green-refactor** — write a failing test, make it pass minimally, then refactor while it
  stays green.
- **co-18 · property-based-testing** — Hypothesis (and fast-check in TS) generates many inputs asserting an
  invariant rather than hand-picked examples.
- **co-19 · shrinking** — on failure, a property tool shrinks the input to a minimal reproducing
  counterexample.
- **co-20 · strategies** — Hypothesis strategies (`st.integers`, `st.text`, composites, `assume`) describe
  and constrain the generated input space.
- **co-21 · coverage** — `coverage.py` measures which lines and branches ran; high coverage is necessary but
  not sufficient for correctness.
- **co-22 · mutation-testing** — `mutmut` (Python) / Stryker (TS) mutate the code and check the tests catch
  it, measuring test strength beyond coverage.
- **co-23 · integration-testing** — a test exercises multiple real components together (e.g. app + DB) past
  the seams unit tests stub out.
- **co-24 · contract-testing** — Pact lets a consumer and provider agree on an interface and verify it
  independently, without full integration.
- **co-25 · e2e-and-test-containers** — end-to-end tests drive the whole system; test-containers supply
  ephemeral real dependencies for them.
- **co-26 · test-isolation-and-determinism** — tests must be independent, order-free, and deterministic by
  controlling time, randomness, and IO.
- **co-27 · reading-reports** — reading pytest output, coverage reports, and mutation scores from the
  terminal turns a run into an actionable signal.
- **co-28 · bdd-given-when-then** — behavior-driven development frames each behavior as a Given (context)
  / When (action) / Then (outcome) scenario in ubiquitous language shared with non-engineers, pushing TDD
  outward from units to whole behaviors.
- **co-29 · gherkin-feature-scenario** — Gherkin's `Feature` / `Scenario` / `Given` / `When` / `Then` /
  `And` / `But` grammar expresses an executable specification in near-natural language that both the
  runner and non-engineer stakeholders can read.
- **co-30 · step-definitions** — a step definition binds one Gherkin step to executable code via a
  pattern; `pytest-bdd` and `behave` (Python) or Cucumber.js (TS) run the `.feature` against those
  bindings.
- **co-31 · scenario-outline-examples** — `Scenario Outline` plus an `Examples` table runs one scenario
  over many rows — the BDD analog of pytest parametrization (co-06) — keeping data-driven cases readable.
- **co-32 · bdd-vs-tdd-and-atdd** — BDD / ATDD / specification-by-example add shared-language acceptance
  tests at the outside of the pyramid; they complement, never replace, unit TDD (co-17) — judge which a
  given change actually earns.

## Worked examples

Colocated under `software-testing/learning/code/`; each is a runnable test (pytest idioms primarily, with
TS/Vitest and fast-check cross-refs where noted) (DD-20/DD-30), and each cites the `co-NN` it exercises.
Contiguous `ex-01..ex-86`.

### Beginner

- **ex-01 · first-passing-test** — write `def test_adds(): assert add(2, 3) == 5` — verify `pytest` reports
  `1 passed`. (co-01, co-02)
- **ex-02 · failing-test-output** — assert a wrong value — verify pytest prints the expected-vs-actual
  introspection. (co-03)
- **ex-03 · arrange-act-assert** — structure a test in three clear phases — verify it passes and each phase
  is distinct. (co-01)
- **ex-04 · run-single-test** — run `pytest path::test_name` — verify only that test executes. (co-02)
- **ex-05 · assert-equality** — assert two values equal — verify it passes on a match and fails otherwise.
  (co-03)
- **ex-06 · assert-truthiness** — assert a boolean condition — verify pytest reports the operands on
  failure. (co-03)
- **ex-07 · assert-membership** — assert `x in items` — verify it passes for a present element. (co-03)
- **ex-08 · raises-valueerror** — wrap a bad call in `pytest.raises(ValueError)` — verify the test passes
  when it raises. (co-04)
- **ex-09 · raises-match-message** — use `pytest.raises(..., match="...")` — verify it asserts the message
  text. (co-04)
- **ex-10 · approx-float** — assert `0.1 + 0.2 == pytest.approx(0.3)` — verify the float comparison passes.
  (co-07)
- **ex-11 · simple-fixture** — a fixture returning a sample object injected by name — verify the test
  receives it. (co-05)
- **ex-12 · fixture-teardown** — a fixture that `yield`s then cleans up — verify teardown runs after the
  test body. (co-05)
- **ex-13 · fixture-scope** — a `scope="module"` fixture — verify it is built once across the module's
  tests. (co-05)
- **ex-14 · parametrize-cases** — `@parametrize` over three `(input, expected)` rows — verify three cases
  run. (co-06)
- **ex-15 · parametrize-ids** — add readable `ids` to parametrized cases — verify each shows its id in the
  output. (co-06)
- **ex-16 · parametrize-multiple-args** — parametrize two arguments together — verify each combination runs.
  (co-06)
- **ex-17 · mark-skip** — apply `@pytest.mark.skip` — verify the test reports skipped, not failed. (co-08)
- **ex-18 · mark-xfail** — apply `@pytest.mark.xfail` to a known-broken test — verify it reports xfail.
  (co-08)
- **ex-19 · custom-marker-select** — mark tests `@pytest.mark.slow` and run `-m "not slow"` — verify the
  slow ones are excluded. (co-08)
- **ex-20 · keyword-select** — run `pytest -k "add"` — verify only matching-named tests run. (co-08)
- **ex-21 · group-tests-in-class** — group related tests in a `class TestAdder` — verify they run together.
  (co-09)
- **ex-22 · shared-conftest-fixture** — put a fixture in `conftest.py` — verify multiple test files can use
  it. (co-09, co-05)
- **ex-23 · tdd-write-failing-first** — write the test before the function exists — verify it fails red with
  an `ImportError`/`AssertionError`. (co-17)
- **ex-24 · tdd-make-it-pass** — implement the function minimally — verify the previously red test goes
  green. (co-17)
- **ex-25 · tdd-refactor-under-green** — refactor the implementation — verify the tests stay green
  throughout. (co-17)
- **ex-26 · test-pure-function** — test a pure function over several inputs — verify deterministic outputs.
  (co-01, co-26)
- **ex-27 · deterministic-no-hidden-state** — run the same test twice — verify identical results with no
  order dependence. (co-26)
- **ex-28 · run-verbose-report** — run `pytest -v` — verify per-test names and PASS/FAIL lines appear.
  (co-27, co-02)

### Intermediate

- **ex-29 · stub-returns-canned-value** — inject a stub returning a fixed value — verify the unit uses it
  without the real dependency. (co-12, co-11)
- **ex-30 · dummy-object-unused** — pass a dummy that is never called — verify it only satisfies the
  signature. (co-11)
- **ex-31 · mock-records-call** — use `MagicMock`, call the unit, assert `mock.called` — verify the
  interaction happened. (co-13)
- **ex-32 · mock-assert-called-with** — assert `mock.assert_called_once_with(...)` — verify the exact
  arguments passed. (co-13)
- **ex-33 · mock-return-value** — configure `mock.return_value` — verify the unit consumes the mocked
  return. (co-13, co-12)
- **ex-34 · mock-side-effect-raises** — set `side_effect=Error` — verify the unit handles the raised error.
  (co-13, co-04)
- **ex-35 · patch-dependency** — `mock.patch("module.dep")` inside a test — verify the real dependency is
  replaced during the call. (co-14)
- **ex-36 · monkeypatch-attr** — `monkeypatch.setattr` to swap a function — verify the patched version runs.
  (co-14)
- **ex-37 · monkeypatch-env** — `monkeypatch.setenv` — verify code reads the patched environment variable.
  (co-14, co-26)
- **ex-38 · spy-wraps-real** — build `MagicMock(wraps=real)` — verify calls are recorded while delegating to
  the real object. (co-15)
- **ex-39 · fake-in-memory-repo** — substitute an in-memory repository fake — verify the service works
  against it. (co-16)
- **ex-40 · fake-vs-mock-contrast** — solve one scenario with a fake and with a mock — verify both pass but
  assert different things (state vs interaction). (co-16, co-13)
- **ex-41 · patch-time** — freeze `datetime`/`time` via monkeypatch — verify time-dependent logic becomes
  deterministic. (co-14, co-26)
- **ex-42 · control-randomness-seed** — seed the RNG in a fixture — verify repeatable "random" output.
  (co-26)
- **ex-43 · property-idempotent** — Hypothesis: assert `f(f(x)) == f(x)` over generated ints — verify the
  invariant holds. (co-18, co-20)
- **ex-44 · property-roundtrip** — assert `decode(encode(x)) == x` over `st.text()` — verify the round-trip
  property. (co-18, co-20)
- **ex-45 · property-commutative** — assert `add(a, b) == add(b, a)` over integers — verify commutativity.
  (co-18)
- **ex-46 · property-list-invariant** — assert `sorted(xs)` is ordered and same-length over `st.lists` —
  verify both invariants. (co-18, co-20)
- **ex-47 · shrinking-minimal-counterexample** — write a buggy function so Hypothesis fails — verify it
  reports a minimal shrunk input. (co-19)
- **ex-48 · custom-strategy-composite** — build a `@st.composite` strategy for a domain object — verify
  generated values satisfy the preconditions. (co-20)
- **ex-49 · hypothesis-assume** — use `assume()` to discard invalid inputs — verify only valid cases are
  exercised. (co-20)
- **ex-50 · example-plus-property** — combine `@example` with a property test — verify the pinned case
  always runs alongside generated ones. (co-18)
- **ex-51 · fast-check-property-ts** — the same round-trip property in fast-check (TS) — verify it passes in
  the TS stack. (co-18)
- **ex-52 · coverage-line-report** — run `pytest --cov` — verify the report shows per-file line coverage.
  (co-21, co-27)
- **ex-53 · coverage-branch** — enable branch coverage — verify an untaken branch is reported as missed.
  (co-21)
- **ex-54 · coverage-gap-then-cover** — find an uncovered line and add a test — verify coverage rises to
  include it. (co-21)
- **ex-55 · coverage-not-proof** — a fully covered function with a latent bug — verify coverage passes yet a
  property test catches the bug. (co-21, co-18)
- **ex-56 · fixture-parametrized** — a parametrized fixture feeding several tests — verify each variant
  runs. (co-05, co-06)
- **ex-57 · aaa-with-double** — arrange a mock, act, then assert on both the result and the interaction —
  verify the combined check. (co-01, co-13)
- **ex-58 · tdd-with-double** — TDD a unit that needs a stubbed collaborator — verify red→green with the
  double in place. (co-17, co-12)
- **ex-59 · isolate-io-boundary** — inject a fake for the filesystem/network — verify the unit test performs
  no real IO. (co-16, co-26)
- **ex-60 · marker-for-integration** — mark integration tests and run `-m "not integration"` — verify they
  are skipped in the fast unit run. (co-08, co-10)

### Advanced

- **ex-61 · pyramid-shape-suite** — organize a suite as many unit, some integration, and few e2e tests —
  verify the counts reflect the pyramid. (co-10)
- **ex-62 · trophy-weighted-integration** — reweight the same suite toward integration (trophy) — verify the
  integration tier carries the most cases. (co-10)
- **ex-63 · integration-two-modules** — test two real collaborating modules together — verify the combined
  behavior without stubbing the seam. (co-23)
- **ex-64 · integration-app-plus-db** — run a test against the app with a real temporary database — verify a
  write then read round-trips. (co-23, co-25)
- **ex-65 · integration-http-endpoint** — hit a Backend-Essentials endpoint with a test client — verify the
  response status and body. (co-23)
- **ex-66 · testcontainers-ephemeral-db** — spin up a throwaway DB container for a test — verify it is
  created and torn down around the run. (co-25, co-23)
- **ex-67 · contract-consumer-pact** — write a Pact consumer test defining the expected interaction — verify
  it produces a pact file. (co-24)
- **ex-68 · contract-provider-verify** — verify the provider against the pact — verify the provider
  satisfies the recorded contract. (co-24)
- **ex-69 · e2e-happy-path** — drive the whole system through one user flow — verify the resulting end-state
  is correct. (co-25)
- **ex-70 · mutation-baseline** — run `mutmut` on a well-tested function — verify the surviving-mutant report
  is produced. (co-22)
- **ex-71 · mutation-kill-survivor** — add a test to kill a surviving mutant — verify the mutation score
  improves. (co-22, co-27)
- **ex-72 · mutation-vs-coverage** — a fully covered function with surviving mutants — verify mutation
  exposes weak assertions that coverage missed. (co-22, co-21)
- **ex-73 · read-coverage-report** — interpret a terminal/HTML coverage report — verify you can name the
  uncovered lines. (co-27, co-21)
- **ex-74 · read-failing-traceback** — read a failing pytest traceback — verify you can locate the assertion
  and the offending values. (co-27, co-03)
- **ex-75 · flaky-test-diagnosis** — reproduce a flaky test caused by shared state, then isolate it — verify
  it becomes deterministic. (co-26, co-09)
- **ex-76 · fixture-cleanup-isolation** — use fixture teardown to reset state between tests — verify
  order-independence across the module. (co-05, co-26)
- **ex-77 · double-taxonomy-mapping** — implement one scenario with each of dummy/stub/spy/mock/fake —
  verify each matches its Meszaros definition. (co-11, co-15, co-16)
- **ex-78 · choose-right-double** — pick the appropriate double for a scenario and justify it — verify the
  test asserts the correct dimension (state vs behavior). (co-11, co-13)
- **ex-79 · full-pyramid-feature** — build unit + integration + one e2e test for a single feature — verify
  every tier is green. (co-10, co-23, co-25)
- **ex-80 · full-verification-suite** — combine TDD unit tests, a property test, an integration test,
  coverage, and a mutation run for one feature — verify every gate passes and the mutation score is read.
  (co-17, co-18, co-23, co-22, co-27)

### BDD & executable specifications

- **ex-81 · pytest-bdd-first-scenario** — write a `.feature` with one Given/When/Then plus its
  `pytest-bdd` step definitions — verify `pytest` runs the scenario and reports `1 passed`. (co-28, co-30)
- **ex-82 · gherkin-feature-grammar** — author a `.feature` using `Feature` / `Scenario` / `Given` /
  `When` / `Then` / `And` — verify the runner parses it and lists the named scenario. (co-29)
- **ex-83 · step-definition-shared-context** — bind steps to functions that share state via a
  context/fixture — verify a value set in `Given` is asserted in `Then`. (co-30, co-05)
- **ex-84 · scenario-outline-examples-table** — drive one `Scenario Outline` over an `Examples` table of
  rows — verify each row runs as its own case. (co-31, co-06)
- **ex-85 · behave-vs-pytest-bdd-same-feature** — run the same `.feature` under `behave` and `pytest-bdd`
  (or Cucumber.js in TS) — verify both execute the identical scenario green. (co-30, co-29)
- **ex-86 · bdd-vs-tdd-decision** — annotate one change with whether a unit TDD test or a BDD acceptance
  scenario fits — verify the choice matches the risk and the audience. (co-32, co-17)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take one small feature and build its full test suite across the pyramid — TDD'd unit tests,
  a mocked-dependency test, a property-based test (Hypothesis + fast-check), and an integration test
  against the Backend-Essentials app — with a coverage report read from the CLI.
- **Concepts exercised**: [ ] arrange–act–assert unit tests (both stacks) [ ] a test double (stub/mock)
  [ ] TDD red→green→refactor [ ] a property-based test with shrinking [ ] an integration test [ ] reading
  coverage.
- **Ordered steps**:
  1. `.../learning/capstone/code/` — TDD a pure function: write the failing `pytest`/Vitest test first,
     then implement. Verify the test goes red→green.
  2. Add a stub/mock isolating a dependency. Verify the unit test runs without the real dependency.
  3. Add a Hypothesis (+ fast-check) property test asserting an invariant. Verify it passes and would
     shrink a counterexample (demonstrate on a seeded bug).
  4. Add an integration test hitting the Backend-Essentials endpoints. Verify it passes against the
     running app; read the coverage report.
- **Acceptance criteria**: all tiers green; the property test demonstrably catches a seeded regression;
  coverage report generated and interpreted; the red→green history is shown.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Test-Driven Development: By Example** — Kent Beck (2002). The originating text of TDD and red-green-refactor.
- **Growing Object-Oriented Software, Guided by Tests** — Freeman, Pryce (2009). Canonical guide to outside-in TDD and disciplined mock use.
- **xUnit Test Patterns: Refactoring Test Code** — Gerard Meszaros (2007). Reference catalog of unit-test patterns and "test smells."

**Papers & articles**

- **"QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs"** — Claessen, Hughes (2000, ICFP). Originating paper of property-based testing. <https://dl.acm.org/doi/10.1145/351240.351266>
- **"Mocks Aren't Stubs"** — Martin Fowler (2007). Canonical explanation of classical vs mockist testing and test doubles; attributes the five-double taxonomy to Gerard Meszaros. <https://martinfowler.com/articles/mocksArentStubs.html>
- **"TestPyramid"** — Martin Fowler (bliki). Explains the test pyramid, crediting Mike Cohn's _Succeeding with Agile_ (2009). <https://martinfowler.com/bliki/TestPyramid.html>
- **"The Testing Trophy and Testing Classifications"** — Kent C. Dodds (2018). The integration-weighted "testing trophy" model. <https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications>

---

← Previous: [14 · Frontend Essentials](./14-frontend-essentials.md) · Next: [16 · Debugging & Profiling](./16-debugging-and-profiling.md) →
