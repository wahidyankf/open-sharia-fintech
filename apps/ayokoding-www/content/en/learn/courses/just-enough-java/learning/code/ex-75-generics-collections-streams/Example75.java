// ex-75 · generics-collections-streams · co-13, co-15, co-18
import java.util.List;
public final class Example75 { public static void main(String[] args){ var result=List.of(1,2,2,3).stream().filter(value -> value > 1).map(value -> value * 10).distinct().toList(); System.out.println(result); } }

