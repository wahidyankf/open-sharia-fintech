import type { Meta, StoryObj } from "@storybook/nextjs-vite";

import { CopyButton } from "./copy-button";

/**
 * A very large reset window so the Copied story stays in its success state for the duration of a
 * visual-regression screenshot (it never auto-reverts mid-capture).
 */
const NO_REVERT_MS = 3_600_000;

/** Clicks the rendered button so the story renders in its copied (success) state. */
async function clickToCopy(canvasElement: HTMLElement): Promise<void> {
  const button = canvasElement.querySelector("button");
  button?.click();
}

const meta: Meta<typeof CopyButton> = {
  title: "Primitives/CopyButton",
  component: CopyButton,
  tags: ["autodocs"],
  argTypes: {
    copyLabel: { control: "text" },
    copiedLabel: { control: "text" },
    resetMs: { control: "number" },
  },
  args: {
    value: "npm install @open-sharia-enterprise/web-ui",
    copyLabel: "Copy",
    copiedLabel: "Copied",
  },
  decorators: [
    (Story) => (
      // A neutral card ground so the ghost button's resting/hover tokens are visible in both themes.
      <div className="inline-flex rounded-md border border-border bg-card p-2">
        <Story />
      </div>
    ),
  ],
};

export default meta;

type Story = StoryObj<typeof CopyButton>;

export const Default: Story = {};

export const Copied: Story = {
  args: { resetMs: NO_REVERT_MS },
  play: async ({ canvasElement }) => {
    await clickToCopy(canvasElement);
  },
};

export const Interactive: Story = {
  args: {
    value: "echo hello",
    copyLabel: "Copy",
    copiedLabel: "Copied",
  },
};
