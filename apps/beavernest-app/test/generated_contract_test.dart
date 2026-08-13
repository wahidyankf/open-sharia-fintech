import 'dart:convert';
import 'dart:io';

import 'package:beavernest_app/api/readiness_client.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;

void main() {
  test('generated client preserves the closed readiness response variants', () {
    for (final model in const ['ReadinessReady', 'ReadinessUnavailable']) {
      final source = File(
        'lib/generated/schema/${_modelFileName(model)}.dart',
      ).readAsStringSync();

      expect(source, contains('abstract class $model'));
    }
  });

  test('parses the declared ready response through the contract adapter', () {
    final response = parseReadinessResponse(200, _readyPayload());

    expect(response, isA<ReadyReadiness>());
  });

  test(
    'parses the declared unavailable response through the contract adapter',
    () {
      final response = parseReadinessResponse(503, _unavailablePayload());

      expect(response, isA<UnavailableReadiness>());
    },
  );

  test(
    'rejects readiness payloads that violate const or closed-object rules',
    () {
      expect(
        () => parseReadinessResponse(200, {
          ..._readyPayload(),
          'unexpected': true,
        }),
        throwsFormatException,
      );
      expect(
        () => parseReadinessResponse(503, {
          ..._unavailablePayload(),
          'status': 'ready',
        }),
        throwsFormatException,
      );
    },
  );

  test('uses the relative same-origin readiness route', () async {
    final client = _RecordingClient(
      http.Response(jsonEncode(_unavailablePayload()), 503),
    );

    expect(defaultReadinessUri, Uri(path: '/api/v1/readiness'));
    expect(defaultReadinessUri.isAbsolute, isFalse);
    expect(
      await ReadinessClient(client).getReadiness(),
      isA<UnavailableReadiness>(),
    );
    expect(client.request?.url, Uri(path: '/api/v1/readiness'));
  });
}

Map<String, Object> _readyPayload() => {
  'status': 'ready',
  'components': {'database': 'ready', 'schema': 'current'},
};

Map<String, Object> _unavailablePayload() => {
  'status': 'not-ready',
  'components': {'database': 'unavailable', 'schema': 'unknown'},
};

String _modelFileName(String model) => model
    .replaceAllMapped(RegExp(r'(?<!^)[A-Z]'), (match) => '_${match[0]}')
    .toLowerCase();

class _RecordingClient extends http.BaseClient {
  _RecordingClient(this._response);

  final http.Response _response;
  http.BaseRequest? request;

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    this.request = request;
    return http.StreamedResponse(
      Stream.value(_response.bodyBytes),
      _response.statusCode,
      headers: _response.headers,
      request: request,
    );
  }
}
