// ex-49 · method-reference · co-22
import java.util.List;
public final class Example49 { public static void main(String[] args){ List<String> values=List.of("ada", "linus"); values.stream().map(String::toUpperCase).forEach(System.out::println); } }

