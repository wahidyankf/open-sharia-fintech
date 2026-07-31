# Monorepo build scaling

| Scaling need                              | Graph capability          |
| ----------------------------------------- | ------------------------- |
| one edit should select relevant projects  | target dependency closure |
| repeated actions across CI and developers | shared cache              |
| machine-independent result                | hermetic declared inputs  |

The build graph exposes both the affected scope and the conditions for safe reuse.
