import Foundation
actor TitleCache { private var value: String?; func get() -> String? { value }; func put(_ title: String) { value = title } }
struct TitleResponse: Decodable { let title: String }
struct TitleRepository { let cache: TitleCache; let session: URLSession; func title(from url: URL) async throws -> String { if let cached = await cache.get() { return cached }; let (data, response) = try await session.data(from: url); guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }; let fresh = try JSONDecoder().decode(TitleResponse.self, from: data).title; await cache.put(fresh); return fresh } }
