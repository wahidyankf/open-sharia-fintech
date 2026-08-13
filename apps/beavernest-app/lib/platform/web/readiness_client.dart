import 'dart:convert';

import 'package:beavernest_app/generated/schema/schema.dart';
import 'package:http/http.dart' as http;

/// The browser-relative route exposed by the combined BeaverNest runtime.
final defaultReadinessUri = Uri(path: '/api/v1/readiness');

/// A validated readiness response safe for application code to consume.
sealed class ReadinessResponse {
  const ReadinessResponse();
}

/// The successfully ready response declared by the OpenAPI contract.
final class ReadyReadiness extends ReadinessResponse {
  const ReadyReadiness(this.value);

  final ReadinessReady value;
}

/// The intentionally detail-free unavailable response declared by the contract.
final class UnavailableReadiness extends ReadinessResponse {
  const UnavailableReadiness(this.value);

  final ReadinessUnavailable value;
}

/// Reads readiness through the generated models while enforcing contract gaps
/// that the selected generator does not currently express.
final class ReadinessClient {
  ReadinessClient(this._client, {Uri? readinessUri})
    : _readinessUri = readinessUri ?? defaultReadinessUri {
    if (_readinessUri.isAbsolute || !_readinessUri.path.startsWith('/')) {
      throw ArgumentError.value(
        _readinessUri,
        'readinessUri',
        'must be an absolute-path, same-origin URI',
      );
    }
  }

  final http.Client _client;
  final Uri _readinessUri;

  Future<ReadinessResponse> getReadiness() async {
    final response = await _client.get(
      _readinessUri,
      headers: const {'accept': 'application/json'},
    );
    final body = _decodeObject(response.body);
    return parseReadinessResponse(response.statusCode, body);
  }
}

/// Parses only the two closed readiness response variants from the OpenAPI
/// contract. Generated models are used after these invariants are verified.
ReadinessResponse parseReadinessResponse(int statusCode, Object? payload) {
  final body = _asObject(payload, 'readiness response');
  _requireExactKeys(body, const {'status', 'components'}, 'readiness response');
  final components = _asObject(body['components'], 'readiness components');
  _requireExactKeys(components, const {
    'database',
    'schema',
  }, 'readiness components');

  switch (statusCode) {
    case 200:
      _requireValue(body, 'status', 'ready', 'readiness response');
      _requireValue(components, 'database', 'ready', 'readiness components');
      _requireValue(components, 'schema', 'current', 'readiness components');
      return ReadyReadiness(ReadinessReady.fromJson(body));
    case 503:
      _requireValue(body, 'status', 'not-ready', 'readiness response');
      _requireValue(
        components,
        'database',
        'unavailable',
        'readiness components',
      );
      _requireValue(components, 'schema', 'unknown', 'readiness components');
      return UnavailableReadiness(ReadinessUnavailable.fromJson(body));
    default:
      throw FormatException('Unsupported readiness status code: $statusCode');
  }
}

Map<String, dynamic> _decodeObject(String body) {
  try {
    return _asObject(jsonDecode(body), 'readiness response');
  } on FormatException {
    rethrow;
  } on Object catch (_) {
    throw const FormatException('Readiness response is not valid JSON.');
  }
}

Map<String, dynamic> _asObject(Object? value, String context) {
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

void _requireExactKeys(
  Map<String, dynamic> value,
  Set<String> expected,
  String context,
) {
  if (value.length != expected.length ||
      !value.keys.toSet().containsAll(expected)) {
    throw FormatException(
      '$context must contain exactly ${expected.join(', ')}.',
    );
  }
}

void _requireValue(
  Map<String, dynamic> value,
  String key,
  String expected,
  String context,
) {
  if (value[key] != expected) {
    throw FormatException('$context.$key must equal $expected.');
  }
}
