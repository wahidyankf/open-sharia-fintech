// ex-48 · lambda-comparator · co-21
import java.util.List;
public final class Example48 { public static void main(String[] args){ List<String> values=List.of("ada", "linus"); values.stream().map(String::toUpperCase).forEach(System.out::println); } }

