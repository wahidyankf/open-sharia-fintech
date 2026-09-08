package com.oseplatform.lms.steps;

import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

/**
 * Binds the Cucumber glue to a single Spring context.
 *
 * <p>{@code MOCK} keeps every HTTP scenario in-process: no port is bound, so the Unit adapter never
 * contends with a developer's running service. The E2E adapter added in DU4 exercises the real
 * listener.
 *
 * <p>The web layer is driven through a {@code MockMvc} built from the injected context in {@code
 * HttpSteps} rather than through {@code @AutoConfigureMockMvc}: Spring Boot 4 no longer ships that
 * annotation in {@code spring-boot-test-autoconfigure}, and building the instance from {@code
 * spring-test} needs no extra dependency.
 */
@CucumberContextConfiguration
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
public class CucumberSpringConfiguration {}
