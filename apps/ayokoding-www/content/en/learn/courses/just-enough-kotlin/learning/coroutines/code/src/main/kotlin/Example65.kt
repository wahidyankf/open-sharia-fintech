import kotlinx.coroutines.runBlocking

suspend fun fetch() = "done"

fun main() = runBlocking {
    println(fetch())
}
