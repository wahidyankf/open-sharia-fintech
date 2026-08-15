// ex-36 · generic-class · co-13
import java.util.List;
public final class Example36 { static <T> T first(List<? extends T> values){ return values.get(0); } public static void main(String[] args){ System.out.println(first(List.of("safe"))); } }

