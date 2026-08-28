//! Mermaid flowchart block extractor and parser.

use std::collections::{HashMap, HashSet};
use std::sync::OnceLock;

use regex::Regex;

use super::types::{Direction, Edge, MermaidBlock, Node, ParsedDiagram, Subgraph};

/// Extracts all ` ```mermaid ` / `~~~mermaid` code blocks from `content`.
///
/// Returns one [`MermaidBlock`] per fenced block, in document order.
/// Unclosed blocks at the end of the file are silently ignored.
pub fn extract_blocks(file_path: &str, content: &str) -> Vec<MermaidBlock> {
    let mut blocks = Vec::new();
    let mut in_block = false;
    let mut source_lines: Vec<String> = Vec::new();
    let mut block_index = 0;
    let mut start_line = 0;
    for (i, line) in content.split('\n').enumerate() {
        let trimmed = line.trim();
        if !in_block {
            if line.starts_with("```mermaid") || line.starts_with("~~~mermaid") {
                in_block = true;
                source_lines.clear();
                start_line = i + 1;
            }
        } else if trimmed == "```" || trimmed == "~~~" {
            blocks.push(MermaidBlock {
                file_path: file_path.to_string(),
                block_index,
                source: source_lines.join("\n"),
                start_line,
            });
            block_index += 1;
            in_block = false;
        } else {
            source_lines.push(line.to_string());
        }
    }
    blocks
}

/// Returns the compiled regex that matches a `flowchart` or `graph` header line.
fn flowchart_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"(?m)^\s*(flowchart|graph)(\s+(TB|TD|BT|LR|RL))?\s*$")
            .expect("valid hardcoded regex")
    })
}

/// Returns the compiled regex that matches a `subgraph` header line.
fn subgraph_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r#"^subgraph(?:\s+([^\s\["]+))?(?:\s*\[\s*"?([^"\]]*)"?\s*\])?\s*$"#)
            .expect("valid hardcoded regex")
    })
}

/// Returns the compiled regex that matches Mermaid arrow / edge connectors.
fn arrow_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"-->|---|-\.->|==>|--o|--x|<-->").expect("valid hardcoded regex"))
}

/// Returns the compiled regex that matches edge labels (`-- text -->`).
fn link_text_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"--[^->\n]+?-->").expect("valid hardcoded regex"))
}

/// Returns the compiled regex that matches a pipe-delimited edge label
/// immediately following an arrow (`-->|text|`).
fn pipe_label_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"(-->|---|-\.->|==>|--o|--x|<-->)\s*\|[^|\n]*\|")
            .expect("valid hardcoded regex")
    })
}

/// Returns the compiled regex that matches a bare node identifier (word characters only).
fn node_id_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"^(\w+)$").expect("valid hardcoded regex"))
}

/// Returns compiled regexes for all Mermaid node shape syntaxes, in match-priority order.
///
/// Each regex captures `(id, label)` in groups 1 and 2.
fn node_shape_patterns() -> &'static Vec<Regex> {
    static PATTERNS: OnceLock<Vec<Regex>> = OnceLock::new();
    PATTERNS.get_or_init(|| {
        vec![
            Regex::new(r"^(\w+)\(\(\(([^)]*)\)\)\)").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\(\[([^\]]*)\]\)").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\(\(([^)]*)\)\)").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\[\[([^\]]*)\]\]").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\[\(([^)]*)\)\]").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\(([^)]*)\)").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\{\{([^}]*)\}\}").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\{([^}]*)\}").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)>([^\]]*)\]").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\[/([^/]*)/\]").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\[\\([^\\]*)\\]").expect("valid hardcoded regex"),
            Regex::new(r"^(\w+)\[([^\]]*)\]").expect("valid hardcoded regex"),
            Regex::new(r#"^(\w+)@\{\s*[^}]*label:\s*"([^"]*)"\s*[^}]*\}"#)
                .expect("valid hardcoded regex"),
        ]
    })
}

