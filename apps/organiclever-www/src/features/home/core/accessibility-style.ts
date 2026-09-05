export const LANDING_ACCESSIBILITY_COLORS = {
  background: "#fdfcf9",
  text: "#3d3630",
  interactiveBackground: "#1a7474",
  interactiveText: "#ffffff",
  focusRing: "#005f5f",
} as const;

export const LANDING_FOCUS_RING_WIDTH_PX = 3;

function channel(value: number): number {
  const normalized = value / 255;
  return normalized <= 0.04045 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
}

function luminance(hex: string): number {
  const channels = /^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/iu.exec(hex);
  if (!channels) throw new Error(`Expected a six-digit hex colour, received ${hex}`);
  const [, red, green, blue] = channels;
  return (
    0.2126 * channel(Number.parseInt(red!, 16)) +
    0.7152 * channel(Number.parseInt(green!, 16)) +
    0.0722 * channel(Number.parseInt(blue!, 16))
  );
}

/** WCAG contrast ratio used by the landing-page style decision and its Unit contract. */
export function contrastRatio(foreground: string, background: string): number {
  const lighter = Math.max(luminance(foreground), luminance(background));
  const darker = Math.min(luminance(foreground), luminance(background));
  return (lighter + 0.05) / (darker + 0.05);
}
