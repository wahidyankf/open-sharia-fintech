import { describe, it, expect } from "vitest";
import * as webUi from "../../src/index";

/**
 * The package's public barrel (`src/index.ts`) is never imported by a component test, since every
 * component test imports its subject directly. This is a real production module — the entry point
 * consuming apps actually resolve `@open-sharia-enterprise/web-ui` to — so it needs its own smoke
 * test asserting every re-export resolves, mirroring `web-ui-token`'s `tokens-export.steps.ts`.
 */
describe("web-ui package exports", () => {
  it("exports the utility", () => {
    expect(webUi.cn).toBeDefined();
  });

  it("exports the un-barreled primitives re-exported at the top level", () => {
    expect(webUi.Command).toBeDefined();
    expect(webUi.DropdownMenu).toBeDefined();
    expect(webUi.Tabs).toBeDefined();
    expect(webUi.Tooltip).toBeDefined();
    expect(webUi.ScrollArea).toBeDefined();
    expect(webUi.Separator).toBeDefined();
    expect(webUi.Table).toBeDefined();
  });

  it("exports every OSE composite component", () => {
    expect(webUi.Button).toBeDefined();
    expect(webUi.Alert).toBeDefined();
    expect(webUi.Input).toBeDefined();
    expect(webUi.Card).toBeDefined();
    expect(webUi.Label).toBeDefined();
    expect(webUi.Dialog).toBeDefined();
    expect(webUi.Icon).toBeDefined();
    expect(webUi.Toggle).toBeDefined();
    expect(webUi.ProgressRing).toBeDefined();
    expect(webUi.Sheet).toBeDefined();
    expect(webUi.AppHeader).toBeDefined();
    expect(webUi.HuePicker).toBeDefined();
    expect(webUi.HUES).toBeDefined();
    expect(webUi.InfoTip).toBeDefined();
    expect(webUi.StatCard).toBeDefined();
    expect(webUi.TabBar).toBeDefined();
    expect(webUi.SideNav).toBeDefined();
    expect(webUi.HighlightText).toBeDefined();
    expect(webUi.highlightText).toBeDefined();
    expect(webUi.ScrollToTop).toBeDefined();
    expect(webUi.SearchComponent).toBeDefined();
    expect(webUi.ThemeToggle).toBeDefined();
    expect(webUi.Textarea).toBeDefined();
    expect(webUi.Badge).toBeDefined();
  });
});
