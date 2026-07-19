# 51 · Cloud & IaC (Annotated-concept, HCL/YAML †)

**prd row**: Pass 3 · Build for the Real World · Annotated-concept · HCL/YAML † · Learn 151 / Drill 251 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the cloud service-model mental map (compute/storage/network/managed services) and
declarative infrastructure as code — the Terraform/OpenTofu plan → apply → destroy lifecycle, state,
modules, and the cost/security discipline of cloud. `†`: the "language" is HCL + YAML; `*`-style annotated
where a concept is diagrammed. Runnable locally against a local provider (LocalStack / a local backend) so
no paid cloud account is required (DD-20). Containers/K8s are [`50-containers-and-orchestration`](./50-containers-and-orchestration.md).

## Why this exists · the big idea

- **The problem before the solution**: infrastructure clicked together by hand in a console is unreviewable,
  unreproducible, and drifts — nobody can say what exists, why, or how to rebuild it after a loss.
- **Keep-this-if-you-forget-everything**: describe infrastructure as declarative code and let the tool
  compute the plan to converge reality to it — infra becomes reviewable, reproducible, and diff-able, at the
  cost of a state file you must guard.
- **Big ideas touched**: `mechanism-vs-policy` (you declare the desired infra; the provider reconciles it),
  `determinism-vs-emergence` (code-defined infra buys reproducibility and drift detection).

## Prerequisites

- **Prior topics**: [topic 50 Containers & Orchestration](./50-containers-and-orchestration.md) (the
  workload to run), [topic 5 Just Enough Bash](./05-just-enough-bash.md)
  (CLI + env), and [topic 11 Backend Essentials](./11-backend-essentials.md) (the service being deployed).
- **Tools & environment**: a macOS/Linux terminal; **Terraform** (or OpenTofu — note the license split,
  DD-15) + a **local provider / LocalStack** so `apply` needs no paid account; a local state backend;
  `docker` (from topic 50). No real cloud credentials committed (secrets rule).
- **Assumed knowledge**: containers + a deployable workload (topic 50); shell + env vars (topic 05); reading
  declarative config (YAML from topic 50).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **Terraform is on the Business Source License 1.1** (HashiCorp writes it "BSL 1.1,
  also known as BUSL 1.1" — both abbreviations are sanctioned; prefer spelling it out once as "Business
  Source License 1.1 (BUSL 1.1, sometimes abbreviated BSL)"). **OpenTofu is MPL-2.0** (Mozilla Public
  License 2.0), a Linux Foundation project. (opentofu.org / github.com/opentofu/opentofu)
- 2026-07-12 — verified: plan → apply → destroy lifecycle, state, modules, providers/resources/variables/
  outputs are unchanged Terraform-core concepts. LocalStack remains the standard no-paid-account local
  AWS-API-compatible provider.

> DD-35 primary-source pass (2026-07-12). Definitions and CLI wording traced to primary sources (NIST
> SP 800-145, developer.hashicorp.com, docs.aws.amazon.com, learn.microsoft.com, docs.cloud.google.com,
> opengitops.dev, opentelemetry.io, martinfowler.com, finops.org) and fetched/read. Unverifiable items flagged.

- **Cloud computing (NIST)** — NIST SP 800-145 (Mell & Grance, Sept 2011): "a model for enabling ubiquitous,
  convenient, on-demand network access to a shared pool of configurable computing resources … composed of
  five essential characteristics, three service models, and four deployment models." Source:
  [NIST SP 800-145 PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf) (fetched, verbatim).
- **Service models** — SaaS/PaaS/IaaS defined verbatim in §2 of SP 800-145 (control boundary descends
  applications→platform→infrastructure). `[Verified]`.
- **Shared responsibility** — AWS: "AWS is responsible for protecting the infrastructure that runs all of
  the services" (Security **of** the Cloud) vs "Customer responsibility will be determined by the AWS Cloud
  services that a customer selects" (Security **in** the Cloud). Azure publishes a customer/shared/Microsoft
  matrix by IaaS/PaaS/SaaS. Sources: [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/), [Azure — Shared responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility) (fetched, verbatim).
