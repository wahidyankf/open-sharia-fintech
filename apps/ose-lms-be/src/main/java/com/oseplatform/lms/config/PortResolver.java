package com.oseplatform.lms.config;

/**
 * Resolves the listener port from the prefixed environment variable, falling back to the default.
 *
 * <p>The environment value is a parameter rather than an ambient lookup, so the resolution order is
 * provable in-process without starting a server or mutating the JVM environment.
 *
 * <p>Range validation deliberately lives in the server, not here. Tomcat rejects an out-of-range
 * port when it binds, which is still a startup failure, so duplicating the check would add a branch
 * this service has no scenario for.
 */
public final class PortResolver {

  /** The port {@code application.yaml} falls back to when nothing overrides it. */
  public static final int DEFAULT_PORT = 8303;

  /** The prefixed environment variable that overrides {@link #DEFAULT_PORT}. */
  public static final String PORT_ENVIRONMENT_VARIABLE = "OSE_LMS_BE_PORT";

  /**
   * @param environmentValue the value of {@link #PORT_ENVIRONMENT_VARIABLE}, or {@code null}
   * @return the port the listener binds to
   * @throws IllegalArgumentException when the override is present but is not a number
   */
  public int resolve(String environmentValue) {
    if (environmentValue == null || environmentValue.isBlank()) {
      return DEFAULT_PORT;
    }
    try {
      return Integer.parseInt(environmentValue.trim());
    } catch (NumberFormatException cause) {
      throw new IllegalArgumentException("Port value is not a number: " + environmentValue, cause);
    }
  }
}
