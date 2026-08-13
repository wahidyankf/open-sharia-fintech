// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: invalid_annotation_target
part of beavernest_api_schema;

// =============================================================================
// CLASS: Error
// =============================================================================

/// Response body for any unmatched route (404).
@freezed
abstract class Error with _$Error {
  const Error._();

  /// Factory constructor for Error
  const factory Error({
    /// Non-empty human-readable error message.
    required String error,
  }) = _Error;

  /// Object construction from a JSON representation
  factory Error.fromJson(Map<String, dynamic> json) => _$ErrorFromJson(json);

  /// List of all property names of schema
  static const List<String> propertyNames = ['error'];

  /// Perform validations on the schema property values
  String? validateSchema() {
    return null;
  }

  /// Map representation of object (not serialized)
  Map<String, dynamic> toMap() {
    return {'error': error};
  }
}
