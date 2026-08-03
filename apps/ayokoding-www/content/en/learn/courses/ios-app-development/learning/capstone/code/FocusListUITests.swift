import XCTest

final class FocusListUITests: XCTestCase {
  func testOpenAndSaveArticle() {
    let app = XCUIApplication()
    app.launchArguments = [
      "-useFixtureArticles", "YES",
      "-resetSavedArticles", "YES",
    ]
    app.launch()

    let article = app.staticTexts["article-1"]
    XCTAssertTrue(article.waitForExistence(timeout: 5))
    article.tap()

    XCTAssertTrue(app.staticTexts["detail-title"].waitForExistence(timeout: 5))

    let saveButton = app.buttons["save"]
    XCTAssertTrue(saveButton.waitForExistence(timeout: 5))
    XCTAssertEqual(saveButton.label, "Save")

    saveButton.tap()
    XCTAssertTrue(app.buttons["Unsave"].waitForExistence(timeout: 5))

    app.buttons["Unsave"].tap()
    XCTAssertTrue(app.buttons["Save"].waitForExistence(timeout: 5))
  }
}
