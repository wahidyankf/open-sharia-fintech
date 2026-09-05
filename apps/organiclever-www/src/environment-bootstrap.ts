import { loadTierEnv, type LoadTierEnvOptions } from "@open-sharia-enterprise/ts-env-loader";

/** App-owned composition seam used before OrganicLever WWW validates its environment. */
export function loadOrganicLeverWwwEnvironment(options: LoadTierEnvOptions = {}): void {
  loadTierEnv(options);
}
