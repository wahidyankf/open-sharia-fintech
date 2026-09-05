import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("@/features/search/shell/search-dialog", () => ({ SearchDialog: () => null }));

import { SearchProvider } from "../../../../../src/features/search/shell/search-provider";
import { useSearchOpen } from "../../../../../src/features/search/shell/use-search";

function SearchControls() {
  const { setOpen } = useSearchOpen();
  return (
    <>
      <button type="button" onClick={(event) => setOpen(true, event.currentTarget)}>
        Open search
      </button>
      <button type="button" onClick={() => setOpen(false)}>
        Close search
      </button>
    </>
  );
}

afterEach(cleanup);

describe("SearchProvider", () => {
  it("restores focus to the exact external control that opened search", async () => {
    render(
      <SearchProvider>
        <SearchControls />
      </SearchProvider>,
    );
    const opener = screen.getByRole("button", { name: "Open search" });
    fireEvent.click(opener);
    fireEvent.click(screen.getByRole("button", { name: "Close search" }));

    await waitFor(() => expect(document.activeElement).toBe(opener));
  });
});
