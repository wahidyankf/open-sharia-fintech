plugins {
    kotlin("jvm") version "2.4.10"
    application
}

repositories { mavenCentral() }

dependencies { implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.11.0") }

kotlin { jvmToolchain(17) }

sourceSets { main { kotlin.srcDir(".") } }

application { mainClass.set("MainKt") }
