import kotlinx.coroutines.delay // => suspends without blocking the CLI thread
import kotlinx.coroutines.runBlocking // => bridges the process entry point to suspend code

data class Item(val sku: String, val quantity: Int) // => immutable inventory record

interface Inventory { // => callers depend on a lookup contract
    suspend fun find(sku: String): Item? // => an item may be absent
}

class MapInventory(private val items: Map<String, Item>) : Inventory { // => small concrete implementation
    override suspend fun find(sku: String): Item? { // => fulfills the suspend lookup contract
        delay(1) // => demonstrates a suspension point
        return items[sku] // => nullable map lookup preserves absence
    }
}

fun main() = runBlocking { // => waits until all child work completes before exit
    val inventory: Inventory = MapInventory(mapOf("tea" to Item("tea", 4))) // => interface-typed dependency
    val requested = listOf("tea", "coffee") // => immutable input collection
    val report = requested.map { sku -> // => transforms each requested SKU in order
        val item = inventory.find(sku) // => calls suspending interface method
        item?.let { "${it.sku}: ${it.quantity} available" } ?: "$sku: unavailable" // => null-safe display policy
    }
    report.forEach(::println) // => effectfully prints the completed report
}
