// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: invalid_annotation_target
part of beavernest_api_schema;

// =============================================================================
// CLASS: ReadinessReady
// =============================================================================

/// Safe readiness response for a workspace with a queryable current database schema.
@freezed
abstract class ReadinessReady with _$ReadinessReady {
  const ReadinessReady._();

  /// Factory constructor for ReadinessReady
  const factory ReadinessReady({
    /// Fixed readiness status.
    required String status,

    /// Safe readiness component states.
    required ReadinessReadyComponents components,
  }) = _ReadinessReady;

  /// Object construction from a JSON representation
  factory ReadinessReady.fromJson(Map<String, dynamic> json) =>
      _$ReadinessReadyFromJson(json);

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
// CLASS: ReadinessReadyComponents
// =============================================================================

/// Safe readiness component states.
@freezed
abstract class ReadinessReadyComponents with _$ReadinessReadyComponents {
  const ReadinessReadyComponents._();

  /// Factory constructor for ReadinessReadyComponents
  const factory ReadinessReadyComponents({
    /// Fixed database readiness state.
    required String database,

    /// Fixed schema readiness state.
    required String schema,
  }) = _ReadinessReadyComponents;

  /// Object construction from a JSON representation
  factory ReadinessReadyComponents.fromJson(Map<String, dynamic> json) =>
      _$ReadinessReadyComponentsFromJson(json);

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
