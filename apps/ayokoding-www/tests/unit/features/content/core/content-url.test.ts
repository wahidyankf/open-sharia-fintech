import { describe, expect, it } from "vitest";
import { contentUrl } from "../../../../../src/features/content/core/content-url";

describe("contentUrl", () => {
  it("uniformly joins en content-tree slugs bare (no /c/, DD-48)", () => {
    expect(contentUrl("en", "learn/software-engineering")).toBe("/en/learn/software-engineering");
  });

  it("uniformly joins id content-tree slugs bare (no /c/, DD-48)", () => {
    expect(contentUrl("id", "belajar/ikhtisar")).toBe("/id/belajar/ikhtisar");
  });

  it("leaves en loose top-level pages bare too — no distinct branch remains", () => {
    expect(contentUrl("en", "about-ayokoding")).toBe("/en/about-ayokoding");
    expect(contentUrl("en", "terms-and-conditions")).toBe("/en/terms-and-conditions");
  });

  it("leaves id loose top-level pages bare too — no distinct branch remains", () => {
    expect(contentUrl("id", "tentang-ayokoding")).toBe("/id/tentang-ayokoding");
    expect(contentUrl("id", "syarat-dan-ketentuan")).toBe("/id/syarat-dan-ketentuan");
  });

  it("maps empty/root slug to the locale root", () => {
    expect(contentUrl("en", "")).toBe("/en");
    expect(contentUrl("id", "")).toBe("/id");
  });

  it("maps the _index slug to the locale root", () => {
    expect(contentUrl("en", "_index")).toBe("/en");
    expect(contentUrl("id", "_index")).toBe("/id");
  });

  it("normalizes leading and trailing slashes on content slugs", () => {
    expect(contentUrl("en", "/learn/software-engineering/")).toBe("/en/learn/software-engineering");
  });

  // Cycle 2.4 (course-paths plan): contentUrl gains an optional third `pathId` param that
  // appends `?path=<path-id>` to whatever URL contentUrl already returns for the first two
  // arguments — additive only, no existing return path changes shape.
  //
  // NOTE: DD-48 ("de-namespacing", ayokoding-learning-path-01-url-restructure, archived
  // 2026-07-23) already removed the `/c/` content-tree segment before this cycle runs — every
  // content-tree URL contentUrl emits today is the bare `/{locale}/{slug}` form asserted by the
  // tests above, not the `/{locale}/c/{slug}` form an earlier draft of this plan's own delivery.md
  // describes. The two assertions below are written against the REAL current shape (re-verified
  // 2026-07-24, matching this plan's own Phase 0 baseline snapshot), not that stale draft text.
  it("appends the path context query param when a third pathId argument is given", () => {
    expect(contentUrl("en", "learn/courses/x", "careers/interview-ready/software-engineer")).toBe(
      "/en/learn/courses/x?path=careers/interview-ready/software-engineer",
    );
  });

  it("characterizes today's shipped no-pathId behaviour unchanged (no third argument)", () => {
    expect(contentUrl("en", "learn/courses/x")).toBe("/en/learn/courses/x");
  });
});
