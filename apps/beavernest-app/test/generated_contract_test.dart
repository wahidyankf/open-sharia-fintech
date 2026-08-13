import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  test('generated client preserves the closed readiness response variants', () {
    for (final model in const ['ReadinessReady', 'ReadinessUnavailable']) {
      final source = File(
        'lib/generated/schema/${_modelFileName(model)}.dart',
      ).readAsStringSync();

      expect(source, contains('abstract class $model'));
    }
  });
}

String _modelFileName(String model) => model
    .replaceAllMapped(RegExp(r'(?<!^)[A-Z]'), (match) => '_${match[0]}')
    .toLowerCase();
