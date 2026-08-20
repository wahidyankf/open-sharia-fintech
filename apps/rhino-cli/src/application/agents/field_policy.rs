//! Shared field-action types for Claude-agent frontmatter conversion policies.

/// How a Claude frontmatter field should be handled during conversion.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FieldAction {
    /// Copy to target output unchanged.
    Preserve,
    /// Transform the value before writing to target output.
    Translate,
    /// Silently discard the field.
    Drop,
    /// Discard the field and emit a conversion warning.
    DropWarn,
}

/// Per-field conversion policy entry.
pub struct FieldPolicy {
    /// What to do with this field.
    pub action: FieldAction,
    /// Human-readable reason, used in conversion warnings.
    pub reason: &'static str,
}

/// Reason recorded when a frontmatter key has no entry in a harness's policy
/// table at all. Distinct from a table entry's own `reason`, which explains a
/// deliberate drop.
pub const UNKNOWN_FIELD_REASON: &str = "unknown claude code field";

/// A frontmatter field the walk did not carry into the target output, paired
/// with why. Callers wrap these in their own warning type.
#[derive(Debug, Clone)]
pub struct DroppedField {
    /// The Claude frontmatter key that was dropped.
    pub field: String,
    /// Why it was dropped — either the policy entry's reason or
    /// [`UNKNOWN_FIELD_REASON`].
    pub reason: String,
}

/// Walk a Claude agent's parsed frontmatter mapping against `policy`, invoking
/// `apply` for every key the policy carries forward and collecting every key it
/// drops.
///
/// Shared by every harness emitter so one implementation decides what
/// `Preserve` / `Translate` / `Drop` / `DropWarn` mean, and an unknown key
/// warns identically everywhere. `apply` is called only for `Preserve` and
/// `Translate`; interpreting the distinction is the emitter's job, since only
/// it knows its own output shape.
pub fn walk_frontmatter_fields<F, S: std::hash::BuildHasher>(
    mapping: &serde_norway::Mapping,
    policy: &std::collections::HashMap<&'static str, FieldPolicy, S>,
    mut apply: F,
) -> Vec<DroppedField>
where
    F: FnMut(FieldAction, &str, &serde_norway::Value),
{
    let mut dropped = Vec::new();
    for (k, v) in mapping {
        let Some(key) = k.as_str() else { continue };
        let Some(entry) = policy.get(key) else {
            dropped.push(DroppedField {
                field: key.to_string(),
                reason: UNKNOWN_FIELD_REASON.to_string(),
            });
            continue;
        };
        match entry.action {
            FieldAction::Drop => {}
            FieldAction::DropWarn => dropped.push(DroppedField {
                field: key.to_string(),
                reason: entry.reason.to_string(),
            }),
            FieldAction::Preserve | FieldAction::Translate => apply(entry.action, key, v),
        }
    }
    dropped
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    fn policy() -> HashMap<&'static str, FieldPolicy> {
        HashMap::from([
            (
                "keep",
                FieldPolicy {
                    action: FieldAction::Preserve,
                    reason: "",
                },
            ),
            (
                "convert",
                FieldPolicy {
                    action: FieldAction::Translate,
                    reason: "",
                },
            ),
            (
                "silent",
                FieldPolicy {
                    action: FieldAction::Drop,
                    reason: "",
                },
            ),
            (
                "loud",
                FieldPolicy {
                    action: FieldAction::DropWarn,
                    reason: "no target equivalent",
                },
            ),
        ])
    }

    fn mapping(yaml: &str) -> serde_norway::Mapping {
        match serde_norway::from_str::<serde_norway::Value>(yaml).unwrap() {
            serde_norway::Value::Mapping(m) => m,
            other => panic!("not a mapping: {other:?}"),
        }
    }

    #[test]
    fn applies_preserve_and_translate_and_drops_the_rest() {
        let m = mapping("keep: a\nconvert: b\nsilent: c\nloud: d\n");
        let mut applied: Vec<(FieldAction, String)> = Vec::new();
        let dropped = walk_frontmatter_fields(&m, &policy(), |action, key, _| {
            applied.push((action, key.to_string()));
        });

        assert_eq!(
            applied,
            vec![
                (FieldAction::Preserve, "keep".to_string()),
                (FieldAction::Translate, "convert".to_string()),
            ]
        );
        let dropped_fields: Vec<&str> = dropped.iter().map(|d| d.field.as_str()).collect();
        assert_eq!(dropped_fields, vec!["loud"], "Drop must stay silent");
        assert_eq!(dropped[0].reason, "no target equivalent");
    }

    #[test]
    fn an_unknown_key_is_reported_with_the_shared_reason() {
        let m = mapping("mystery: x\n");
        let dropped = walk_frontmatter_fields(&m, &policy(), |_, _, _| {
            panic!("apply must not run for an unknown key");
        });
        assert_eq!(dropped.len(), 1);
        assert_eq!(dropped[0].field, "mystery");
        assert_eq!(dropped[0].reason, UNKNOWN_FIELD_REASON);
    }
}
