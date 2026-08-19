//! Renders the platform-binding catalog table from the harness registry.
//!
//! The catalog document is mostly hand-authored prose. This module owns exactly
//! one delimited region inside it — the verification stamp and the Platform
//! Binding Directories table — and rewrites nothing else.
//!
//! # Prettier parity
//!
//! The catalog document is checked by Prettier, which reformats markdown tables
//! to its own padding: every cell padded with spaces to the widest cell in its
//! column, and a separator row of that same width. The emitter reproduces that
//! padding rather than the file being added to `.prettierignore`, because the
//! document is ~300 lines of hand-authored prose that Prettier currently keeps
//! formatted; ignoring the file to accommodate one generated region would
//! unformat all of it.

use std::fmt::Write as _;

use crate::application::repo_config::{CatalogEntry, HarnessEntry};

/// Opening delimiter of the region this emitter owns.
///
/// An HTML comment rather than a markdown construct, so it is invisible in the
/// rendered document and survives Prettier untouched.
pub const REGION_START: &str =
    "<!-- >>> rhino-cli generated: harness catalog - do not edit inside this region -->";

/// Closing delimiter of the generated region.
///
/// **Marker-first hazard**: [`rewrite_region`] looks for THIS marker before it
/// looks for any insertion anchor. An anchor-first implementation finds the
/// anchor on every run and appends a fresh region each time, so the document
/// grows a duplicate table per invocation. The end marker is the only reliable
/// "already applied" signal.
pub const REGION_END: &str = "<!-- <<< rhino-cli generated: harness catalog -->";

/// Remediation sentence shared by catalog drift findings.
pub const CATALOG_REMEDIATION: &str =
    "run `rhino-cli harness catalog generate` to regenerate the catalog region";

/// One table column: its header, and the function reading its cell.
///
/// Pairing the two means a column is added, removed, or reordered by editing
/// exactly one entry of [`COLUMNS`]. The earlier shape kept headers in one array
/// and cell extraction in another, so a column addition had to be made twice in
/// the same order, and a mismatch between them would silently render every cell
/// under the wrong heading.
struct Column {
    /// Header text for this column.
    header: &'static str,
    /// Reads this column's cell out of a catalog entry.
    cell: fn(&CatalogEntry) -> &str,
}

/// Every column, in emitted order. Adding a column is one entry here plus one
/// field on [`CatalogEntry`].
const COLUMNS: &[Column] = &[
    Column {
        header: "Platform",
        cell: |entry| &entry.platform,
    },
    Column {
        header: "Reads root `AGENTS.md` natively?",
        cell: |entry| &entry.reads_agents_md,
    },
    Column {
        header: "Tool-specific instruction surface",
        cell: |entry| &entry.instruction_surface,
    },
    Column {
        header: "Project MCP config",
        cell: |entry| &entry.mcp_config,
    },
    Column {
        header: "Custom-agent surface",
        cell: |entry| &entry.agent_surface,
    },
    Column {
        header: "Skills surface",
        cell: |entry| &entry.skills_surface,
    },
    Column {
        header: "Status",
        cell: |entry| &entry.status,
    },
];

/// Errors this module reports to its callers.
#[derive(Debug)]
pub enum Error {
    /// A registry entry carries no `catalog:` block.
    MissingCatalog {
        /// The harness `name` that lacks one.
        harness: String,
    },
    /// The document does not carry both markers, in order.
    MissingRegion {
        /// Repository-relative document path.
        document: String,
    },
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::MissingCatalog { harness } => write!(
                f,
                "harness {harness:?} has no `catalog:` block in repo-config.yml; \
                 every registry entry must declare one so the table cannot silently omit a harness"
            ),
            Self::MissingRegion { document } => write!(
                f,
                "{document} does not contain the generated-region markers in order; \
                 expected {REGION_START} before {REGION_END}"
            ),
        }
    }
}

impl std::error::Error for Error {}

/// The cells of one table row, in emitted order.
fn row_cells(entry: &CatalogEntry) -> Vec<&str> {
    COLUMNS.iter().map(|column| (column.cell)(entry)).collect()
}

/// Display width of a cell, in the same terms Prettier measures.
///
/// Character count rather than byte count: the catalog carries em dashes and
/// other multi-byte characters that occupy one column each, and byte-length
/// padding would misalign every row containing one.
fn cell_width(cell: &str) -> usize {
    cell.chars().count()
}

/// Renders one markdown table line from already-padded cells.
fn table_line(cells: &[String]) -> String {
    format!("| {} |", cells.join(" | "))
}

/// Pads `cell` to `width` with trailing spaces.
fn pad(cell: &str, width: usize) -> String {
    let mut out = cell.to_owned();
    out.extend(std::iter::repeat_n(
        ' ',
        width.saturating_sub(cell_width(cell)),
    ));
    out
}

/// Per-column width: the widest cell in that column, header included.
fn column_widths(rows: &[Vec<&str>]) -> Vec<usize> {
    let mut widths: Vec<usize> = COLUMNS
        .iter()
        .map(|column| cell_width(column.header))
        .collect();
    for row in rows {
        for (index, cell) in row.iter().enumerate() {
            widths[index] = widths[index].max(cell_width(cell));
        }
    }
    widths
}

