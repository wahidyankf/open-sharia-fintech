val verifyLocal = tasks.register("verifyLocal") {
    doLast {
        println("verified")
    }
}

tasks.register("build") {
    dependsOn(verifyLocal)
}
