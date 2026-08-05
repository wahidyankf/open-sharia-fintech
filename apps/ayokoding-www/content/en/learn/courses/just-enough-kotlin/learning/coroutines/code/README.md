**Coroutine example runner**

This complete Gradle Kotlin/JVM project runs the six coroutine examples. It uses an installed Gradle
distribution; no Gradle wrapper is committed with the course.

From this directory, run a selected example:

```sh
gradle run -Pexample=64
```

Replace `64` with any number from `63` through `68`. The corresponding
`src/main/kotlin/ExampleNN.kt` source file matches the Markdown example, without its teaching
annotations. Examples 64–66 and 68 use
`kotlinx-coroutines-core`; the shared project also runs 63 and 67 so the whole coroutine sequence
uses one command pattern.
