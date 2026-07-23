// ex-62: verify Enter and Space both activate a role=button div once keydown handling is added (co-26, co-25).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#fake-button").focus();
await page.keyboard.press("Enter");
const afterEnter = await page.locator("#report").innerText();
console.log("report after Enter:", afterEnter);
if (afterEnter !== "activated") throw new Error("Enter did not activate the custom button");

await page.evaluate(() => (document.getElementById("report").textContent = "not activated"));
await page.locator("#fake-button").focus();
await page.keyboard.press("Space");
const afterSpace = await page.locator("#report").innerText();
console.log("report after Space:", afterSpace);
if (afterSpace !== "activated") throw new Error("Space did not activate the custom button");
console.log("PASS: both Enter and Space activated the custom role=button element via keydown handling");

await browser.close();
