import 'package:dart_availability_cli/availability.dart'; // => imports the capstone behavior under test
import 'package:test/test.dart'; // => supplies Dart's package test expectations

void main() {
  test('reports present and absent items in request order', () async {
    final inventory = <String, Item<String>>{
      // => creates a predictable generic fixture
      'dart': const Item('dart', 'Dart'), // => supplies one available item
    };
    final reports = await availabilityReports(inventory, ['dart', 'missing'])
        .toList(); // => fully consumes the stream
    expect(reports, [
      'Dart: available',
      'missing: unavailable'
    ]); // => proves fallback text and event order
  });
}
