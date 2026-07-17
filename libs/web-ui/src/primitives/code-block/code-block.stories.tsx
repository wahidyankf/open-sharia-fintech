import type { Meta, StoryObj } from "@storybook/nextjs-vite";

import { CodeBlock } from "./code-block";

/** Large reset window so the Copied story holds its success state through a screenshot. */
const NO_REVERT_MS = 3_600_000;

const SAMPLE_CODE = [
  "-- Example 59: error() can raise ANY value, not just a string",
  "local ok, err = pcall(function()   -- => runs inner fn",
  "  error({ code = 42 })             -- => any Lua value",
  "end)",
  "print(err.code)                    -- => err IS the table",
].join("\n");

/**
 * A stand-in for the app's already-highlighted `rehype-pretty-code` figure, styled to resemble the
 * real `github-light` / `github-dark` code ground so the overlaid button's contrast is visible.
 */
function HighlightedFigure() {
  return (
    <figure className="m-0 overflow-x-auto rounded-md bg-[#f6f8fa] p-4 dark:bg-[#24292e]">
      <pre className="m-0 font-mono text-sm text-[#24292e] dark:text-[#e1e4e8]">
        <code>{SAMPLE_CODE}</code>
      </pre>
    </figure>
  );
}

async function clickToCopy(canvasElement: HTMLElement): Promise<void> {
  const button = canvasElement.querySelector("button");
  button?.click();
}

const meta: Meta<typeof CodeBlock> = {
  title: "Primitives/CodeBlock",
  component: CodeBlock,
  tags: ["autodocs"],
  args: {
    code: SAMPLE_CODE,
    copyLabel: "Copy",
    copiedLabel: "Copied",
  },
  decorators: [
    (Story) => (
      <div className="max-w-2xl p-4">
        <Story />
      </div>
    ),
  ],
  render: (args) => (
    <CodeBlock {...args}>
      <HighlightedFigure />
    </CodeBlock>
  ),
};

export default meta;

type Story = StoryObj<typeof CodeBlock>;

export const Default: Story = {};

export const Copied: Story = {
  args: { resetMs: NO_REVERT_MS },
  play: async ({ canvasElement }) => {
    await clickToCopy(canvasElement);
  },
};
