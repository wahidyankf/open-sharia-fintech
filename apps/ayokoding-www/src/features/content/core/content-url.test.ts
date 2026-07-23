import { describe, expect, it } from "vitest";
import { contentUrl } from "./content-url";

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
});
