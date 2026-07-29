// Example 71: A Web Manifest Makes the App Installable. (co-34)
//
// A web app manifest (a linked manifest.json) with the required fields makes the app installable --
// "Add to Home Screen" / "Install app". Browsers check the manifest + a service worker + HTTPS
// before offering the install prompt. This example validates those install criteria.

// The required manifest fields for installability.
interface Manifest {
  // => browsers check these specific fields before offering the install prompt
  name: string; // => the app's display name
  start_url: string; // => where the installed app launches
  display: "standalone" | "fullscreen" | "minimal-ui" | "browser"; // => standalone = no browser chrome
  icons: { src: string; sizes: string; purpose: string }[]; // => at least one icon (often 192px + 512px)
}

// canInstall checks the installability criteria (manifest fields + a service worker + https).
function canInstall(
  manifest: Manifest,
  hasServiceWorker: boolean,
  isHttps: boolean,
): { ok: boolean; reasons: string[] } {
  // => co-34: installability is a checklist; each missing item is a reason it will not prompt
  const reasons: string[] = [];
  if (!manifest.name) reasons.push("missing name"); // => required field
  if (manifest.display === "browser") reasons.push("display must not be 'browser'"); // => needs standalone-ish
  if (manifest.icons.length === 0) reasons.push("no icons"); // => at least one icon
  if (!hasServiceWorker) reasons.push("no service worker"); // => SW with a fetch handler is required
  if (!isHttps) reasons.push("not HTTPS"); // => install requires a secure context
  return { ok: reasons.length === 0, reasons }; // => ok === true means the prompt will appear
}

const manifest: Manifest = {
  // => a complete, installable manifest
  name: "Tasks",
  start_url: "/",
  display: "standalone", // => no browser address bar when installed
  icons: [{ src: "/icon-512.png", sizes: "512x512", purpose: "any maskable" }],
};
const verdict = canInstall(manifest, true, true); // => SW + HTTPS both present

console.log("installable:", verdict.ok); // => Output: installable: true
console.log("blocking reasons:", verdict.reasons); // => Output: blocking reasons: []
