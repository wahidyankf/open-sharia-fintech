// ex-08 · class-methods · co-04
public final class Example08 { static final class Task { final String name; Task(String name){this.name=name;} String label(){return name.toUpperCase();} } public static void main(String[] args){ System.out.println(new Task("read").label()); } }

