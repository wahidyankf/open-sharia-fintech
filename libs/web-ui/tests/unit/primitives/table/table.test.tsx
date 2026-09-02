import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  TableCaption,
} from "../../../../src/primitives/table/table";

describe("Table primitive", () => {
  it("renders a <table> element with role table", () => {
    render(
      <Table>
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(screen.getByRole("table")).toBeTruthy();
  });

  it("renders TableHeader as <thead>", () => {
    const { container } = render(
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Col</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(container.querySelector("thead")).toBeTruthy();
  });

  it("renders TableBody as <tbody>", () => {
    const { container } = render(
      <Table>
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(container.querySelector("tbody")).toBeTruthy();
  });

  it("renders TableRow as <tr>", () => {
    const { container } = render(
      <Table>
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(container.querySelector("tr")).toBeTruthy();
  });

  it("renders TableHead as <th> with columnheader role", () => {
    render(
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>City</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(screen.getByRole("columnheader", { name: "City" })).toBeTruthy();
  });

  it("renders TableCell as <td> with cell role", () => {
    render(
      <Table>
        <TableBody>
          <TableRow>
            <TableCell>Singapore</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(screen.getByRole("cell", { name: "Singapore" })).toBeTruthy();
  });

  it("renders TableCaption as <caption>", () => {
    render(
      <Table>
        <TableCaption>Software-engineering roles</TableCaption>
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(screen.getByText("Software-engineering roles")).toBeTruthy();
  });

  it("accepts className overrides on each sub-component", () => {
    const { container } = render(
      <Table className="custom-table">
        <TableHeader className="custom-header">
          <TableRow className="custom-row">
            <TableHead className="custom-head">H</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody className="custom-body">
          <TableRow>
            <TableCell className="custom-cell">D</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    expect(container.querySelector(".custom-table")).toBeTruthy();
    expect(container.querySelector(".custom-header")).toBeTruthy();
    expect(container.querySelector(".custom-head")).toBeTruthy();
    expect(container.querySelector(".custom-body")).toBeTruthy();
    expect(container.querySelector(".custom-cell")).toBeTruthy();
  });

  // Regression: DWT-003's migration of `model-table.tsx` onto this primitive silently dropped the
  // bespoke table's `lg:overflow-visible` override, disabling `position: sticky` on its `<thead>`
  // at `lg`+ (pr-review-synthesis-maker HIGH finding, PR #122 cycle 1) — `overflow-x-auto` forces
  // `overflow-y` to compute to `auto` too, making the wrapper a scroll container in both axes with
  // no way for a consumer to override it. `wrapperClassName` is the fix.
  it("merges wrapperClassName onto the table-wrapper div, not the <table> element", () => {
    const { container } = render(
      <Table wrapperClassName="lg:overflow-visible" className="custom-table">
        <TableBody>
          <TableRow>
            <TableCell>data</TableCell>
          </TableRow>
        </TableBody>
      </Table>,
    );
    const wrapper = container.querySelector('[data-slot="table-wrapper"]');
    expect(wrapper?.className).toContain("lg:overflow-visible");
    expect(wrapper?.className).toContain("overflow-x-auto");
    expect(wrapper?.className).not.toContain("custom-table");
    expect(container.querySelector("table")?.className).not.toContain("lg:overflow-visible");
  });
});
