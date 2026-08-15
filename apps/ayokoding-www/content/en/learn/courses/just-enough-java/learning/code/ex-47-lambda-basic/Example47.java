// ex-47 · lambda-basic · co-21
import java.util.List;
public final class Example47 { public static void main(String[] args){ List<String> values=List.of("ada", "linus"); values.stream().map(String::toUpperCase).forEach(System.out::println); } }

