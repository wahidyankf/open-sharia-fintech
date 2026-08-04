suspend fun twice(value: Int): Int {
    return value * 2
}

suspend fun main() {
    println(twice(6))
}
