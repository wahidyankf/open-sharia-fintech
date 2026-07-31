# Selection by dependency model

| Requirement               | Prefer | Reason                                 |
| ------------------------- | ------ | -------------------------------------- |
| A named local action      | just   | recipe runs when requested             |
| A file output with inputs | Make   | target freshness follows prerequisites |

The tools may compose, but neither changes the other's fundamental model.
