// ex-50: verify state and the controlled input stay in sync (co-22).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#name").fill("Grace Hopper");
const inputValue = await page.locator("#name").inputValue();
const stateView = await page.locator("#state-view").innerText();
console.log("input value:", inputValue, "state view:", stateView);
if (inputValue !== "Grace Hopper") throw new Error("input value did not update");
if (stateView !== 'state.name = "Grace Hopper"') throw new Error(`state did not sync: ${stateView}`);
console.log("PASS: the controlled input's value and the state object stayed in sync");

await browser.close();
