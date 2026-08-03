**Kotlin example runners**

The learning pages are the primary annotated source. Each fenced Kotlin block is a complete,
copy-paste-ready program identified by `ex-NN`; the blocks do not have matching `ex-NN` source
directories. Save a standard-library block as `Example.kt` before compiling it. The materialized
Gradle projects are limited to the capstone and the coroutine runner, where `kotlinx.coroutines` is
required.

For a Kotlin-only example, save its block as `Example.kt` and run:

```sh
kotlinc Example.kt -include-runtime -d example.jar
java -jar example.jar
```

For the capstone, run `gradle run` from `learning/capstone/code/`. For Examples 64–66 and 68, use the
[coroutine runner](../coroutines/code/README.md).
