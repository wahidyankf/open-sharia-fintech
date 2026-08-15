// ex-39 · map-iterate · co-16
import java.util.Map;
public final class Example39 { public static void main(String[] args){ Map<String,Integer> scores=new java.util.HashMap<>(); scores.computeIfAbsent("Ada", ignored -> 9); scores.forEach((name,score)->System.out.println(name+":"+score)); } }

