import XCTest

@testable import FocusList

struct FakeArticleService: ArticleService {
  let result: Result<[Article], any Error>

  func fetchArticles() async throws -> [Article] {
    try result.get()
  }
}

@MainActor
final class FocusListTests: XCTestCase {
  func testLoadUsesDecodedServiceResult() async {
    let article = Article(id: 1, title: "Plan", body: "Write it down")
    let model = FocusListModel(service: FakeArticleService(result: .success([article])))

    await model.load()

    XCTAssertEqual(model.state, .content([article]))
    XCTAssertEqual(model.article(withID: article.id), article)
  }
}
