# Remote cache model

| Producer          | Shared value                     |
| ----------------- | -------------------------------- |
| developer machine | output for a complete action key |
| CI runner         | output for a complete action key |

A remote cache shares validated action outputs. It does not replace source control or make undeclared
machine state safe.
