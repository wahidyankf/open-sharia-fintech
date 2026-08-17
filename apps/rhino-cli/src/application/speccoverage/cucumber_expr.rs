//! Cucumber-expression to regex conversion.

/// Finds the byte range of the next Cucumber parameter placeholder
/// (`{type}`) in `text`, skipping any `{`/`}` immediately preceded by a
/// backslash — Cucumber's escape syntax for a literal brace (e.g.
/// `\{literal\}`), which must not be mistaken for a placeholder.
fn find_next_param(text: &str) -> Option<(usize, usize)> {
    let mut chars = text.char_indices();
    while let Some((i, c)) = chars.next() {
        if c == '\\' {
            chars.next();
            continue;
        }
        if c == '{' {
            while let Some((j, c2)) = chars.next() {
                if c2 == '\\' {
                    chars.next();
                    continue;
                }
                if c2 == '}' {
                    return Some((i, j + c2.len_utf8()));
                }
            }
            return None;
        }
    }
    None
}

/// Decodes Cucumber expression escape sequences in literal text.
///
/// The sequence `\X` becomes `X` for any character `X`, matching the
/// Cucumber specification that allows escaping `\(`, `\)`, `\{`, `\}`,
/// `\/`, and `\\`.
pub fn unescape_cucumber_expr(s: &str) -> String {
    let chars: Vec<char> = s.chars().collect();
    let mut out = String::with_capacity(s.len());
    let mut i = 0usize;
    while i < chars.len() {
        if chars[i] == '\\' && i + 1 < chars.len() {
            out.push(chars[i + 1]);
            i += 2;
        } else {
            out.push(chars[i]);
            i += 1;
        }
    }
    out
}

/// Maps a Cucumber parameter type name to the corresponding regex fragment.
///
/// Known types: `string`, `int`, `byte`, `short`, `long`, `float`, `double`,
/// `bigdecimal`, `word`. Any unrecognised name maps to `.+`.
pub fn cucumber_param_to_regex(param_name: &str) -> &'static str {
    match param_name {
        "string" => "\"[^\"]*\"",
        "int" | "byte" | "short" | "long" => r"-?\d+",
        "float" | "double" | "bigdecimal" => r"-?\d+\.?\d*",
        "word" => r"\S+",
        _ => ".+",
    }
}

/// Converts a full Cucumber expression string into a regex pattern string
/// (without anchors).
///
/// Each `{type}` placeholder is replaced by the regex from
/// [`cucumber_param_to_regex`]. Literal text segments are regex-escaped and
/// Cucumber escape sequences are decoded first.
pub fn cucumber_expr_to_regex(text: &str) -> String {
    let mut sb = String::new();
    let mut remaining = text;
    loop {
        match find_next_param(remaining) {
            None => {
                sb.push_str(&regex::escape(&unescape_cucumber_expr(remaining)));
                break;
            }
            Some((start, end)) => {
                sb.push_str(&regex::escape(&unescape_cucumber_expr(&remaining[..start])));
                let param = &remaining[start..end];
                let inner = &param[1..param.len() - 1];
                sb.push_str(cucumber_param_to_regex(inner));
                remaining = &remaining[end..];
            }
        }
    }
    sb
}

/// Returns `true` if `text` contains at least one Cucumber parameter
/// placeholder (e.g. `{string}`, `{int}`).
pub fn has_cucumber_expressions(text: &str) -> bool {
    find_next_param(text).is_some()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use regex::Regex;

    use super::*;

    #[test]
    fn unescape_basic_escapes() {
        assert_eq!(unescape_cucumber_expr(r"\(foo\)"), "(foo)");
        assert_eq!(unescape_cucumber_expr(r"a\\b"), "a\\b");
        assert_eq!(unescape_cucumber_expr("no escapes"), "no escapes");
    }

    #[test]
    fn cucumber_param_string_maps_to_quoted() {
        assert_eq!(cucumber_param_to_regex("string"), "\"[^\"]*\"");
    }

    #[test]
    fn cucumber_param_int_maps_to_signed_digits() {
        assert_eq!(cucumber_param_to_regex("int"), r"-?\d+");
        assert_eq!(cucumber_param_to_regex("long"), r"-?\d+");
    }

    #[test]
    fn cucumber_param_float_maps_to_signed_decimal() {
        assert_eq!(cucumber_param_to_regex("float"), r"-?\d+\.?\d*");
    }

    #[test]
    fn cucumber_param_word_maps_to_non_whitespace() {
        assert_eq!(cucumber_param_to_regex("word"), r"\S+");
    }

    #[test]
    fn cucumber_param_unknown_maps_to_any() {
        assert_eq!(cucumber_param_to_regex("custom"), ".+");
    }

    #[test]
    fn cucumber_expr_to_regex_string_param() {
        let r = cucumber_expr_to_regex("user enters {string}");
        assert_eq!(r, "user enters \"[^\"]*\"");
    }

    #[test]
    fn cucumber_expr_to_regex_escapes_literals() {
        let r = cucumber_expr_to_regex("a (1.0) b");
        // ( and . are regex specials → must be escaped.
        assert!(r.contains("\\("));
        assert!(r.contains("\\."));
    }

    #[test]
    fn cucumber_expr_to_regex_handles_escape_then_param() {
        // \(foo\) is literal "(foo)", then {int}
        let r = cucumber_expr_to_regex(r"\(foo\) {int}");
        assert!(r.contains(r"\(foo\)") || r.contains("\\(foo\\)"));
        assert!(r.contains(r"-?\d+"));
    }

    #[test]
    fn escaped_braces_are_not_treated_as_a_parameter() {
        // `\{expenseId\}` is Cucumber's escape syntax for a literal
        // `{expenseId}` substring (e.g. a URL path segment the Gherkin
        // author writes out literally) — it must not be mistaken for an
        // unescaped `{type}` parameter placeholder.
        let text = r"GET /expenses/\{expenseId\}";
        assert!(!has_cucumber_expressions(text));
        let re = Regex::new(&format!("^{}$", cucumber_expr_to_regex(text))).unwrap();
        assert!(re.is_match("GET /expenses/{expenseId}"));
    }

    #[test]
    fn unescaped_param_still_detected_alongside_escaped_braces() {
        let text = r"GET /expenses/\{expenseId\} returns {int} results";
        assert!(has_cucumber_expressions(text));
        let re = Regex::new(&format!("^{}$", cucumber_expr_to_regex(text))).unwrap();
        assert!(re.is_match("GET /expenses/{expenseId} returns 5 results"));
    }

    #[test]
    fn has_cucumber_expressions_detects_braces() {
        assert!(has_cucumber_expressions("user enters {string}"));
        assert!(!has_cucumber_expressions("user enters foo"));
    }
}
