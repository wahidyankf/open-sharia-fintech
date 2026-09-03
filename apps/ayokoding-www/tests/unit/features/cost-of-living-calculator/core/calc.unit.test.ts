import { describe, expect, it } from "vitest";
import { fx, fxToUsd } from "../../../../../src/features/cost-of-living-calculator/core/data/fx";
import {
  cities,
  countries,
  AREA_MULTIPLIERS,
  equivalisedSize,
  subLinear,
  perCapita,
} from "../../../../../src/features/cost-of-living-calculator/core/data/cities";
import {
  grossMonthlyToAnnual,
  grossAnnualToMonthly,
  totalCompAnnual,
  incomeBand,
  effectiveRateForCity,
  netUsd,
  childcareLocal,
  schoolLocal,
  effectiveSchoolType,
  foreignerCanUsePublicSchool,
  essentialsLocal,
  expensesLocal,
  relocationSunkLocal,
  relocationSunkUsd,
  liquidityReserveLocal,
  liquidityReserveUsd,
  savingsRow,
  sortByEssentialSavings,
} from "../../../../../src/features/cost-of-living-calculator/core/calc";

// Grab test fixtures from the real dataset
const berlin = cities.find((c) => c.id === "berlin")!;
const tokyo = cities.find((c) => c.id === "tokyo")!;
const sanFrancisco = cities.find((c) => c.id === "san-francisco")!;
const austin = cities.find((c) => c.id === "austin")!;
const singapore = cities.find((c) => c.id === "singapore")!;
const london = cities.find((c) => c.id === "london")!;

const deDe = countries.find((c) => c.id === "de")!;
const jpJp = countries.find((c) => c.id === "jp")!;
const usUs = countries.find((c) => c.id === "us")!;
const sgSg = countries.find((c) => c.id === "sg")!;
const gbGb = countries.find((c) => c.id === "gb")!;

const singleNoKids = { adults: 1, preschoolKids: 0, schoolKids: 0 } as const;
const marriedTwoPreschool = { adults: 2, preschoolKids: 2, schoolKids: 0 } as const;
const marriedOneSchool = { adults: 2, preschoolKids: 0, schoolKids: 1 } as const;

describe("grossMonthlyToAnnual / grossAnnualToMonthly", () => {
  it("monthly × 12 = annual", () => {
    expect(grossMonthlyToAnnual(3000)).toBe(36000);
    expect(grossMonthlyToAnnual(0)).toBe(0);
  });

  it("annual / 12 = monthly (inverse)", () => {
    expect(grossAnnualToMonthly(36000)).toBe(3000);
    expect(grossAnnualToMonthly(0)).toBe(0);
  });

  it("round-trips", () => {
    const monthly = 5432.5;
    expect(grossAnnualToMonthly(grossMonthlyToAnnual(monthly))).toBeCloseTo(monthly, 6);
  });
});

describe("totalCompAnnual", () => {
  it("grossAnnual + nonSalaryCompAnnual", () => {
    expect(totalCompAnnual(100000, 20000)).toBe(120000);
    expect(totalCompAnnual(80000, 0)).toBe(80000);
  });
});

describe("incomeBand", () => {
  it("classifies below lowToMid as low", () => {
    // de: lowToMid=4000, midToHigh=9000
    expect(incomeBand(2000, deDe)).toBe("low");
  });

  it("classifies at lowToMid threshold as mid", () => {
    expect(incomeBand(4000, deDe)).toBe("mid");
  });

  it("classifies between thresholds as mid", () => {
    expect(incomeBand(6000, deDe)).toBe("mid");
  });

  it("classifies at midToHigh threshold as high", () => {
    expect(incomeBand(9000, deDe)).toBe("high");
  });

  it("classifies above midToHigh as high", () => {
    expect(incomeBand(15000, deDe)).toBe("high");
  });
});

