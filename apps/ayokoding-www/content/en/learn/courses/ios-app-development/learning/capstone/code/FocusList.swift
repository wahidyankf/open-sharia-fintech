import Foundation
import Observation
import SwiftData
import SwiftUI

struct Article: Codable, Hashable, Identifiable, Sendable {
  let id: Int
  let title: String
  let body: String
}

protocol ArticleService: Sendable {
  func fetchArticles() async throws -> [Article]
}

struct RemoteArticleService: ArticleService {
  let url: URL

  func fetchArticles() async throws -> [Article] {
    let (data, response) = try await URLSession.shared.data(from: url)

    guard (response as? HTTPURLResponse)?.statusCode == 200 else {
      throw URLError(.badServerResponse)
    }

    return try JSONDecoder().decode([Article].self, from: data)
  }
}

struct FixtureArticleService: ArticleService {
  func fetchArticles() async throws -> [Article] {
    [
      Article(
        id: 1,
        title: "Make a focused plan",
        body: "Choose one important outcome and write the next concrete step."
      ),
    ]
  }
}

actor ArticleCache {
  private var articles: [Article]?

  func read() -> [Article]? {
    articles
  }

  func write(_ articles: [Article]) {
    self.articles = articles
  }
}

enum ScreenState: Equatable, Sendable {
  case loading
  case content([Article])
  case failed(String)
}

@Observable
@MainActor
final class FocusListModel {
  let service: any ArticleService
  let cache: ArticleCache
  private(set) var state: ScreenState = .loading

  init(service: any ArticleService, cache: ArticleCache = ArticleCache()) {
    self.service = service
    self.cache = cache
  }

  func load() async {
    state = .loading

    do {
      if let cached = await cache.read() {
        state = .content(cached)
        return
      }

      let articles = try await service.fetchArticles()
      await cache.write(articles)
      state = .content(articles)
    } catch {
      state = .failed("Could not load articles. Try again.")
    }
  }

  func article(withID id: Article.ID) -> Article? {
    guard case let .content(articles) = state else {
      return nil
    }

    return articles.first { $0.id == id }
  }
}

@Model
final class SavedArticle {
  @Attribute(.unique) var articleID: Int
  var title: String
  var body: String

  init(article: Article) {
    articleID = article.id
    title = article.title
    body = article.body
  }
}

@main
struct FocusListApp: App {
  private let modelContainer: ModelContainer
  private let articleService: any ArticleService

  init() {
    do {
      modelContainer = try ModelContainer(for: SavedArticle.self)

      if UserDefaults.standard.bool(forKey: "resetSavedArticles") {
        try modelContainer.mainContext.delete(model: SavedArticle.self)
        try modelContainer.mainContext.save()
      }
    } catch {
      fatalError("Could not create the Focus List data store: \(error)")
    }

    articleService = UserDefaults.standard.bool(forKey: "useFixtureArticles")
      ? FixtureArticleService()
      : RemoteArticleService(url: URL(string: "https://example.com/focus-list/articles.json")!)
  }

  var body: some Scene {
    WindowGroup {
      FocusListView(service: articleService)
    }
    .modelContainer(modelContainer)
  }
}

struct FocusListView: View {
  @State private var model: FocusListModel

  init(service: any ArticleService) {
    _model = State(initialValue: FocusListModel(service: service))
  }

  var body: some View {
    NavigationStack {
      Group {
        switch model.state {
        case .loading:
          ProgressView("Loading")
            .accessibilityIdentifier("loading")
        case let .failed(message):
          ContentUnavailableView(
            "Unable to load",
            systemImage: "wifi.exclamationmark",
            description: Text(message)
          ) {
            Button("Retry") {
              Task {
                await model.load()
              }
            }
            .accessibilityIdentifier("retry")
          }
        case let .content(articles):
          if articles.isEmpty {
            ContentUnavailableView("No articles", systemImage: "text.page")
          } else {
            List(articles) { article in
              NavigationLink(value: article.id) {
                Text(article.title)
                  .accessibilityIdentifier("article-\(article.id)")
              }
            }
          }
        }
      }
      .navigationTitle("Focus List")
      .navigationDestination(for: Article.ID.self) { articleID in
        if let article = model.article(withID: articleID) {
          ArticleDetail(article: article)
        } else {
          ContentUnavailableView("Article unavailable", systemImage: "exclamationmark.triangle")
        }
      }
      .task {
        await model.load()
      }
    }
  }
}

struct ArticleDetail: View {
  let article: Article

  @Environment(\.modelContext) private var modelContext
  @Query private var savedArticles: [SavedArticle]

  private var savedArticle: SavedArticle? {
    savedArticles.first { $0.articleID == article.id }
  }

  var body: some View {
    VStack(alignment: .leading, spacing: 16) {
      Text(article.title)
        .font(.title)
        .accessibilityIdentifier("detail-title")
      Text(article.body)
      Button(savedArticle == nil ? "Save" : "Unsave") {
        toggleSavedArticle()
      }
      .accessibilityIdentifier("save")
    }
    .padding()
  }

  private func toggleSavedArticle() {
    if let savedArticle {
      modelContext.delete(savedArticle)
    } else {
      modelContext.insert(SavedArticle(article: article))
    }

    do {
      try modelContext.save()
    } catch {
      assertionFailure("Could not save the article: \(error)")
    }
  }
}