- **Core primitives** — EC2 "provides on-demand, scalable computing capacity … An EC2 instance is a virtual
  server"; S3 "stores data as objects … within buckets"; EBS "provides scalable, high-performance block
  storage … used with … EC2 instances." Sources: AWS [EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html), [S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html), [EBS](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html) (fetched, verbatim).
- **Regions & AZs** — "Regions are separate geographic areas … isolated from the other Regions"; "Each Region
  has multiple, isolated locations known as Availability Zones"; span AZs for HA. Source:
  [AWS — Regions and Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) (fetched, verbatim).
- **IaC declarative** — "Terraform's configuration language is declarative, meaning that it describes the
  desired end-state … in contrast to procedural programming languages that require step-by-step instructions."
  Source: [HashiCorp — IaC with Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code) (fetched, verbatim). Idempotency (apply-twice = same state) is a standard CS
  definition; the Ansible glossary wording could not be direct-fetched (docs.ansible.com HTTP 429) — `[Needs Verification]` on the exact Ansible-glossary phrasing.
- **Terraform basics** — providers = "plugins … to interact with cloud providers, SaaS providers, and other
  APIs"; HCL constructs are "arguments" and "blocks"; `init` "initializes a working directory"; `plan`
  "creates an execution plan, which lets you preview the changes"; `apply` "executes the operations proposed
  in a Terraform plan"; `destroy` "deprovisions all objects managed by a Terraform configuration" (alias for
  `apply -destroy`). Source: developer.hashicorp.com/terraform CLI + language pages (fetched, verbatim). `[Verified]`.
