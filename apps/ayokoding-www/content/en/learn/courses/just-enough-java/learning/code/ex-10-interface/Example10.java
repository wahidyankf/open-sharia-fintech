// ex-10 · interface · co-05
public final class Example10 { interface Named { String name(); default String label(){return "task:" + name();} } static final class Task implements Named { public String name(){return "read";} } public static void main(String[] args){ System.out.println(new Task().label()); } }

