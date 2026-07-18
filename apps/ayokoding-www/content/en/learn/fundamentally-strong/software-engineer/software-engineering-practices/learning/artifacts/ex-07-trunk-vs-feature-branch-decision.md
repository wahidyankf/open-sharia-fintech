---
title: "Artifact: Trunk-Based vs. Feature-Branch Decision"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 47
---

> ex-07 &middot; exercises co-01 &middot; two teams, two branching models, two different right
> answers.

| Team                                            | Shape of the work                                                                            | Branching model                                                                                  | Cadence/team-size property that drives it                                                                                                                                                                                                                   |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A two-person team shipping to production daily  | Small, frequent, low-blast-radius changes; both engineers see every change land within hours | **Trunk-based development** -- short-lived branches (hours, not days), merged straight to `main` | Daily release cadence makes a long-lived branch's merge cost (days of drift) larger than the coordination cost of two people integrating constantly; a two-person team can also review every change fast enough to keep trunk green.                        |
| A five-person team on a quarterly release train | Large, coordinated feature sets that must all land together for one dated release            | **Feature branches** (a release-scoped integration branch per quarter)                           | A quarterly cadence means release isolation genuinely matters -- an in-progress feature must not leak into a release train it is not ready for, and five people's parallel work needs a place to integrate before the release gate without touching `main`. |

**Verify**: each pick cites the specific cadence/team-size property (daily release cadence for team
A; quarterly release isolation for team B) that drove it -- not a blanket "trunk-based is always
better" or "GitFlow is always safer" -- satisfying co-01's rule that the right branching model
depends on team size and release cadence, not fashion.

**Key takeaway**: trunk-based development wins when integration frequency matters more than release
isolation; feature branches win when the reverse is true -- and both of these teams are making the
correct choice for their own shape of work.

**Why It Matters**: a team that copies trunk-based development from a blog post without a daily (or
faster) release cadence to match it gets all of the coordination discipline trunk-based dev demands
and none of the payoff -- while a team that copies GitFlow without needing release isolation pays
merge-conflict cost for a safety property it never actually uses.
