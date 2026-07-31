val cachedHello = tasks.register("cachedHello") {
    outputs.cacheIf { true }
    outputs.file(layout.buildDirectory.file("hello.txt"))
    doLast {
        layout.buildDirectory.file("hello.txt").get().asFile.writeText("cached hello\\n")
    }
}
