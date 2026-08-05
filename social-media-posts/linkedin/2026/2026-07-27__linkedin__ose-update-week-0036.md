Posted: Monday, July 27, 2026
Platform: LinkedIn
Window: 2026-07-21 → 2026-07-27. 216 commits across the three repos (ose-public 153, ose-primer 11, ose-infra 52), 39 pull requests merged (31 / 4 / 4).

---

OPEN SHARIA ENTERPRISE
Week 36 / Phase 1, Week 24

Highlights: the learning platform grew a navigable spine — courses, paths, and the URL space they live in — and a chronic "the server is down again" fault finally got a name.

🌳 ose-public

- Three of the five learning-path waves closed and are live on ayokoding.com: every course bundle re-homed into one flat namespace, a prerequisite-DAG schema behind it, and path-aware navigation on top — paths hub, category and arc landings, a path rail, path-aware prev/next.
- Paths split into two categories with deliberately different URL depth: `careers/<arc>/<role>` and `skills/<subject>`. Path ids are variable-depth by design — the parser validates that an id resolves to a manifest, not its segment count.
- Course authoring opened. Eleven new courses shipped: six on AI engineering, from evaluating AI output and product patterns for probabilistic systems through inference serving and fine-tuning; five on data, from database internals through search, NoSQL, and graph.

🌐 Cross-repo

- Phase 0 of a plan now opens no pull request; the earliest is Phase 1. And PRs open at delivery boundaries — where work becomes shippable — not once per phase.
- The PR reviewer split into eight discipline specialists — architecture, correctness, security, performance, governance, test integrity, docs, instruction decay — feeding a coordinator that posts one review.
- ose-primer took the governance changes byte-for-byte.

🏗️ ose-infra

The twin-clusters milestone got re-architected: one shared three-node k3s cluster with embedded etcd that tolerates losing a host, staging as a vcluster on it, prod as namespaces beside it. Five steps, strictly ordered — stabilise the hosts, rename the repo, add the third node, staging, prod. Step one is done.

🔧 The bug worth naming

Both on-premise hosts kept vanishing from the network for hours — eight-plus outages since mid-June, one near 49 hours, each ended only by reseating a cable in person. The cause: the onboard Intel NIC's transmit ring wedges while the PHY link stays up. Every probe reported the interface up while the machine passed no traffic. And the runbook's reflex for a silent host — power-cycle — is the wrong lever; the reseat works because it forces a link renegotiation that resets the adapter. Fixed in three layers: disable the aggravating offloads, a watchdog that recognises the signature and bounces the link, and alerting that does not depend on the wedged NIC.

Up is not the same as working.

🔜 Next 2–4 weeks

Finish the course bands and publish the path manifests, so the learning paths carry real course order. Expand the on-premise fleet to three nodes, then get the Kubernetes cluster working on it.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
