# CI/CD and Release Engineering (By Example, YAML + Python)

**Course ID**: `cicd-and-release-engineering` · **Format**: By Example · **Language**: YAML + Python.

**Short summary**: Pipelines, artifacts, deployment, release

**Scope note**: automating the path from commit to production — GitHub Actions hands-on (matrix
builds, caching, artifacts, environments, secrets, reusable/composite workflows), CD strategies
(blue-green, canary, progressive delivery), release automation, and supply-chain basics (SLSA,
provenance, signing). GitHub Actions is free for public repos, so every example is reproducible.
`†`: pipelines are YAML; automation scripts are Python, fully type-annotated (DD-39) — every snippet
carries type hints in the pyright-clean spirit.

## Why this exists · the big idea

- **The problem before the solution**: manual releases are where quality goes to die — a human runs
  the tests "usually", copies a build to a server on a Friday, and forgets a step, so the difference
  between what was tested and what's in production is a mystery nobody can reconstruct. Ship-by-hand
  makes every deploy a risk and every rollback a scramble.
- **Keep-this-if-you-forget-everything**: make the path from commit to production a single automated,
  repeatable pipeline — every change goes through the same gates, produces the same kind of artifact,
  and deploys the same way, so a release is boring and a rollback is a button.
- **Big ideas touched**: `correctness-vs-pragmatism` (a pipeline encodes "provably tested" as gates
  but must still ship — you tune which checks block vs warn so the gate protects without paralyzing),
  `mechanism-vs-policy` (the CI/CD engine is mechanism — runners, steps, artifacts — while _what
  must pass to deploy_ and _who approves production_ are policy layered on top, and keeping them
  separate is what makes both reusable).

## Prerequisites

- **Prior topics**: [topic 6 Version Control & Git](./version-control-and-git.md) (branches, PRs,
  the trunk the pipeline triggers on), [topic 15 Software Testing](./software-testing.md) (the
  gates a pipeline runs), [topic 30 Software Engineering Practices](./software-engineering-practices.md)
  (review, trunk-based flow), [topic 50 Containers & Orchestration](./containers-and-orchestration.md)
  (the image artifact you build and deploy), and [topic 51 Cloud & IaC](./cloud-and-iac.md) (the
  environments you deploy into).
- **Tools & environment**: a macOS/Linux terminal; a **GitHub** repo (public, so Actions is free);
  the `gh` CLI; **Python** at a recent stable release with type hints and `pyright` for automation
  scripts; a container registry and a deploy target (from topics 50/51); optionally `cosign`/an SLSA
  provenance tool; Neovim/VSCode with YAML + Python LSPs (DD-17).
- **Assumed knowledge**: opening a PR against a trunk (topic 06); running a test suite from the CLI
  (topic 15); building a container image (topic 50); provisioning an environment (topic 51).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **GitHub Actions** remains free for standard runners on public repositories
  and is the widely adopted CI/CD platform for open source. The workflow syntax (jobs/steps/matrix/
  caching/`environment`/`secrets`, reusable and composite workflows) is stable; left correctly
  version-unpinned, but pin specific action versions (by SHA for supply-chain safety) at drafting.
- 2026-07-12 — verified (GAP for plan owner): supply-chain tooling is the fastest-moving part —
  **SLSA** (provenance levels) and artifact signing (Sigstore/`cosign`) evolve; teach the concepts
  (provenance, attestation, signature verification) and pin exact tool versions/commands only when the
  examples are drafted. DORA metrics remain the standard delivery-performance frame.

> DD-35 primary-source pass (2026-07-12). Definitions, spec rules, and CLI/YAML field names traced to
> primary sources (martinfowler.com, Farley's 2007 pipeline paper, semver.org, conventionalcommits.org,
> docs.github.com, dora.dev, trunkbaseddevelopment.com, nvie.com, jenkins.io) and fetched/read. Fast-moving
> action versions and numeric thresholds flagged.

