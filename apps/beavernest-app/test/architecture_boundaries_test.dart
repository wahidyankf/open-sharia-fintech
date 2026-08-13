import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  test('keeps framework and generated dependencies outside inner layers', () {
    _expectNoImports('lib/domain', const [
      'package:flutter/',
      'dart:html',
      'dart:js',
      'package:web/',
      '/generated/',
    ]);
    _expectNoImports('lib/application', const [
      'package:flutter/',
      'dart:html',
      'dart:js',
      'package:web/',
      '/generated/',
    ]);
  });

  test('keeps transport details out of presentation', () {
    _expectNoImports('lib/presentation', const [
      'package:http/',
      '/generated/',
    ]);
  });

  test('allows generated contracts only in platform adapters', () {
    for (final file in _dartFilesIn('lib')) {
      if (file.path.contains(
        '${Platform.pathSeparator}platform${Platform.pathSeparator}',
      )) {
        continue;
      }
      expect(
        file.readAsStringSync(),
        isNot(contains('/generated/')),
        reason: '${file.path} must not import generated contracts.',
      );
    }
  });
}

void _expectNoImports(String directoryPath, List<String> forbiddenImports) {
  final directory = Directory(directoryPath);
  expect(directory.existsSync(), isTrue, reason: '$directoryPath must exist.');

  for (final file in _dartFilesIn(directoryPath)) {
    final source = file.readAsStringSync();
    for (final forbiddenImport in forbiddenImports) {
      expect(
        source,
        isNot(contains(forbiddenImport)),
        reason: '${file.path} must not import $forbiddenImport.',
      );
    }
  }
}

Iterable<File> _dartFilesIn(String directoryPath) => Directory(directoryPath)
    .listSync(recursive: true)
    .whereType<File>()
    .where((file) => file.path.endsWith('.dart'));
