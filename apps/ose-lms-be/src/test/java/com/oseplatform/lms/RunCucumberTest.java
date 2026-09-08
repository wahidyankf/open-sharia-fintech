package com.oseplatform.lms;

import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.Suite;

/**
 * JUnit Platform entry point for the Cucumber engine.
 *
 * <p>The corpus root and the glue package are supplied by {@code build.gradle.kts} as system
 * properties, because the feature files live in the shared specs corpus outside this project.
 */
@Suite
@IncludeEngines("cucumber")
public class RunCucumberTest {}
