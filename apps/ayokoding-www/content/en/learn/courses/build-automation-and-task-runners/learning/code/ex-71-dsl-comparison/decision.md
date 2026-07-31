# Gradle DSL comparison

| DSL    | Script extension | Same underlying model |
| ------ | ---------------- | --------------------- |
| Groovy | .gradle          | Gradle task graph     |
| Kotlin | .gradle.kts      | Gradle task graph     |

The authoring syntax differs, while declared task dependencies and incremental inputs carry the same role.
