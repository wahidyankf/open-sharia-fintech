// ex-52: verify choosing an option updates the controlling state (co-22).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#color").selectOption("blue");
const view = await page.locator("#state-view").innerText();
console.log("state view after selecting blue:", view);
if (view !== 'state.color = "blue"') throw new Error(`state did not update: ${view}`);
console.log("PASS: selecting an option updated the controlling state object to match");

await browser.close();
