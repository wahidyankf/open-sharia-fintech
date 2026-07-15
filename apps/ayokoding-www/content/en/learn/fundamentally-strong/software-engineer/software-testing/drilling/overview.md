---
title: "Overview"
date: 2026-07-15T00:00:00+07:00
draft: false
weight: 1
---

This page is the active-recall companion to the Software Testing learning track: four fixed drills
that force retrieval instead of passive re-reading. Work through them in order -- short-answer recall
first, then scenario judgment, then hands-on implementation, then a checklist to confirm real
automaticity. Every answer is hidden in a `<details>` block; try each item yourself, out loud or on
paper, before opening it. Every prompt below uses its own mocked, self-contained input -- different
function names, domains, and scenarios from anything in the learning track's 86 worked examples -- so
recognizing an answer isn't enough; you have to actually reconstruct the reasoning. Nothing on this
page touches a live third-party host, a real database, or the network: every scenario is entirely
self-contained, in memory, reasoned about on paper.

## Recall Q&A

Thirty-two short-answer questions, one per concept (`co-01` through `co-32`). Answer from memory,
then check.

**Q1 (co-01 -- why-test-and-aaa).** In one sentence, what does a test actually encode, and name the
three phases arrange-act-assert structures it into.

<details>
<summary>Answer</summary>

A test encodes an expectation as executable truth -- a claim about behavior that a machine can check
every time, not just once by eye. The three phases are arrange (set up the inputs/state), act (call
the thing under test), and assert (check the result).

</details>

**Q2 (co-02 -- test-discovery-and-run).** A file is named `helpers_test.py` and contains a function
named `check_helper()`. Will plain `pytest` (no arguments) discover and run it? Why or why not?

<details>
<summary>Answer</summary>

No. Pytest's default discovery looks for files matching `test_*.py` or `*_test.py` -- `helpers_test.py`
matches the `*_test.py` form, so the FILE is fine, but pytest also requires the function itself to be
named `test_*` (not `check_*`). `check_helper()` needs renaming to `test_helper()` (or similar) to be
collected.

</details>

**Q3 (co-03 -- assertions).** Why does pytest not need a `assertEqual`/`assertTrue`/`assertIn` method
zoo the way some other testing frameworks do?

<details>
<summary>Answer</summary>

Pytest rewrites the plain `assert` statement at import time so that, on failure, it introspects the
actual expression and prints the real values of both operands -- so a bare `assert a == b` already
reports exactly what a dedicated `assertEqual` method would, with no extra API to memorize.

</details>

**Q4 (co-04 -- exception-testing).** Write, from memory, the general shape of a `pytest.raises` block
that asserts a call raises a `KeyError` whose message contains the text `"missing"`.

<details>
<summary>Answer</summary>

```python
with pytest.raises(KeyError, match="missing"):
    do_the_call_that_should_raise()
```

`match` runs `re.search` against `str(exception)`, so it's a substring/regex check, not an exact-equality
check.

</details>

**Q5 (co-05 -- fixtures).** A fixture is decorated `@pytest.fixture` and contains a single `yield`
statement instead of a `return`. What does the code AFTER that `yield` do, and when does it run?

<details>
<summary>Answer</summary>

The code after `yield` is teardown -- it runs after the test that used the fixture finishes (pass or
fail), giving the fixture a guaranteed place to clean up whatever it set up before the `yield`.

</details>

**Q6 (co-06 -- parametrization).** `@pytest.mark.parametrize("n,expected", [(1, 1), (2, 4), (3, 9)])`
decorates one test function. How many times does pytest actually run that function's body, and how
are the runs reported?

<details>
<summary>Answer</summary>

Three times -- once per tuple in the list -- and each run is reported as its own independent test
case (pass/fail tracked separately), not as one combined result.

</details>

**Q7 (co-07 -- approx-and-floats).** Why does `0.1 + 0.1 + 0.1 == 0.3` evaluate to `False` in Python,
and what pytest helper fixes an assertion built on that comparison?

<details>
<summary>Answer</summary>

Floating-point numbers are binary approximations of decimal values, so tiny representation errors
accumulate across arithmetic -- `0.1 + 0.1 + 0.1` is actually `0.30000000000000004`, not exactly
`0.3`. `pytest.approx(0.3)` compares within a small tolerance instead of requiring bit-exact equality.

