package com.oseplatform.lms.steps;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import com.oseplatform.lms.config.PortResolver;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/**
 * The five port-resolution step expressions.
 *
 * <p>The resolver is a plain object, so these scenarios never bind a socket and never mutate the
 * JVM environment — which is why all three carry {@code @e2e-exempt}.
 */
public class PortResolutionSteps {

  private final PortResolver resolver = new PortResolver();

  private String environmentValue;
  private Integer resolvedPort;
  private RuntimeException failure;

  @Given("no port override is configured")
  public void noPortOverrideIsConfigured() {
    environmentValue = null;
  }

  @Given("the environment variable {string} is set to {string}")
  public void theEnvironmentVariableIsSetTo(String name, String value) {
    assertEquals(PortResolver.PORT_ENVIRONMENT_VARIABLE, name);
    environmentValue = value;
  }

  @When("the listener port is resolved")
  public void theListenerPortIsResolved() {
    resolvedPort = null;
    failure = null;
    try {
      resolvedPort = resolver.resolve(environmentValue);
    } catch (IllegalArgumentException caught) {
      failure = caught;
    }
  }

  @Then("the resolved port is {int}")
  public void theResolvedPortIs(int expected) {
    assertEquals(expected, resolvedPort);
  }

  @Then("port resolution fails with a startup error")
  public void portResolutionFailsWithAStartupError() {
    assertNotNull(failure, "expected port resolution to fail");
  }
}
