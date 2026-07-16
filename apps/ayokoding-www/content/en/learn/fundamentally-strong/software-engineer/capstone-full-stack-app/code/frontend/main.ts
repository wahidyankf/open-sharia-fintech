// Full-stack capstone: main.ts -- the browser entry point, wiring api.ts's typed HTTP client to
// app.ts's imperative shell with this deployment's backend base URL (topic 12: same-machine,
// different-port HTTP, exactly what the CORS allow-list on the backend expects).
import { makeApi } from "./api.js";
import { mountApp } from "./app.js";

const BACKEND_BASE_URL = "http://127.0.0.1:8120";

const root = document.getElementById("app");
if (root === null) throw new Error("missing #app root element");

mountApp(root, makeApi(BACKEND_BASE_URL));
