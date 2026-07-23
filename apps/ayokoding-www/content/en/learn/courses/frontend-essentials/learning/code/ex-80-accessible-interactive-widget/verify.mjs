// ex-80: verify the disclosure widget toggles its content and is fully keyboard-and-AT-operable (co-25, co-26, co-18).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const initialExpanded = await page.locator("#toggle").getAttribute("aria-expanded");
const initialHidden = await page.locator("#panel").isHidden();
console.log("initial aria-expanded:", initialExpanded, "panel hidden:", initialHidden);
if (initialExpanded !== "false" || !initialHidden) throw new Error("widget should start collapsed");

// activate with a real keyboard Enter on the (real, focusable) <button>
await page.locator("#toggle").focus();
await page.keyboard.press("Enter");
const openedExpanded = await page.locator("#toggle").getAttribute("aria-expanded");
const openedVisible = await page.locator("#panel").isVisible();
console.log("after keyboard activation -- aria-expanded:", openedExpanded, "panel visible:", openedVisible);
if (openedExpanded !== "true" || !openedVisible) throw new Error("widget did not open via keyboard");

await page.keyboard.press("Enter");
const closedExpanded = await page.locator("#toggle").getAttribute("aria-expanded");
const closedHidden = await page.locator("#panel").isHidden();
console.log("after second activation -- aria-expanded:", closedExpanded, "panel hidden:", closedHidden);
if (closedExpanded !== "false" || !closedHidden) throw new Error("widget did not close again via keyboard");
console.log("PASS: the disclosure widget toggled open/closed via keyboard, with aria-expanded in sync");

await browser.close();
