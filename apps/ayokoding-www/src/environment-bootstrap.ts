import { loadTierEnv, type LoadTierEnvOptions } from "@open-sharia-enterprise/ts-env-loader";

/** App-owned composition seam used before Ayokoding validates its environment. */
export function loadAyokodingEnvironment(options: LoadTierEnvOptions = {}): void {
  loadTierEnv(options);
}
