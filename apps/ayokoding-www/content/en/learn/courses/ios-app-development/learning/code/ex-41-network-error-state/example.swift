import Foundation
import Observation
enum LoadState: Equatable { case loading, loaded([String]), failed(String) }
protocol TitlesClient { func fetch() async throws -> [String] }
@Observable @MainActor final class ErrorModel { let client: any TitlesClient; var state: LoadState = .loading; init(client: any TitlesClient) { self.client = client }; func load() async { state = .loading; do { state = .loaded(try await client.fetch()) } catch is URLError { state = .failed("Check your connection") } catch { state = .failed("Try again") } } }
