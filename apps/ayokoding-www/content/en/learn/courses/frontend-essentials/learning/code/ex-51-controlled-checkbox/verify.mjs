// ex-51: verify toggling the checkbox updates both state and the checked property (co-22).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#agree").check();
const checkedAfter = await page.locator("#agree").isChecked();
const view = await page.locator("#state-view").innerText();
console.log("checked:", checkedAfter, "state view:", view);
if (!checkedAfter) throw new Error("checkbox.checked did not become true");
if (view !== "state.agreed = true") throw new Error(`state did not sync: ${view}`);
console.log("PASS: checking the box updated both the checked property and the state object");

await browser.close();
