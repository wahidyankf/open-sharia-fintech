import Foundation

enum Availability {
    case available(sku: String, quantity: Int)
    case unavailable(sku: String)
}

protocol Inventory {
    func find(_ sku: String) -> Availability
}

struct LocalInventory: Inventory {
    let quantities: [String: Int]

    func find(_ sku: String) -> Availability {
        guard let quantity = quantities[sku] else { return .unavailable(sku: sku) }
        return .available(sku: sku, quantity: quantity)
    }
}

func render(_ availability: Availability) -> String {
    switch availability {
    case let .available(sku, quantity):
        return "\(sku): \(quantity) available"
    case let .unavailable(sku):
        return "\(sku): unavailable"
    }
}

func fetchRequests() async -> [String?] {
    ["tea", nil, "coffee"]
}

let inventory: Inventory = LocalInventory(quantities: ["tea": 4])

Task {
    let requests = await fetchRequests()
    let lines = requests.compactMap { $0 }.map { render(inventory.find($0)) }
    lines.forEach { print($0) }
}

RunLoop.current.run(until: Date().addingTimeInterval(0.01))
