# CI build entry points

| Tool   | Example verification command |
| ------ | ---------------------------- |
| Make   | make ci                      |
| Bazel  | bazel test //...             |
| Gradle | gradle build                 |

CI orchestrates the job and records results; the selected build tool owns its target dependency model.
