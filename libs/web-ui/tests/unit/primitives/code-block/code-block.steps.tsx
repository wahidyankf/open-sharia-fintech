import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import { expect, vi } from "vitest";

import { CodeBlock } from "../../../../src/primitives/code-block/code-block";
import codeBlockStories, {
  Copied as CodeBlockCopiedStory,
  Default as CodeBlockDefaultStory,
} from "../../../../src/primitives/code-block/code-block.stories";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviors/code-block/code-block.feature"),
);

/** Installs a mock `navigator.clipboard.writeText` (jsdom lacks it). Returns the spy. */
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

// The @visual scenario is exercised by the Playwright Storybook baselines, not by this unit-level
// step binder, so it is excluded here.
describeFeature(
  feature,
  ({ Scenario }) => {
    Scenario("The code block renders its highlighted children and a copy button", ({ Given, When, Then, And }) => {
      let childPresent = false;
      let copyButtonPresent = false;

      Given("a CodeBlock rendered with code text and a highlighted <pre> child", () => {
        // mount + inspection happen together in the When step
      });

      When("the component mounts", () => {
        cleanup();
        stubClipboard();
        const { container } = render(
          <CodeBlock code="print('hi')">
            <pre data-testid="highlighted">print(&apos;hi&apos;)</pre>
          </CodeBlock>,
        );
        childPresent = screen.queryByTestId("highlighted") !== null;
        copyButtonPresent = getWrapper(container).querySelector('[data-slot="code-block-copy"]') !== null;
      });

      Then("the highlighted child is present", () => {
        expect(childPresent).toBe(true);
      });

      And("a copy button is present within the code-block wrapper", () => {
        expect(copyButtonPresent).toBe(true);
      });
    });

    Scenario("Copying from the code block yields the verbatim multi-line source", ({ Given, When, Then }) => {
      let writeText: ReturnType<typeof vi.fn>;
      const code = [
        "local ok = pcall(fn)   -- => runs inner fn",
        "error({ code = 42 })   -- => any Lua value",
        "print(err.code)        -- => err IS the table",
      ].join("\n");

      Given("a CodeBlock whose code prop is a three-line annotated snippet with trailing comments", () => {
        // render + click happen together in the When step
      });

      When("the user clicks the code block's copy button", () => {
        cleanup();
        writeText = stubClipboard();
        const { container } = render(
          <CodeBlock code={code}>
            <pre>highlighted</pre>
          </CodeBlock>,
        );
        const button = getWrapper(container).querySelector('[data-slot="code-block-copy"]');
        fireEvent.click(button as HTMLElement);
      });

      Then("the clipboard receives the snippet byte-for-byte including every annotation and newline", () => {
        // Compared against the in-process value handed to writeText (pre-clipboard), per
        // tech-docs.md's Windows \r\n caveat.
        expect(writeText).toHaveBeenCalledWith(code);
      });
    });

    Scenario("The code block establishes its own positioning context", ({ Given, When, Then }) => {
      let dataSlot: string | null = null;
      let className = "";

      Given("a CodeBlock is rendered", () => {
        // render + inspection happen together in the When step
      });

      When("its wrapper is inspected", () => {
        cleanup();
        stubClipboard();
        const { container } = render(
          <CodeBlock code="x">
            <pre>x</pre>
          </CodeBlock>,
        );
        const wrapper = getWrapper(container);
        dataSlot = wrapper.getAttribute("data-slot");
        className = wrapper.className;
      });

      Then('the wrapper is a relatively-positioned element carrying data-slot "code-block"', () => {
        expect(dataSlot).toBe("code-block");
        expect(className).toContain("relative");
      });
    });

    Scenario("The copy button stays pinned outside the code's horizontal-scroll region", ({ Given, When, Then }) => {
      let buttonParentIsWrapper = false;
      let buttonInsidePre = true;

      Given("a CodeBlock rendered with a highlighted <pre> child", () => {
        // render + inspection happen together in the When step
      });

      When("the copy button's position in the DOM is inspected", () => {
        cleanup();
        stubClipboard();
        const { container } = render(
          <CodeBlock code="x">
            <pre data-testid="pre">x</pre>
          </CodeBlock>,
        );
        const wrapper = getWrapper(container);
        const button = wrapper.querySelector('[data-slot="code-block-copy"]');
        const pre = screen.getByTestId("pre");
        buttonParentIsWrapper = button?.parentElement === wrapper;
        buttonInsidePre = pre.contains(button);
      });

      Then("the copy button is a child of the wrapper, not a descendant of the scrolling <pre>", () => {
        // Structural guarantee behind the PRD's rejection of "Option C" (a control inside the
        // overflow-x:auto <pre> would clip/scroll away): the button is a direct child of the
        // positioning wrapper and never lives inside the scrolling <pre>.
        expect(buttonParentIsWrapper).toBe(true);
        expect(buttonInsidePre).toBe(false);
      });
    });

    Scenario(
      "The copy button is discoverable at rest and reveals fully on hover or focus",
      ({ Given, When, Then, And }) => {
        let className = "";

        Given("a CodeBlock is rendered", () => {
          // render + inspection happen together in the When step
        });

        When("the copy button's resting presentation is inspected", () => {
          cleanup();
          stubClipboard();
          const { container } = render(
            <CodeBlock code="x">
              <pre>x</pre>
            </CodeBlock>,
          );
          const button = getWrapper(container).querySelector('[data-slot="code-block-copy"]');
          className = (button as HTMLElement).className;
        });

        Then("the copy button is partially visible at rest rather than fully hidden", () => {
          // jsdom performs no layout, so the resting affordance is asserted through the utility class:
          // `opacity-60` (subtle, discoverable) rather than the old fully-hidden `opacity-0`.
          expect(className).toContain("opacity-60");
          expect(className).not.toContain("opacity-0 ");
        });

        And("it becomes fully visible on hover, focus, and touch", () => {
          expect(className).toContain("group-hover:opacity-100");
          expect(className).toContain("group-focus-within:opacity-100");
          expect(className).toContain("focus-visible:opacity-100");
          expect(className).toContain("[@media(hover:none)]:opacity-100");
        });
      },
    );

    Scenario(
      "The code block reserves scroll-margin so its copy button clears a sticky header",
      ({ Given, When, Then }) => {
        let className = "";

        Given("a CodeBlock is rendered", () => {
          // render + inspection happen together in the When step
        });

        When("the wrapper is inspected", () => {
          cleanup();
          stubClipboard();
          const { container } = render(
            <CodeBlock code="x">
              <pre>x</pre>
            </CodeBlock>,
          );
          className = getWrapper(container).className;
        });

        Then("the wrapper reserves top scroll-margin", () => {
          // `scroll-mt-16` (4rem) keeps the top-right copy button clear of a sticky site header when a
          // block is scrolled/anchored to the viewport top (UWT-002).
          expect(className).toContain("scroll-mt-16");
        });
      },
    );

    // The pixel comparison itself is the Playwright Storybook baseline
    // (`libs/web-ui/e2e/components.visual.ts`), which is not a CI-gated unit target; this
    // `@visual`-tagged binder is skipped at runtime (see `excludeTags` below) and exists so the
    // spec-coverage checker sees the scenario bound. Its bodies smoke-check that the resting +
    // copied stories the baselines capture actually exist, so a story rename can't silently strand
    // the visual cases.
    Scenario("The code block renders correctly in light and dark themes", ({ Given, When, Then }) => {
      Given("the CodeBlock stories are loaded in Storybook", () => {
        expect(codeBlockStories.title).toBe("Primitives/CodeBlock");
      });

      When("the resting and copied stories are captured in light and dark themes", () => {
        // Capture happens in Playwright against the light default and the `&globals=theme:dark`
        // global; here we assert the two captured stories are defined.
        expect(CodeBlockDefaultStory).toBeDefined();
        expect(CodeBlockCopiedStory).toBeDefined();
      });

      Then("each screenshot matches its committed visual baseline", () => {
        // The committed PNG baselines live beside `components.visual.ts`; the byte comparison is a
        // Playwright concern, not a jsdom one.
        expect(codeBlockStories.component).toBe(CodeBlock);
      });
    });
  },
  { excludeTags: ["visual"] },
);
