import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { dataset } from "../../../../../src/features/cost-of-living-calculator/core/data/cities";
import { CostOfLivingTable } from "../../../../../src/features/cost-of-living-calculator/shell/cost-of-living";

afterEach(cleanup);

// Gherkin (binds): "Cost-of-living breakdown lists category expenses per city"
describe("CostOfLivingTable", () => {
  const defaultProps = {
    dataset,
    household: { adults: 1 as const, preschoolKids: 0 as const, schoolKids: 0 as const },
    schoolType: "public" as const,
    area: "center" as const,
  };

  it("renders a table of tech-hub cities with Country column left of City column", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    // Table present
    expect(screen.getByRole("table")).toBeTruthy();

    // Headers present — Country before City
    const columnHeaders = screen.getAllByRole("columnheader");
    const headerTexts = columnHeaders.map((h) => h.textContent ?? "");
    const countryIdx = headerTexts.findIndex((t) => /country/i.test(t));
    const cityIdx = headerTexts.findIndex((t) => /city/i.test(t));
    expect(countryIdx).toBeGreaterThanOrEqual(0);
    expect(cityIdx).toBeGreaterThan(countryIdx);
  });

  it("each row shows all 7 expense categories plus school, essentials subtotal, total, relocation sunk-cost and liquidity reserve", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const columnHeaders = screen.getAllByRole("columnheader");
    const headerTexts = columnHeaders.map((h) => h.textContent?.toLowerCase() ?? "");

    // 7 expense categories
    expect(headerTexts.some((t) => t.includes("housing"))).toBe(true);
    expect(headerTexts.some((t) => t.includes("food"))).toBe(true);
    expect(headerTexts.some((t) => t.includes("transport"))).toBe(true);
    expect(headerTexts.some((t) => t.includes("utilities"))).toBe(true);
    expect(headerTexts.some((t) => t.includes("healthcare"))).toBe(true);
    expect(headerTexts.some((t) => t.includes("childcare"))).toBe(true);
    expect(headerTexts.some((t) => t.includes("school"))).toBe(true);

    // Essentials subtotal
    expect(headerTexts.some((t) => t.includes("essentials"))).toBe(true);

    // Total (monthly)
    expect(headerTexts.some((t) => t.includes("total"))).toBe(true);

    // Separate one-time relocation sunk-cost total
    expect(headerTexts.some((t) => t.includes("relocation") || t.includes("sunk"))).toBe(true);

    // Separately labelled liquidity reserve
    expect(headerTexts.some((t) => t.includes("liquidity") || t.includes("reserve"))).toBe(true);
  });

  it("renders a row for each city in the dataset", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const rows = screen.getAllByRole("row");
    // rows = 1 header row + N city rows
    expect(rows.length).toBe(dataset.cities.length + 1);
  });

  // Gherkin (binds): "Country and city are always shown together on every tab"
  it("every data row shows Country cell immediately to the left of City cell", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const rows = screen.getAllByRole("row").slice(1); // skip header
    expect(rows.length).toBeGreaterThan(0);

    for (const city of dataset.cities.slice(0, 5)) {
      const country = dataset.countries.find((c) => c.id === city.countryId)!;
      const cityRow = rows.find((r) => r.textContent?.includes(city.name.en));
      expect(cityRow).toBeTruthy();
      const cells = within(cityRow!).getAllByRole("cell");
      // Country in cell[0], City in cell[1]
      expect(cells[0]!.textContent).toContain(country.name.en);
      expect(cells[1]!.textContent).toContain(city.name.en);
    }
  });

  // Gherkin (binds): "Healthcare funding scheme is always shown"
  it("each row shows a healthcare funding-scheme badge", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const badges = screen.getAllByTestId("healthcare-badge");
    expect(badges.length).toBe(dataset.cities.length);

    const validTexts = ["tax-funded", "mandatory payroll insurance", "out-of-pocket"];
    for (const badge of badges) {
      expect(validTexts).toContain(badge.textContent?.trim());
    }
  });

  // Gherkin (binds): "Clicking a city name opens its single-city cost-of-living detail"
  it("each city name is a link to the single-city detail", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    for (const city of dataset.cities.slice(0, 5)) {
      // Some cities share a name with their country (e.g. Singapore) — filter by href
      const links = screen.getAllByRole("link", { name: city.name.en });
      const cityLink = links.find((l) => l.getAttribute("href") === `?tab=cost&city=${city.id}`);
      expect(cityLink).toBeDefined();
      expect(cityLink).toHaveAttribute("href", `?tab=cost&city=${city.id}`);
    }
  });

  // Gherkin (binds): "Clicking a country opens Cost-of-living filtered to that country"
  it("each country name is a link to the country-filtered view", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const countriesInDataset = dataset.countries.filter((c) => dataset.cities.some((city) => city.countryId === c.id));

    for (const country of countriesInDataset.slice(0, 5)) {
      const links = screen.getAllByRole("link", { name: country.name.en });
      expect(links.length).toBeGreaterThan(0);
      expect(links[0]).toHaveAttribute("href", `?tab=cost&country=${country.id}`);
    }
  });

  // Responsive parity: mobile stacked-card view exists alongside the table (toggled by CSS),
  // one card per city, each card a city link. (Desktop/tablet use the table.)
  it("renders a mobile city-card view with one card per city", () => {
    render(<CostOfLivingTable {...defaultProps} />);
    const cards = screen.getByTestId("mobile-city-cards");
    expect(cards).toBeTruthy();
    const cityLinks = cards.querySelectorAll('a[href^="?tab=cost&city="]');
    expect(cityLinks.length).toBe(dataset.cities.length);
  });

  // UWT-005: definition tooltips on relocation column headers
  it("UWT-005: Relocation (sunk) column header has a tooltip explaining it is a one-time cost", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const columnHeaders = screen.getAllByRole("columnheader");
    const relocationHeader = columnHeaders.find((h) => /relocation/i.test(h.textContent ?? ""));
    expect(relocationHeader).toBeDefined();
    // Tooltip: either title attribute, aria-label on abbr, or data-tooltip
    const title = relocationHeader!.querySelector("[title]") ?? relocationHeader!.closest("[title]");
    const abbr = relocationHeader!.querySelector("abbr");
    const hasTooltip = title !== null || (abbr !== null && abbr.hasAttribute("title"));
    expect(hasTooltip).toBe(true);
  });

  it("UWT-005: Liquidity reserve column header has a tooltip explaining it is a cash cushion kept not spent", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const columnHeaders = screen.getAllByRole("columnheader");
    const liquidityHeader = columnHeaders.find((h) => /liquidity/i.test(h.textContent ?? ""));
    expect(liquidityHeader).toBeDefined();
    const title = liquidityHeader!.querySelector("[title]") ?? liquidityHeader!.closest("[title]");
    const abbr = liquidityHeader!.querySelector("abbr");
    const hasTooltip = title !== null || (abbr !== null && abbr.hasAttribute("title"));
    expect(hasTooltip).toBe(true);
  });

  // Phase 5 — Cycle 1c: Right-edge scroll affordance indicator
  it("Phase5-1c: a scroll affordance element with data-testid='scroll-affordance' is rendered", () => {
    render(<CostOfLivingTable {...defaultProps} />);
    const affordance = screen.getByTestId("scroll-affordance");
    expect(affordance).toBeTruthy();
  });

  // Phase 5 — Cycle 1a: Summary columns (Total, Essentials) appear immediately after City
  it("Phase5-1a: Total column header appears before Housing column header", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const columnHeaders = screen.getAllByRole("columnheader");
    const headerTexts = columnHeaders.map((h) => h.textContent?.toLowerCase() ?? "");

    const totalIdx = headerTexts.findIndex((t) => /^total$/i.test(t.trim()));
    const housingIdx = headerTexts.findIndex((t) => /housing/i.test(t));

    expect(totalIdx).toBeGreaterThanOrEqual(0);
    expect(housingIdx).toBeGreaterThanOrEqual(0);
    // Total must come BEFORE Housing (summary-first ordering)
    expect(totalIdx).toBeLessThan(housingIdx);
  });

  // Phase 5 — Cycle 1b: Total/Essentials in DOM and table wrapper has overflow-x-auto
  it("Phase5-1b: Total and Essentials column headers are in the DOM and table wrapper has overflow-x-auto class", () => {
    const { container } = render(<CostOfLivingTable {...defaultProps} />);

    // Both summary columns must be present in the DOM
    const columnHeaders = screen.getAllByRole("columnheader");
    const headerTexts = columnHeaders.map((h) => h.textContent?.toLowerCase() ?? "");
    expect(headerTexts.some((t) => /^total$/i.test(t.trim()))).toBe(true);
    expect(headerTexts.some((t) => /essentials/i.test(t))).toBe(true);

    // Table wrapper must have overflow-x-auto for horizontal scrollability
    const tableWrapper = container.querySelector(".overflow-x-auto");
    expect(tableWrapper).not.toBeNull();
  });

  // Phase 5 — Cycle 1a: Essentials also appears before Housing
  it("Phase5-1a: Essentials column header appears before Housing column header", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const columnHeaders = screen.getAllByRole("columnheader");
    const headerTexts = columnHeaders.map((h) => h.textContent?.toLowerCase() ?? "");

    const essentialsIdx = headerTexts.findIndex((t) => /essentials/i.test(t));
    const housingIdx = headerTexts.findIndex((t) => /housing/i.test(t));

    expect(essentialsIdx).toBeGreaterThanOrEqual(0);
    expect(housingIdx).toBeGreaterThanOrEqual(0);
    // Essentials must come BEFORE Housing (summary-first ordering)
    expect(essentialsIdx).toBeLessThan(housingIdx);
  });

  // UWT-014: "OOP" must be wrapped in an <abbr> with title="out-of-pocket"
  it("UWT-014: the text 'OOP' is inside an abbr element with title='out-of-pocket'", () => {
    const { container } = render(<CostOfLivingTable {...defaultProps} />);

    const abbrElements = Array.from(container.querySelectorAll("abbr"));
    const oopAbbr = abbrElements.find(
      (el) => el.textContent?.trim() === "OOP" && el.getAttribute("title") === "out-of-pocket",
    );
    expect(oopAbbr).toBeDefined();
  });

  // EWT-004 / UWT-014: the OOP abbr title must be localized — in id it must NOT be the
  // hardcoded English "out-of-pocket".
  it("EWT-004: the OOP abbr title is localized in the id locale (not 'out-of-pocket')", () => {
    const { container } = render(<CostOfLivingTable {...defaultProps} locale="id" />);
    const abbrElements = Array.from(container.querySelectorAll("abbr"));
    const oopAbbrs = abbrElements.filter((el) => el.textContent?.trim() === "OOP");
    expect(oopAbbrs.length).toBeGreaterThan(0);
    for (const abbr of oopAbbrs) {
      expect(abbr.getAttribute("title")).not.toBe("out-of-pocket");
      expect(abbr.getAttribute("title")).toBe("bayar sendiri");
    }
  });

  // UWT-012 (test-fixing): EVERY rendered "OOP" acronym must be inside an
  // <abbr title="out-of-pocket"> — audits all occurrences incl. the mobile card label.
  it("UWT-012: every rendered 'OOP' acronym is inside an abbr title='out-of-pocket'", () => {
    const { container } = render(<CostOfLivingTable {...defaultProps} />);

    // Find every text node using "OOP" as a standalone acronym/label. Exclude the
    // explanatory legend ("OOP = out-of-pocket — …"), which defines the term in prose
    // and is intentionally not an <abbr>.
    const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
    const oopTextNodes: Text[] = [];
    let node = walker.nextNode();
    while (node) {
      const text = node.textContent ?? "";
      const isLegend = /OOP\s*=\s*out-of-pocket/.test(text);
      if (/\bOOP\b/.test(text) && !isLegend) {
        oopTextNodes.push(node as Text);
      }
      node = walker.nextNode();
    }

    expect(oopTextNodes.length).toBeGreaterThan(0);

    // Each such text node's closest <abbr> must carry title="out-of-pocket".
    for (const textNode of oopTextNodes) {
      const abbr = (textNode.parentElement as HTMLElement | null)?.closest("abbr");
      expect(abbr, `'OOP' text "${textNode.textContent}" must be wrapped in <abbr>`).not.toBeNull();
      expect(abbr!.getAttribute("title")).toBe("out-of-pocket");
    }
  });

  // UWT-011: healthcare scheme badge should be sentence-cased (not ALL-CAPS)
  it("UWT-011: healthcare scheme badge text is sentence-cased, not all-caps", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const badges = screen.getAllByTestId("healthcare-badge");
    expect(badges.length).toBeGreaterThan(0);

    for (const badge of badges) {
      const text = badge.textContent?.trim() ?? "";
      if (text === "—") continue;
      // Must NOT be all-caps (i.e., text !== text.toUpperCase())
      expect(text).not.toBe(text.toUpperCase());
    }
  });

  // UWT-012: the healthcare scheme badge must render in sentence-case visually — the
  // design-system Badge defaults to `uppercase`, so each scheme badge must opt out via
  // `normal-case` so a long label ("mandatory payroll insurance") does not read ALL-CAPS
  // while shorter ones look lower-case.
  it("UWT-012: every healthcare scheme badge opts out of uppercase (normal-case)", () => {
    render(<CostOfLivingTable {...defaultProps} />);
    const badges = screen.getAllByTestId("healthcare-badge");
    expect(badges.length).toBeGreaterThan(0);
    for (const badge of badges) {
      if (badge.textContent?.trim() === "—") continue;
      expect(badge.className).toContain("normal-case");
      expect(badge.className).not.toContain("uppercase");
    }
  });

  // UWT-011: healthcare scheme column header should have a tooltip
  it("UWT-011: Healthcare scheme column header has a tooltip (title attribute)", () => {
    render(<CostOfLivingTable {...defaultProps} />);

    const columnHeaders = screen.getAllByRole("columnheader");
    const healthcareSchemeHeader = columnHeaders.find((h) =>
      /healthcare scheme|skema kesehatan/i.test(h.textContent ?? ""),
    );
    expect(healthcareSchemeHeader).toBeDefined();

    const abbr = healthcareSchemeHeader!.querySelector("abbr");
    const titleEl = healthcareSchemeHeader!.querySelector("[title]");
    const hasTooltip = abbr !== null || titleEl !== null || healthcareSchemeHeader!.hasAttribute("title");
    expect(hasTooltip).toBe(true);
  });

  // EWT-006: per-category column values must scale for household size so their sum
  // equals the Essentials subtotal shown in the same row.
  it("EWT-006: for a 2-adult household, per-category column amounts sum to the Essentials subtotal for each city row", () => {
    const twoAdultProps = {
      ...defaultProps,
      household: { adults: 2 as const, preschoolKids: 0 as const, schoolKids: 0 as const },
    };
    render(<CostOfLivingTable {...twoAdultProps} />);

    // Read all city rows via data-testid on individual cells
    for (const city of dataset.cities) {
      const housingCell = screen.getByTestId(`col-housing-${city.id}`);
      const foodCell = screen.getByTestId(`col-food-${city.id}`);
      const transportCell = screen.getByTestId(`col-transport-${city.id}`);
      const utilitiesCell = screen.getByTestId(`col-utilities-${city.id}`);
      const healthcareCell = screen.getByTestId(`col-healthcare-${city.id}`);
      const childcareCell = screen.getByTestId(`col-childcare-${city.id}`);
      const schoolCell = screen.getByTestId(`col-school-${city.id}`);
      const essentialsCell = screen.getByTestId(`col-essentials-${city.id}`);

      const housing = parseFloat(housingCell.getAttribute("data-raw") ?? "NaN");
      const food = parseFloat(foodCell.getAttribute("data-raw") ?? "NaN");
      const transport = parseFloat(transportCell.getAttribute("data-raw") ?? "NaN");
      const utilities = parseFloat(utilitiesCell.getAttribute("data-raw") ?? "NaN");
      const healthcare = parseFloat(healthcareCell.getAttribute("data-raw") ?? "NaN");
      const childcare = parseFloat(childcareCell.getAttribute("data-raw") ?? "NaN");
      const school = parseFloat(schoolCell.getAttribute("data-raw") ?? "NaN");
      const essentials = parseFloat(essentialsCell.getAttribute("data-raw") ?? "NaN");

      const categorySum = housing + food + transport + utilities + healthcare + childcare + school;
      expect(Math.abs(categorySum - essentials)).toBeLessThan(0.01);
    }
  });

  // Phase 9 Cluster H — area-toggle visible feedback
  describe("Phase 9H — area toggle shows visible caption", () => {
    it("Phase9H: cost table shows a visible area caption indicating current area (center)", () => {
      render(<CostOfLivingTable {...defaultProps} area="center" />);
      const caption = screen.getByTestId("area-caption");
      expect(caption).toBeTruthy();
      expect(caption.textContent).toMatch(/city center/i);
    });

    it("Phase9H: area caption updates when area is rural", () => {
      const { rerender } = render(<CostOfLivingTable {...defaultProps} area="center" />);
      rerender(<CostOfLivingTable {...defaultProps} area="rural" />);
      const caption = screen.getByTestId("area-caption");
      expect(caption.textContent).toMatch(/rural/i);
    });
  });

  // Phase 8: mobile cost card header shows both city and country
  describe("Phase 8 — mobile card header shows city and country", () => {
    it("Phase8: each mobile cost card header links to the country (en locale)", () => {
      render(<CostOfLivingTable {...defaultProps} />);
      const cards = screen.getByTestId("mobile-city-cards");
      const countryLinks = cards.querySelectorAll('a[href*="country="]');
      expect(countryLinks.length).toBe(dataset.cities.length);
    });

    it("Phase8: mobile cost card header shows Indonesian country name in id locale", () => {
      render(<CostOfLivingTable {...defaultProps} locale="id" />);
      const cards = screen.getByTestId("mobile-city-cards");
      const countryLinks = Array.from(cards.querySelectorAll('a[href*="country="]'));
      const countryTexts = countryLinks.map((l) => l.textContent ?? "");
      expect(countryTexts.some((t) => t === "Singapura")).toBe(true);
    });
  });

  // Cluster 3 (UWT-002 / DWT-006): the foreigner private-fallback flag reads as a warning-tone
  // Badge with plain-language wording, NOT a muted caption with cryptic "public n/a → private".
  describe("Cluster 3 — foreigner public-school flag (table)", () => {
    // Singapore (country sg, access "limited") with public school + 1 school-age child triggers
    // the private-fallback flag.
    const fallbackProps = {
      ...defaultProps,
      household: { adults: 1 as const, preschoolKids: 0 as const, schoolKids: 1 as const },
      schoolType: "public" as const,
    };

    it("renders the flag with plain-language wording (en), not the cryptic arrow", () => {
      render(<CostOfLivingTable {...fallbackProps} />);
      const flag = screen.getByTestId("school-foreigner-flag-singapore");
      expect(flag.textContent).toContain("Private — public not open to foreigners");
      expect(flag.textContent).not.toContain("→");
    });

    it("renders the flag with plain-language wording (id)", () => {
      render(<CostOfLivingTable {...fallbackProps} locale="id" />);
      const flag = screen.getByTestId("school-foreigner-flag-singapore");
      expect(flag.textContent).toContain("Swasta — negeri tak terbuka untuk WNA");
    });

    it("flag is a warning-tone Badge (not a text-muted-foreground caption)", () => {
      render(<CostOfLivingTable {...fallbackProps} />);
      const flag = screen.getByTestId("school-foreigner-flag-singapore");
      // The Badge primitive carries data-slot="badge" and a hue style.
      expect(flag.getAttribute("data-slot")).toBe("badge");
      expect(flag.className).not.toContain("text-muted-foreground");
      // Warning hue applied via the --hue-color custom property.
      expect(flag.getAttribute("style") ?? "").toContain("--hue");
    });
  });

  // Gherkin (binds): "id-locale tables use Indonesian city and country names"
  describe("id locale name rendering", () => {
    it("renders 'Singapura' (not 'Singapore') in the Country column when locale=id", () => {
      render(<CostOfLivingTable {...defaultProps} locale="id" />);
      // Singapore country name in Indonesian is "Singapura" — should appear in at least one country link
      const countryLinks = screen.getAllByRole("link").filter((el) => el.getAttribute("href")?.includes("country="));
      const countryTexts = countryLinks.map((l) => l.textContent ?? "");
      expect(countryTexts.some((t) => t === "Singapura")).toBe(true);
    });

    it("renders 'Jepang' (not 'Japan') in the Country column when locale=id", () => {
      render(<CostOfLivingTable {...defaultProps} locale="id" />);
      // Japan country name in Indonesian is "Jepang"
      const countryLinks = screen.getAllByRole("link").filter((el) => el.getAttribute("href")?.includes("country="));
      const countryTexts = countryLinks.map((l) => l.textContent ?? "");
      expect(countryTexts.some((t) => t === "Jepang")).toBe(true);
    });
  });
});
