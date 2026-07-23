// ex-65: verify the 'loading' branch of the discriminated union renders a spinner (co-27).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const spinnerCount = await page.locator("#spinner").count();
const spinnerText = await page.locator("#spinner").innerText();
console.log("spinner present:", spinnerCount === 1, "text:", spinnerText);
if (spinnerCount !== 1) throw new Error("expected the loading branch to render #spinner");
if (spinnerText !== "Loading...") throw new Error(`unexpected spinner text: "${spinnerText}"`);
console.log("PASS: state.status === 'loading' rendered exactly the spinner branch");

await browser.close();
