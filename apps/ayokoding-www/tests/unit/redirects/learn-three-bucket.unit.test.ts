import { describe, expect, it } from "vitest";
import { learnThreeBucketRedirects, RELOCATED_DOMAINS } from "../../../src/redirects/learn-three-bucket";

describe("learnThreeBucketRedirects", () => {
  it("declares exactly 12 rules, two per relocated domain — an exact bare rule plus a wildcard rule (single-hop fix, EWT-001)", () => {
    expect(learnThreeBucketRedirects.length).toBe(12);
  });

  it("every rule is a permanent (308) redirect with non-empty source/destination", () => {
    for (const rule of learnThreeBucketRedirects) {
      expect(rule.permanent).toBe(true);
      expect(rule.source.length).toBeGreaterThan(0);
      expect(rule.destination.length).toBeGreaterThan(0);
    }
  });

  it("each wildcard rule's destination equals its source with legacy/ inserted at the bucket position", () => {
    const wildcardRules = learnThreeBucketRedirects.filter((r) => r.source.endsWith("/:path*"));
    expect(wildcardRules.length).toBe(RELOCATED_DOMAINS.length);
    for (const rule of wildcardRules) {
      // source: /en/learn/{domain}/:path*  ->  destination: /en/learn/legacy/{domain}/:path*
      const match = rule.source.match(/^\/en\/learn\/([^/]+)\/:path\*$/);
      expect(match, `source not in expected shape: ${rule.source}`).not.toBeNull();
      const [, domain] = match as RegExpMatchArray;
      expect(rule.destination).toBe(`/en/learn/legacy/${domain}/:path*`);
    }
  });

  it("each domain has an exact bare rule with no :path* and no trailing slash, redirecting in a single hop (EWT-001)", () => {
    for (const domain of RELOCATED_DOMAINS) {
      const bareRule = learnThreeBucketRedirects.find((r) => r.source === `/en/learn/${domain}`);
      expect(bareRule, `missing exact bare rule for domain: ${domain}`).toBeDefined();
      expect(bareRule?.source).not.toContain(":path*");
      expect(bareRule?.destination).toBe(`/en/learn/legacy/${domain}`);
      expect(bareRule?.destination.endsWith("/")).toBe(false);
      expect(bareRule?.permanent).toBe(true);
    }
  });

  it("each domain's exact bare rule is ordered before its wildcard rule (first-match-wins single-hop)", () => {
    for (const domain of RELOCATED_DOMAINS) {
      const bareIndex = learnThreeBucketRedirects.findIndex((r) => r.source === `/en/learn/${domain}`);
      const wildcardIndex = learnThreeBucketRedirects.findIndex((r) => r.source === `/en/learn/${domain}/:path*`);
      expect(bareIndex, `bare rule not found for domain: ${domain}`).toBeGreaterThanOrEqual(0);
      expect(wildcardIndex, `wildcard rule not found for domain: ${domain}`).toBeGreaterThanOrEqual(0);
      expect(bareIndex).toBeLessThan(wildcardIndex);
    }
  });

  it("does NOT declare a self-recursing blanket /en/learn/:path* source (DD-42)", () => {
    const blanket = learnThreeBucketRedirects.find((r) => r.source === "/en/learn/:path*");
    expect(blanket).toBeUndefined();
  });

  it("no rule shadows courses, paths, or fundamentally-strong (DD-42/DD-43)", () => {
    const shadowed = learnThreeBucketRedirects.find((r) =>
      /^\/en\/learn\/(courses|paths|fundamentally-strong)\//.test(r.source),
    );
    expect(shadowed).toBeUndefined();
  });

  it("no rule's source or destination contains a /c/ segment (loop-safety invariant, DD-48)", () => {
    for (const rule of learnThreeBucketRedirects) {
      expect(rule.source).not.toContain("/c/");
      expect(rule.destination).not.toContain("/c/");
    }
  });

  it("RELOCATED_DOMAINS names exactly the six expected domains, no more, no fewer", () => {
    expect([...RELOCATED_DOMAINS].sort()).toEqual(
      [
        "software-engineering",
        "artificial-intelligence",
        "information-security",
        "personal-development",
        "it-governance",
        "business",
      ].sort(),
    );
  });
});
