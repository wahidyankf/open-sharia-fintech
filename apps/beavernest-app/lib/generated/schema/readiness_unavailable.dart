// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: invalid_annotation_target
part of beavernest_api_schema;

// =============================================================================
// CLASS: ReadinessUnavailable
// =============================================================================

/// Safe readiness response when the workspace cannot complete its readiness query.
@freezed
abstract class ReadinessUnavailable with _$ReadinessUnavailable {
  const ReadinessUnavailable._();

  /// Factory constructor for ReadinessUnavailable
  const factory ReadinessUnavailable({
    /// Fixed unavailable readiness status.
    required String status,

    /// Safe unavailable component states without operational detail.
    required ReadinessUnavailableComponents components,
  }) = _ReadinessUnavailable;

  /// Object construction from a JSON representation
  factory ReadinessUnavailable.fromJson(Map<String, dynamic> json) =>
      _$ReadinessUnavailableFromJson(json);

  /// List of all property names of schema
  static const List<String> propertyNames = ['status', 'components'];

  /// Perform validations on the schema property values
  String? validateSchema() {
    return null;
  }

  /// Map representation of object (not serialized)
  Map<String, dynamic> toMap() {
    return {'status': status, 'components': components};
  }
}

// =============================================================================
// CLASS: ReadinessUnavailableComponents
// =============================================================================

/// Safe unavailable component states without operational detail.
@freezed
abstract class ReadinessUnavailableComponents
    with _$ReadinessUnavailableComponents {
  const ReadinessUnavailableComponents._();

  /// Factory constructor for ReadinessUnavailableComponents
  const factory ReadinessUnavailableComponents({
    /// Fixed unavailable database state.
    required String database,

    /// Fixed unknown schema state.
    required String schema,
  }) = _ReadinessUnavailableComponents;

  /// Object construction from a JSON representation
  factory ReadinessUnavailableComponents.fromJson(Map<String, dynamic> json) =>
      _$ReadinessUnavailableComponentsFromJson(json);

  /// List of all property names of schema
  static const List<String> propertyNames = ['database', 'schema'];

  /// Perform validations on the schema property values
  String? validateSchema() {
    return null;
  }

  /// Map representation of object (not serialized)
  Map<String, dynamic> toMap() {
    return {'database': database, 'schema': schema};
  }
}
