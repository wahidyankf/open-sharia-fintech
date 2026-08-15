// ex-50 · optional-basic · co-23
import java.util.Optional;
public final class Example50 { public static void main(String[] args){ Optional<String> value=Optional.of("java"); System.out.println(value.map(String::toUpperCase).orElse("missing")); } }

