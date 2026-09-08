// Versions are pinned to the values resolved in Phase 0 of the lms-init plan. Bumping any of them
// is a deliberate change, not a side effect of a rebuild.
plugins {
    java
    jacoco
    id("org.springframework.boot") version "4.1.1"
    id("io.spring.dependency-management") version "1.1.7"
    id("com.diffplug.spotless") version "8.10.2"
}

group = "com.oseplatform.lms"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}

repositories {
    mavenCentral()
}

// OpenAPI Generator writes models-only output in the standard Maven layout, so the generated
// sources are compiled as an extra source directory rather than copied into src/main/java.
sourceSets {
    main {
        java {
            srcDir(layout.projectDirectory.dir("generated-contracts/src/main/java"))
        }
    }
}

val cucumberVersion = "7.34.8"

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    // Actuator ships every management endpoint; application.yaml exposes only health.
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    // The generated models keep jakarta.validation constraint annotations for the contract's
    // required fields, so the API they compile against must be on the compile classpath.
    implementation("org.springframework.boot:spring-boot-starter-validation")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("io.cucumber:cucumber-java:$cucumberVersion")
    testImplementation("io.cucumber:cucumber-spring:$cucumberVersion")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:$cucumberVersion")
    testImplementation("org.junit.platform:junit-platform-suite")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

spotless {
    java {
        target("src/**/*.java")
        googleJavaFormat("1.36.1")
    }
}

jacoco {
    toolVersion = "0.8.15"
}

tasks.named<Test>("test") {
    // Only the suite engine is discovered directly. The Cucumber engine is on the test classpath
    // and would otherwise be discovered twice — once by Gradle and once through RunCucumberTest —
    // running every scenario twice and making "resolved exactly once" untrue.
    useJUnitPlatform {
        includeEngines("junit-platform-suite")
    }
    // Cucumber's JUnit Platform engine needs the corpus root and the glue package declared here;
    // the feature files live in the specs corpus, outside this Gradle project.
    systemProperty("cucumber.glue", "com.oseplatform.lms.steps")
    systemProperty("cucumber.features", "../../specs/apps/ose/lms-be/behaviours")
    finalizedBy(tasks.named("jacocoTestReport"), tasks.named("jacocoTestCoverageVerification"))
}

// Classes are dropped from the analysed set rather than from the rule: a rule-level `excludes`
// list filters elements of the rule's own scope, so on a bundle-scoped rule a class name there
// silently matches nothing and the class is still counted.
//
// Two exclusions, for two different reasons:
//   - OseLmsBeApplication: its only statement is SpringApplication.run, which no in-process test
//     can execute without starting a second context.
//   - com/oseplatform/lms/contracts: OpenAPI-generated model output, regenerated on every codegen
//     run and never hand-edited. The floor measures authored code; generated equals/hashCode/
//     toString boilerplate is not code this project wrote or can meaningfully test.
fun Iterable<java.io.File>.authoredClassesOnly(): Any =
    files(
        map {
            fileTree(it) {
                exclude("**/OseLmsBeApplication.class")
                exclude("com/oseplatform/lms/contracts/**")
            }
        }
    )

// The Unit line-coverage floor is declared as a Gradle property on the Nx `test:unit` command
// surface so the static behaviour-coverage validator can read the exact number this build enforces;
// the default keeps a direct `./gradlew` invocation from being weaker than the Nx target.
val coverageLineMinimum: java.math.BigDecimal =
    ((findProperty("coverage.line.minimum") as String?) ?: "99")
        .toBigDecimal()
        .movePointLeft(2)

tasks.named<JacocoReport>("jacocoTestReport") {
    dependsOn(tasks.named("test"))
    classDirectories.setFrom(classDirectories.files.authoredClassesOnly())
}

tasks.named<JacocoCoverageVerification>("jacocoTestCoverageVerification") {
    dependsOn(tasks.named("test"))
    classDirectories.setFrom(classDirectories.files.authoredClassesOnly())
    violationRules {
        rule {
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = coverageLineMinimum
            }
        }
    }
}

// The jar name is stable so the E2E harness added in DU4 can start it by a fixed path.
tasks.named<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar") {
    archiveFileName.set("ose-lms-be.jar")
}
