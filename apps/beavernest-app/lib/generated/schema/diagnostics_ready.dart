// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: invalid_annotation_target
part of beavernest_api_schema;

// =============================================================================
// CLASS: DiagnosticsReady
// =============================================================================

/// Safe live snapshot for a ready workspace.
@freezed
abstract class DiagnosticsReady with _$DiagnosticsReady {
  const DiagnosticsReady._();

  /// Factory constructor for DiagnosticsReady
  const factory DiagnosticsReady({
    /// No Description
    required String status,

    /// No Description
    required String version,

    /// Whole elapsed seconds since the service process started, rounded down.
    required int uptimeSeconds,

    /// Current UTC server time in RFC 3339 form.
    required String serverTimeUtc,

    /// Fixed named readiness component states for a ready snapshot.
    required DiagnosticsReadyComponents components,
  }) = _DiagnosticsReady;

  /// Object construction from a JSON representation
  factory DiagnosticsReady.fromJson(Map<String, dynamic> json) =>
      _$DiagnosticsReadyFromJson(json);

  /// List of all property names of schema
  static const List<String> propertyNames = [
    'status',
    'version',
    'uptimeSeconds',
    'serverTimeUtc',
    'components',
  ];

  /// Validation constants
  static const versionMinLengthValue = 1;
  static const uptimeSecondsMinValue = 0;

  /// Perform validations on the schema property values
  String? validateSchema() {
    if (version.length < versionMinLengthValue) {
      return "The value of 'version' cannot be < $versionMinLengthValue characters";
    }
    if (uptimeSeconds <= uptimeSecondsMinValue) {
      return "The value of 'uptimeSeconds' cannot be <= $uptimeSecondsMinValue";
    }
    return null;
  }

  /// Map representation of object (not serialized)
  Map<String, dynamic> toMap() {
    return {
      'status': status,
      'version': version,
      'uptimeSeconds': uptimeSeconds,
      'serverTimeUtc': serverTimeUtc,
      'components': components,
    };
  }
}

// =============================================================================
// CLASS: DiagnosticsReadyComponents
// =============================================================================

/// Fixed named readiness component states for a ready snapshot.
@freezed
abstract class DiagnosticsReadyComponents with _$DiagnosticsReadyComponents {
  const DiagnosticsReadyComponents._();

  /// Factory constructor for DiagnosticsReadyComponents
  const factory DiagnosticsReadyComponents({
    /// No Description
    required String database,

    /// No Description
    required String schema,
  }) = _DiagnosticsReadyComponents;

  /// Object construction from a JSON representation
  factory DiagnosticsReadyComponents.fromJson(Map<String, dynamic> json) =>
      _$DiagnosticsReadyComponentsFromJson(json);

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
