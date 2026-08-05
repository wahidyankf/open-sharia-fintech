import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:focus_shelf/main.dart';
import 'package:provider/provider.dart';

void main() {
  test('saving an article changes shared model state', () {
    final model = ShelfModel();
    final article = ShelfModel.articles.first;

    expect(model.isSaved(article), isFalse);
    model.toggleSaved(article);
    expect(model.isSaved(article), isTrue);
  });

  testWidgets(
      'narrow detail saves an article and shares the saved state with the list',
      (tester) async {
    tester.view.physicalSize = const Size(600, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => ShelfModel(),
        child: const FocusShelfApp(),
      ),
    );
    await tester.tap(find.byKey(const Key('article-widgets')));
    await tester.pumpAndSettle();

    expect(find.text('Save'), findsOneWidget);
    await tester.tap(find.byKey(const Key('save-widgets')));
    await tester.pump();
    expect(find.text('Saved'), findsOneWidget);

    await tester.pageBack();
    await tester.pumpAndSettle();
    expect(find.byIcon(Icons.star), findsOneWidget);
  });

  testWidgets('missing native hint handler renders the documented fallback',
      (tester) async {
    const channel = MethodChannel('focus_shelf/native_hint');
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      channel,
      (call) async => throw MissingPluginException(),
    );
    addTearDown(() => TestDefaultBinaryMessengerBinding
        .instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, null));

    tester.view.physicalSize = const Size(600, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      ChangeNotifierProvider(
          create: (_) => ShelfModel(), child: const FocusShelfApp()),
    );
    await tester.tap(find.byKey(const Key('article-widgets')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('read-native-hint')));
    await tester.pump();

    expect(find.text('Native hint unavailable on this target'), findsOneWidget);
  });

  testWidgets('wide layout keeps selection in its detail pane', (tester) async {
    tester.view.physicalSize = const Size(900, 800);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      ChangeNotifierProvider(
          create: (_) => ShelfModel(), child: const FocusShelfApp()),
    );
    expect(find.text('Select an article'), findsOneWidget);
    await tester.tap(find.byKey(const Key('article-widgets')));
    await tester.pumpAndSettle();

    expect(find.text('Select an article'), findsNothing);
    expect(find.byKey(const Key('save-widgets')), findsOneWidget);
  });
}
