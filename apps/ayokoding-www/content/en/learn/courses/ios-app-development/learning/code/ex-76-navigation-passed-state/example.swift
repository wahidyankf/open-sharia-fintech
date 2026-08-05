import SwiftUI
struct Article: Identifiable, Hashable { let id: UUID; let title: String }
struct SelectionRoute: View { let articles = [Article(id: UUID(), title: "Plan")]; var body: some View { NavigationStack { List(articles) { article in NavigationLink(article.title, value: article) }.navigationDestination(for: Article.self) { article in Text(article.title).navigationTitle("Article") } } } }