</details>

**Q8 (co-08 -- markers-and-selection).** What is the practical difference between `@pytest.mark.skip`
and `@pytest.mark.xfail` on a test that currently fails?

<details>
<summary>Answer</summary>

`skip` never runs the test body at all -- it's reported as skipped, full stop. `xfail` DOES run the
test body, expects it to fail, and reports `xfail` if it fails as expected -- but if it unexpectedly
PASSES, that's reported as `XPASS`, which can be configured to fail the suite (catching a bug that got
silently fixed without anyone updating the marker).

</details>

**Q9 (co-09 -- test-organization).** A fixture is defined once in `conftest.py` at the root of a test
directory. Which test files can use it, and does any file need to import it?

<details>
<summary>Answer</summary>

Every test file at or below that `conftest.py`'s directory can use the fixture by naming it as a
parameter -- pytest auto-discovers `conftest.py` fixtures without any explicit import.

</details>

**Q10 (co-10 -- test-pyramid-vs-trophy).** A team has 500 unit tests, 40 integration tests, and 5 e2e
tests. Is this shaped more like the pyramid or the testing trophy? What would make it look like the
other one?

<details>
<summary>Answer</summary>

This is pyramid-shaped -- heavily weighted toward fast unit tests, with integration and e2e as a
thin, expensive top. It would look trophy-shaped instead if the integration tier carried the LARGEST
share of tests (more integration cases than unit cases), reflecting a bet that testing real component
seams catches more real bugs per test than isolated units do.

</details>

**Q11 (co-11 -- test-doubles-taxonomy).** Name all five kinds of test double in the Meszaros
taxonomy, and state the one dimension that separates mocks from every other kind.

<details>
<summary>Answer</summary>

Dummy, stub, spy, mock, and fake. Mocks are the only double whose PASS/FAIL verdict depends on
verifying an INTERACTION happened (a call, with specific arguments) -- every other double is judged
by its effect on the test's STATE-based assertions, not by what was called on it.

</details>

**Q12 (co-12 -- stubbing).** A test replaces a `PaymentGateway` collaborator with an object whose
`charge()` method always returns `{"status": "approved"}}`, no matter what arguments it receives.
What kind of double is this, and what is it NOT doing?

<details>
<summary>Answer</summary>

A stub -- it returns a canned answer regardless of input. It is NOT recording or verifying HOW it was
called (that would make it a mock or a spy); its only job is to let the unit under test run without
touching the real payment gateway.

</details>

**Q13 (co-13 -- mocking-and-verification).** What does `mock.assert_called_once_with(x, y)` actually
check, distinct from just checking the unit's return value?

<details>
<summary>Answer</summary>

It checks the INTERACTION -- that the mock was invoked exactly once, with exactly the arguments `x`
and `y` -- which is a claim about behavior/collaboration, entirely separate from whatever the unit
under test happened to return.

</details>

**Q14 (co-14 -- patching).** `monkeypatch.setattr("mymodule.send_email", fake_send)` is called inside
a test. When does the real `send_email` function get restored, and why doesn't the test need to
restore it manually?

<details>
<summary>Answer</summary>

Automatically, at the end of that test (whether it passes, fails, or errors) -- the `monkeypatch`
fixture undoes every patch it applied once its owning test function returns, so there's no manual
teardown to write or forget.

</details>

**Q15 (co-15 -- spies).** A test wraps a real `Logger` object with `MagicMock(wraps=real_logger)`.
After calling the unit under test, the assertion checks `spy.info.call_count == 2`. Did the real
logger's `info()` method actually execute? How do you know?

<details>
<summary>Answer</summary>

Yes. `wraps=` makes the mock DELEGATE every call through to the real object after recording it -- a
spy's defining trait is that it still performs the real behavior while also observing it, unlike a
mock or stub, which typically replace the real behavior entirely.

</details>

**Q16 (co-16 -- fakes).** An `InMemoryUserRepository` implements the exact same `save()`/`find_by_id()`
interface as the real database-backed repository, using a plain Python dict internally. Why is this a
fake and not a stub?

<details>
<summary>Answer</summary>

