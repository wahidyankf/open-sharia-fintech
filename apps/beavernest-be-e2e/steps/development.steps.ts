/**
 * Aggregate binding for the development-wrapper contract. The executable
 * shell contract owns the filesystem assertions; browser E2E keeps the shared
 * feature represented without introducing a production test route.
 */
import { createBdd } from "playwright-bdd";

const { Given, When, Then } = createBdd();

Given("the local development command receives an explicit developer-owned data directory", async () => undefined);
When("it starts the backend on the local development port", async () => undefined);
Then("the database resolves only within that development directory", async () => undefined);
Then("the command neither reads nor inherits the production host data-bind source", async () => undefined);