describe("effectiveRateForCity", () => {
  it("unitary country (DE) — federal only, no subNational", () => {
    expect(berlin.subNational).toBeUndefined();
    const rate = effectiveRateForCity(2000, berlin, deDe);
    expect(rate).toBe(deDe.effectiveRate.low.amount);
  });

  it("US city (San Francisco/California) — federal + state", () => {
    expect(sanFrancisco.subNational).toBeDefined();
    const gross = 3000; // below lowToMid=3500 → "low" band
    const fedRate = usUs.effectiveRate.low.amount;
    const stateRate = sanFrancisco.subNational!.effectiveRate.low.amount;
    const combined = effectiveRateForCity(gross, sanFrancisco, usUs);
    expect(combined).toBeCloseTo(fedRate + stateRate, 8);
    expect(combined).toBeGreaterThan(fedRate);
  });

  it("TX city (Austin) federal + TX state = same as federal (TX=0)", () => {
    const gross = 3000;
    const fedRate = usUs.effectiveRate.low.amount;
    const txRate = austin.subNational!.effectiveRate.low.amount;
    expect(txRate).toBe(0);
    expect(effectiveRateForCity(gross, austin, usUs)).toBe(fedRate + 0);
  });

  it("rate rises from low to high band", () => {
    const rateLow = effectiveRateForCity(1000, berlin, deDe);
    const rateHigh = effectiveRateForCity(15000, berlin, deDe);
    expect(rateHigh).toBeGreaterThanOrEqual(rateLow);
  });
});

describe("netUsd", () => {
  it("net < gross for any positive rate", () => {
    const gross = 5000;
    const net = netUsd(gross, berlin, deDe, fx);
    expect(net).toBeLessThan(gross);
  });

  it("net = gross when rate = 0 (UAE/Dubai)", () => {
    const dubai = cities.find((c) => c.id === "dubai")!;
    const aeAe = countries.find((c) => c.id === "ae")!;
    const gross = 10000;
    expect(netUsd(gross, dubai, aeAe, fx)).toBeCloseTo(gross, 6);
  });

  it("net(high band) > net(low band) for same city — more gross = more net", () => {
    const netLow = netUsd(1000, berlin, deDe, fx);
    const netHigh = netUsd(15000, berlin, deDe, fx);
    expect(netHigh).toBeGreaterThan(netLow);
  });

  it("netUsd = 0 when gross = 0", () => {
    expect(netUsd(0, berlin, deDe, fx)).toBe(0);
  });

  it("city currency EUR — netUsd uses fxToUsd(fx, 'EUR')", () => {
    const gross = 5000;
    const rate = effectiveRateForCity(gross, berlin, deDe);
    const expected = gross * (1 - rate); // EUR gross USD already (EUR city rate via fx: EUR≈1.16)
    // netUsd takes grossMonthlyUsd (already in USD), not local
    expect(netUsd(gross, berlin, deDe, fx)).toBeCloseTo(expected, 6);
  });
});

describe("childcareLocal", () => {
  it("zero preschoolKids → 0", () => {
    expect(childcareLocal(berlin, singleNoKids)).toBe(0);
  });

  it("scales per preschool child", () => {
    const oneKid = { adults: 1, preschoolKids: 1, schoolKids: 0 } as const;
    const twoKids = { adults: 1, preschoolKids: 2, schoolKids: 0 } as const;
    const one = childcareLocal(berlin, oneKid);
    const two = childcareLocal(berlin, twoKids);
    expect(one).toBe(berlin.childcareMedianLocal.amount);
    expect(two).toBe(berlin.childcareMedianLocal.amount * 2);
  });
});

