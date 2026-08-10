import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import "./styles.css";
import { bootstrapTheme } from "./theme";

const disposeTheme = bootstrapTheme();

if (import.meta.hot) {
  import.meta.hot.dispose(disposeTheme);
}

const root = document.getElementById("root");

if (!root) {
  throw new Error("BeaverNest requires a #root element.");
}

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
