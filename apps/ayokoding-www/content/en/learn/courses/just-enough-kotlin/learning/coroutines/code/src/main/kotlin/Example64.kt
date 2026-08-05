import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch

suspend fun main() = coroutineScope {
    launch { println("child") }
    println("parent")
}