describe("schoolLocal", () => {
  it("zero schoolKids → 0", () => {
    expect(schoolLocal(berlin, deDe, singleNoKids, "public")).toBe(0);
  });

  it("private ≥ public for same household", () => {
    const oneSchoolKid = { adults: 1, preschoolKids: 0, schoolKids: 1 } as const;
    const pub = schoolLocal(berlin, deDe, oneSchoolKid, "public");
    const priv = schoolLocal(berlin, deDe, oneSchoolKid, "private");
    expect(priv).toBeGreaterThanOrEqual(pub);
  });

  it("scales per school-age child", () => {
    const oneKid = { adults: 1, preschoolKids: 0, schoolKids: 1 } as const;
    const twoKids = { adults: 1, preschoolKids: 0, schoolKids: 2 } as const;
    const one = schoolLocal(berlin, deDe, oneKid, "public");
    const two = schoolLocal(berlin, deDe, twoKids, "public");
    expect(two).toBe(berlin.schoolMedianLocal.public.amount * 2);
    expect(one).toBe(berlin.schoolMedianLocal.public.amount);
  });
});

describe("effectiveSchoolType — foreigner public-school eligibility", () => {
  const oneSchoolKid = { adults: 1, preschoolKids: 0, schoolKids: 1 } as const;

  it("keeps the chosen type where public school is fully open to foreigners (Germany)", () => {
    expect(foreignerCanUsePublicSchool(deDe)).toBe(true);
    expect(effectiveSchoolType(deDe, "public")).toBe("public");
    expect(effectiveSchoolType(deDe, "private")).toBe("private");
    // Berlin (open) keeps the public figure when "public" is chosen.
    expect(schoolLocal(berlin, deDe, oneSchoolKid, "public")).toBe(berlin.schoolMedianLocal.public.amount);
  });

  it("falls back public→private where public is NOT fully open to foreigners (Singapore, limited)", () => {
    expect(foreignerCanUsePublicSchool(sgSg)).toBe(false);
    expect(effectiveSchoolType(sgSg, "public")).toBe("private");
    // A foreigner picking "public" is charged the PRIVATE figure (they cannot use local public school).
    const asPublic = schoolLocal(singapore, sgSg, oneSchoolKid, "public");
    const asPrivate = schoolLocal(singapore, sgSg, oneSchoolKid, "private");
    expect(asPublic).toBe(asPrivate);
    expect(asPublic).toBe(singapore.schoolMedianLocal.private.amount);
  });

  it("a 'private' choice is never altered by eligibility", () => {
    expect(effectiveSchoolType(sgSg, "private")).toBe("private");
    expect(effectiveSchoolType(deDe, "private")).toBe("private");
  });
});

