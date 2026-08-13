// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: invalid_annotation_target
part of beavernest_api_schema;

// =============================================================================
// CLASS: DiagnosticsUnavailable
// =============================================================================

/// Safe response when the workspace cannot provide a ready snapshot.
@freezed
abstract class DiagnosticsUnavailable with _$DiagnosticsUnavailable {
  const DiagnosticsUnavailable._();

  /// Factory constructor for DiagnosticsUnavailable
  const factory DiagnosticsUnavailable({
    /// No Description
    required String status,

    /// Fixed named readiness component states without an unavailable cause.
    required DiagnosticsUnavailableComponents components,
  }) = _DiagnosticsUnavailable;

  /// Object construction from a JSON representation
  factory DiagnosticsUnavailable.fromJson(Map<String, dynamic> json) =>
      _$DiagnosticsUnavailableFromJson(json);

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
// CLASS: DiagnosticsUnavailableComponents
// =============================================================================

/// Fixed named readiness component states without an unavailable cause.
@freezed
abstract class DiagnosticsUnavailableComponents
    with _$DiagnosticsUnavailableComponents {
  const DiagnosticsUnavailableComponents._();

  /// Factory constructor for DiagnosticsUnavailableComponents
  const factory DiagnosticsUnavailableComponents({
    /// No Description
    required String database,

    /// No Description
    required String schema,
  }) = _DiagnosticsUnavailableComponents;

  /// Object construction from a JSON representation
  factory DiagnosticsUnavailableComponents.fromJson(
    Map<String, dynamic> json,
  ) => _$DiagnosticsUnavailableComponentsFromJson(json);

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
