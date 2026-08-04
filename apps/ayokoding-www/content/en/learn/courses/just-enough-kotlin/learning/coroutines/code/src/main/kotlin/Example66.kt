import kotlinx.coroutines.delay

suspend fun main() {
    delay(1)
    println("resumed")
}