/// Renders the markdown table: header, separator, one row per entry.
///
/// # Errors
///
/// Returns [`Error::MissingCatalog`] when any entry lacks a `catalog:` block.
pub fn render_table(harnesses: &[HarnessEntry]) -> Result<String, Error> {
    let mut catalogs = Vec::with_capacity(harnesses.len());
    for harness in harnesses {
        let catalog = harness
            .catalog
            .as_ref()
            .ok_or_else(|| Error::MissingCatalog {
                harness: harness.name.clone(),
            })?;
        catalogs.push(catalog);
    }

    let rows: Vec<Vec<&str>> = catalogs.iter().map(|c| row_cells(c)).collect();
    let widths = column_widths(&rows);

    let mut out = String::new();
    let header: Vec<String> = COLUMNS
        .iter()
        .zip(&widths)
        .map(|(column, width)| pad(column.header, *width))
        .collect();
    let _ = writeln!(out, "{}", table_line(&header));

    let separator: Vec<String> = widths.iter().map(|width| "-".repeat(*width)).collect();
    let _ = writeln!(out, "{}", table_line(&separator));

    for row in &rows {
        let padded: Vec<String> = row
            .iter()
            .zip(&widths)
            .map(|(cell, width)| pad(cell, *width))
            .collect();
        let _ = writeln!(out, "{}", table_line(&padded));
    }
    Ok(out)
}

/// Renders the whole generated region, markers included.
///
/// # Errors
///
/// Propagates [`render_table`]'s error.
pub fn render_region(harnesses: &[HarnessEntry], verified: &str) -> Result<String, Error> {
    let table = render_table(harnesses)?;
    Ok(format!(
        "{REGION_START}\n\n**Verified {verified}.**\n\n{table}\n{REGION_END}"
    ))
}

/// Replaces the region between the markers in `existing`, leaving every byte
/// outside them untouched.
///
/// # Errors
///
/// Returns [`Error::MissingRegion`] when both markers are not present in order.
pub fn rewrite_region(existing: &str, region: &str, document: &str) -> Result<String, Error> {
    let missing = || Error::MissingRegion {
        document: document.to_owned(),
    };
    // Marker-first: the END marker is located before anything else, so a
    // document that already carries a region is rewritten rather than appended
    // to. See the constant's doc comment.
    let end_at = existing.find(REGION_END).ok_or_else(missing)?;
    let start_at = existing.find(REGION_START).ok_or_else(missing)?;
    if start_at >= end_at {
        return Err(missing());
    }
    Ok(format!(
        "{}{region}{}",
        &existing[..start_at],
        &existing[end_at + REGION_END.len()..]
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn entry(name: &str, platform: &str, status: &str) -> HarnessEntry {
        let yaml = format!(
            "name: {name}\n\
             tier: source\n\
             catalog:\n  \
               platform: {platform}\n  \
               reads-agents-md: 'Yes'\n  \
               instruction-surface: '`{name}.md`'\n  \
               mcp-config: '`.mcp.json`'\n  \
               agent-surface: '`.{name}/agents/*.md`'\n  \
               skills-surface: '`.{name}/skills/`'\n  \
               status: {status}\n"
        );
        serde_norway::from_str(&yaml).expect("fixture entry parses")
    }

    #[test]
    fn table_renders_one_row_per_entry() {
        let harnesses = [
            entry("alpha", "Alpha", "Active"),
            entry("beta", "Beta", "Partial"),
        ];
        let table = render_table(&harnesses).expect("renders");
        let data_rows = table
            .lines()
            .filter(|line| line.starts_with('|') && !line.contains("---"))
            .count()
            - 1;
        assert_eq!(data_rows, 2, "table:\n{table}");
    }

    #[test]
    fn every_line_is_padded_to_the_same_width() {
        let harnesses = [
            entry("alpha", "A Very Long Platform Name Indeed", "Active"),
            entry("beta", "B", "Partial"),
        ];
        let table = render_table(&harnesses).expect("renders");
        let widths: Vec<usize> = table.lines().map(|line| line.chars().count()).collect();
        assert!(
            widths.windows(2).all(|pair| pair[0] == pair[1]),
            "ragged table:\n{table}"
        );
    }

    #[test]
    fn an_entry_without_a_catalog_block_is_an_error() {
        let bare: HarnessEntry =
            serde_norway::from_str("name: bare\ntier: source\n").expect("parses");
        let error = render_table(&[bare]).expect_err("must reject");
        assert!(
            matches!(&error, Error::MissingCatalog { harness } if harness == "bare"),
            "got {error:?}"
        );
    }

    #[test]
    fn rewrite_touches_only_the_region() {
        let existing =
            format!("above\n\n{REGION_START}\nstale table\n{REGION_END}\n\nbelow [^mcp]\n");
        let region = format!("{REGION_START}\nfresh\n{REGION_END}");
        let out = rewrite_region(&existing, &region, "doc.md").expect("rewrites");
        assert!(out.starts_with("above\n\n"), "got:\n{out}");
        assert!(out.ends_with("\n\nbelow [^mcp]\n"), "got:\n{out}");
        assert!(!out.contains("stale table"), "got:\n{out}");
    }

    #[test]
    fn rewrite_is_idempotent() {
        let existing = format!("above\n\n{REGION_START}\nstale\n{REGION_END}\n\nbelow\n");
        let region = format!("{REGION_START}\nfresh\n{REGION_END}");
        let once = rewrite_region(&existing, &region, "doc.md").expect("rewrites");
        let twice = rewrite_region(&once, &region, "doc.md").expect("rewrites");
        assert_eq!(once, twice);
        assert_eq!(
            twice.matches(REGION_END).count(),
            1,
            "a second run appended a duplicate region:\n{twice}"
        );
    }

    #[test]
    fn a_document_without_markers_is_an_error() {
        let error = rewrite_region("no markers here", "x", "doc.md").expect_err("must reject");
        assert!(
            matches!(&error, Error::MissingRegion { document } if document == "doc.md"),
            "got {error:?}"
        );
    }
}
