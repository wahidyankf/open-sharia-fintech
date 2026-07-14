// ex-66: verify the 'error' branch of the discriminated union shows the error text (co-27).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const messageCount = await page.locator("#error-message").count();
const messageText = await page.locator("#error-message").innerText();
console.log("error message present:", messageCount === 1, "text:", messageText);
if (messageCount !== 1) throw new Error("expected the error branch to render #error-message");
if (messageText !== "Could not reach the server") {
  throw new Error(`unexpected error text: "${messageText}"`);
}
console.log("PASS: state.status === 'error' rendered exactly the error branch, with its message");

await browser.close();
