# Hermetic build boundary

| Inside the action boundary      | Outside the action boundary            |
| ------------------------------- | -------------------------------------- |
| declared source files           | undeclared host library                |
| declared compiler/configuration | developer-specific environment setting |

Equivalent declared inputs can produce a repeatable result only when the action does not read hidden
machine state.
