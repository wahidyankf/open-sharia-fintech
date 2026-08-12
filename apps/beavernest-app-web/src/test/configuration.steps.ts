type StepDefinition = () => void;
const Given = (_step: string, _definition: StepDefinition) => undefined;
const When = (_step: string, _definition: StepDefinition) => undefined;
const Then = (_step: string, _definition: StepDefinition) => undefined;

Given('the Nx "<target>" target for beavernest-app-web', () => undefined);
When('it runs with APP_ENV set to "<tier>"', () => undefined);
Then('Vite is invoked with "--mode <tier>"', () => undefined);
Given("a VITE_-prefixed variable already exported in the process", () => undefined);
When('beavernest-app-web starts at mode "local"', () => undefined);
Then("the exported process value is used", () => undefined);
Then("no .env.local value overrides it", () => undefined);
Given('a stray "<file>" exists beside beavernest-app-web\'s tier file', () => undefined);
When("beavernest-app-web starts at a non-local mode", () => undefined);
Then("the guard throws before the build proceeds", () => undefined);

// Keeps this file's top-level `const`s module-scoped rather than global,
// so they do not clash with the identical stub pattern in workspace.steps.ts.
export {};
