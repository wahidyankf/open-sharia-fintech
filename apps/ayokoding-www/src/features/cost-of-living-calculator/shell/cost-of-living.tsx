import {
  Badge,
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@open-sharia-enterprise/web-ui";
import { healthcareBadgeHue } from "../core/format";
import type { Dataset, Household } from "../core/data/cities";
import type { Area, SchoolType } from "../core/calc";
import {
  childcareLocal,
  essentialsLocal,
  expensesLocal,
  liquidityReserveLocal,
  relocationSunkLocal,
  scaleAmount,
  schoolLocal,
} from "../core/calc";
import { fmtDualCurrency } from "../core/format";
import { fxToUsd } from "../core/data/fx";
import { ForeignerSchoolFlag } from "./foreigner-school-flag";
import { localeName } from "./geo-filters";
import type { Locale } from "@/features/i18n/core/config";
import type { ReactNode } from "react";
import { t } from "@/features/i18n/core/translations";

type Props = {
  dataset: Dataset;
  household: Household;
  schoolType: SchoolType;
  area: Area;
  locale?: Locale;
};

function healthcareBadgeLabel(type: "oop" | "tax-funded" | "mixed", locale: Locale): string {
  if (type === "oop") return t(locale, "healthcareOutOfPocket");
  if (type === "tax-funded") return t(locale, "healthcareTaxFunded");
  return t(locale, "healthcareMandatoryPayroll");
}

// One labelled row inside a mobile city card.
function CardRow({ label, value, emphasis }: { label: ReactNode; value: string; emphasis?: "subtotal" | "total" }) {
  const cls =
    emphasis === "total"
      ? "flex items-baseline justify-between border-t pt-1.5 text-sm font-semibold"
      : emphasis === "subtotal"
        ? "flex items-baseline justify-between border-t pt-1.5 text-sm font-medium"
        : "flex items-baseline justify-between text-sm";
  return (
    <div className={cls}>
      <span className="text-muted-foreground">{label}</span>
      <span className="tabular-nums">{value}</span>
    </div>
  );
}

export function CostOfLivingTable({ dataset, household, schoolType, area, locale = "en" }: Props) {
  const countryById = Object.fromEntries(dataset.countries.map((c) => [c.id, c]));

  // Compute every city's figures once; both the table and the mobile cards render from this.
  const rows = dataset.cities.map((city) => {
    const country = countryById[city.countryId]!;
    const e = city.expenses;
    const fxRate = fxToUsd(dataset.fx, city.currency);
    return {
      city,
      country,
      fxRate,
      housing: scaleAmount(e.housing.amount, "housing", household, area),
      food: scaleAmount(e.food.amount, "food", household, area),
      transport: scaleAmount(e.transport.amount, "transport", household, area),
      utilities: scaleAmount(e.utilities.amount, "utilities", household, area),
      healthcare: scaleAmount(e.healthcare.amount, "healthcare", household, area),
      childcare: childcareLocal(city, household),
      school: schoolLocal(city, country, household, schoolType),
      lifestyle: e.lifestyle.amount,
      essentials: essentialsLocal(city, country, household, schoolType, area),
      total: expensesLocal(city, country, household, schoolType, area),
      relocation: relocationSunkLocal(city),
      liquidity: liquidityReserveLocal(city),
      // True when "public" is selected but this country isn't fully open to foreign residents, so
      // the shown school figure is actually the PRIVATE one (effectiveSchoolType fell back).
      schoolForeignerFallback:
        schoolType === "public" && household.schoolKids > 0 && country.foreignerPublicSchool.access !== "open",
    };
  });

  // Per-category columns are hidden on tablet (md) and shown only on desktop (lg+).
  const tabletHidden = "hidden lg:table-cell";

  return (
    <>
      <p data-testid="oop-legend" className="mb-1 text-xs text-muted-foreground">
        {t(locale, "oopLegend")}
      </p>

      {/* Tablet + desktop (md+): table. Granular columns collapse on tablet, full on lg+.
          Rendered before the mobile cards so country/city links keep their DOM order
          (a country link precedes the same-named city link) regardless of breakpoint. */}
      <div className="relative hidden md:block">
        {/* Right-edge scroll affordance: gradient fade indicates more columns exist to the right */}
        <div
          data-testid="scroll-affordance"
          aria-hidden="true"
          className="pointer-events-none absolute inset-y-0 right-0 w-12 bg-gradient-to-l from-background/80 to-transparent"
        />
        <div className="overflow-x-auto">
          <Table>
            <TableCaption data-testid="area-caption" className="text-xs text-muted-foreground">
              {t(locale, area === "center" ? "optCenter" : "optRural")}
            </TableCaption>
            <TableHeader>
              <TableRow>
                {/* Identity columns — always visible */}
                <TableHead>{t(locale, "colCountry")}</TableHead>
                <TableHead>{t(locale, "colCity")}</TableHead>
                {/* Summary columns — always visible, placed before breakdown so they appear without scrolling */}
                <TableHead>{t(locale, "colTotal")}</TableHead>
                <TableHead>{t(locale, "colEssentials")}</TableHead>
                {/* Breakdown columns — hidden on tablet, shown on desktop (lg+) */}
                <TableHead className={tabletHidden}>
                  <abbr title={t(locale, "tooltipHealthcareScheme")}>{t(locale, "colHealthcareScheme")}</abbr>
                </TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colHousing")}</TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colFood")}</TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colTransport")}</TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colUtilities")}</TableHead>
                <TableHead className={tabletHidden}>
                  {t(locale, "colHealthcareOOPPrefix")} (<abbr title={t(locale, "healthcareOutOfPocket")}>OOP</abbr>)
                </TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colChildcare")}</TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colSchool")}</TableHead>
                <TableHead className={tabletHidden}>{t(locale, "colLifestyle")}</TableHead>
                {/* One-time cost columns */}
                <TableHead>
                  <abbr title={t(locale, "tooltipRelocationSunk")}>{t(locale, "colRelocationSunk")}</abbr>
                </TableHead>
                <TableHead>
                  <abbr title={t(locale, "tooltipLiquidityReserve")}>{t(locale, "colLiquidityReserve")}</abbr>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.map((r) => (
                <TableRow key={r.city.id}>
                  {/* Identity cells */}
                  <TableCell>
                    <a href={`?tab=cost&country=${r.city.countryId}`}>
                      {r.country ? localeName(r.country.name, locale) : r.city.countryId}
                    </a>
                  </TableCell>
                  <TableCell>
                    <a href={`?tab=cost&city=${r.city.id}`}>{localeName(r.city.name, locale)}</a>
                  </TableCell>
                  {/* Summary cells */}
                  <TableCell className="text-right font-medium">
                    {fmtDualCurrency(r.total, r.city.currency, r.total * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-essentials-${r.city.id}`}
                    data-raw={r.essentials}
                    className="text-right font-medium"
                  >
                    {fmtDualCurrency(r.essentials, r.city.currency, r.essentials * r.fxRate)}
                  </TableCell>
                  {/* Breakdown cells */}
                  <TableCell className={tabletHidden}>
                    {r.country ? (
                      <Badge
                        data-testid="healthcare-badge"
                        variant="outline"
                        hue={healthcareBadgeHue(r.country.healthcareModelType)}
                        className="normal-case"
                      >
                        {healthcareBadgeLabel(r.country.healthcareModelType, locale)}
                      </Badge>
                    ) : (
                      <span data-testid="healthcare-badge">—</span>
                    )}
                  </TableCell>
                  <TableCell
                    data-testid={`col-housing-${r.city.id}`}
                    data-raw={r.housing}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.housing, r.city.currency, r.housing * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-food-${r.city.id}`}
                    data-raw={r.food}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.food, r.city.currency, r.food * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-transport-${r.city.id}`}
                    data-raw={r.transport}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.transport, r.city.currency, r.transport * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-utilities-${r.city.id}`}
                    data-raw={r.utilities}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.utilities, r.city.currency, r.utilities * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-healthcare-${r.city.id}`}
                    data-raw={r.healthcare}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.healthcare, r.city.currency, r.healthcare * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-childcare-${r.city.id}`}
                    data-raw={r.childcare}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.childcare, r.city.currency, r.childcare * r.fxRate)}
                  </TableCell>
                  <TableCell
                    data-testid={`col-school-${r.city.id}`}
                    data-raw={r.school}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.school, r.city.currency, r.school * r.fxRate)}
                    {r.schoolForeignerFallback && (
                      <span className="block">
                        <ForeignerSchoolFlag cityId={r.city.id} locale={locale} />
                      </span>
                    )}
                  </TableCell>
                  <TableCell
                    data-testid={`col-lifestyle-${r.city.id}`}
                    data-raw={r.lifestyle}
                    className={`text-right ${tabletHidden}`}
                  >
                    {fmtDualCurrency(r.lifestyle, r.city.currency, r.lifestyle * r.fxRate)}
                  </TableCell>
                  {/* One-time cost cells */}
                  <TableCell className="text-right">
                    {fmtDualCurrency(r.relocation, r.city.currency, r.relocation * r.fxRate)}
                  </TableCell>
                  <TableCell className="text-right">
                    {fmtDualCurrency(r.liquidity, r.city.currency, r.liquidity * r.fxRate)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Mobile (<md): stacked city cards */}
      <div data-testid="mobile-city-cards" className="space-y-3 md:hidden">
        {rows.map((r) => (
          <div key={r.city.id} className="overflow-hidden rounded-lg border bg-card shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-2 bg-primary px-3 py-2 text-primary-foreground">
              <a href={`?tab=cost&city=${r.city.id}`} className="font-semibold underline">
                {r.city.name[locale] ?? r.city.name.en}
              </a>
              {r.country && (
                <a
                  href={`?tab=cost&country=${r.city.countryId}`}
                  className="text-xs text-primary-foreground/80 underline"
                >
                  {localeName(r.country.name, locale)}
                </a>
              )}
              {r.country && (
                <Badge
                  variant="outline"
                  hue={healthcareBadgeHue(r.country.healthcareModelType)}
                  className="border-white/40 bg-white/15 text-white normal-case"
                >
                  {healthcareBadgeLabel(r.country.healthcareModelType, locale)}
                </Badge>
              )}
            </div>
            <div className="space-y-1 p-3">
              <CardRow
                label={t(locale, "colHousing")}
                value={fmtDualCurrency(r.housing, r.city.currency, r.housing * r.fxRate)}
              />
              <CardRow
                label={t(locale, "colFood")}
                value={fmtDualCurrency(r.food, r.city.currency, r.food * r.fxRate)}
              />
              <CardRow
                label={t(locale, "colTransport")}
                value={fmtDualCurrency(r.transport, r.city.currency, r.transport * r.fxRate)}
              />
              <CardRow
                label={t(locale, "colUtilities")}
                value={fmtDualCurrency(r.utilities, r.city.currency, r.utilities * r.fxRate)}
              />
              <CardRow
                label={
                  <>
                    {t(locale, "colHealthcareOOPPrefix")} (<abbr title={t(locale, "healthcareOutOfPocket")}>OOP</abbr>)
                  </>
                }
                value={fmtDualCurrency(r.healthcare, r.city.currency, r.healthcare * r.fxRate)}
              />
              <CardRow
                label={t(locale, "colChildcare")}
                value={fmtDualCurrency(r.childcare, r.city.currency, r.childcare * r.fxRate)}
              />
              <CardRow
                label={t(locale, "colSchool")}
                value={fmtDualCurrency(r.school, r.city.currency, r.school * r.fxRate)}
              />
              {r.schoolForeignerFallback && (
                <div className="flex justify-end">
                  <ForeignerSchoolFlag cityId={r.city.id} locale={locale} testIdSuffix="-mobile" />
                </div>
              )}
              <CardRow
                label={t(locale, "colEssentials")}
                value={fmtDualCurrency(r.essentials, r.city.currency, r.essentials * r.fxRate)}
                emphasis="subtotal"
              />
              <CardRow
                label={t(locale, "colTotal")}
                value={fmtDualCurrency(r.total, r.city.currency, r.total * r.fxRate)}
                emphasis="total"
              />
              <CardRow
                label={t(locale, "colRelocationSunk")}
                value={fmtDualCurrency(r.relocation, r.city.currency, r.relocation * r.fxRate)}
              />
              <CardRow
                label={t(locale, "colLiquidityReserve")}
                value={fmtDualCurrency(r.liquidity, r.city.currency, r.liquidity * r.fxRate)}
              />
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
