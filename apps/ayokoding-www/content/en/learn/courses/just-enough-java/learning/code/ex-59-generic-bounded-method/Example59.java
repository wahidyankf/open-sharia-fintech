// ex-59 · generic-bounded-method · co-14, co-18
import java.util.List;
public final class Example59 { static <T> T first(List<? extends T> values){ return values.get(0); } public static void main(String[] args){ System.out.println(first(List.of("safe"))); } }

