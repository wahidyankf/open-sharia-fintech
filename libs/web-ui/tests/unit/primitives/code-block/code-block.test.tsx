import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import { axe } from "vitest-axe";
import { describe, it, expect, afterEach, vi } from "vitest";

import { CodeBlock } from "../../../../src/primitives/code-block/code-block";

function stubClipboard(): ReturnType<typeof vi.fn> {
  const writeText = vi.fn(() => Promise.resolve());
  Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
  return writeText;
}

function getWrapper(container: HTMLElement): HTMLElement {
  const wrapper = container.querySelector('[data-slot="code-block"]');
  if (!(wrapper instanceof HTMLElement)) {
    throw new Error("code-block wrapper not found");
  }
  return wrapper;
}

describe("CodeBlock", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  // Cycle 1.10
  it("renders its highlighted children and a copy button inside the wrapper", () => {
    stubClipboard();
    const { container } = render(
      <CodeBlock code="print('hi')">
        <pre data-testid="highlighted">print('hi')</pre>
      </CodeBlock>,
    );

    const wrapper = getWrapper(container);
    expect(screen.getByTestId("highlighted")).toBeTruthy();
    expect(wrapper.querySelector('[data-slot="code-block-copy"]')).not.toBeNull();
  });

  // Cycle 1.11
  it("copies the code prop verbatim, byte-for-byte including every annotation and newline", () => {
    const writeText = stubClipboard();
    // Three-line annotated snippet with trailing comments. Compared against the in-process value
    // handed to writeText (pre-clipboard), per tech-docs.md's Windows \r\n caveat.
    const code = [
      "local ok = pcall(fn)   -- => runs inner fn",
      "error({ code = 42 })   -- => any Lua value",
      "print(err.code)        -- => err IS the table",
    ].join("\n");

    const { container } = render(
      <CodeBlock code={code}>
        <pre>highlighted</pre>
      </CodeBlock>,
    );

    const button = getWrapper(container).querySelector('[data-slot="code-block-copy"]');
    fireEvent.click(button as HTMLElement);

    expect(writeText).toHaveBeenCalledTimes(1);
    expect(writeText).toHaveBeenCalledWith(code);
  });

  // Cycle 1.12
  it("establishes its own positioning context via a relative wrapper carrying data-slot code-block", () => {
    stubClipboard();
    const { container } = render(
      <CodeBlock code="x">
        <pre>x</pre>
      </CodeBlock>,
    );

    const wrapper = getWrapper(container);
    expect(wrapper.getAttribute("data-slot")).toBe("code-block");
    expect(wrapper.className).toContain("relative");
  });

  it("merges a passthrough className onto the wrapper", () => {
    stubClipboard();
    const { container } = render(
      <CodeBlock code="x" className="my-wrapper-class">
        <pre>x</pre>
      </CodeBlock>,
    );
    expect(getWrapper(container).className).toContain("my-wrapper-class");
  });

  it("forwards a localized copyLabel to the copy button", () => {
    stubClipboard();
    render(
      <CodeBlock code="x" copyLabel="Salin" copiedLabel="Tersalin">
        <pre>x</pre>
      </CodeBlock>,
    );
    expect(screen.getByRole("button", { name: "Salin" })).toBeTruthy();
  });

  it("has no accessibility violations", async () => {
    stubClipboard();
    const { container } = render(
      <CodeBlock code="x">
        <pre>x</pre>
      </CodeBlock>,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
