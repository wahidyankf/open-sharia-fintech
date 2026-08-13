// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'schema.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_Health _$HealthFromJson(Map<String, dynamic> json) =>
    _Health(status: json['status'] as String);

Map<String, dynamic> _$HealthToJson(_Health instance) => <String, dynamic>{
  'status': instance.status,
};

_ReadinessReady _$ReadinessReadyFromJson(Map<String, dynamic> json) =>
    _ReadinessReady(
      status: json['status'] as String,
      components: ReadinessReadyComponents.fromJson(
        json['components'] as Map<String, dynamic>,
      ),
    );

Map<String, dynamic> _$ReadinessReadyToJson(_ReadinessReady instance) =>
    <String, dynamic>{
      'status': instance.status,
      'components': instance.components,
    };

_ReadinessReadyComponents _$ReadinessReadyComponentsFromJson(
  Map<String, dynamic> json,
) => _ReadinessReadyComponents(
  database: json['database'] as String,
  schema: json['schema'] as String,
);

Map<String, dynamic> _$ReadinessReadyComponentsToJson(
  _ReadinessReadyComponents instance,
) => <String, dynamic>{
  'database': instance.database,
  'schema': instance.schema,
};

_ReadinessUnavailable _$ReadinessUnavailableFromJson(
  Map<String, dynamic> json,
) => _ReadinessUnavailable(
  status: json['status'] as String,
  components: ReadinessUnavailableComponents.fromJson(
    json['components'] as Map<String, dynamic>,
  ),
);

Map<String, dynamic> _$ReadinessUnavailableToJson(
  _ReadinessUnavailable instance,
) => <String, dynamic>{
  'status': instance.status,
  'components': instance.components,
};

_ReadinessUnavailableComponents _$ReadinessUnavailableComponentsFromJson(
  Map<String, dynamic> json,
) => _ReadinessUnavailableComponents(
  database: json['database'] as String,
  schema: json['schema'] as String,
);

Map<String, dynamic> _$ReadinessUnavailableComponentsToJson(
  _ReadinessUnavailableComponents instance,
) => <String, dynamic>{
  'database': instance.database,
  'schema': instance.schema,
};

_DiagnosticsReady _$DiagnosticsReadyFromJson(Map<String, dynamic> json) =>
    _DiagnosticsReady(
      status: json['status'] as String,
      version: json['version'] as String,
      uptimeSeconds: (json['uptimeSeconds'] as num).toInt(),
      serverTimeUtc: json['serverTimeUtc'] as String,
      components: DiagnosticsReadyComponents.fromJson(
        json['components'] as Map<String, dynamic>,
      ),
    );

Map<String, dynamic> _$DiagnosticsReadyToJson(_DiagnosticsReady instance) =>
    <String, dynamic>{
      'status': instance.status,
      'version': instance.version,
      'uptimeSeconds': instance.uptimeSeconds,
      'serverTimeUtc': instance.serverTimeUtc,
      'components': instance.components,
    };

_DiagnosticsReadyComponents _$DiagnosticsReadyComponentsFromJson(
  Map<String, dynamic> json,
) => _DiagnosticsReadyComponents(
  database: json['database'] as String,
  schema: json['schema'] as String,
);

Map<String, dynamic> _$DiagnosticsReadyComponentsToJson(
  _DiagnosticsReadyComponents instance,
) => <String, dynamic>{
  'database': instance.database,
  'schema': instance.schema,
};

_DiagnosticsUnavailable _$DiagnosticsUnavailableFromJson(
  Map<String, dynamic> json,
) => _DiagnosticsUnavailable(
  status: json['status'] as String,
  components: DiagnosticsUnavailableComponents.fromJson(
    json['components'] as Map<String, dynamic>,
  ),
);

Map<String, dynamic> _$DiagnosticsUnavailableToJson(
  _DiagnosticsUnavailable instance,
) => <String, dynamic>{
  'status': instance.status,
  'components': instance.components,
};

_DiagnosticsUnavailableComponents _$DiagnosticsUnavailableComponentsFromJson(
  Map<String, dynamic> json,
) => _DiagnosticsUnavailableComponents(
  database: json['database'] as String,
  schema: json['schema'] as String,
);

Map<String, dynamic> _$DiagnosticsUnavailableComponentsToJson(
  _DiagnosticsUnavailableComponents instance,
) => <String, dynamic>{
  'database': instance.database,
  'schema': instance.schema,
};

_Error _$ErrorFromJson(Map<String, dynamic> json) =>
    _Error(error: json['error'] as String);

Map<String, dynamic> _$ErrorToJson(_Error instance) => <String, dynamic>{
  'error': instance.error,
};
