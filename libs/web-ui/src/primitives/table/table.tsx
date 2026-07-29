import * as React from "react";
import { cn } from "../../utils/cn";

type TableProps = React.ComponentProps<"table"> & {
  /**
   * Extra classes merged onto the `data-slot="table-wrapper"` div (the actual `overflow-x-auto`
   * scroll container), NOT the `<table>` element `className` reaches. A consumer that needs a
   * `position: sticky` element inside the table (e.g. a sticky `<thead>` or sticky first column)
   * to stop being a scroll container at some breakpoint — `overflow-x: auto` forces `overflow-y`
   * to compute to `auto` too (MDN `overflow-x`), making this wrapper a scroll container in BOTH
   * axes, and `position: sticky` resolves against its nearest scroll-container ancestor — needs
   * this prop to override the wrapper's `overflow` (e.g. `wrapperClassName="lg:overflow-visible"`).
   */
  wrapperClassName?: string;
};

function Table({ className, wrapperClassName, ...props }: TableProps) {
  return (
    <div data-slot="table-wrapper" className={cn("relative w-full overflow-x-auto", wrapperClassName)}>
      <table data-slot="table" className={cn("w-full caption-bottom text-sm", className)} {...props} />
    </div>
  );
}

function TableHeader({ className, ...props }: React.ComponentProps<"thead">) {
  return <thead data-slot="table-header" className={cn("[&_tr]:border-b", className)} {...props} />;
}

function TableBody({ className, ...props }: React.ComponentProps<"tbody">) {
  return <tbody data-slot="table-body" className={cn("[&_tr:last-child]:border-0", className)} {...props} />;
}

function TableRow({ className, ...props }: React.ComponentProps<"tr">) {
  return (
    <tr
      data-slot="table-row"
      className={cn("border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted", className)}
      {...props}
    />
  );
}

function TableHead({ className, ...props }: React.ComponentProps<"th">) {
  return (
    <th
      data-slot="table-head"
      className={cn(
        "h-10 px-2 text-left align-middle font-medium whitespace-nowrap text-muted-foreground [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        className,
      )}
      {...props}
    />
  );
}

function TableCell({ className, ...props }: React.ComponentProps<"td">) {
  return (
    <td
      data-slot="table-cell"
      className={cn(
        "p-2 align-middle whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        className,
      )}
      {...props}
    />
  );
}

function TableCaption({ className, ...props }: React.ComponentProps<"caption">) {
  return (
    <caption data-slot="table-caption" className={cn("mt-4 text-sm text-muted-foreground", className)} {...props} />
  );
}

export { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption };
