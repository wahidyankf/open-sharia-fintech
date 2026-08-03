import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

void main() => runApp(
      ChangeNotifierProvider(
        create: (_) => ShelfModel(),
        child: const FocusShelfApp(),
      ),
    );

class Article {
  const Article(this.id, this.title);

  final String id;
  final String title;
}

class ShelfModel extends ChangeNotifier {
  static const articles = [
    Article('widgets', 'Compose widgets'),
    Article('state', 'Choose a state owner'),
    Article('targets', 'Build for each target'),
  ];

  final Set<String> _savedIds = {};
  Article? selected;

  bool isSaved(Article article) => _savedIds.contains(article.id);

  void select(Article article) {
    selected = article;
    notifyListeners();
  }

  void toggleSaved(Article article) {
    isSaved(article) ? _savedIds.remove(article.id) : _savedIds.add(article.id);
    notifyListeners();
  }
}

class FocusShelfApp extends StatelessWidget {
  const FocusShelfApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Focus Shelf',
        theme: ThemeData(colorSchemeSeed: Colors.teal, useMaterial3: true),
        home: const ShelfScreen(),
      );
}

class ShelfScreen extends StatelessWidget {
  const ShelfScreen({super.key});

  @override
  Widget build(BuildContext context) => LayoutBuilder(
        builder: (context, constraints) {
          final wide = constraints.maxWidth >= 720;
          final list = const ArticleList();
          if (!wide) {
            return Scaffold(
              appBar: AppBar(title: const Text('Focus Shelf')),
              body: list,
            );
          }
          final selected = context.watch<ShelfModel>().selected;
          return Scaffold(
            appBar: AppBar(title: const Text('Focus Shelf')),
            body: Row(
              children: [
                const SizedBox(width: 320, child: ArticleList()),
                const VerticalDivider(width: 1),
                Expanded(
                  child: selected == null
                      ? const Center(child: Text('Select an article'))
                      : ArticleDetail(article: selected),
                ),
              ],
            ),
          );
        },
      );
}

class ArticleList extends StatelessWidget {
  const ArticleList({super.key});

  @override
  Widget build(BuildContext context) {
    final model = context.watch<ShelfModel>();
    return ListView(
      children: [
        for (final article in ShelfModel.articles)
          ListTile(
            key: Key('article-${article.id}'),
            title: Text(article.title),
            trailing: Icon(
              model.isSaved(article) ? Icons.star : Icons.star_border,
              semanticLabel: model.isSaved(article)
                  ? 'Saved ${article.title}'
                  : 'Unsaved ${article.title}',
            ),
            onTap: () {
              model.select(article);
              if (MediaQuery.sizeOf(context).width < 720) {
                Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (_) => ArticleDetail(article: article),
                  ),
                );
              }
            },
          ),
      ],
    );
  }
}

class ArticleDetail extends StatefulWidget {
  const ArticleDetail({required this.article, super.key});

  final Article article;

  @override
  State<ArticleDetail> createState() => _ArticleDetailState();
}

class _ArticleDetailState extends State<ArticleDetail> {
  static const _channel = MethodChannel('focus_shelf/native_hint');
  String _nativeHint = 'Native hint not requested';

  Future<void> _readNativeHint() async {
    try {
      final hint = await _channel.invokeMethod<String>('hint');
      if (mounted)
        setState(() => _nativeHint = hint ?? 'No native hint returned');
    } on MissingPluginException {
      if (mounted)
        setState(() => _nativeHint = 'Native hint unavailable on this target');
    } on PlatformException catch (error) {
      if (mounted)
        setState(() => _nativeHint = 'Native hint failed: ${error.code}');
    }
  }

  @override
  Widget build(BuildContext context) {
    final model = context.watch<ShelfModel>();
    final saved = model.isSaved(widget.article);
    return Scaffold(
      appBar: AppBar(title: Text(widget.article.title)),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.article.title,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 16),
            Text(_nativeHint),
            const Spacer(),
            FilledButton.icon(
              key: Key('save-${widget.article.id}'),
              onPressed: () => model.toggleSaved(widget.article),
              icon: Icon(saved ? Icons.star : Icons.star_border),
              label: Text(saved ? 'Saved' : 'Save'),
            ),
            TextButton(
              key: const Key('read-native-hint'),
              onPressed: _readNativeHint,
              child: const Text('Read native hint'),
            ),
          ],
        ),
      ),
    );
  }
}
