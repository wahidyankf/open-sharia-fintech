# Scope of a Bazel target pattern

| Selection       | Scope                                                                       |
| --------------- | --------------------------------------------------------------------------- |
| //:message_copy | one root-package target                                                     |
| //...           | eligible rule targets in main-repository packages, excluding manual targets |

Use the broad form for an intentionally broad validation, not as a substitute for selecting the
smallest relevant target during local work.
