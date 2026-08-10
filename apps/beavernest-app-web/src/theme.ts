type Theme = "dark" | "light";

let activeCleanup: (() => void) | undefined;

function setTheme(isDark: boolean) {
  document.documentElement.dataset.theme = isDark ? "dark" : "light";
}

export function bootstrapTheme(): () => void {
  if (activeCleanup) {
    return activeCleanup;
  }

  const media = window.matchMedia("(prefers-color-scheme: dark)");
  const updateTheme = (event: MediaQueryListEvent) => setTheme(event.matches);

  setTheme(media.matches);
  media.addEventListener("change", updateTheme);

  let disposed = false;
  const cleanup = () => {
    if (disposed) {
      return;
    }

    disposed = true;
    media.removeEventListener("change", updateTheme);
    if (activeCleanup === cleanup) {
      activeCleanup = undefined;
    }
  };

  activeCleanup = cleanup;
  return cleanup;
}

export type { Theme };
