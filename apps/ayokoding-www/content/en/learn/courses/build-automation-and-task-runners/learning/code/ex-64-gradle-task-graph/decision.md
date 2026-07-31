# Gradle lifecycle

| Phase         | Responsibility                                         |
| ------------- | ------------------------------------------------------ |
| configuration | evaluate build logic and assemble requested task graph |
| execution     | run selected tasks in graph order                      |

The task graph exists before Gradle begins executing task actions.
