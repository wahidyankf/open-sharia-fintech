// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: invalid_annotation_target
part of beavernest_api_schema;

// =============================================================================
// CLASS: Health
// =============================================================================

/// Liveness response body.
@freezed
abstract class Health with _$Health {
  const Health._();

  /// Factory constructor for Health
  const factory Health({
    /// Always "ok" when the service is live.
    required String status,
  }) = _Health;

  /// Object construction from a JSON representation
  factory Health.fromJson(Map<String, dynamic> json) => _$HealthFromJson(json);

  /// List of all property names of schema
  static const List<String> propertyNames = ['status'];

  /// Perform validations on the schema property values
  String? validateSchema() {
    return null;
  }

  /// Map representation of object (not serialized)
  Map<String, dynamic> toMap() {
    return {'status': status};
  }
}
