//! Step-definition matcher — stores compiled step patterns and performs lookups.
//!
//! Port of `stepMatcher` from `apps/rhino-cli/internal/speccoverage/checker.go`.
//! Maintains the canonical `entries` store alongside O(1) `exact_index` lookup
//! and legacy `exact` / `patterns` write-through views consumed by per-language
//! extractors and unit tests.

use std::collections::HashMap;

use regex::Regex;

use super::cucumber_expr::{
    cucumber_expr_to_regex, has_cucumber_expressions, unescape_cucumber_expr,
};
use super::util::normalize_ws;

/// Distinguishes how a step entry was registered.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MatcherKind {
    /// The step was registered as a verbatim (whitespace-normalised) string.
    Exact,
    /// The step was registered as a compiled regex pattern.
    Pattern,
}

/// A single step-definition record stored inside [`StepMatcher`].
#[derive(Debug, Clone)]
pub struct StepMatcherEntry {
    /// How this entry is matched.
    pub kind: MatcherKind,
    /// Whitespace-normalised text used when `kind == Exact`.
    pub exact_text: String,
    /// Raw regex source string used when `kind == Pattern`.
    pub pattern_text: String,
    /// Absolute path of the source file that defines this step.
    /// The reporter resolves it to a repo-relative path before display.
    pub file: String,
}

/// In-memory collection of step definitions extracted from source files.
///
/// Supports two match modes:
/// - **Exact** – O(1) `HashMap` lookup after whitespace normalisation.
/// - **Pattern** – linear scan over compiled [`Regex`] patterns.
///
/// The `entries` field is the canonical store; `exact` and `patterns` are
/// derived write-through views kept for compatibility with the Go original.
#[derive(Debug, Default)]
pub struct StepMatcher {
    /// All registered entries in insertion order.
    pub(crate) entries: Vec<StepMatcherEntry>,
    /// Maps normalised exact text to its index in `entries`.
    pub(crate) exact_index: HashMap<String, usize>,
    /// Legacy derived view — maps normalised exact text to `true`.
    pub(crate) exact: HashMap<String, bool>,
    /// Legacy derived view — compiled regex patterns in insertion order.
    pub(crate) patterns: Vec<Regex>,
}

impl StepMatcher {
    /// Creates an empty `StepMatcher`.
    pub fn new() -> Self {
        Self::default()
    }

    /// Returns `true` if `step_text` matches either an exact entry (O(1)) or
    /// any compiled regex pattern (linear scan).
    ///
    /// Whitespace in `step_text` is normalised before comparison, mirroring
    /// the Go implementation.
    pub fn matches(&self, step_text: &str) -> bool {
        let normalized = normalize_ws(step_text);
        if self.exact.contains_key(&normalized) {
            return true;
        }
        for re in &self.patterns {
            if re.is_match(&normalized) {
                return true;
            }
        }
        false
    }

    /// Registers `text` as an exact-match entry after whitespace normalisation.
    ///
    /// Empty strings (after normalisation) are silently ignored.
    pub fn add_exact_with_origin(&mut self, text: &str, origin_file: &str) {
        let normalized = normalize_ws(text);
        if normalized.is_empty() {
            return;
        }
        let idx = self.entries.len();
        self.entries.push(StepMatcherEntry {
            kind: MatcherKind::Exact,
            exact_text: normalized.clone(),
            pattern_text: String::new(),
            file: origin_file.to_string(),
        });
        self.exact_index.insert(normalized.clone(), idx);
        self.exact.insert(normalized, true);
    }

    /// Registers `re` as a compiled regex pattern entry.
    ///
    /// `pattern_text` is the raw source string stored for display; `re` is the
    /// pre-compiled pattern used for matching.
    pub fn add_pattern_with_origin(&mut self, re: Regex, pattern_text: &str, origin_file: &str) {
        self.entries.push(StepMatcherEntry {
            kind: MatcherKind::Pattern,
            exact_text: String::new(),
            pattern_text: pattern_text.to_string(),
            file: origin_file.to_string(),
        });
        self.patterns.push(re);
    }
}

/// Inserts a step-text string into `sm`, choosing the correct entry kind
/// automatically:
///
/// - Text starting with `^` → compiled as a traditional regex pattern.
/// - Text containing `{...}` → compiled as a Cucumber expression (anchored
///   with `^…$`).
/// - Otherwise → stored as an exact literal after Cucumber escape decoding.
pub fn add_step_to_matcher_with_origin(sm: &mut StepMatcher, text: &str, origin_file: &str) {
    let text = normalize_ws(text);
    if text.is_empty() {
        return;
    }
    if text.starts_with('^') {
        if let Ok(re) = Regex::new(&text) {
            sm.add_pattern_with_origin(re, &text, origin_file);
        }
        return;
    }
    if has_cucumber_expressions(&text) {
        let pattern = format!("^{}$", cucumber_expr_to_regex(&text));
        if let Ok(re) = Regex::new(&pattern) {
            sm.add_pattern_with_origin(re, &text, origin_file);
        }
        return;
    }
    sm.add_exact_with_origin(&unescape_cucumber_expr(&text), origin_file);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_exact_lookup_via_matches() {
        let mut sm = StepMatcher::new();
        sm.add_exact_with_origin("user logs in", "x.rs");
        assert!(sm.matches("user logs in"));
        assert!(sm.matches("user  logs  in")); // ws normalized
        assert!(!sm.matches("user logs out"));
    }

    #[test]
    fn add_pattern_via_cucumber_expression() {
        let mut sm = StepMatcher::new();
        add_step_to_matcher_with_origin(&mut sm, "user enters {string}", "x.rs");
        assert!(sm.matches(r#"user enters "alice""#));
        assert!(!sm.matches("user enters alice"));
    }

    #[test]
    fn add_pattern_via_raw_caret_regex() {
        let mut sm = StepMatcher::new();
        add_step_to_matcher_with_origin(&mut sm, r"^count is (\d+)$", "x.rs");
        assert!(sm.matches("count is 42"));
        assert!(!sm.matches("count is forty-two"));
    }

    #[test]
    fn add_empty_text_is_skipped() {
        let mut sm = StepMatcher::new();
        sm.add_exact_with_origin("", "x.rs");
        assert!(sm.entries.is_empty());
    }
}