/// Parses a [`MermaidBlock`] into a [`ParsedDiagram`] and the number of
/// `flowchart` / `graph` headers found in the block.
///
/// A count of `0` means the block is not a flowchart (e.g. a sequence diagram).
/// A count `> 1` indicates multiple diagrams packed into one block, which is a violation.
#[allow(clippy::collapsible_if)]
pub fn parse_diagram(block: MermaidBlock) -> (ParsedDiagram, usize) {
    let matches: Vec<_> = flowchart_re().captures_iter(&block.source).collect();
    let count = matches.len();
    if count == 0 {
        return (
            ParsedDiagram {
                block,
                direction: Direction::TB,
                nodes: Vec::new(),
                edges: Vec::new(),
                subgraphs: Vec::new(),
            },
            0,
        );
    }
    let first = &matches[0];
    let dir = match first.get(3) {
        Some(m) if !m.as_str().trim().is_empty() => Direction::parse(m.as_str().trim()),
        _ => Direction::TB,
    };
    let mut node_map: Vec<(String, String)> = Vec::new();
    let mut node_index: HashMap<String, usize> = HashMap::new();
    let mut edges: Vec<Edge> = Vec::new();
    let mut subgraphs: Vec<Subgraph> = Vec::new();
    let mut stack: Vec<Subgraph> = Vec::new();
    let lines: Vec<&str> = block.source.split('\n').collect();
    for (line_idx, raw) in lines.iter().enumerate() {
        let line = raw.trim();
        if line.is_empty() {
            continue;
        }
        if line.starts_with("subgraph") {
            let (id, label) = parse_subgraph_header(line);
            stack.push(Subgraph {
                id,
                label,
                node_ids: Vec::new(),
                start_line: line_idx + 1,
            });
            continue;
        }
        if line == "end" {
            if let Some(s) = stack.pop() {
                subgraphs.push(s);
            }
            continue;
        }
        if flowchart_re().is_match(line) {
            continue;
        }
        let before: HashSet<String> = node_index.keys().cloned().collect();
        if arrow_re().is_match(line) {
            extract_edge_line(line, &mut node_map, &mut node_index, &mut edges);
        } else {
            extract_standalone_node(line, &mut node_map, &mut node_index);
        }
        let new_ids: Vec<String> = node_index
            .keys()
            .filter(|k| !before.contains(*k))
            .cloned()
            .collect();
        if !new_ids.is_empty() {
            if let Some(top) = stack.last_mut() {
                for id in dedup_order(&new_ids) {
                    if !top.node_ids.contains(&id) {
                        top.node_ids.push(id);
                    }
                }
            }
        }
    }
    while let Some(s) = stack.pop() {
        subgraphs.push(s);
    }
    let seen_order = collect_node_order(&block.source, &node_index);
    let nodes: Vec<Node> = seen_order
        .into_iter()
        .map(|id| {
            let label = node_map
                .iter()
                .find(|(k, _)| *k == id)
                .map(|(_, v)| v.clone())
                .unwrap_or_default();
            Node { id, label }
        })
        .collect();
    (
        ParsedDiagram {
            block,
            direction: dir,
            nodes,
            edges,
            subgraphs,
        },
        count,
    )
}

/// Extracts `(id, label)` from a `subgraph` header line.
///
/// Falls back to an empty id and the trimmed remainder as label when the regex
/// does not match.
fn parse_subgraph_header(line: &str) -> (String, String) {
    if let Some(m) = subgraph_re().captures(line) {
        let id = m.get(1).map(|s| s.as_str().to_string()).unwrap_or_default();
        let label = m.get(2).map(|s| s.as_str().to_string()).unwrap_or_default();
        return (id, label);
    }
    let rest = line.trim_start_matches("subgraph").trim();
    let rest = rest.trim_matches('"');
    (String::new(), rest.to_string())
}

/// Returns `ids` with duplicates removed, preserving first-occurrence order.
fn dedup_order(ids: &[String]) -> Vec<String> {
    let mut seen: HashSet<String> = HashSet::new();
    let mut out = Vec::new();
    for id in ids {
        if seen.insert(id.clone()) {
            out.push(id.clone());
        }
    }
    out
}

/// Collects node identifiers from `source` in the order they first appear,
/// filtered to only those present in `node_map`.
fn collect_node_order(source: &str, node_map: &HashMap<String, usize>) -> Vec<String> {
    let mut seen: HashSet<String> = HashSet::new();
    let mut order = Vec::new();
    for raw in source.split('\n') {
        let line = raw.trim();
        if line.is_empty() || line.starts_with("subgraph") || line == "end" {
            continue;
        }
        if flowchart_re().is_match(line) {
            continue;
        }
        for id in extract_all_node_ids(line) {
            if node_map.contains_key(&id) && seen.insert(id.clone()) {
                order.push(id);
            }
        }
    }
    // Sorted, not raw `node_map.keys()` order — this fallback only fires
    // for node ids the line-by-line source scan above didn't already
    // capture, and `std::collections::HashMap`'s randomized per-process
    // iteration order made that leftover order nondeterministic across
    // runs of the same binary, breaking shadow-diff byte-identity (Wave D
    // integration, rewrite-rhino-cli-to-fsharp) — the same class of bug
    // already fixed in `links.rs`'s `broken_by_category` and
    // `reporter.rs::format_text`'s per-file grouping.
    let mut leftover: Vec<&String> = node_map.keys().collect();
    leftover.sort();
    for k in leftover {
        if seen.insert(k.clone()) {
            order.push(k.clone());
        }
    }
    order
}

/// Extracts all node identifiers mentioned on `line`, handling both edge lines
/// (splitting on arrows) and standalone node lines.
fn extract_all_node_ids(line: &str) -> Vec<String> {
    let mut ids = Vec::new();
    if arrow_re().is_match(line) {
        for seg in arrow_re().split(line) {
            ids.extend(extract_node_ids_from_segment(seg));
        }
    } else {
        ids.extend(extract_node_ids_from_segment(line));
    }
    ids
}

