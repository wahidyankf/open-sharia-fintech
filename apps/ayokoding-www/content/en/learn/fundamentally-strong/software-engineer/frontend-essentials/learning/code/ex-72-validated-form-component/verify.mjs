// ex-72: verify an invalid submit is blocked with a visible error, and a valid submit succeeds (co-22, co-23, co-24).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#email").fill("not-an-email");
await page.locator('button[type="submit"]').click();
const blockedResult = await page.locator("#result").innerText();
const errorVisible = await page.locator("#error").isVisible();
console.log("after invalid submit -> result:", blockedResult, "error visible:", errorVisible);
if (blockedResult !== "blocked: invalid") throw new Error("invalid submit was not blocked");
if (!errorVisible) throw new Error("error message should be visible after an invalid submit");

await page.locator("#email").fill("ada@example.com");
await page.locator('button[type="submit"]').click();
const successResult = await page.locator("#result").innerText();
const errorHiddenAfter = await page.locator("#error").isHidden();
console.log("after valid submit -> result:", successResult, "error hidden:", errorHiddenAfter);
if (successResult !== "submitted: ada@example.com") throw new Error("valid submit did not succeed");
if (!errorHiddenAfter) throw new Error("error message should hide again once valid");
console.log("PASS: invalid submit was blocked with a visible error; a valid submit succeeded cleanly");

await browser.close();
