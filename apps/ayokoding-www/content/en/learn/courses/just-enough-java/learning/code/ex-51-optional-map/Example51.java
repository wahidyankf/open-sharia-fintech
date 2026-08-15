// ex-51 · optional-map · co-23
import java.util.Optional;
public final class Example51 { public static void main(String[] args){ Optional<String> value=Optional.of("java"); System.out.println(value.map(String::toUpperCase).orElse("missing")); } }

