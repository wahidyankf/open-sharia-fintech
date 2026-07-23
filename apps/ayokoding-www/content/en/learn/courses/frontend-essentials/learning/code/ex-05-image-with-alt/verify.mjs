// ex-05: verify the alt text surfaces once the deliberately-missing image fails to load (co-03).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const img = page.locator("#photo");
await page.waitForFunction(() => {
  const el = document.getElementById("photo");
  return el.complete;
});

const naturalWidth = await img.evaluate((el) => el.naturalWidth);
const alt = await img.getAttribute("alt");
console.log("naturalWidth after load attempt:", naturalWidth);
console.log("alt attribute:", alt);

if (naturalWidth !== 0) {
  throw new Error("expected the image request to fail (naturalWidth === 0)");
}
if (!alt || alt.trim().length === 0) {
  throw new Error("alt text is missing");
}

const accessible = page.getByAltText("Five engineers around a whiteboard sketching a system diagram");
if ((await accessible.count()) !== 1) {
  throw new Error("alt text is not exposed as the image's accessible name");
}
console.log("PASS: broken image still exposes its alt text as the accessible name");

await browser.close();