- **State & locking** — "Terraform must store state about your … managed infrastructure"; default file
  `terraform.tfstate`; state "can result in … exposure of secrets"; "Terraform will lock your state for all
  operations that could write state … Not all backends support locking." Sources:
  [Terraform state](https://developer.hashicorp.com/terraform/language/state), [state locking](https://developer.hashicorp.com/terraform/language/state/locking) (fetched, verbatim).
- **Modules / dependency graph** — "A module is a collection of resources that Terraform manages together";
  the root config is the "root module"; "Terraform builds a dependency graph … Graph walking is done in
  parallel … By default, up to 10 nodes in the graph will be processed concurrently." Sources:
  [modules](https://developer.hashicorp.com/terraform/language/modules), [graph internals](https://developer.hashicorp.com/terraform/internals/graph) (fetched, verbatim).
- **Drift / import** — refresh-only plan "update[s] the Terraform state … to match changes made to remote
  objects outside of Terraform"; `terraform import` requires you to "manually write a resource configuration
  block" first and "does not generate configuration" (CLI form). Source:
  [plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [import](https://developer.hashicorp.com/terraform/cli/import) (fetched, verbatim).
- **Immutable infrastructure / cattle-not-pets** — Fowler: "An Immutable Server is … a server that once
  deployed, is never modified, merely replaced with a new updated instance"
  ([ImmutableServer](https://martinfowler.com/bliki/ImmutableServer.html), 2013-06-13, fetched). Cattle-vs-pets
  is attributed to Bill Baker (~2011–12) and popularized by Randy Bias; exact original slide wording is
  `[Needs Verification]` (best primary-adjacent source: [Cloudscaling / Bias](http://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/), fetched). The Terraform-vs-Ansible
  provisioning-vs-configuration-management framing is standard but `[Needs Verification]` as a single-source
  quote — cite Kief Morris, _Infrastructure as Code_ (2nd ed.) for the taxonomy.
- **Serverless / managed** — Lambda "is a serverless compute service that lets you run code without
  provisioning or managing servers"; a cold start is the environment-setup on first invocation (Init phase
  "limited to 10 seconds" — `[Needs Verification]`, secondary-corroborated). Managed Kubernetes: EKS/GKE/AKS
  each state "AWS/Google Cloud/Azure manages the … control plane." Sources: [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), [EKS](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html), [GKE](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview), [AKS](https://learn.microsoft.com/en-us/azure/aks/what-is-aks) (fetched).
- **IAM / secrets** — "grant only the permissions required to perform a task … least-privilege permissions";
  roles deliver "temporary credentials" to workloads so "there is no need to distribute long lived
  credentials." AWS Secrets Manager: "you no longer need hard-coded credentials in application source code."
  Sources: [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html), [HashiCorp Vault](https://developer.hashicorp.com/vault/docs/what-is-vault) (fetched, verbatim).
- **Cost / FinOps** — FinOps = "an operational framework and cultural practice which maximizes the business
  value of technology … through collaboration between engineering, finance, and business teams"; maturity =
  "Crawl, Walk, Run" (the "Inform/Optimize/Operate" phrasing is a _different_ FinOps page — `[Needs Verification]` if quoted here). Tagging whitepaper is dated 2023-03-30 (re-check currency). Sources:
  [FinOps](https://www.finops.org/introduction/what-is-finops/), [AWS tagging](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html) (fetched).
- **GitOps** — OpenGitOps v1.0.0 four principles verbatim: **Declarative**, **Versioned and Immutable**,
  **Pulled Automatically**, **Continuously Reconciled**. Source: [opengitops.dev](https://opengitops.dev/) (fetched, verbatim).
- **Observability** — OpenTelemetry signals: **Traces** ("The path of a request through your application"),
  **Metrics** ("A measurement captured at runtime"), **Logs** ("A recording of an event"). Source:
  [OpenTelemetry — Signals](https://opentelemetry.io/docs/concepts/signals/) (fetched, verbatim).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · cloud-computing-nist** — the NIST five essential characteristics (on-demand self-service, broad
  network access, resource pooling, rapid elasticity, measured service).
- **co-02 · service-models-iaas-paas-saas** — three service models sit on a control boundary that descends
  applications → platform → infrastructure.
- **co-03 · deployment-models** — public, private, community, and hybrid cloud deployment models.
- **co-04 · shared-responsibility** — the provider secures "of the cloud"; the customer secures "in the
  cloud", with the split shifting by service model.
- **co-05 · compute-vm** — a virtual machine (EC2) is on-demand virtual-server capacity.
- **co-06 · object-storage** — object storage (S3) holds data as objects within buckets, addressed by key.
- **co-07 · block-storage** — block storage (EBS) is an attachable volume used like a local disk.
- **co-08 · regions-availability-zones** — regions are isolated geographies; multiple Availability Zones per
  region enable HA by spanning failure domains.
- **co-09 · cloud-networking-vpc** — a VPC is a logically isolated virtual network; subnets partition it,
  each in one AZ.
- **co-10 · security-groups** — a security group is a stateful virtual firewall on a resource's traffic.
- **co-11 · nat-load-balancer** — a NAT gateway gives private subnets outbound-only egress; a load balancer
  distributes traffic across healthy targets.
- **co-12 · iac-declarative** — IaC describes desired end-state declaratively, not step-by-step imperative
  instructions.
- **co-13 · idempotency** — applying the same configuration repeatedly converges to the same state.
- **co-14 · terraform-providers-resources** — providers are plugins that implement resource types the config
  declares.
- **co-15 · hcl-syntax** — HCL is built from arguments (name = value) and blocks (containers).
- **co-16 · terraform-lifecycle** — `init` → `plan` → `apply` → `destroy` is the core Terraform workflow.
- **co-17 · terraform-state** — state maps declared resources to real objects and can hold secrets, so it is
  sensitive.
- **co-18 · state-locking-remote** — a remote backend enables collaboration and locks state to prevent
  concurrent-write corruption.
- **co-19 · terraform-modules** — a module is a reusable collection of resources with input variables and
  outputs; the registry shares them.
- **co-20 · dependency-graph** — Terraform builds a dependency DAG and walks it in parallel (default 10
  concurrent nodes).
- **co-21 · drift-detection** — `plan` (and refresh-only plan) detects divergence between configuration and
  the real-world state.
- **co-22 · terraform-import** — `import` brings an existing, unmanaged resource under Terraform management.
- **co-23 · immutable-infrastructure** — an immutable server is never modified in place, only replaced with a
  new image (Fowler).
- **co-24 · cattle-not-pets** — treat servers as numbered, replaceable cattle, not hand-nursed pets.
- **co-25 · config-management-vs-provisioning** — provisioning tools (Terraform) create infrastructure;
  configuration-management tools (Ansible) idempotently converge existing hosts.
- **co-26 · serverless-faas** — functions-as-a-service (Lambda) run event-driven code with no server
  management; the first invocation pays a cold-start cost.
- **co-27 · managed-services** — managed databases and Kubernetes (RDS, EKS/GKE/AKS) offload control-plane
  operation to the provider.
- **co-28 · iam-least-privilege** — grant only the permissions a task requires; deliver temporary
  credentials to workloads via roles, not long-lived keys.
- **co-29 · secrets-management** — secrets live in a manager/vault retrieved at runtime, never hard-coded in
  code or committed state.
- **co-30 · cost-management-finops** — tagging, right-sizing, and the FinOps framework create cost
  accountability across engineering and finance.
- **co-31 · gitops** — the four OpenGitOps principles: declarative, versioned-and-immutable,
  pulled-automatically, continuously-reconciled.
- **co-32 · infra-observability** — the three OpenTelemetry signals — metrics, logs, and traces — instrument
  infrastructure.

## Tensions & trade-offs — when NOT to reach for this

- **State is the soft underbelly**: IaC's power comes from a state file mapping code to real resources — and
  that file holds secrets, corrupts under concurrent applies, and drifts the moment someone clicks in the
  console. Remote locked state and no-manual-changes discipline are the _cost_ of the reproducibility.
- **Abstraction vs control**: modules and higher-level frameworks (CDK, Terragrunt) buy reuse and charge a
  leaky abstraction over the provider; when the abstraction breaks you debug two layers. Start with plain
  resources and abstract only when duplication actually hurts.
- **When NOT to use it**: a one-off throwaway environment or a tiny personal project may not repay the IaC
  setup cost — click it and move on. IaC earns its keep for environments that must be reproduced, reviewed,
  or rebuilt.

## Lineage — why it beat the alternative

- IaC answered the "works in prod, nobody knows why" era of hand-configured servers (snowflakes) —
  CFEngine/Puppet/Chef brought convergence, then Terraform (2014) brought declarative, provider-agnostic,
  plan-before-apply infra reviewable like code. The 2023 HashiCorp BSL relicensing and the OpenTofu fork are
  a live reminder that even your tooling's license is an engineering input (DD-15). The invariant: infra you
  can review, reproduce, and diff beats infra you merely remember — the same determinism-over-emergence bet
  as immutable images in [`50-containers-and-orchestration`](./50-containers-and-orchestration.md).

## Worked examples

Colocated under `cloud-and-iac/learning/`; each artifact is HCL/YAML applied against a local provider
(LocalStack) **or** an annotated cloud/decision artifact per the annotated-concept designation
(DD-20/DD-30). Contiguous `ex-01..ex-53`. Every example cites the `co-NN` it exercises. Concepts before examples.

### Beginner

- **ex-01 · nist-five-characteristics** — annotate the NIST five essential characteristics against a real
  service — verify all five are named. (co-01)
- **ex-02 · iaas-paas-saas-table** — a decision table mapping IaaS/PaaS/SaaS to what you manage — verify the
  control boundary shifts per model. (co-02)
- **ex-03 · deployment-models** — annotate public/private/community/hybrid — verify all four are
  distinguished. (co-03)
- **ex-04 · shared-responsibility-matrix** — a customer/shared/provider matrix by service model — verify the
  split shifts from IaaS to SaaS. (co-04)
- **ex-05 · compute-vm** — annotate a VM/EC2 instance as virtual-server capacity — verify the on-demand
  property. (co-05)
- **ex-06 · object-storage-bucket** — annotate the bucket/object/key model — verify objects live in a
  bucket. (co-06)
- **ex-07 · block-storage-volume** — annotate an attached block volume used like a disk — verify it attaches
  to one instance. (co-07)
- **ex-08 · regions-azs** — a diagram of a region containing multiple AZs — verify AZs nest under a region.
  (co-08)
- **ex-09 · ha-across-azs** — annotate HA by spanning AZs — verify a single-AZ failure is survived. (co-08)
- **ex-10 · iac-declarative-vs-imperative** — a decision table declarative vs imperative — verify declarative
  states end-state, not steps. (co-12)
- **ex-11 · idempotency** — annotate apply-twice converging to one state — verify the second apply is a
  no-op. (co-13)
- **ex-12 · tf-provider-block** — an HCL `provider` block against the local provider — verify it initializes.
  (co-14)
- **ex-13 · tf-resource-block** — an HCL `resource` block — verify the resource type is provider-implemented.
  (co-14)
- **ex-14 · hcl-arguments-blocks** — annotate HCL arguments vs blocks — verify each construct is labeled.
  (co-15)
- **ex-15 · tf-init** — `terraform init` initializes the working directory — verify providers are installed.
  (co-16)
- **ex-16 · tf-plan** — `terraform plan` previews changes — verify no change is applied yet. (co-16)
- **ex-17 · tf-apply** — `terraform apply` executes the plan — verify the resource is created. (co-16)
- **ex-18 · tf-destroy** — `terraform destroy` deprovisions — verify all managed objects are removed. (co-16)

### Intermediate

- **ex-19 · tf-variables-outputs** — input variables + outputs parameterize a config — verify a variable
  changes the plan and an output is emitted. (co-19)
- **ex-20 · tf-module-reuse** — a reusable module instantiated twice — verify both instances share one
  definition. (co-19)
- **ex-21 · tf-registry-module** — consume a public registry module by source address — verify it resolves.
  (co-19)
- **ex-22 · tf-state-file** — annotate the `terraform.tfstate` config↔real mapping — verify a resource maps
  to state. (co-17)
- **ex-23 · state-sensitive** — annotate why state may hold secrets — verify the sensitivity caveat. (co-17)
- **ex-24 · remote-backend** — a remote backend configuration — verify state moves off local disk. (co-18)
- **ex-25 · state-locking** — annotate locking preventing concurrent writes — verify a second apply is
  blocked while locked. (co-18)
- **ex-26 · dependency-graph** — annotate the DAG walked in parallel (default 10) — verify dependency order
  is respected. (co-20)
- **ex-27 · drift-replan** — re-plan detecting an out-of-band change — verify the plan shows the drift.
  (co-21)
- **ex-28 · refresh-only-plan** — a refresh-only plan reconciling state to reality — verify state updates
  without config change. (co-21)
- **ex-29 · tf-import** — import an existing resource after writing its block — verify it enters state.
  (co-22)
- **ex-30 · dev-vs-stage** — dev and stage from one config driven by variables — verify environments differ
  only by variable values. (co-19)
- **ex-31 · vpc-subnet** — an HCL VPC + subnet — verify the subnet resides in one AZ. (co-09)
- **ex-32 · security-group-stateful** — a stateful security-group rule — verify return traffic is auto-allowed.
  (co-10)
- **ex-33 · nat-gateway** — annotate a NAT gateway for private-subnet egress — verify inbound connections
  can't initiate. (co-11)
- **ex-34 · load-balancer** — annotate a load balancer distributing to healthy targets — verify unhealthy
  targets are skipped. (co-11)
- **ex-35 · immutable-server** — annotate immutable-server (never modified, replaced) — verify changes go via
  a new image. (co-23)
- **ex-36 · cattle-not-pets** — annotate cattle-vs-pets — verify servers are numbered and replaceable.
  (co-24)
- **ex-37 · provisioning-vs-config-mgmt** — a decision table Terraform (provision) vs Ansible (converge) —
  verify each tool's category. (co-25)
- **ex-38 · idempotent-ansible** — annotate an idempotent config-management task — verify re-run makes no
  change. (co-25)

### Advanced

- **ex-39 · lambda-faas** — a serverless function definition — verify it runs without a provisioned server.
  (co-26)
- **ex-40 · cold-start** — annotate the cold-start Init phase — verify the first invocation pays setup cost.
  (co-26)
- **ex-41 · managed-rds** — annotate a managed RDS database (backups/patching offloaded) — verify the
  provider owns operations. (co-27)
- **ex-42 · managed-k8s** — annotate EKS/GKE/AKS control-plane management — verify the provider runs the
  control plane. (co-27)
- **ex-43 · iam-least-privilege** — an IAM policy granting only required actions — verify no wildcard grant.
  (co-28)
- **ex-44 · iam-role-workload** — a role delivering temporary credentials to a workload — verify no long-lived
  key is embedded. (co-28)
- **ex-45 · secrets-manager** — retrieve a secret at runtime from a manager — verify no hard-coded credential.
  (co-29)
- **ex-46 · no-secrets-in-state** — annotate keeping secrets out of committed state — verify state holds no
  plaintext secret. (co-29)
- **ex-47 · tagging-strategy** — a consistent key/value tagging scheme — verify resources carry the required
  tags. (co-30)
- **ex-48 · right-sizing** — annotate right-sizing recommendations — verify an over-provisioned resource is
  flagged. (co-30)
- **ex-49 · finops-crawl-walk-run** — annotate the FinOps Crawl/Walk/Run maturity model — verify the phases
  are named. (co-30)
- **ex-50 · gitops-principles** — annotate the four OpenGitOps principles — verify all four are stated.
  (co-31)
- **ex-51 · gitops-reconcile** — annotate continuous reconciliation from a Git source of truth — verify drift
  is auto-corrected. (co-31)
- **ex-52 · otel-signals** — annotate the metrics/logs/traces signals — verify each signal's role. (co-32)
- **ex-53 · iac-capstone** — a reusable module + dev/stage from variables + full `plan→apply→destroy` +
  least-privilege + tagging + secrets-out-of-state against the local provider — verify the lifecycle runs and
  re-plan shows no drift. (co-16, co-17, co-19, co-28, co-29, co-30)

## Capstone spec — intra-topic (subject → full runnable, local provider)

- **Goal**: describe the deployment of the backend service entirely as code — a reusable Terraform/OpenTofu
  module (variables/outputs), a dev and a stage environment driven by variables, provisioned through the
  full `plan → apply → destroy` lifecycle against a local provider (LocalStack), with least-privilege +
  tagging + secrets kept out of state — a reproducible, reviewable infrastructure definition.
- **Concepts exercised**: [ ] provider + resource + the plan/apply/destroy lifecycle (co-14, co-16) [ ]
  variables + outputs → a reusable module (co-19) [ ] dev vs stage from one config (co-19) [ ]
  least-privilege + tagging (co-28, co-30) [ ] secrets kept out of state (co-17, co-29) [ ] drift detection
  via re-plan (co-21).
- **Ordered steps**:
  1. `.../learning/capstone/` — a module (provider + the service's resources + variables + outputs). Verify
     `terraform init && plan` produces a clean, readable plan against the local provider.
  2. `apply` it, then re-`plan`. Verify `apply` creates the resources and the re-plan shows no drift.
  3. Add a dev and a stage environment from the same module driven by variables. Verify each environment
     differs only by its variable values.
  4. Confirm secrets are supplied via variables/env (never hard-coded, never in committed state) + tagging +
     least-privilege, then `destroy`. Verify `destroy` removes everything and no secret is present in any
     committed file.
- **Acceptance criteria**: the full lifecycle runs against the local provider; re-plan shows no drift; two
  environments come from one module; no secret appears in committed files or state; resources are tagged
  and least-privilege.
- **Done bar**: runnable end-to-end (local provider) + web-verified.

## Read more

**Books**

- **Terraform: Up & Running** — Yevgeniy Brikman (1st ed., 2019; 3rd ed., 2022). The standard practical reference for Terraform and infrastructure-as-code workflows.
- **Infrastructure as Code** — Kief Morris (2nd ed., 2020). Broader, tool-agnostic treatment of IaC principles and patterns.

**Papers & articles**

- **AWS Well-Architected Framework** — Amazon Web Services (ongoing). The canonical vendor framework for cloud architecture quality attributes and the "well-architected" mindset. <https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html>
- **Google Cloud Architecture Framework** — Google Cloud (ongoing). Google's equivalent canonical framework for cloud system design tradeoffs. <https://cloud.google.com/architecture/framework>
- **Terraform Documentation** — HashiCorp (ongoing). The official, authoritative reference for the Terraform configuration language and providers. <https://developer.hashicorp.com/terraform/docs>

---

← Previous: [50 · Containers & Orchestration](./50-containers-and-orchestration.md) · Next: [52 · Bare-Metal Virtualization](./52-bare-metal-virtualization.md) →