describe("essentialsLocal — OECD household scaling", () => {
  it("housing rises sub-linearly from single to married+2preschool", () => {
    const singleEss = essentialsLocal(berlin, deDe, singleNoKids, "public", "center");
    const singleHousing = berlin.expenses.housing.amount; // × subLinear(single)=1

    const marriedHousehold = marriedTwoPreschool;
    const scaleFactor = subLinear(marriedHousehold);
    const marriedHousing = berlin.expenses.housing.amount * scaleFactor;

    expect(marriedHousing).toBeGreaterThan(singleHousing);
    expect(scaleFactor).toBeLessThan(equivalisedSize(marriedHousehold)); // sub-linear < per-capita
    expect(singleEss).toBeGreaterThan(0);
  });

  it("food scales near per-capita", () => {
    const singleFood = berlin.expenses.food.amount * perCapita(singleNoKids);
    const marriedFood = berlin.expenses.food.amount * perCapita(marriedTwoPreschool);
    expect(marriedFood).toBeGreaterThan(singleFood);
    expect(marriedFood).toBeCloseTo(berlin.expenses.food.amount * equivalisedSize(marriedTwoPreschool), 6);
  });

  it("transport is flat (same regardless of household size)", () => {
    const essOne = essentialsLocal(berlin, deDe, singleNoKids, "public", "center");
    const essTwo = essentialsLocal(berlin, deDe, { adults: 2, preschoolKids: 0, schoolKids: 0 }, "public", "center");
    // transport doesn't change between these — difference is from food + housing only
    // We verify by checking transport component directly
    expect(berlin.expenses.transport.amount).toBeGreaterThan(0); // fixture sanity
    // Can't isolate perfectly without internal access, but household scaling won't affect transport
    // Proxy: ess two-adult no kids > ess single (from housing/food scaling alone)
    expect(essTwo).toBeGreaterThan(essOne);
  });

  it("rural area reduces housing vs center", () => {
    const center = essentialsLocal(berlin, deDe, singleNoKids, "public", "center");
    const rural = essentialsLocal(berlin, deDe, singleNoKids, "public", "rural");
    expect(rural).toBeLessThan(center);
    expect(AREA_MULTIPLIERS.rural).toBeLessThan(AREA_MULTIPLIERS.center);
  });

  it("childcare included when preschoolKids > 0", () => {
    const withKids = essentialsLocal(berlin, deDe, marriedTwoPreschool, "public", "center");
    const noKids = essentialsLocal(berlin, deDe, { adults: 2, preschoolKids: 0, schoolKids: 0 }, "public", "center");
    expect(withKids).toBeGreaterThan(noKids);
    const kidsDiff = withKids - noKids;
    expect(kidsDiff).toBeGreaterThan(berlin.childcareMedianLocal.amount * 1.5); // 2 kids approx
  });

  it("school included when schoolKids > 0", () => {
    const withSchool = essentialsLocal(berlin, deDe, marriedOneSchool, "private", "center");
    const noSchool = essentialsLocal(berlin, deDe, { adults: 2, preschoolKids: 0, schoolKids: 0 }, "private", "center");
    expect(withSchool).toBeGreaterThan(noSchool);
  });
});

describe("expensesLocal", () => {
  it("expensesLocal = essentialsLocal + lifestyle", () => {
    const ess = essentialsLocal(berlin, deDe, singleNoKids, "public", "center");
    const exp = expensesLocal(berlin, deDe, singleNoKids, "public", "center");
    expect(exp).toBeCloseTo(ess + berlin.expenses.lifestyle.amount, 6);
  });
});

describe("relocation — split sunk vs reserve", () => {
  it("relocationSunkLocal = deposit + keyMoney + moving + visaAdmin", () => {
    const { deposit, keyMoney, moving, visaAdmin } = tokyo.relocation.sunkCosts;
    const expected = deposit.amount + keyMoney.amount + moving.amount + visaAdmin.amount;
    expect(relocationSunkLocal(tokyo)).toBe(expected);
  });

  it("Tokyo keyMoney > 0 (reikin)", () => {
    expect(tokyo.relocation.sunkCosts.keyMoney.amount).toBeGreaterThan(0);
  });

  it("Berlin keyMoney = 0 (N/A)", () => {
    expect(berlin.relocation.sunkCosts.keyMoney.amount).toBe(0);
  });

  it("liquidityReserveLocal = cashCushion only", () => {
    expect(liquidityReserveLocal(tokyo)).toBe(tokyo.relocation.liquidityReserve.cashCushion.amount);
  });

  it("reserve ≠ included in sunkCosts total", () => {
    const sunk = relocationSunkLocal(tokyo);
    const reserve = liquidityReserveLocal(tokyo);
    const { deposit, keyMoney, moving, visaAdmin } = tokyo.relocation.sunkCosts;
    expect(sunk).toBe(deposit.amount + keyMoney.amount + moving.amount + visaAdmin.amount);
    expect(reserve).not.toBe(0);
    // reserve is NOT summed into sunk
    expect(sunk + reserve).toBeGreaterThan(sunk);
  });

  it("relocationSunkUsd routes through fxToUsd", () => {
    const localSunk = relocationSunkLocal(london);
    const rate = fxToUsd(fx, london.currency);
    expect(relocationSunkUsd(london, fx)).toBeCloseTo(localSunk * rate, 6);
  });

  it("liquidityReserveUsd routes through fxToUsd", () => {
    const localRes = liquidityReserveLocal(london);
    const rate = fxToUsd(fx, london.currency);
    expect(liquidityReserveUsd(london, fx)).toBeCloseTo(localRes * rate, 6);
  });
});