/// Extracts node identifiers from a segment that may contain `&`-separated groups.
fn extract_node_ids_from_segment(seg: &str) -> Vec<String> {
    seg.split('&')
        .filter_map(|sub| {
            let id = extract_node_id_from_segment(sub);
            if id.is_empty() { None } else { Some(id) }
        })
        .collect()
}

/// Extracts the node identifier from a single (non-`&`) segment.
///
/// Returns an empty string when no known shape pattern or bare identifier is recognised.
fn extract_node_id_from_segment(seg: &str) -> String {
    let seg = seg.trim();
    if seg.is_empty() {
        return String::new();
    }
    for re in node_shape_patterns() {
        if let Some(m) = re.captures(seg) {
            return m[1].to_string();
        }
    }
    if let Some(m) = node_id_re().captures(seg) {
        return m[1].to_string();
    }
    String::new()
}

/// Parses a standalone node declaration line (no arrow) and upserts it into `node_map`.
fn extract_standalone_node(
    line: &str,
    node_map: &mut Vec<(String, String)>,
    node_index: &mut HashMap<String, usize>,
) {
    let line = line.trim();
    for re in node_shape_patterns() {
        if let Some(m) = re.captures(line) {
            upsert_node(node_map, node_index, &m[1], normalize_label(&m[2]));
            return;
        }
    }
    if let Some(m) = node_id_re().captures(line) {
        let not_seen = !node_index.contains_key(&m[1]);
        if not_seen {
            upsert_node(node_map, node_index, &m[1], String::new());
        }
    }
}

/// Inserts a new node or updates an existing node's label in `node_map`.
///
/// `node_index` maps identifiers to their position in `node_map`.
fn upsert_node(
    node_map: &mut Vec<(String, String)>,
    node_index: &mut HashMap<String, usize>,
    id: &str,
    label: String,
) {
    if let Some(&idx) = node_index.get(id) {
        node_map[idx].1 = label;
    } else {
        node_index.insert(id.to_string(), node_map.len());
        node_map.push((id.to_string(), label));
    }
}

/// Parses an edge line (containing at least one arrow), upserts all referenced
/// nodes, and appends cartesian-product edges for each `&`-group pair.
fn extract_edge_line(
    line: &str,
    node_map: &mut Vec<(String, String)>,
    node_index: &mut HashMap<String, usize>,
    edges: &mut Vec<Edge>,
) {
    let line = link_text_re().replace_all(line, "-->");
    let line = pipe_label_re().replace_all(&line, "$1");
    let parts: Vec<&str> = arrow_re().split(&line).collect();
    if parts.len() < 2 {
        return;
    }
    let groups: Vec<Vec<String>> = parts
        .iter()
        .filter_map(|p| {
            let ids = extract_node_group(p, node_map, node_index);
            if ids.is_empty() { None } else { Some(ids) }
        })
        .collect();
    for i in 0..groups.len().saturating_sub(1) {
        for from in &groups[i] {
            for to in &groups[i + 1] {
                edges.push(Edge {
                    from: from.clone(),
                    to: to.clone(),
                    label: String::new(),
                });
            }
        }
    }
}

/// Parses one arrow-separated segment (`part`) which may contain `&`-separated
/// node references, upserts each node, and returns the list of identifiers.
fn extract_node_group(
    part: &str,
    node_map: &mut Vec<(String, String)>,
    node_index: &mut HashMap<String, usize>,
) -> Vec<String> {
    part.split('&')
        .filter_map(|seg| {
            let seg = seg.trim();
            if seg.is_empty() {
                return None;
            }
            let id = extract_node_id_and_label(seg, node_map, node_index);
            if id.is_empty() { None } else { Some(id) }
        })
        .collect()
}

/// Extracts a node identifier (and optional label) from `seg`, upserts it, and
/// returns the identifier string.  Returns an empty string when unrecognised.
fn extract_node_id_and_label(
    seg: &str,
    node_map: &mut Vec<(String, String)>,
    node_index: &mut HashMap<String, usize>,
) -> String {
    for re in node_shape_patterns() {
        if let Some(m) = re.captures(seg) {
            upsert_node(node_map, node_index, &m[1], normalize_label(&m[2]));
            return m[1].to_string();
        }
    }
    if let Some(m) = node_id_re().captures(seg) {
        if !node_index.contains_key(&m[1]) {
            upsert_node(node_map, node_index, &m[1], String::new());
        }
        return m[1].to_string();
    }
    String::new()
}

/// Strips surrounding quote characters (`"`, `'`, or `` ` ``) from a label string.
fn normalize_label(s: &str) -> String {
    let s = s.trim();
    if s.len() >= 2 {
        let bytes = s.as_bytes();
        let first = bytes[0];
        let last = bytes[s.len() - 1];
        if (first == b'"' && last == b'"')
            || (first == b'\'' && last == b'\'')
            || (first == b'`' && last == b'`')
        {
            return s[1..s.len() - 1].to_string();
        }
    }
    s.to_string()
}
