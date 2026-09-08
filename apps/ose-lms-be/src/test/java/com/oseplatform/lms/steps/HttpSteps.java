package com.oseplatform.lms.steps;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

/**
 * The four HTTP step expressions shared by the health, hello, and actuator features.
 *
 * <p>Each expression is declared exactly once across the whole test source set; a second binding
 * for the same text is an ambiguity error under Cucumber-JVM, not a duplicate.
 *
 * <p>{@code MockMvc} is built from the injected context rather than autowired, because Spring Boot
 * 4 no longer ships {@code @AutoConfigureMockMvc} in {@code spring-boot-test-autoconfigure}.
 */
public class HttpSteps {

  @Autowired private WebApplicationContext webApplicationContext;

  private final ObjectMapper objectMapper = new ObjectMapper();

  private MockMvc mockMvc;

  private MvcResult result;

  @Given("the ose-lms-be service is running")
  public void theServiceIsRunning() {
    // The Spring context declared by CucumberSpringConfiguration is the running service; the MOCK
    // web environment means there is nothing further to start.
    mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
  }

  @When("I send GET {word}")
  public void iSendGet(String path) throws Exception {
    result = mockMvc.perform(MockMvcRequestBuilders.get(path)).andReturn();
  }

  @Then("the response status is {int}")
  public void theResponseStatusIs(int expected) {
    assertEquals(expected, result.getResponse().getStatus());
  }

  @Then("the response body has a {string} field equal to {string}")
  public void theResponseBodyHasFieldEqualTo(String field, String expected) throws Exception {
    JsonNode body = objectMapper.readTree(result.getResponse().getContentAsString());
    assertEquals(expected, body.path(field).asText());
  }
}
