import SwiftUI
struct CancellableLoad: View { @State private var status = "Waiting"; var body: some View { Text(status).task { do { try await Task.sleep(for: .seconds(1)); try Task.checkCancellation(); status = "Loaded" } catch is CancellationError { } catch { status = "Failed" } } } }
