// ex-34: verify the fluid image never overflows its container, at several viewport widths (co-11).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

for (const width of [320, 500, 900, 1400]) {
  await page.setViewportSize({ width, height: 600 });
  const frame = await page.locator(".frame").boundingBox();
  const img = await page.locator("#pic").boundingBox();
  console.log(`viewport ${width}: frame width ${frame.width.toFixed(1)}, img width ${img.width.toFixed(1)}`);
  if (img.width > frame.width + 0.5) {
    throw new Error(`image (${img.width}) overflowed its container (${frame.width}) at viewport ${width}`);
  }
}
console.log("PASS: max-width:100% kept the image within its container at every tested viewport");

await browser.close();
