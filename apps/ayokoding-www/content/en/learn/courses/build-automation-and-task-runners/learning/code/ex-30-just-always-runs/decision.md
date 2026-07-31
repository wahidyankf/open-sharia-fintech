# Command-runner execution

| Request                         | just             | Make file target    |
| ------------------------------- | ---------------- | ------------------- |
| Ask twice with no source change | run recipe twice | skip a fresh output |

just is a command runner: every requested recipe is treated as phony. Make behavior depends on the
target and prerequisites it has been given.
