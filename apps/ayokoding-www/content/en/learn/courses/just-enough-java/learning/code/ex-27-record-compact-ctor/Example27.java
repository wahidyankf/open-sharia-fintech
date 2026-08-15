// ex-27 · record-compact-ctor · co-07
public final class Example27 { record Task(String name, int priority) { Task { if(priority<0) throw new IllegalArgumentException("priority"); } } public static void main(String[] args){ System.out.println(new Task("read", 1)); } }

