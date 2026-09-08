---
description: Choose the fewest build-valid, independently reviewable and revertible commits after explicit authorization.
when_to_use: Use after the user authorizes committing a named change set and before staging it.
---

# Thematic Commit Composition and Boundaries

Staging and committing remain unauthorized until the user explicitly authorizes a named change set.
Once authorized, choose its commit boundaries without another prompt unless the user prescribed the
boundaries or a proposed split would exceed the authorized scope.

## Boundary Test

Partition the authorized change set into the **fewest** commits that each satisfy all of these tests:

- **Build-valid**: required local checks pass at that commit boundary.
- **Independently reviewable**: the commit states one coherent purpose without relying on a later
  commit to explain or complete it.
- **Independently revertible**: reverting it does not strand references, migrations, generated
  bindings, or other required completion artifacts.

Keep required tests, documentation, specifications, references, migrations with rollback, and
generated mirrors in the commit containing the change they complete. Different file types, scopes,
or conventional types do not by themselves justify a split.

Split independent concerns that pass these tests separately. A new feature and an unrelated lint
repair are separate; a renamed symbol and all required call-site updates are one atomic change.

## Authorization Examples

```text
PASS: User authorizes “commit the authentication change.”
      Agent selects one commit containing implementation, tests, docs, and references.

PASS: User authorizes “commit these changes as implementation and migration commits.”
      Agent follows those prescribed boundaries.

FAIL: User has not authorized a commit.
      Agent stages files because the work appears complete.

FAIL: User authorizes one named change set.
      Agent adds an unrelated cleanup to make a preferred split.
```
