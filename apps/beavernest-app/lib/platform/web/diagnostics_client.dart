import 'dart:convert';

import 'package:beavernest_app/generated/schema/schema.dart';
import 'package:http/http.dart' as http;

/// The browser-relative, same-origin diagnostics route.
final defaultDiagnosticsUri = Uri(path: '/api/v1/diagnostics');

/// A contract-checked diagnostics variant that application code may consume.
sealed class DiagnosticsResponse {
  const DiagnosticsResponse();
}

final class ReadyDiagnostics extends DiagnosticsResponse {
  const ReadyDiagnostics(this.value);
  final DiagnosticsReady value;
}

final class UnavailableDiagnostics extends DiagnosticsResponse {
  const UnavailableDiagnostics(this.value);
  final DiagnosticsUnavailable value;
}

/// Enforces the closed diagnostics contract before constructing generated DTOs.
final class DiagnosticsClient {
  DiagnosticsClient(this._client, {Uri? diagnosticsUri})
    : _diagnosticsUri = diagnosticsUri ?? defaultDiagnosticsUri {
    if (_diagnosticsUri.isAbsolute || !_diagnosticsUri.path.startsWith('/')) {
      throw ArgumentError.value(
        _diagnosticsUri,
        'diagnosticsUri',
        'must be an absolute-path, same-origin URI',
      );
    }
  }

  final http.Client _client;
  final Uri _diagnosticsUri;

  Future<DiagnosticsResponse> getDiagnostics() async {
    final response = await _client.get(
      _diagnosticsUri,
      headers: const {'accept': 'application/json'},
    );
    return parseDiagnosticsResponse(
      response.statusCode,
      _decode(response.body),
    );
  }
}

DiagnosticsResponse parseDiagnosticsResponse(int statusCode, Object? payload) {
  final body = _object(payload, 'diagnostics response');
  final components = _object(body['components'], 'diagnostics components');
  _keys(components, const {'database', 'schema'}, 'diagnostics components');
  switch (statusCode) {
    case 200:
      _keys(body, const {
        'status',
        'version',
        'uptimeSeconds',
        'serverTimeUtc',
        'components',
      }, 'diagnostics response');
      _value(body, 'status', 'ready', 'diagnostics response');
      _value(components, 'database', 'ready', 'diagnostics components');
      _value(components, 'schema', 'current', 'diagnostics components');
      final serverTimeUtc = body['serverTimeUtc'];
      if (body['version'] is! String ||
          (body['version'] as String).isEmpty ||
          body['uptimeSeconds'] is! int ||
          (body['uptimeSeconds'] as int) < 0 ||
          serverTimeUtc is! String ||
          DateTime.tryParse(serverTimeUtc)?.isUtc != true) {
        throw const FormatException(
          'Diagnostics response has invalid safe values.',
        );
      }
      return ReadyDiagnostics(DiagnosticsReady.fromJson(body));
    case 503:
      _keys(body, const {'status', 'components'}, 'diagnostics response');
      _value(body, 'status', 'unavailable', 'diagnostics response');
      _value(components, 'database', 'unavailable', 'diagnostics components');
      _value(components, 'schema', 'unknown', 'diagnostics components');
      return UnavailableDiagnostics(DiagnosticsUnavailable.fromJson(body));
    default:
      throw FormatException('Unsupported diagnostics status code: $statusCode');
  }
}

Map<String, dynamic> _decode(String source) {
  try {
    return _object(jsonDecode(source), 'diagnostics response');
  } on FormatException {
    rethrow;
  } on Object catch (_) {
    throw const FormatException('Diagnostics response is not valid JSON.');
  }
}

Map<String, dynamic> _object(Object? value, String context) {
  if (value is! Map<Object?, Object?>) {
    throw FormatException('$context must be a JSON object.');
  }
  final object = <String, dynamic>{};
  for (final entry in value.entries) {
    if (entry.key is! String) {
      throw FormatException('$context keys must be strings.');
    }
    object[entry.key as String] = entry.value;
  }
  return object;
}

void _keys(Map<String, dynamic> value, Set<String> expected, String context) {
  if (value.length != expected.length ||
      !value.keys.toSet().containsAll(expected)) {
    throw FormatException(
      '$context must contain exactly ${expected.join(', ')}.',
    );
  }
}

void _value(
  Map<String, dynamic> value,
  String key,
  String expected,
  String context,
) {
  if (value[key] != expected) {
    throw FormatException('$context.$key must equal $expected.');
  }
}
