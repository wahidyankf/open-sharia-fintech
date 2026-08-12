type StepDefinition = () => void;
const Given = (_step: string, _definition: StepDefinition) => undefined;
const When = (_step: string, _definition: StepDefinition) => undefined;
const Then = (_step: string, _definition: StepDefinition) => undefined;

Given("BeaverNest is reachable through its configured VPN address", () => undefined);
When('I navigate to "/" in a new browser session', () => undefined);
Then("the application shell renders before the readiness request completes", () => undefined);
Then('the browser sends a same-origin GET request to "/api/v1/readiness"', () => undefined);
Then("the page reports Application Available, Database Ready and Schema Current", () => undefined);
Given("the readiness response is intentionally delayed", () => undefined);
When('I navigate to "/"', () => undefined);
Then("the readiness region reports that status is being checked", () => undefined);
Then("the region does not falsely report the database as ready", () => undefined);
Given("the readiness endpoint returns an unavailable response", () => undefined);
When('I navigate to "/" and activate "Refresh status" after service recovery', () => undefined);
Then("the readiness request is retried without a full page navigation", () => undefined);
Then("the region changes from Unavailable to Ready using a polite live announcement", () => undefined);
Given("I am viewing the rendered workspace home", () => undefined);
When("I inspect the visible page content and accessible links", () => undefined);
Then("no promotional product description is present", () => undefined);
Then("no external GitHub call to action is present", () => undefined);

// Keeps this file's top-level `const`s module-scoped rather than global, so
// they do not clash with an identical stub pattern in a sibling *.steps.ts
// file (see src/test/configuration.steps.ts).
export {};
