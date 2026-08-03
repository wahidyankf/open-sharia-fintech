mixin Labelled {
  String label() => 'available'; // => adds focused reusable display behavior
}

class Item<T> with Labelled {
  const Item(this.code, this.value); // => initializes a generic immutable item

  final String code; // => identifies an item in the inventory
  final T value; // => preserves the stored value's concrete type
}

Future<Item<String>?> findItem(
    Map<String, Item<String>> inventory, String code) async {
  return inventory[code]; // => completes with a typed item or explicit absence
}

Stream<String> availabilityReports(
    Map<String, Item<String>> inventory, List<String> requested) async* {
  for (final code in requested) {
    // => consumes requested codes in input order
    final item = await findItem(
        inventory, code); // => waits for the nullable lookup future
    yield item == null
        ? '$code: unavailable'
        : '${item.value}: ${item.label()}'; // => emits one report line
  }
}