Because it's a genuinely WORKING lightweight implementation -- it actually stores and retrieves data
correctly, just via a dict instead of a real database -- rather than a canned-answer object that only
returns fixed values regardless of what's asked of it.

</details>

**Q17 (co-17 -- tdd-red-green-refactor).** Put these three TDD steps in the correct order: "refactor
while staying green," "write a failing test," "make the test pass with the simplest code that works."

<details>
<summary>Answer</summary>

Write a failing test (red) -> make it pass with the simplest code that works (green) -> refactor
while staying green. The test must fail FIRST, for a real reason (the behavior doesn't exist yet), or
the cycle isn't actually verifying anything.

</details>

**Q18 (co-18 -- property-based-testing).** How does a property-based test (Hypothesis/fast-check)
differ from a parametrized test (co-06) in HOW it chooses its inputs?

<details>
<summary>Answer</summary>

A parametrized test runs over a FIXED, hand-picked list of input rows the author wrote out in
advance. A property-based test instead runs over MANY generated inputs from a described strategy
(e.g. "any integer," "any list of strings"), asserting an invariant that should hold for all of them
-- trading hand-picked examples for a much wider, automatically explored input space.

</details>

**Q19 (co-19 -- shrinking).** A Hypothesis test fails on a randomly generated list of 340 integers.
What does Hypothesis do next, automatically, before reporting the failure to you?

<details>
<summary>Answer</summary>

It shrinks the failing input -- repeatedly trying smaller/simpler variations that still reproduce the
failure -- until it finds a MINIMAL counterexample, then reports that minimal case instead of the
original 340-integer list, so the actual bug is far easier to read and reason about.

</details>

**Q20 (co-20 -- strategies).** What does `st.integers(min_value=0, max_value=100)` describe, and what
does calling `assume(x % 2 == 0)` inside a property test do to the values Hypothesis generates?

<details>
<summary>Answer</summary>

`st.integers(min_value=0, max_value=100)` is a STRATEGY describing the space of values Hypothesis may
generate for that parameter -- any integer from 0 to 100 inclusive. `assume(x % 2 == 0)` DISCARDS any
generated case where the condition is false (it doesn't fail the test, it just skips that particular
generated value and tries another), narrowing the exercised space to only even values.

</details>

**Q21 (co-21 -- coverage).** A function has 100% line coverage from its test suite. Does that prove
the function is correct? What does 100% line coverage actually guarantee?

<details>
<summary>Answer</summary>

No -- coverage measures which lines EXECUTED during the test run, not whether the test made a
meaningful assertion about what those lines did. 100% line coverage only guarantees every line ran at
least once; a test can execute a buggy line and still pass if it never actually asserts on the wrong
result that line produced.

</details>

**Q22 (co-22 -- mutation-testing).** A mutation tool changes `if x > 0:` to `if x >= 0:` in your
source, reruns your test suite, and the suite still passes. What does this "surviving mutant" tell
you, and what should you do about it?

<details>
<summary>Answer</summary>

It tells you your test suite has a WEAK ASSERTION near that boundary -- no existing test distinguishes
between the `>` and `>=` behavior at `x == 0`, so a real bug introduced at exactly that boundary would
also slip through undetected. The fix is to add (or strengthen) a test that specifically exercises
`x == 0` and asserts the correct boundary behavior, killing the mutant.

</details>

**Q23 (co-23 -- integration-testing).** A unit test replaces a database with an in-memory fake. What
would need to change to turn that same test into an integration test?

<details>
<summary>Answer</summary>

Replace the in-memory fake with the REAL database (or a real instance of it) so the test exercises
the actual seam between the application code and the real component, instead of stubbing that seam
out -- integration testing is specifically about NOT substituting the real collaborator.

</details>

**Q24 (co-24 -- contract-testing).** Two teams own a consumer service and a provider service that
talk over an API neither team can fully integration-test together on every commit. What does contract
testing let each team verify independently, without running the other team's service?

<details>
<summary>Answer</summary>

Contract testing lets the consumer record the exact interaction it expects (request shape, response
shape) as a shareable "contract" (e.g. a Pact file), and lets the provider independently verify its
real responses satisfy that same recorded contract -- so each side proves compatibility without
either side needing the other's service actually running.

</details>

**Q25 (co-25 -- e2e-and-test-containers).** What does an end-to-end test drive that an integration
test typically does not, and what problem do test-containers solve for tests that need a real
dependency like a database?

<details>
<summary>Answer</summary>

An e2e test drives the WHOLE system through a real (or near-real) user-facing flow, often across
multiple services/layers, whereas an integration test usually exercises just two or a few real
components together. Test-containers solve the "where does a real, ephemeral database/service come
from" problem -- they spin up a genuine, throwaway instance (e.g. via Docker) for the duration of a
test run, then tear it down automatically.

</details>

**Q26 (co-26 -- test-isolation-and-determinism).** A test suite passes when run alone but fails when
run as part of the full suite in a certain order. What category of problem is this, and name two
specific sources of nondeterminism this topic teaches you to control.

<details>
<summary>Answer</summary>

This is a test-isolation/order-dependence problem -- almost always caused by shared mutable state one
test leaves behind that another test's outcome depends on. Two sources of nondeterminism this topic
teaches controlling directly: the current time/date (frozen via `monkeypatch`/`freezegun`) and random
number generation (seeded explicitly), plus uncontrolled IO as a third common source.

</details>

**Q27 (co-27 -- reading-reports).** A pytest run ends with the line `3 failed, 47 passed, 2 skipped in
1.84s`. Before opening any traceback, what does this summary line alone already tell you?

<details>
<summary>Answer</summary>

That 52 tests were collected and attempted; 47 genuinely passed; 3 have real, currently-broken
behavior (or broken tests) that need investigation; and 2 were deliberately not run at all (via
`@pytest.mark.skip` or a skip condition) -- and the whole run took 1.84 seconds, useful for judging
whether the suite is still fast enough to run on every change.

</details>

**Q28 (co-28 -- bdd-given-when-then).** Rewrite this unit-test-style description as a Given/When/Then
scenario: "test that withdrawing more than the balance raises an error." Name the audience BDD's
ubiquitous language is written for that a raw unit test name usually isn't.

<details>
<summary>Answer</summary>

`Given` an account with a balance of $50, `When` the customer withdraws $75, `Then` the withdrawal is
rejected with an insufficient-funds error. BDD's Given/When/Then framing targets a SHARED audience of
engineers AND non-engineer stakeholders (product, QA, business) who can all read and validate the
scenario without needing to read code.

</details>

**Q29 (co-29 -- gherkin-feature-scenario).** Name the four keywords, in order, that structure a single
Gherkin scenario body (not counting the `Feature`/`Scenario` lines themselves), and what does `And`
do.

<details>
<summary>Answer</summary>

`Given`, `When`, `Then` -- context, action, expected outcome, in that order. `And` (and `But`) extends
the PRECEDING keyword's step without repeating it -- so `Given ... And ...` adds another piece of
context, while `Then ... And ...` adds another expected outcome, keeping a multi-step scenario
readable instead of repeating `Given`/`Then` over and over.

</details>

**Q30 (co-30 -- step-definitions).** A `.feature` file contains the step `Given a cart with 3 items`.
What does a step definition do with this line, and name the two Python tools this topic teaches that
can run it.

<details>
<summary>Answer</summary>

A step definition binds that exact (or pattern-matched) Gherkin text to a real, executable function --
it's the glue between the near-natural-language scenario and actual test code. `pytest-bdd` and
`behave` are the two Python runners this topic teaches (Cucumber.js plays the same role in TypeScript).

</details>

**Q31 (co-31 -- scenario-outline-examples).** A `Scenario Outline` has three placeholder variables and
an `Examples` table with 5 data rows underneath it. How many times does the scenario actually run,
and what is this the BDD analog of from the pytest side of this topic?

<details>
<summary>Answer</summary>

Five times -- once per row in the `Examples` table, with the placeholders substituted from that row
each time. This is the direct BDD analog of `@pytest.mark.parametrize` (co-06): one scenario body,
many data-driven runs, each reported as its own case.

</details>

**Q32 (co-32 -- bdd-vs-tdd-and-atdd).** A change adds a purely internal caching helper with no
user-visible behavior. A separate change adds a new customer-facing checkout discount rule. Which of
these two changes more naturally earns a BDD acceptance scenario over a plain unit test, and why?

<details>
<summary>Answer</summary>

The checkout discount rule -- it's customer-facing, has real business risk, and benefits from a
scenario product/QA/business stakeholders can read and validate in near-natural language. The internal
caching helper is better served by a plain unit TDD test: writing a full Given/When/Then scenario for
something only engineers will ever read is disproportionate ceremony. BDD/ATDD complement unit TDD at
the outside of the pyramid; they don't replace it everywhere.

</details>

## Applied problems

Fifteen scenarios spanning beginner through advanced material. Each describes a realistic engineering
situation without naming the specific tool or technique -- decide what applies and why, then check
your reasoning against the worked solution. Every scenario below is invented for this drill and does
not reuse any function, fixture, or domain from the 86 worked examples.

**AP1.** A test named `test_discount()` asserts `apply_discount(100, 0.1) == 90`. A teammate asks "how
do I know which part of this test is the setup versus the check?" What's your one-sentence answer,
and how would you restructure the test to make the answer obvious just from reading it?

<details>
<summary>Worked solution</summary>

Structure it explicitly in three phases (co-01): arrange (`price = 100; rate = 0.1`), act
(`result = apply_discount(price, rate)`), assert (`assert result == 90`) -- as three visually distinct
lines/blocks rather than one dense expression, so the boundary between setup and check is legible at
a glance, not just inferable.

</details>

**AP2.** A new hire runs bare `pytest` in a project and sees `collected 0 items`, even though they can
see test functions in the file they're looking at. What are the two most likely naming mistakes
causing this?

<details>
<summary>Worked solution</summary>

Either the FILE doesn't match `test_*.py`/`*_test.py` discovery, or the FUNCTIONS inside a
correctly-named file aren't prefixed `test_` (co-02) -- pytest requires both the file and the function
names to match its discovery convention; a class of test methods also needs the enclosing class
prefixed `Test` with no `__init__`.

</details>

**AP3.** A test asserts `compute_total(cart) == 42.30` and fails intermittently with values like
`42.299999999999997`. What's the root cause, and the one-line fix?

<details>
<summary>Worked solution</summary>

Floating-point arithmetic accumulates tiny representation errors (co-07); the fix is
`assert compute_total(cart) == pytest.approx(42.30)` instead of exact equality, comparing within a
small numeric tolerance rather than requiring a bit-exact match.

</details>

**AP4.** A suite has 40 tests that hit a real external payment API and take 6 minutes to run, so
engineers stopped running them locally before pushing. What two concepts from this topic would you
reach for first to fix this, and in what order?

<details>
<summary>Worked solution</summary>

First, isolate the IO boundary (co-16/co-26) by replacing the real external API with a stub or fake
for the fast local run, so the 40 tests no longer need real network calls. Second, mark whichever
tests genuinely need the real API as `@pytest.mark.integration` (co-08) and exclude them from the
default fast run with `-m "not integration"`, keeping a slower, separately-scheduled pass for the
handful that truly need real IO.

</details>

**AP5.** Two tests both call a shared `shopping_cart` fixture. Test A adds an item and asserts the
cart has 1 item; Test B asserts the cart is empty. Run alone, both pass. Run together, Test B
sometimes fails. What's the fixture's scope almost certainly set to, and what should it be instead?

<details>
<summary>Worked solution</summary>

It's almost certainly `scope="module"` (or wider) with mutable state, so Test A's mutation leaks into
whatever instance Test B receives, depending on run order (co-26). The default `scope="function"`
(a fresh instance built for every single test) removes the shared mutable state entirely, restoring
order-independence.

</details>

**AP6.** A code review comment says "this test verifies the mock was called, but never checks what the
function actually returned to its caller." What kind of double is likely being misused here, and what
should a more complete test add?

<details>
<summary>Worked solution</summary>

The test is checking interaction only (a mock, co-13) but skipping the STATE-based assertion on the
unit's actual return value or observable effect -- a complete test usually wants both: verify the
collaborator was called correctly AND assert the caller's own output/behavior is right (co-01's
arrange-act-assert applied to both dimensions at once, as in this topic's "aaa-with-double" pattern).

</details>

**AP7.** A test needs `os.environ["FEATURE_FLAG"]` to read `"on"` for the duration of one test only,
without affecting any other test in the suite, and without a `try/finally` block. What's the exact
mechanism?

<details>
<summary>Worked solution</summary>

`monkeypatch.setenv("FEATURE_FLAG", "on")` inside the test (co-14) -- the `monkeypatch` fixture
automatically restores the original environment (or removes the variable if it wasn't set before) the
moment that test function returns, with no manual cleanup code required.

</details>

**AP8.** A property test asserts `sorted(reverse_list(xs)) == sorted(xs)` for any list `xs` of
integers, generated by Hypothesis. What TWO distinct properties is a well-written version of this test
likely also checking about `reverse_list`, beyond just "the same elements come back"?

<details>
<summary>Worked solution</summary>

That `reverse_list` preserves LENGTH (`len(reverse_list(xs)) == len(xs)`) and that it's actually
reversing ORDER, not just permuting arbitrarily (e.g. `reverse_list(reverse_list(xs)) == xs`, a
round-trip/involution property) -- `sorted(...) == sorted(...)` alone only confirms the multiset of
elements is unchanged, not that the function does what its name claims.

</details>

**AP9.** A Hypothesis test that asserts `parse(render(value)) == value` fails on a huge, oddly-shaped
generated `value`. Before even reading the failure, what should you expect Hypothesis to have already
done to that failing input, and why does that matter for how quickly you can debug it?

<details>
<summary>Worked solution</summary>

Hypothesis automatically shrinks the failing case to a minimal reproducing counterexample (co-19)
before reporting it -- so instead of staring at the huge original generated value, you get the
smallest input that still fails, which is dramatically faster to reason about by hand.

</details>

**AP10.** A function has 100% branch coverage, and the whole suite is green. A bug ships anyway. What
class of testing gap does this scenario most directly illustrate, and which technique in this topic
is specifically designed to expose it?

<details>
<summary>Worked solution</summary>

This illustrates coverage-is-not-proof (co-21): every branch executed, but the assertions accompanying
those branches were too weak to catch the actual defect. Mutation testing (co-22) is designed
specifically to expose this -- it deliberately introduces small defects (mutants) and checks whether
the existing suite actually notices, which line/branch coverage alone cannot tell you.

</details>

**AP11.** A team wants to verify their order-service and their shipping-service agree on the shape of
the "order placed" event, but shipping-service's team is in a different timezone and the two services
are never deployed together in CI. What testing technique fits this constraint directly, and why not
just write an end-to-end test instead?

<details>
<summary>Worked solution</summary>

Contract testing (co-24) fits directly -- the consumer (shipping-service) records its expectations as
a shareable contract, and the provider (order-service) verifies against that recorded contract
independently, on its own schedule, with no live coordination required. A true e2e test would require
both services running together at the same time, which the timezone/deployment constraint rules out.

</details>

**AP12.** A test spins up a real, ephemeral Postgres instance via a container library, runs a write
then a read against it, then tears the container down -- all inside one test function. Which two
concepts does this single test combine, and what's the key difference from a test that uses an
in-memory fake repository instead?

<details>
<summary>Worked solution</summary>

It combines integration testing (co-23, exercising a real database, not a stub) with test-containers
(co-25, supplying a genuine ephemeral instance of that real dependency). The key difference from an
in-memory fake (co-16) is fidelity versus speed: the fake is instant and always available but can't
catch real-database-specific bugs (SQL dialect quirks, constraint behavior); the container is slower
and needs Docker, but exercises the actual database engine.

</details>

**AP13.** A suite passes locally every time but fails roughly one run in twenty on CI, always on a
different test. What's the FIRST thing this topic teaches you to suspect, before assuming CI's
hardware is simply slower?

<details>
<summary>Worked solution</summary>

A test-isolation/determinism problem (co-26) -- shared mutable state, uncontrolled time, uncontrolled
randomness, or real IO with variable timing/ordering across parallel or reordered runs. "Different test
each time" is a strong signal of leaking shared state rather than one specific test simply being
slow or broken.

</details>

**AP14.** A product manager reads a `.feature` file and says "I understand exactly what this scenario
checks, but I have no idea which function in the codebase actually implements it." Is that a defect in
the `.feature` file? Why or why not?

<details>
<summary>Worked solution</summary>

No -- that's Gherkin (co-29) working as intended. The `.feature` file's job is to be readable by a
non-engineer stakeholder in near-natural language; the mapping from each step to actual executable
code lives in a separate step-definition file (co-30), which the PM was never meant to need to read.

</details>

**AP15.** A team is deciding whether a newly proposed regression (a subtle off-by-one bug reported by
a single internal power user, in a rarely-used admin CSV export) should get a full BDD acceptance
scenario or a targeted unit test. Which fits better, and what's the one-sentence judgment call this
topic teaches for making this decision generally?

<details>
<summary>Worked solution</summary>

A targeted unit test fits better -- low audience breadth (one internal power user, not
customer-facing), low ceremony needed to describe an off-by-one. The general judgment call (co-32):
match the verification ceremony to the change's real risk and its real audience, never apply BDD
acceptance scenarios uniformly just because they exist.

</details>

## Code katas

Eight self-contained exercises. Every kata uses in-memory data and stdlib-only dependencies -- no live
network host, no real database, no Docker container -- so every kata is runnable anywhere this
topic's pinned toolchain (pytest 9.1.1, Hypothesis 6.156.6) is installed, with nothing else to set up.

### Kata 1 -- Write a failing test first, for a function that doesn't exist yet

Write `test_slugify()` asserting `slugify("Hello World!") == "hello-world"` BEFORE writing `slugify`
at all. Run it and confirm it fails with an `ImportError` or `NameError` (co-17, co-23's red step).
Then implement the simplest `slugify` that makes it pass, then refactor it to handle repeated
whitespace and leading/trailing punctuation while the test stays green throughout.

### Kata 2 -- Parametrize a boundary-heavy function

Write a `classify_grade(score: int) -> str` returning `"F"`/`"D"`/`"C"`/`"B"`/`"A"` for standard
letter-grade cutoffs. Write ONE parametrized test (co-06) covering every boundary value (59, 60, 69,
70, ... 100) rather than five separate test functions -- confirm each row shows its own id in `-v`
output.

### Kata 3 -- Build a stub, then a mock, for the same collaborator

Write a `NotificationService` that depends on an injected `sender` object with a `send(to, body)`
method. Write one test using a STUB sender (co-12, returns a canned success value, assertion checks
the service's own return value) and a second test using a MOCK sender (co-13, assertion checks
`sender.send.assert_called_once_with(...)`) for the same underlying behavior -- confirm both pass while
asserting genuinely different things.

### Kata 4 -- A property test that catches a seeded bug

Write `dedupe(xs: list[int]) -> list[int]` with a deliberately planted bug (e.g. it also silently
drops legitimate duplicates of the value `0`). Write a Hypothesis property test (co-18) asserting
`len(set(dedupe(xs))) == len(set(xs))` over `st.lists(st.integers())` -- confirm it fails, read the
shrunk counterexample (co-19), fix the bug, and confirm the same test then passes.

### Kata 5 -- Freeze time and seed randomness in one fixture

Write a function `greeting_id() -> str` that combines the current hour and a random 4-digit suffix.
Write a fixture that both freezes the clock (`monkeypatch`, co-14) and seeds the RNG (co-26) so two
separate test runs of the same test produce the IDENTICAL output -- confirm by running the test twice
and diffing the captured output.

### Kata 6 -- Deliberately plant a surviving mutant, then kill it

Write a `is_adult(age: int) -> bool` returning `age >= 18`. Write ONE test that only checks `age = 25`
and `age = 10`. Manually mutate the source to `age > 18` (simulating what `mutmut` would try, co-22)
and confirm your existing test suite still passes against the mutant -- then add a boundary test for
`age == 18` and confirm the mutant is now caught.

### Kata 7 -- Diagnose and fix an order-dependent test pair

Write two tests sharing a module-scoped fixture that returns a mutable `dict`. Test A mutates it; Test
B asserts on its original state. Run them in both orders (`pytest test_x.py::test_a test_x.py::test_b`
vs. reversed) and observe the order-dependent failure (co-26) -- then fix it by narrowing the fixture's
scope to `function` and confirm both orders now pass identically.

### Kata 8 -- Write one Gherkin scenario and bind it two ways

Write a `.feature` file with one `Given`/`When`/`Then` scenario for a simple `Stack` (`push`, then
`pop` returns the pushed value). Bind it once with `pytest-bdd` step definitions and once with
`behave` step definitions (co-30) against the SAME `.feature` file -- confirm both runners report the
identical scenario passing.

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can name the three phases of arrange-act-assert and explain what each one is responsible for.
      (co-01)
- [ ] I can state pytest's exact file- and function-naming discovery convention from memory. (co-02)
- [ ] I can explain why pytest doesn't need a separate `assertEqual`/`assertTrue` method zoo. (co-03)
- [ ] I can write a `pytest.raises(..., match=...)` block from memory, including what `match` actually
      checks. (co-04)
- [ ] I can explain what code placed after a fixture's `yield` does and when it runs. (co-05)
- [ ] I can state how many times a `@pytest.mark.parametrize`d test body runs for N rows, and how
      those runs are reported. (co-06)
- [ ] I can explain why `0.1 + 0.2 == 0.3` is `False` in Python and name the pytest helper that fixes
      an assertion built on it. (co-07)
- [ ] I can explain the practical difference between `@pytest.mark.skip` and `@pytest.mark.xfail`.
      (co-08)
- [ ] I can explain how a `conftest.py` fixture becomes available to test files without any import.
      (co-09)
- [ ] I can describe the pyramid and the testing trophy and state which tier each one weights most
      heavily. (co-10)
- [ ] I can name all five kinds of test double in the Meszaros taxonomy and the one dimension that
      separates mocks from the rest. (co-11)
- [ ] I can explain what a stub does and does NOT do, distinct from a mock. (co-12)
- [ ] I can explain what `assert_called_once_with(...)` verifies, distinct from a return-value
      assertion. (co-13)
- [ ] I can explain when `monkeypatch`'s patches get restored, and why no manual teardown is needed.
      (co-14)
- [ ] I can explain what makes a spy different from a mock, in terms of whether the real behavior
      still executes. (co-15)
- [ ] I can explain what makes a fake different from a stub, in terms of whether it's a genuinely
      working implementation. (co-16)
- [ ] I can state TDD's three steps in the correct order and explain why the test must fail first, for
      a real reason. (co-17)
- [ ] I can explain how a property-based test chooses its inputs differently from a parametrized test.
      (co-18)
- [ ] I can explain what shrinking does to a failing generated input, and why it matters for
      debuggability. (co-19)
- [ ] I can explain what a Hypothesis strategy describes, and what `assume()` does to generated values
      that fail its condition. (co-20)
- [ ] I can explain what 100% line coverage actually guarantees and what it does NOT guarantee. (co-21)
- [ ] I can explain what a "surviving mutant" tells you about your test suite, and what action it
      calls for. (co-22)
- [ ] I can explain what distinguishes an integration test from a unit test that stubs the same seam.
      (co-23)
- [ ] I can explain what contract testing lets two independently-deployed services verify without
      running together. (co-24)
- [ ] I can explain what an end-to-end test drives that a typical integration test doesn't, and what
      problem test-containers solve. (co-25)
- [ ] I can name at least three distinct sources of test nondeterminism this topic teaches you to
      control. (co-26)
- [ ] I can read a one-line pytest summary (`N failed, M passed, K skipped`) and state what each count
      means before opening any traceback. (co-27)
- [ ] I can rewrite a plain test description as a Given/When/Then scenario and name BDD's intended
      dual audience. (co-28)
- [ ] I can name Gherkin's four step keywords in order and explain what `And` does relative to the
      keyword before it. (co-29)
- [ ] I can explain what a step definition does and name the two Python BDD runners this topic
      teaches. (co-30)
- [ ] I can explain how many times a `Scenario Outline` with an `Examples` table of N rows actually
      runs, and its pytest-side analog. (co-31)
- [ ] I can state, in one sentence, the judgment call for choosing a BDD acceptance scenario over a
      plain unit test for a given change. (co-32)
- [ ] I can explain what `correctness-vs-pragmatism` means for this topic -- name one technique that
      exposes it directly, and why 100% of any single metric (coverage, or an all-green suite) is
      never by itself proof of correctness. (`correctness-vs-pragmatism`)

---

← Previous: [Capstone](../learning/capstone/overview.md)
