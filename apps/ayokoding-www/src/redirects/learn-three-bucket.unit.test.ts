import { describe, expect, it } from "vitest";
import { learnThreeBucketRedirects, RELOCATED_DOMAINS } from "./learn-three-bucket";

describe("learnThreeBucketRedirects", () => {
  it("declares exactly 6 rules, one per relocated domain, single tier (DD-48 collapse of DD-42)", () => {
    expect(learnThreeBucketRedirects.length).toBe(6);
  });

  it("every rule is a permanent (308) redirect with non-empty source/destination", () => {
    for (const rule of learnThreeBucketRedirects) {
      expect(rule.permanent).toBe(true);
      expect(rule.source.length).toBeGreaterThan(0);
      expect(rule.destination.length).toBeGreaterThan(0);
    }
  });

  it("each destination equals its source with legacy/ inserted at the bucket position", () => {
    for (const rule of learnThreeBucketRedirects) {
      // source: /en/learn/{domain}/:path*  ->  destination: /en/learn/legacy/{domain}/:path*
      const match = rule.source.match(/^\/en\/learn\/([^/]+)\/:path\*$/);
      expect(match, `source not in expected shape: ${rule.source}`).not.toBeNull();
      const [, domain] = match as RegExpMatchArray;
      expect(rule.destination).toBe(`/en/learn/legacy/${domain}/:path*`);
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
