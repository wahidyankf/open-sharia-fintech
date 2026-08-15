// ex-64 · record-as-map-key · co-07, co-16
import java.util.Map;
public final class Example64 { public static void main(String[] args){ Map<String,Integer> scores=new java.util.HashMap<>(); scores.computeIfAbsent("Ada", ignored -> 9); scores.forEach((name,score)->System.out.println(name+":"+score)); } }

