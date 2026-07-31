val copyInput = tasks.register("copyInput") {
    inputs.file("input.txt")
    outputs.file(layout.buildDirectory.file("output.txt"))
    doLast {
        layout.buildDirectory.file("output.txt").get().asFile.writeText(file("input.txt").readText())
    }
}
