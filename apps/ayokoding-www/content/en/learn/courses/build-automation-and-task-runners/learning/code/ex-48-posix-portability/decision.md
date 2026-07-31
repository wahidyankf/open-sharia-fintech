# POSIX portability decision

| Requirement                                     | Choice        | Not implied         |
| ----------------------------------------------- | ------------- | ------------------- |
| Same Makefile across POSIX make implementations | .POSIX marker | GNU Make extensions |

The marker selects standardized make behavior; it does not turn every implementation-specific feature
into portable syntax.
