import Observation
import SwiftUI
struct Note: Identifiable { let id = UUID(); let title: String }
@Observable @MainActor final class NoteAdder { var notes = [Note(title: "Plan")]; func add() { notes.append(Note(title: "Review")) } }
struct NoteList: View { @State private var model = NoteAdder(); var body: some View { List(model.notes) { Text($0.title) }.toolbar { Button("Add", action: model.add) } } }
