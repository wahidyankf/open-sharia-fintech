import Foundation
struct Project: Codable { struct Owner: Codable { let name: String }; let title: String; let owner: Owner; let tags: [String] }
let data = Data(#"{"title":"Focus","owner":{"name":"Ari"},"tags":["ios","swift"]}"#.utf8)
let project = try JSONDecoder().decode(Project.self, from: data)
print("\(project.owner.name): \(project.title), tags=\(project.tags.count)")