- **Continuous integration** — Fowler: "each member of a team merges their changes into a codebase … at
  least daily. Each of these integrations is verified by an automated build (including test) to detect
  integration errors as quickly as possible." Formalized by Kent Beck as an XP practice; the exact
  _Extreme Programming Explained_ book wording is `[Needs Verification]` (Fowler's XP-origin attribution is
  `[Verified]`). Source: [Fowler — Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) (fetched, verbatim).
- **Continuous delivery vs deployment** — CD = "build software in such a way that the software can be
  released to production at any time"; continuous deployment = "every change goes through the pipeline and
  automatically gets put into production." CD is the prerequisite capability; deployment is the policy of
  always shipping. Source: [Fowler — ContinuousDelivery](https://martinfowler.com/bliki/ContinuousDelivery.html) (fetched, verbatim); book: Humble & Farley, _Continuous Delivery_ (2010).
- **Deployment pipeline** — Farley (2007): "this sequence of gates, as a Deployment Pipeline"; "The objective
  of these commit-tests is to fail fast"; "it is not possible to progress any release candidate beyond this
  stage into production unless all acceptance criteria are met." Stages: commit → compile → unit test →
  assemble → acceptance → deploy. Source: [Farley — The Deployment Pipeline (PDF, 2007)](https://continuousdelivery.com/wp-content/uploads/2010/01/The-Deployment-Pipeline-by-Dave-Farley-2007.pdf) (fetched PDF, verbatim, page-cited).
- **Trunk-based development / GitFlow** — TBD: "developers collaborate on code in a single branch called
  'trunk' … resist any pressure to create other long-lived development branches"
  ([trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/), fetched). GitFlow (Driessen) with the
  verbatim 2020 caveat: "If your team is doing continuous delivery of software, I would suggest to adopt a
  much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team."
  ([nvie.com](https://nvie.com/posts/a-successful-git-branching-model/), fetched, verbatim).
- **GitHub Actions syntax** — "A workflow run is made up of one or more `jobs`, which run in parallel by
  default"; "run jobs sequentially … using the `jobs.<job_id>.needs` keyword"; "A matrix strategy lets you
  use variables … to automatically create multiple job runs" (`fail-fast` default true, `max-parallel`);
  `uses` references `{owner}/{repo}@{ref}`; a job referencing an `environment` "must follow any protection
  rules … before … accessing the environment's secrets." Source: [GitHub — Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) (fetched, verbatim; large page — some sections cross-verified).
- **Caching / artifacts** — `actions/cache` (v6 at fetch): "caching dependencies and build outputs to
  improve workflow execution time" (`key`/`restore-keys`/`cache-hit`); `actions/upload-artifact` (v7) /
  `download-artifact` (v8). **Action major versions bump periodically — re-verify + SHA-pin before drafting.**
  Sources: [actions/cache](https://github.com/actions/cache), [upload-artifact](https://github.com/actions/upload-artifact) (fetched).
- **Required status checks** — "all required status checks must pass before collaborators can merge changes
  into the protected branch." Source: [GitHub — Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) (fetched, verbatim).
- **Semantic Versioning 2.0.0** — "increment the: MAJOR … when you make incompatible API changes; MINOR …
  when you add functionality in a backward compatible manner; PATCH … when you make backward compatible bug
  fixes." Pre-release has lower precedence than the normal version (`1.0.0-alpha < 1.0.0`). Source:
  [semver.org](https://semver.org/) (fetched, verbatim).
- **Conventional Commits 1.0.0** — structure `<type>[optional scope]: <description>`; `feat` correlates with
  SemVer MINOR, `fix` with PATCH; a breaking change is `BREAKING CHANGE:` footer or `!` before the colon.
  Source: [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/) (fetched, verbatim).
- **Release automation** — semantic-release "automates the whole package release workflow including:
  determining the next version number, generating the release notes, and publishing the package." Source:
  [semantic-release docs](https://semantic-release.gitbook.io/semantic-release) (fetched, verbatim). Publishing:
  `npm publish` "Publishes a package to the registry"; `docker image push` "share your images to … a
  registry." Sources: [npm publish](https://docs.npmjs.com/cli/v11/commands/npm-publish), [docker push](https://docs.docker.com/reference/cli/docker/image/push/) (fetched).
- **Deployment strategies** — blue-green: maintain "two production environments, as identical as possible" and
  "switch the router" (Fowler, [BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html), fetched). Canary: "slowly rolling out the change to a small
  subset of users before rolling it out to the entire infrastructure" (Sato, [CanaryRelease](https://martinfowler.com/bliki/CanaryRelease.html), fetched). Rollback:
  Google SRE — on a bad canary "we should pause and roll back the deployment"
  ([SRE Workbook — Canarying](https://sre.google/workbook/canarying-releases/), fetched). The "roll back first, investigate second" framing is `[Needs Verification]`
  (not found verbatim in the two SRE chapters read).
- **Feature toggles** — Hodgson's four categories verbatim: **Release Toggles** ("ship … as latent code"),
  **Experiment Toggles** ("multivariate or A/B testing … cohort"), **Ops Toggles** ("control operational
  aspects … disable or degrade … quickly"), **Permissioning Toggles** ("change the features … certain users
  receive"). Source: [Fowler/Hodgson — Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) (fetched, verbatim).
- **Pipeline as code** — Jenkins: "The definition of a Jenkins Pipeline is written into a text file (called a
  `Jenkinsfile`) which … can be committed to a project's source control repository. This is the foundation of
  'Pipeline-as-code'." Source: [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/) (fetched, verbatim).
- **Quality gates** — CodeQL "is the code analysis engine developed by GitHub to automate security checks"
  (SAST); Dependabot: alerts / security updates / version updates. Sources: [GitHub — Code scanning](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning), [Dependabot](https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide) (fetched, verbatim).
- **DORA four keys** — Deployment Frequency ("number of deployments over a given period"), Change Lead Time
  ("time … for a change to go from committed … to deployed in production"), Change Failure Rate ("ratio of
  deployments that require immediate intervention"), Failed Deployment Recovery Time ("time it takes to
  recover"). Definitions `[Verified]`; the **Elite/High/Medium/Low numeric thresholds and any 2025
  percentile-shift are `[Needs Verification]`** (gated report PDF not fetchable — treat benchmarks as
  illustrative). Source: [dora.dev — DORA metrics](https://dora.dev/guides/dora-metrics-four-keys/) (fetched, verbatim).
- **Runners / OIDC** — self-hosted runners "Give you more control of hardware, operating system, and
  software" but "should almost never be used for public repositories … any user can open pull requests …
  and compromise the environment." OIDC lets a workflow "request a short-lived access token directly from the
  cloud provider" instead of storing long-lived secrets. Sources: [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners), [OIDC hardening](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect) (fetched, verbatim).
- **Monorepo affected CI** — Nx: "Nx determines the minimum set of projects that are affected by the change
  [and] only runs tasks on those affected projects"; default `base` = main branch, `head` = working tree.
  Source: [Nx — Affected](https://nx.dev/ci/features/affected) (fetched, verbatim).
- **Progressive delivery + automated canary (co-33/co-34, ex-81–83)** — added 2026-07-12. The umbrella term
  "progressive delivery" (canary/blue-green/flags gated by metrics; decouple deploy from release) is
  attributed to James Governor / RedMonk — `[Needs Verification]`: confirm the coinage against redmonk.com
  before quoting. **Argo Rollouts** (canary/blue-green + `AnalysisTemplate` metric gating, auto-promote/
  rollback) and **Flagger** (weighted traffic shift driven by success-rate/latency metric checks) are both
  **Apache-2.0** CNCF-ecosystem controllers — `[Needs Verification]` at authoring: confirm each project's
  current CRD field names + license against argoproj.github.io/argo-rollouts + fluxcd.io/flagger before
  drafting the ex-81/ex-82 manifests. Existing blue-green/canary/feature-toggle citations above (Fowler/
  Sato/Hodgson, all fetched-verbatim) remain the primary sources for co-23–25.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · continuous-integration** — merge to a shared mainline at least daily, each integration verified
  by an automated self-testing build (Fowler/Beck XP).
- **co-02 · continuous-delivery** — build so the software can be released to production at any time (Humble &
  Farley).
- **co-03 · continuous-deployment** — every change that passes the pipeline is automatically deployed to
  production.
- **co-04 · deployment-pipeline** — a sequence of gates that build a single promotable artifact once and
  raise confidence at each stage (Farley).
- **co-05 · commit-stage-fail-fast** — the commit stage runs the fastest tests first and fails fast.
- **co-06 · acceptance-test-gate** — only release candidates that pass all acceptance tests progress toward
  production.
- **co-07 · trunk-based-development** — collaborate on a single trunk, avoiding long-lived branches.
- **co-08 · gitflow-and-caveat** — the GitFlow develop/release/hotfix model, and Driessen's 2020 caveat to
  prefer a simpler flow for continuous delivery.
- **co-09 · github-actions-workflow** — a workflow's `on`/`jobs`/`steps`/`runs-on`/`run`/`uses` YAML.
- **co-10 · matrix-builds** — a matrix strategy runs a job across variable combinations (`fail-fast`,
  `max-parallel`).
- **co-11 · job-dependencies** — `needs` sequences jobs by dependency.
- **co-12 · caching** — `actions/cache` keys and restores dependencies/build outputs to speed the pipeline.
- **co-13 · artifacts** — `upload-artifact`/`download-artifact` pass build outputs between jobs.
- **co-14 · required-status-checks** — required checks must pass before a protected branch accepts a merge.
- **co-15 · environments-approvals** — a protected `environment` with required reviewers gates production.
- **co-16 · secrets-in-ci** — secrets are injected via the `secrets` context and masked in logs.
- **co-17 · oidc-cloud-auth** — OIDC issues a short-lived cloud token per job instead of storing long-lived
  credentials.
- **co-18 · reusable-composite-workflows** — reusable workflows and composite actions factor shared pipeline
  logic.
- **co-19 · semantic-versioning** — MAJOR.MINOR.PATCH conveys incompatible / additive / fix changes (SemVer
  2.0.0).
- **co-20 · conventional-commits** — `type(scope): description` with `feat`/`fix`/`BREAKING CHANGE` driving
  versioning.
- **co-21 · release-automation** — tags, releases, and changelogs generated automatically (semantic-release).
- **co-22 · package-publishing** — publishing artifacts to a registry (`npm publish`, `docker push`).
- **co-23 · blue-green-deployment** — two identical environments with a router switch for instant cutover and
  rollback (Fowler).
- **co-24 · canary-release** — gradually shift traffic to a new version over a subset before full rollout
  (Sato).
- **co-25 · feature-toggles** — release / experiment / ops / permission toggles change behavior without
  changing code (Hodgson).
- **co-26 · rollback-forward-fix** — recover from a bad deploy by rolling back or fixing forward.
- **co-27 · pipeline-as-code** — the pipeline definition lives in version control and is reviewed like code.
- **co-28 · quality-gates** — lint, type-check, coverage, SAST, and dependency scans gate the pipeline.
- **co-29 · supply-chain-provenance** — SLSA provenance/attestation and Sigstore/cosign signing let consumers
  verify what they run.
- **co-30 · dora-metrics** — deployment frequency, change lead time, change failure rate, and recovery time
  are the four delivery-performance keys.
- **co-31 · self-hosted-vs-hosted-runners** — hosted vs self-hosted runners trade control for upkeep, and
  self-hosted on public repos is a security risk.
- **co-32 · monorepo-affected-ci** — an affected-graph build runs only the tasks touched by a change (Nx
  affected).
- **co-33 · progressive-delivery** — the umbrella over blue-green / canary / feature-flags / ring
  deployments (co-23–25): release to progressively wider audiences gated by health and metrics, decoupling
  _deploy_ from _release_ to shrink blast radius (term coined by James Governor / RedMonk).
- **co-34 · automated-canary-analysis** — controllers that drive the rollout from live metric analysis rather
  than a human clicking promote: **Argo Rollouts** and **Flagger** (both Apache-2.0) shift traffic in weighted
  steps, evaluate a success-rate / latency SLO at each step, and auto-promote or auto-rollback — the GitOps
  form of progressive delivery (ties to [`53-self-managed-kubernetes-and-gitops`](./self-managed-kubernetes-and-gitops.md)).

## Tensions & trade-offs — when NOT to reach for this

- **A slow or flaky pipeline is worse than none**: if CI takes 40 minutes or fails randomly,
  developers learn to ignore or bypass it, and the gate stops protecting anything. Pipeline speed and
  reliability are first-class — cache aggressively, parallelize, and quarantine flakes, or the whole
  discipline erodes.
- **Not every project needs canary and provenance**: blue-green, progressive delivery, and full SLSA
  provenance solve real risks at scale, but on a small internal service they're operational weight
  with little payoff. Match the deployment strategy to the blast radius, not to the trend.
- **Gates can ossify**: every mandatory check is a tax on every change. A gate that blocks more than it
  catches — a redundant lint, a duplicative test tier — should be demoted to a warning. The goal is
  the fewest gates that keep production safe, not the most gates possible.

## Lineage — why it beat the alternative

- CI/CD grew out of the pain of "integration hell" and big-bang releases: continuous integration
  (merge and test constantly) answered the first, and _Continuous Delivery_ (Humble and Farley, 2010)
  named the discipline of keeping software always-releasable through an automated pipeline. The
  _Accelerate_/DORA research then showed empirically that elite delivery performance — frequent,
  low-risk deploys with fast recovery — correlates with these practices, which settled the debate in
  their favor. Managed platforms like GitHub Actions made the pipeline itself version-controlled and
  reusable. This hands a reliable, automated release path to
  [topic 93 Platform Engineering & Developer Experience](./platform-engineering-and-devex.md)
  (golden paths built on it) and depends on the containers and infrastructure of
  [topic 50 Containers & Orchestration](./containers-and-orchestration.md) and
  [topic 51 Cloud & IaC](./cloud-and-iac.md).

## Worked examples

Colocated under `cicd-and-release-engineering/learning/code/`; each is a runnable GitHub Actions
workflow (public-repo free) plus typed Python automation, `pyright`-clean (DD-20/DD-30/DD-34/DD-39). Contiguous
`ex-01..ex-83`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · ci-daily-merge** — annotate the daily-merge + self-testing-build CI practice — verify both
  halves are named. (co-01)
- **ex-02 · ci-broken-build-fix** — a red build blocking the mainline until fixed — verify merges pause
  while red. (co-01)
- **ex-03 · cd-always-releasable** — annotate the always-releasable capability — verify releasability is
  continuous. (co-02)
- **ex-04 · cd-vs-continuous-deployment** — a decision table CD (capability) vs continuous deployment
  (policy) — verify the distinction. (co-02, co-03)
- **ex-05 · continuous-deployment-auto** — annotate auto-deploy on every green pipeline — verify no manual
  gate. (co-03)
- **ex-06 · deployment-pipeline-stages** — annotate commit → test → acceptance → deploy stages — verify the
  order. (co-04)
- **ex-07 · commit-stage-fail-fast** — a fast commit-test stage that fails early — verify slow tests run
  later. (co-05)
- **ex-08 · acceptance-gate** — a gate blocking promotion until acceptance passes — verify a failing
  candidate can't progress. (co-06)
- **ex-09 · tbd-single-trunk** — annotate trunk-based single-branch flow — verify no long-lived branch.
  (co-07)
- **ex-10 · gitflow-branches** — annotate GitFlow develop/release/hotfix branches — verify each branch's
  role. (co-08)
- **ex-11 · gitflow-cd-caveat** — annotate Driessen's 2020 "prefer a simpler flow for CD" caveat — verify the
  caveat is quoted. (co-08)
- **ex-12 · gha-hello-workflow** — a minimal `on: push` workflow with one job/step — verify it runs. (co-09)
- **ex-13 · gha-on-triggers** — `on: [push, pull_request]` triggers — verify both events fire it. (co-09)
- **ex-14 · gha-run-vs-uses** — a `run:` step and a `uses:` action step — verify each step type. (co-09)
- **ex-15 · gha-runs-on** — `runs-on: ubuntu-latest` — verify the runner OS. (co-09)
- **ex-16 · gha-python-setup** — `actions/setup-python` then run pytest — verify tests execute. (co-09)
- **ex-17 · matrix-python-versions** — a matrix across Python versions — verify one job per version. (co-10)
- **ex-18 · matrix-fail-fast** — annotate `fail-fast`/`max-parallel` on a matrix — verify their effect.
  (co-10)
- **ex-19 · job-needs** — a deploy job with `needs: [test]` — verify it waits for test. (co-11)
- **ex-20 · cache-deps** — `actions/cache` with a `hashFiles` key — verify a cache hit skips install.
  (co-12)
- **ex-21 · cache-hit-output** — branch on the `cache-hit` output — verify conditional restore. (co-12)
- **ex-22 · upload-artifact** — `actions/upload-artifact` of a build — verify the artifact is stored.
  (co-13)
- **ex-23 · download-artifact** — `actions/download-artifact` in a later job — verify it consumes the
  upload. (co-13)
- **ex-24 · required-check** — annotate a required status check gating merge — verify a red check blocks.
  (co-14)
- **ex-25 · semver-increment** — annotate MAJOR/MINOR/PATCH increments — verify each maps to a change kind.
  (co-19)
- **ex-26 · semver-precedence** — annotate pre-release precedence ordering — verify `1.0.0-alpha < 1.0.0`.
  (co-19)
- **ex-27 · conventional-commit** — a `feat(scope): …` commit message — verify the type/scope form. (co-20)

### Intermediate

- **ex-28 · conventional-commit-breaking** — a `feat!:` or `BREAKING CHANGE:` footer — verify the breaking
  marker. (co-20)
- **ex-29 · conventional-to-semver** — map feat→minor, fix→patch, breaking→major — verify each correlation.
  (co-19, co-20)
- **ex-30 · protected-environment** — an `environment:` with a required reviewer — verify the gate exists.
  (co-15)
- **ex-31 · approval-wait** — annotate a deploy job waiting for approval — verify it blocks pre-approval.
  (co-15)
- **ex-32 · secret-injection** — reference `${{ secrets.X }}` in `env` — verify the value is injected.
  (co-16)
- **ex-33 · secret-masking** — annotate `::add-mask::` + the no-redact-if-not-a-secret caveat — verify
  masking behavior. (co-16)
- **ex-34 · oidc-cloud-token** — annotate the OIDC short-lived-token flow (no stored creds) — verify the
  token is per-job. (co-17)
- **ex-35 · reusable-workflow** — a `workflow_call` reusable workflow — verify a caller invokes it. (co-18)
- **ex-36 · composite-action** — a composite action factoring shared steps — verify reuse with no
  duplication. (co-18)
- **ex-37 · reusable-secrets** — pass secrets to a reusable workflow — verify the callee receives them.
  (co-18, co-16)
- **ex-38 · release-tag** — create a git tag + GitHub Release — verify the release is published. (co-21)
- **ex-39 · changelog-gen** — generate a changelog from conventional commits — verify entries group by
  type. (co-21)
- **ex-40 · semantic-release** — annotate semantic-release automating version + release — verify the
  automation chain. (co-21)
- **ex-41 · npm-publish** — `npm publish` to a registry — verify the package is installable by name. (co-22)
- **ex-42 · docker-push** — `docker push` to a registry after login — verify the image is pushed. (co-22)
- **ex-43 · lint-gate** — a lint job as a required check — verify a lint failure blocks. (co-28)
- **ex-44 · typecheck-gate** — a `pyright` type-check gate on Python — verify a type error blocks. (co-28)
- **ex-45 · coverage-gate** — a coverage-threshold gate — verify below-threshold blocks. (co-28)
- **ex-46 · sast-codeql** — annotate a CodeQL SAST scan job — verify it reports findings. (co-28)
- **ex-47 · dependency-scan** — annotate Dependabot alerts/security/version updates — verify the three
  update kinds. (co-28)
- **ex-48 · pipeline-as-code** — annotate the pipeline living in version control — verify it is
  reviewed/diffed. (co-27)
- **ex-49 · jenkinsfile-compare** — annotate a `Jenkinsfile` as pipeline-as-code (vs GHA) — verify the
  common idea. (co-27)
- **ex-50 · self-hosted-runner** — annotate a self-hosted runner + its tradeoffs — verify control-vs-upkeep.
  (co-31)
- **ex-51 · self-hosted-public-repo-risk** — annotate the public-repo self-hosted-runner security warning —
  verify the fork-PR risk. (co-31)
- **ex-52 · monorepo-affected** — `nx affected -t test` in CI — verify only touched projects run. (co-32)
- **ex-53 · affected-base-head** — annotate base/head diff driving affected — verify the diff source.
  (co-32)
- **ex-54 · required-checks-script** — a typed Python script asserting required checks passed — verify it
  gates on the check status. (co-14)
- **ex-55 · fail-fast-ordering** — annotate cheap gates ordered before expensive ones for fast feedback —
  verify the ordering. (co-05)

### Advanced

- **ex-56 · blue-green-switch** — annotate the blue-green router switch — verify one-shot cutover. (co-23)
- **ex-57 · blue-green-rollback** — annotate instant rollback by switching the router back — verify recovery
  is immediate. (co-23, co-26)
- **ex-58 · canary-gradual** — annotate a canary gradual traffic shift — verify a small subset first.
  (co-24)
- **ex-59 · canary-cohort** — annotate cohort/percentage selection for the canary — verify targeted rollout.
  (co-24)
- **ex-60 · canary-auto-rollback** — a typed Python canary watcher that rolls back on a bad signal — verify
  a bad metric triggers rollback. (co-24, co-26)
- **ex-61 · progressive-delivery** — annotate progressive delivery with automatic rollback — verify staged
  promotion. (co-24)
- **ex-62 · rollback-vs-fix-forward** — a decision table rollback vs fix-forward — verify when each applies.
  (co-26)
- **ex-63 · feature-toggle-release** — annotate a release toggle hiding latent code — verify unfinished code
  ships dark. (co-25)
- **ex-64 · feature-toggle-experiment** — annotate an experiment/A-B toggle with cohorts — verify consistent
  cohort routing. (co-25)
- **ex-65 · feature-toggle-ops** — annotate an ops toggle (kill switch) — verify runtime disable. (co-25)
- **ex-66 · feature-toggle-permission** — annotate a permission toggle for premium users — verify per-user
  gating. (co-25)
- **ex-67 · toggle-router-python** — a typed Python toggle router — verify it selects a codepath by toggle.
  (co-25)
- **ex-68 · slsa-provenance** — annotate SLSA provenance/attestation — verify build metadata is attested.
  (co-29)
- **ex-69 · cosign-sign** — annotate `cosign sign` on an image — verify the signature is produced. (co-29)
- **ex-70 · cosign-verify** — annotate `cosign verify` at deploy — verify an unsigned image is rejected.
  (co-29)
- **ex-71 · provenance-verify-gate** — a deploy gate verifying signature + provenance — verify it blocks an
  unverifiable artifact. (co-29, co-28)
- **ex-72 · dora-deploy-frequency** — annotate deployment frequency — verify the metric definition. (co-30)
- **ex-73 · dora-lead-time** — annotate change lead time (commit→prod) — verify the definition. (co-30)
- **ex-74 · dora-change-failure-rate** — annotate change failure rate — verify the ratio definition. (co-30)
- **ex-75 · dora-mttr** — annotate failed-deployment recovery time — verify the definition. (co-30)
- **ex-76 · dora-python-report** — a typed Python script computing the four keys from deploy logs — verify
  the four values are produced. (co-30)
- **ex-77 · promotable-artifact** — annotate the single build-once promotable artifact — verify one artifact
  flows through stages. (co-04)
- **ex-78 · commit-to-prod-pipeline** — a full commit→prod GHA pipeline skeleton — verify each stage is
  wired. (co-04, co-09)
- **ex-79 · gates-cost-tradeoff** — annotate demoting a redundant gate to a warning — verify the tax-vs-catch
  reasoning. (co-28)
- **ex-80 · cicd-capstone** — a full pipeline: matrix CI + caching + artifacts + protected env + reusable
  workflow + canary + signing/provenance — verify the end-to-end pipeline goes green and a bad canary
  auto-rolls-back. (co-09, co-13, co-15, co-18, co-24, co-29)

### Progressive delivery

- **ex-81 · argo-rollouts-canary-analysis** — define an Argo Rollouts (Apache-2.0) canary with an
  `AnalysisTemplate` gating each step on a success-rate metric — verify a failing metric auto-aborts and rolls
  back while a passing one auto-promotes, with no human in the loop. (co-34, co-24)
- **ex-82 · flagger-progressive-delivery** — a Flagger (Apache-2.0) canary shifting traffic in weighted steps
  driven by request-success-rate / latency checks — verify traffic advances only while metrics pass and
  halts/rolls back on a breach. (co-34, co-33)
- **ex-83 · progressive-delivery-strategy-decision** — a decision artifact (DD-20) choosing blue-green vs
  canary vs feature-flag rollout for a stated constraint (instant rollback / gradual blast-radius / per-user
  targeting) under the progressive-delivery umbrella — verify each strategy's trade-off is recorded. (co-33, co-23, co-24, co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a full commit-to-production pipeline for a small containerized service on GitHub
  Actions — matrix CI with caching and artifacts, a protected production environment with approval,
  reusable workflow factoring, a canary/progressive deploy with automatic rollback, and a signed
  artifact with provenance — reproducible on a free public repo.
- **Concepts exercised**: [ ] matrix build + caching + artifacts (co-10, co-12, co-13) [ ] protected
  environment + secrets + approval (co-15, co-16) [ ] reusable/composite workflow (co-18) [ ]
  canary/progressive deploy + rollback (co-24, co-26) [ ] artifact signing + provenance (co-29) [ ] a typed
  deploy/automation script (co-30).
- **Ordered steps**:
  1. `.../learning/capstone/.github/workflows/ci.yml` — matrix test jobs, dependency cache, artifact
     upload. Verify the workflow passes on a PR and produces the artifact.
  2. `.../learning/capstone/.github/workflows/deploy.yml` — a protected `environment` with a required
     reviewer + secrets, deploying the built image. Verify the deploy blocks until approval and injects
     secrets safely (never logged).
  3. `.../learning/capstone/.github/actions/` — factor shared logic into a reusable/composite workflow.
     Verify both CI and deploy consume it with no duplication.
  4. `.../learning/capstone/code/rollout.py` — a typed progressive/canary rollout that watches a health
     signal and rolls back on failure, plus image signing + provenance. Verify a simulated bad deploy
     auto-rolls-back and the artifact's signature/provenance verifies.
- **Acceptance criteria**: CI is green with caching and artifacts; production is gated by approval;
  shared logic is reused not copied; a bad canary rolls back automatically; the artifact is signed and
  its provenance verifies; all Python is type-annotated and `pyright`-clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Continuous Delivery** — Jez Humble, David Farley (2010). The book that named and defined the
  discipline of continuous delivery.
- **The DevOps Handbook** — Gene Kim, Jez Humble, Patrick Debois, John Willis (2016). Widely read
  synthesis connecting CI/CD practice to organizational flow.
- **Accelerate** — Nicole Forsgren, Jez Humble, Gene Kim (2018). The empirical research base (DORA
  metrics) behind modern CI/CD and release-engineering best practice.

**Papers & articles**

- **DORA (DevOps Research and Assessment)** — Google Cloud DORA team (ongoing). The primary empirical
  research program behind the deployment-frequency/lead-time metrics used across the industry.
  <https://dora.dev/>
- **GitHub Actions Documentation** — GitHub (ongoing). The authoritative reference for the most widely
  adopted CI/CD platform in open source. <https://docs.github.com/actions>

## In which paths

- `interview-ready/software-engineer` — Phase 2 · Production-effective (web → cloud).
- `immediately-effective/software-engineer` — Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST.
- `fundamentally-strong/software-engineer` — Stage 10 · Scale, cloud & platform ops.

> _Content originated in the now-closed FS-SE plan (topic 55); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
