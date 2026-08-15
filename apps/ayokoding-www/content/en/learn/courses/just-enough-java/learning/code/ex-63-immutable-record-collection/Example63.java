// ex-63 · immutable-record-collection · co-07, co-15
import java.util.List;
public final class Example63 { record Task(String name) {} public static void main(String[] args){ List<Task> tasks=List.of(new Task("read")); System.out.println(List.copyOf(tasks)); } }