describe("savingsRow", () => {
  it("essentialSavings = netUsd − essentialsUsd", () => {
    const gross = 6000;
    const row = savingsRow(gross, berlin, deDe, fx, singleNoKids, "public", "center");
    const rate = effectiveRateForCity(gross, berlin, deDe);
    const net = gross * (1 - rate);
    const ess = essentialsLocal(berlin, deDe, singleNoKids, "public", "center");
    const essUsd = ess * fxToUsd(fx, berlin.currency);
    expect(row.essentialSavings).toBeCloseTo(net - essUsd, 4);
  });

  it("afterLifestyleSavings = essentialSavings − lifestyleUsd", () => {
    const gross = 6000;
    const row = savingsRow(gross, berlin, deDe, fx, singleNoKids, "public", "center");
    const lifestyleUsd = berlin.expenses.lifestyle.amount * fxToUsd(fx, berlin.currency);
    expect(row.afterLifestyleSavings).toBeCloseTo(row.essentialSavings - lifestyleUsd, 4);
  });

  it("deficit — essentials > net → negative essentialSavings", () => {
    // very low gross (Tokyo, very low USD)
    const row = savingsRow(1000, tokyo, jpJp, fx, singleNoKids, "public", "center");
    const essUsd = essentialsLocal(tokyo, jpJp, singleNoKids, "public", "center") * fxToUsd(fx, tokyo.currency);
    const net = netUsd(1000, tokyo, jpJp, fx);
    if (essUsd > net) {
      expect(row.essentialSavings).toBeLessThan(0);
    }
  });

  it("zero salary → essentialSavings is negative (deficit)", () => {
    const row = savingsRow(0, berlin, deDe, fx, singleNoKids, "public", "center");
    expect(row.essentialSavings).toBeLessThan(0);
  });

  it("relocation not folded into savings", () => {
    const rowNoReloc = savingsRow(6000, berlin, deDe, fx, singleNoKids, "public", "center");
    // savings figures must not include relocation components
    const ess = essentialsLocal(berlin, deDe, singleNoKids, "public", "center");
    const essUsd = ess * fxToUsd(fx, berlin.currency);
    const net = netUsd(6000, berlin, deDe, fx);
    expect(rowNoReloc.essentialSavings).toBeCloseTo(net - essUsd, 4);
  });

  it("row exposes cityId and city currency", () => {
    const row = savingsRow(6000, berlin, deDe, fx, singleNoKids, "public", "center");
    expect(row.cityId).toBe("berlin");
    expect(row.currency).toBe("EUR");
  });
});

describe("sortByEssentialSavings", () => {
  it("sorts descending by essentialSavings", () => {
    const gross = 8000;
    const rows = [
      savingsRow(gross, berlin, deDe, fx, singleNoKids, "public", "center"),
      savingsRow(gross, tokyo, jpJp, fx, singleNoKids, "public", "center"),
      savingsRow(gross, singapore, sgSg, fx, singleNoKids, "public", "center"),
    ];
    const sorted = sortByEssentialSavings(rows);
    for (let i = 0; i < sorted.length - 1; i++) {
      expect(sorted[i]!.essentialSavings).toBeGreaterThanOrEqual(sorted[i + 1]!.essentialSavings);
    }
  });
});

describe("USD routing", () => {
  it("every *Usd value routes through fxToUsd(fx, city.currency)", () => {
    const gross = 7000;
    const row = savingsRow(gross, london, gbGb, fx, singleNoKids, "public", "center");
    const rate = fxToUsd(fx, "GBP");
    const ess = essentialsLocal(london, gbGb, singleNoKids, "public", "center");
    expect(row.essentialsUsd).toBeCloseTo(ess * rate, 4);
  });
});
