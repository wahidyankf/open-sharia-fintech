---
title: "Experiment design and analysis"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

An experiment earns its causal interpretation before anyone sees a result. Start with a hypothesis,
OEC, guardrails, allocation unit, assignment method, minimum detectable effect, sample size, exposure
window, and decision rule. Then preserve those commitments. A complicated test after a weak design
does not restore the counterfactual.

## Randomize and plan for information

| Example                            | Decision artifact                                        | Verify                                                      | Concepts     |
| ---------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------- | ------------ |
| ex-27 · randomized-assignment-hash | Hash user ID plus experiment salt into two arms.         | A large fixed fixture is near 50/50.                        | co-10        |
| ex-28 · deterministic-bucketing    | Repeat assignment for the same ID.                       | It returns the same arm.                                    | co-10        |
| ex-29 · assignment-independence    | Compare arm share by pre-treatment platform.             | No systematic allocation difference appears.                | co-10        |
| ex-30 · type-i-and-ii-errors       | Null and true-effect simulation.                         | False positives approximate alpha; misses approximate beta. | co-11        |
| ex-31 · power-definition           | Power as `1 - beta` at an effect and N.                  | Power rises with N and effect size.                         | co-11        |
| ex-32 · sample-size-formula        | Per-arm estimate `16 * variance / delta²` for 80% power. | A simulation gives a compatible order of magnitude.         | co-12        |
| ex-33 · mde-tradeoff               | Required N across candidate MDEs.                        | Halving MDE roughly quadruples N.                           | co-12        |
| ex-34 · power-curve                | Power across effect sizes for a fixed N.                 | The chosen MDE crosses the planned power bar.               | co-11, co-12 |

### Worked mechanism: persistent assignment

```python
from __future__ import annotations

from hashlib import sha256
from typing import Literal


Arm = Literal["control", "treatment"]


def assign(user_id: str, experiment_salt: str) -> Arm:
    digest: bytes = sha256(f"{experiment_salt}:{user_id}".encode()).digest()
    bucket: int = int.from_bytes(digest[:8], "big") % 100
    return "control" if bucket < 50 else "treatment"


assert assign("user-42", "editor-layout-v1") == assign("user-42", "editor-layout-v1")
```

Persistence stops a user moving between experiences. Independence means the function must use no
treatment-affected property such as a completed purchase. Uniformity is checked empirically with an
SRM guardrail; “the hashing code looks reasonable” is not evidence enough.

## Estimate an effect without overclaiming

| Example                             | Decision artifact                                           | Verify                                                             | Concepts     |
| ----------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ | ------------ |
| ex-35 · two-proportion-z-test       | Conversion difference, z statistic, and two-sided p-value.  | A hand calculation agrees.                                         | co-13        |
| ex-36 · welch-t-test                | Continuous-metric comparison that allows unequal variances. | It differs from pooled-variance assumptions when variance differs. | co-13        |
| ex-37 · p-value-compute             | A null-distribution tail probability.                       | Null simulations are approximately uniform.                        | co-13        |
| ex-38 · p-value-misinterpretation   | Explicit non-claims about `P(null)` and `1 - P(effect)`.    | A counterexample rejects both readings.                            | co-13        |
| ex-39 · ci-p-value-agreement        | 95% CI and alpha .05 test from one model.                   | Both make the same zero-effect decision.                           | co-14        |
| ex-40 · bootstrap-ci                | Resampled difference interval.                              | It tracks an analytic interval on normal data.                     | co-14        |
| ex-41 · ship-no-ship-decision       | Typed decision from effect, CI, OEC, and guardrails.        | A broken guardrail vetoes a significant win.                       | co-09, co-07 |
| ex-42 · guardrail-check-in-analysis | Outcome and latency results reported together.              | Latency regression remains visible beside conversion.              | co-07        |

A p-value is the probability, under a specified null model, of a result at least as extreme as the
one observed. It is neither the probability that the null is true nor the probability the change is
worth shipping. The confidence interval shows magnitude and plausible uncertainty; a team still
needs a pre-stated practical bar and guardrails.

## Validate the experiment before interpreting it

| Example                               | Decision artifact                                                      | Verify                                                    | Concepts |
| ------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------- | -------- |
| ex-43 · srm-chi-square                | Observed versus expected arm counts.                                   | A clean 50/50 split passes and a large 52/48 split fails. | co-18    |
| ex-44 · srm-guardrail-abort           | An analysis gate before effects are reported.                          | Failed SRM returns an abort, not a winner.                | co-18    |
| ex-45 · cuped-adjustment              | Pre-period covariate and `theta = cov(Y, X) / var(X)`.                 | Adjusted arm means preserve the expected difference.      | co-19    |
| ex-46 · cuped-variance-reduction      | Raw versus adjusted variance.                                          | Reduction is near `1 - rho²` for a correlated covariate.  | co-19    |
| ex-47 · delta-method-ratio-metric     | Ratio variance based on numerator and denominator variance/covariance. | It differs from naive per-user-ratio variance.            | co-08    |
| ex-48 · sequential-vs-fixed-preview   | Fixed-horizon and designed sequential procedures.                      | Each controls alpha when its own rules are used.          | co-15    |
| ex-49 · bonferroni-correction         | Family-wise alpha divided by number of planned tests.                  | The adjusted threshold is lower than alpha.               | co-16    |
| ex-50 · benjamini-hochberg-fdr        | Ranked p-values and the largest accepted rank.                         | It can retain more discoveries than Bonferroni.           | co-16    |
| ex-51 · multiple-metrics-family       | One declared metric family.                                            | Naive “any green” creates more false wins.                | co-16    |
| ex-52 · frequentist-vs-bayesian-intro | Side-by-side question and decision rule.                               | Each answer is labeled with its framework.                | co-25    |
| ex-53 · bayesian-beta-posterior       | Two Beta posteriors for binary conversion.                             | Monte Carlo agrees with a grid approximation.             | co-25    |
| ex-54 · feature-flag-assignment       | Flag state as the same mapping as experiment arm.                      | One user cannot receive conflicting mappings.             | co-26    |

**Stop rule:** a failing SRM invalidates the result. Do not “adjust for it” and continue. A pre-period
covariate can reduce variance only when it is measured before treatment; post-treatment adjustment
can erase or manufacture the very effect being measured.

← Previous: [Instrumentation and product measures](./instrumentation-and-product-measures.md) · Next:
[Honest reads and safe delivery](./honest-reads-and-safe-delivery.md) →
