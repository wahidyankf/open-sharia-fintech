# Phase 0 — Resolved Versions

Re-resolved on **2026-09-08** during plan execution. Every row in `tech-docs.md` §3 is re-resolved
here rather than trusted; the Divergence column records whether the authored value still holds.

| Component                             | Resolved value                                                     | Authored value | Divergence | How resolved                                                                    |
| ------------------------------------- | ------------------------------------------------------------------ | -------------- | ---------- | ------------------------------------------------------------------------------- |
| Java LTS major                        | `25`                                                               | 25             | none       | `api.adoptium.net/v3/info/available_releases` → `most_recent_lts`               |
| Temurin JDK 25 patch                  | `jdk-25.0.4.1+1`                                                   | _not authored_ | new value  | `api.adoptium.net/v3/info/release_names` filtered to `[25,26)`, GA, sorted DESC |
| Spring Boot                           | `v4.1.1`                                                           | 4.1.1          | none       | `api.github.com/repos/spring-projects/spring-boot/releases/latest` → `tag_name` |
| Gradle                                | `v9.7.1`                                                           | 9.7.1          | none       | `api.github.com/repos/gradle/gradle/releases/latest` → `tag_name`               |
| Gradle dist SHA-256                   | `acd53f1edaf02f1a8ff99879f8a34b302661a057d9b063ae9e35b552f804d20a` | _not authored_ | new value  | `services.gradle.org/distributions/gradle-9.7.1-bin.zip.sha256` (64 hex chars)  |
| Cucumber-JVM                          | `v7.34.8`                                                          | 7.34.8         | none       | `api.github.com/repos/cucumber/cucumber-jvm/releases/latest` → `tag_name`       |
| JaCoCo                                | `v0.8.15`                                                          | 0.8.15         | none       | `api.github.com/repos/jacoco/jacoco/releases/latest` → `tag_name`               |
| google-java-format                    | `v1.36.1`                                                          | 1.36.1         | none       | `api.github.com/repos/google/google-java-format/releases/latest` → `tag_name`   |
| Spotless Gradle plugin                | `8.10.2`                                                           | 8.10.2         | none       | `api.github.com/repos/diffplug/spotless/releases` newest `gradle/*` tag         |
| OpenAPI Generator                     | `7.20.0`                                                           | 7.20.0         | none       | `openapitools.json` → `generator-cli.version` (repo-grounded, re-read)          |
| `@openapitools/openapi-generator-cli` | `2.30.2`                                                           | 2.30.2         | none       | `package.json` (repo-grounded, re-read)                                         |

## Notes

- `most_recent_lts` is `25`, so the plan's D-2 decision and `tech-docs.md` §3 hold unchanged. The
  Phase 0 checkbox required stopping and reporting if this were not 25; it is 25.
- `available_lts_releases` is `[8, 11, 17, 21, 25]` and `most_recent_feature_release` is `26`, so
  25 is the newest LTS with 26 being a non-LTS feature release — consistent with the authored
  reasoning that JDK 25 is current LTS.
- The exact Temurin patch was not pinned at authoring time. `jdk-25.0.4.1+1` is the newest GA
  release name for the `[25,26)` range.
