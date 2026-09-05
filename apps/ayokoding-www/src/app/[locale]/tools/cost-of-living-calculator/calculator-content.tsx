"use client";

import { useEffect, useRef, useState } from "react";
import { usePathname, useSearchParams, useRouter } from "next/navigation";
import { dataset } from "@/features/cost-of-living-calculator/core/data/cities";
import { roleMatrix } from "@/features/cost-of-living-calculator/core/data/roles";
import type { Household } from "@/features/cost-of-living-calculator/core/data/cities";
import type { Area, SchoolType } from "@/features/cost-of-living-calculator/core/calc";
import type { GeoScope } from "@/features/cost-of-living-calculator/shell/geo-filters";
import { CostOfLivingTable } from "@/features/cost-of-living-calculator/shell/cost-of-living";
import { SavingsTable } from "@/features/cost-of-living-calculator/shell/savings";
import { MinRoleTable } from "@/features/cost-of-living-calculator/shell/min-role";
import { CityDetail } from "@/features/cost-of-living-calculator/shell/city-detail";
import { GeoFilters } from "@/features/cost-of-living-calculator/shell/geo-filters";
import { Controls } from "@/features/cost-of-living-calculator/shell/controls";
import { CalculatorBreadcrumb } from "@/features/cost-of-living-calculator/shell/calculator-breadcrumb";
import { useLocale } from "@/features/i18n/shell/use-locale";
import { t } from "@/features/i18n/core/translations";
import { Tabs, TabsList, TabsTrigger, TabsContent, cn } from "@open-sharia-enterprise/web-ui";
import {
  decodeState,
  encodeState,
  applyCountryChange,
  applyCityChange,
  parentScopeParams,
  PARAM_KEYS,
} from "@/features/cost-of-living-calculator/core/url-state";
import type { CalculatorState } from "@/features/cost-of-living-calculator/core/url-state";

export function CostOfLivingCalculatorContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const rawSearchParams = searchParams.toString();
  const pendingScrollY = useRef<number | null>(null);
  const [hydrated, setHydrated] = useState(false);

  // The URL remains the durable source of truth. Static exports do not reliably propagate native
  // history writes back through useSearchParams, so keep a render replica that is updated with each
  // production write and resynchronized whenever routing or browser history supplies a new URL.
  const [currentState, setCurrentState] = useState(() => decodeState(new URLSearchParams(rawSearchParams), dataset));

  useEffect(() => {
    setCurrentState(decodeState(new URLSearchParams(rawSearchParams), dataset));
  }, [rawSearchParams]);

  useEffect(() => setHydrated(true), []);

  useEffect(() => {
    const syncFromBrowserHistory = () => {
      setCurrentState(decodeState(new URLSearchParams(window.location.search), dataset));
    };
    window.addEventListener("popstate", syncFromBrowserHistory);
    return () => window.removeEventListener("popstate", syncFromBrowserHistory);
  }, []);

  // UWT-015 (A-3): capture, at mount, whether the region/country were auto-derived
  // solely from a city deep link (raw URL has `city` but no explicit
  // `region`/`country`). Mount-time capture so the mount canonicalization — which
  // injects region/country into the URL — does not flip this back to false.
  const [regionAutoDerivedFromCity] = useState(() => {
    const raw = new URLSearchParams(rawSearchParams);
    return raw.has(PARAM_KEYS.city) && !raw.has(PARAM_KEYS.region) && !raw.has(PARAM_KEYS.country);
  });

  const { tab: activeTab, region, countryId, cityId, household, schoolType, area } = currentState;

  // Canonicalize the browser URL after hydration. A statically exported route can
  // ignore its first App Router replace, even when useSearchParams has the browser
  // query. Production therefore replaces the current browser entry directly;
  // normal test and development routing continues to use the App Router.
  useEffect(() => {
    const isProduction = process.env.NODE_ENV === "production";
    const rawParams = new URLSearchParams(isProduction ? window.location.search : rawSearchParams);
    const canonicalParams = encodeState(decodeState(rawParams, dataset));
    if (rawParams.toString() !== canonicalParams.toString()) {
      const qs = canonicalParams.toString();
      if (isProduction) {
        // Replacing the current entry means Back skips the dirty URL.
        window.history.replaceState(window.history.state, "", qs ? `${pathname}?${qs}` : pathname);
      } else {
        router.replace(qs ? `?${qs}` : "?", { scroll: false });
      }
    }
  }, [pathname, rawSearchParams, router]);

  // `scroll: false` normally preserves the viewport for query-only App Router transitions,
  // but statically exported routes can still reset to the document top when the query commits.
  // Restore the exact pre-transition offset after the URL-driven render; the following animation
  // frame also covers the export router's late scroll adjustment.
  useEffect(() => {
    const scrollY = pendingScrollY.current;
    if (scrollY === null) return;
    pendingScrollY.current = null;
    if (scrollY <= 0) return;

    const restore = () => window.scrollTo(window.scrollX, scrollY);
    restore();
    const frame = window.requestAnimationFrame(restore);
    return () => window.cancelAnimationFrame(frame);
  }, [rawSearchParams]);

  // Helper: encode new state and push to URL history.
  //
  // `scroll: false` is mandatory: this is in-page filter/view state, not a page change, so
  // the default Next.js navigation behaviour (scroll to top of document) would yank the
  // viewport away from the control the user just touched on every filter change. Keeping the
  // scroll position is the fix for "updating a filter jumps me back to the top".
  function pushState(next: CalculatorState) {
    const params = encodeState(next);
    const qs = params.toString();
    pendingScrollY.current = window.scrollY;
    if (process.env.NODE_ENV === "production") {
      // Keep static-export navigation on one coherent history mechanism. Mixing a native replace
      // (continuous fields) with a later App Router push leaves that push inert in the exported app.
      // Next patches pushState into useSearchParams, so discrete changes remain reactive and retain
      // their distinct Back entry.
      setCurrentState(next);
      window.history.pushState(window.history.state, "", qs ? `${pathname}?${qs}` : pathname);
    } else {
      router.push(qs ? `?${qs}` : "?", { scroll: false });
    }
  }

  // Like pushState but replaces the current history entry — used for continuous inputs
  // (gross/target text fields) so typing does not spam the browser back stack. Also
  // `scroll: false` for the same in-page-state reason as pushState above.
  function replaceState(next: CalculatorState) {
    const params = encodeState(next);
    const qs = params.toString();
    pendingScrollY.current = window.scrollY;
    if (process.env.NODE_ENV === "production") {
      // On the statically exported route, App Router replace can leave the controlled field's
      // local echo updated without committing its query value. Next patches the native history
      // methods into useSearchParams, so this preserves replace/back-stack semantics and keeps
      // the URL-driven state reactive at the same time.
      setCurrentState(next);
      window.history.replaceState(window.history.state, "", qs ? `${pathname}?${qs}` : pathname);
    } else {
      router.replace(qs ? `?${qs}` : "?", { scroll: false });
    }
  }

  // Build scoped dataset for filtered table views.
  // City selection is the narrowest scope and must win — a city-only filter
  // (Country = "All countries") still scopes candidates to that single city.
  const scopedCities = (() => {
    if (cityId) return dataset.cities.filter((c) => c.id === cityId);
    if (countryId) return dataset.cities.filter((c) => c.countryId === countryId);
    if (region) return dataset.cities.filter((c) => c.region === region);
    return dataset.cities;
  })();
  const scopedDataset = { ...dataset, cities: scopedCities };
  const cityScope = scopedCities === dataset.cities ? null : scopedCities;

  // Event delegation: intercept city/country <a> link clicks inside tab content
  function handleTableClick(e: React.MouseEvent) {
    const a = (e.target as HTMLElement).closest("a");
    if (!a) return;
    // The city-detail "Back to all cities" link must navigate to its bare parent-scope
    // href as written. Without this guard, the delegation below would re-interpret a
    // back href like "?region=…&country=…" as a country click and re-derive (and thus
    // re-inject) the city via applyCountryChange — defeating the parent-scope back link.
    if (a.dataset.backLink === "true") return;
    const href = a.getAttribute("href") ?? "";
    if (!href.startsWith("?")) return;
    const params = new URLSearchParams(href.slice(1));
    if (params.has("city")) {
      e.preventDefault();
      const newCityId = params.get("city")!;
      const next = applyCityChange({ ...currentState, tab: "cost" }, newCityId, dataset);
      pushState(next);
    } else if (params.has("country")) {
      e.preventDefault();
      const newCountryId = params.get("country")!;
      const next = applyCountryChange({ ...currentState, tab: "cost" }, newCountryId, dataset);
      pushState(next);
    }
  }

  const firstCity = dataset.cities[0]!;

  function handleTabChange(value: string) {
    const next = value as CalculatorState["tab"];
    // Tab change: clear cityId when moving away from cost tab
    const nextState: CalculatorState = {
      ...currentState,
      tab: next,
      cityId: next === "cost" ? cityId : null,
    };
    pushState(nextState);
  }

  function handleScopeChange(scope: GeoScope) {
    const nextState: CalculatorState = {
      ...currentState,
      region: scope.region,
      countryId: scope.countryId,
      cityId: scope.cityId,
    };
    pushState(nextState);
  }

  function handleHouseholdChange(h: Household) {
    pushState({ ...currentState, household: h });
  }

  function handleSchoolTypeChange(s: SchoolType) {
    pushState({ ...currentState, schoolType: s });
  }

  function handleAreaChange(a: Area) {
    pushState({ ...currentState, area: a });
  }

  // Tab-description className built via `cn()` so the active/inactive `hidden` toggle is a
  // distinct class token. Building it as a raw template literal previously fused
  // `text-muted-foreground` with `hidden` into the dead class `text-muted-foregroundhidden`,
  // so inactive descriptions never hid (EWT-001 ≡ DWT-001).
  const tabDescClass = (tab: CalculatorState["tab"]) =>
    cn("mt-1 text-sm text-muted-foreground", activeTab === tab ? undefined : "hidden");

  // Shared min-44px touch-target class for the tab triggers (EWT-002, WCAG 2.5.8). The
  // brand-primary active styling is layered on per trigger.
  const tabTriggerClass =
    "min-h-[44px] data-[state=active]:bg-primary data-[state=active]:text-primary-foreground dark:data-[state=active]:!bg-primary dark:data-[state=active]:!text-primary-foreground";

  // Show city detail view when a city is selected on the cost tab
  const detailCityId = activeTab === "cost" ? cityId : null;

  // Back link for city detail: encode parent geo scope (region+country, no city).
  // Falls back to ?tab=cost when no geo scope is set.
  //
  // UWT-015 (A-3): when the region/country were auto-derived solely from a city
  // deep link (i.e. the raw URL has `city` but no explicit `region`/`country`),
  // the user never chose that scope — so the back link returns to the bare
  // calculator (`?tab=cost`) rather than injecting region=…&country=….
  const cityDetailBackHref = (() => {
    if (regionAutoDerivedFromCity) {
      return "?tab=cost";
    }
    const p = parentScopeParams(currentState);
    const qs = p.toString();
    return qs ? `?${qs}` : "?tab=cost";
  })();

  // Shared (generic) geo + household filters. Rendered AFTER each tab's own specific inputs
  // so the tab-specific controls lead and the generic filters follow on every tab. Only the
  // active tab mounts, so this single node is never used in two places at once.
  const filtersSlot = (
    <>
      {/* Shared geo filters — fully controlled, reads from URL-derived state */}
      <GeoFilters
        dataset={dataset}
        locale={locale}
        region={region}
        countryId={countryId}
        cityId={cityId}
        onScopeChange={handleScopeChange}
      />

      {/* Shared cost-basis controls.
          The single-city "Example — estimated monthly essentials" preview is no longer shown on
          any tab. The min-role tab (its only former consumer) now lists every qualifying city, so a
          one-city example is redundant and misleading there. Controls keeps the capability for unit
          tests, but the product never renders it (showPreview is always false). */}
      <Controls
        dataset={dataset}
        previewCityId={detailCityId ?? firstCity.id}
        household={household}
        schoolType={schoolType}
        area={area}
        locale={locale}
        showPreview={false}
        onHouseholdChange={handleHouseholdChange}
        onSchoolTypeChange={handleSchoolTypeChange}
        onAreaChange={handleAreaChange}
      />

      {/* Data last updated + estimates disclaimer */}
      <p data-testid="data-last-updated" className="text-xs text-muted-foreground">
        {t(locale, "dataLastUpdated")}:{" "}
        {new Intl.DateTimeFormat(locale === "id" ? "id-ID" : "en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        }).format(new Date(dataset.snapshotDate))}
        {" · "}
        <span data-testid="estimates-disclaimer">{t(locale, "estimatesOnly")}</span>
      </p>
    </>
  );

  return (
    <main
      data-testid="calc-page"
      data-hydrated={hydrated ? "true" : undefined}
      className="mx-auto max-w-6xl space-y-4 px-4 py-6"
    >
      <CalculatorBreadcrumb />
      <h1 className="text-2xl font-bold tracking-tight">{t(locale, "calcTitle")}</h1>
      <p data-testid="calc-subtitle" className="text-sm text-muted-foreground">
        {t(locale, "calcSubtitle")}
      </p>

      <Tabs value={activeTab} onValueChange={handleTabChange}>
        {/* Colored segmented tab control — active tab uses ayokoding brand primary (blue) */}
        {/* EWT-R01: the tablist must never push document width past the viewport in any
            locale. The web-ui TabsList defaults to `inline-flex w-fit`, so longer locale
            labels (e.g. id: "Biaya hidup"/"Tabungan"/"Jabatan minimum") overflow at 320px.
            Force a full-width, viewport-bounded box so `overflow-x-auto` scrolls the tabs
            INTERNALLY instead of widening the page.
            `overflow-y-hidden` is mandatory: per CSS spec, when overflow-x is `auto` the
            `visible` default of overflow-y computes to `auto` too, so `overflow-x-auto`
            alone silently shows a vertical scrollbar gutter whenever the triggers are even
            a pixel taller than the list box. Pin overflow-y so only horizontal scrolls. */}
        <TabsList
          aria-label={t(locale, "ariaTabsNav")}
          className="flex w-full max-w-full justify-start overflow-x-auto overflow-y-hidden"
        >
          <TabsTrigger value="cost" aria-describedby="tab-desc-cost" className={tabTriggerClass}>
            {t(locale, "tabCostOfLiving")}
          </TabsTrigger>
          <TabsTrigger value="savings" aria-describedby="tab-desc-savings" className={tabTriggerClass}>
            {t(locale, "tabSavings")}
          </TabsTrigger>
          <TabsTrigger value="min-role" aria-describedby="tab-desc-min-role" className={tabTriggerClass}>
            {t(locale, "tabMinRole")}
          </TabsTrigger>
        </TabsList>
        {/* Tab descriptions: visibly rendered and associated with each trigger via
            aria-describedby. Showing only the active tab's description avoids duplicating
            the same prose elsewhere on screen. */}
        <p id="tab-desc-cost" data-testid="tab-desc-cost" className={tabDescClass("cost")}>
          {t(locale, "tabCostDesc")}
        </p>
        <p id="tab-desc-savings" data-testid="tab-desc-savings" className={tabDescClass("savings")}>
          {t(locale, "tabSavingsDesc")}
        </p>
        <p id="tab-desc-min-role" data-testid="tab-desc-min-role" className={tabDescClass("min-role")}>
          {t(locale, "tabMinRoleDesc")}
        </p>

        {/* Tab content — event delegation intercepts clicks bubbling up from the
            interactive <a> links inside the tables. The div is not itself an interactive
            control; the real controls are the anchors. Keyboard activation (Enter on a
            focused link) synthesizes a click that bubbles here, so no separate key handler
            or role is needed — the jsx-a11y heuristics misfire on this delegation pattern.
            Each tab leads with its own specific inputs, then the shared generic filters
            (filtersSlot), then its results. */}
        {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions */}
        <div onClick={handleTableClick}>
          <TabsContent value="cost">
            {/* Cost tab has no tab-specific inputs, so the generic filters lead. */}
            {filtersSlot}
            {detailCityId ? (
              <div data-testid="city-detail">
                <CityDetail
                  dataset={dataset}
                  cityId={detailCityId}
                  household={household}
                  schoolType={schoolType}
                  area={area}
                  locale={locale}
                  backHref={cityDetailBackHref}
                />
              </div>
            ) : (
              <CostOfLivingTable
                dataset={scopedDataset}
                household={household}
                schoolType={schoolType}
                area={area}
                locale={locale}
              />
            )}
          </TabsContent>

          <TabsContent value="savings">
            <SavingsTable
              dataset={scopedDataset}
              matrix={roleMatrix}
              household={household}
              schoolType={schoolType}
              area={area}
              locale={locale}
              filtersSlot={filtersSlot}
              gross={currentState.gross}
              onGrossChange={(gross) => replaceState({ ...currentState, gross })}
            />
          </TabsContent>

          <TabsContent value="min-role">
            <MinRoleTable
              dataset={dataset}
              matrix={roleMatrix}
              household={household}
              schoolType={schoolType}
              area={area}
              cityScope={cityScope}
              locale={locale}
              filtersSlot={filtersSlot}
              inputs={currentState.minRole}
              onInputsChange={(minRole) => replaceState({ ...currentState, minRole })}
            />
          </TabsContent>
        </div>
      </Tabs>

      {/* Full disclaimer block */}
      <details data-testid="disclaimer-block">
        <summary className="cursor-pointer text-xs text-muted-foreground">
          {t(locale, "estimatesOnly")} — disclaimer
        </summary>
        <ul className="mt-1 space-y-1 text-xs text-muted-foreground">
          <li>{t(locale, "disclaimerPension")}</li>
          <li>{t(locale, "disclaimerClothing")}</li>
          <li>{t(locale, "disclaimerFx")}</li>
          <li>{t(locale, "disclaimerSnapshot")}</li>
          <li>{t(locale, "disclaimerTax")}</li>
          <li>{t(locale, "disclaimerHealthcare")}</li>
          <li>{t(locale, "disclaimerRelocation")}</li>
          <li>{t(locale, "disclaimerRoleSalary")}</li>
          <li>{t(locale, "disclaimerNonSalary")}</li>
        </ul>
      </details>
    </main>
  );
}
