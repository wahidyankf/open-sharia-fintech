# Example 41: Self-Hosted vs Managed Trade-Off Writeup

_Traces to: `co-20`, `co-22`._

Not code -- a DECISION ARTIFACT. Deploy the same app both ways (Examples 1-24 self-hosted; Examples
25-31 on a PaaS) and name the concrete trade-off. This file IS the deliverable `co-20`/`co-22` ask
for: a documented recommendation, not a vague "it depends."

## The trade-off, in one table

| Dimension     | Self-hosted (this box)          | Managed PaaS                        |
| ------------- | ------------------------------- | ----------------------------------- |
| Control       | Full -- the whole box is yours  | Constrained -- runtime is theirs    |
| Setup effort  | High (Examples 1-24, by hand)   | Low (one `git push`)                |
| Cost (small)  | ~$5/mo VM                       | free tier, then ~$7-20/mo tier      |
| Ops burden    | YOU patch, back up, wake at 3am | platform absorbs patching and TLS   |
| Debuggability | full substrate visibility       | only the app's logs and the leaks   |
| Lock-in       | none (standard Linux)           | some (PaaS conventions, buildpacks) |

## The recommendation (name a force, not a preference)

For THIS workload -- a single stateless service, a solo developer LEARNING the substrate --
SELF-HOST wins: the point is to see the primitives a managed platform hides. For a small TEAM
shipping a product with no ops appetite, the SAME workload should use the MANAGED PaaS: the
3am-on-call cost dominates.

See Example 45 for the scoped, written-out version of this call.

## Acceptance check

Both deploys serve 200 (Examples 14 and 30) AND this writeup names a concrete winning force for each
side (`co-20`/`co-22`). That dual proof is the bar -- not "we tried both," but "we named why each
would win."
