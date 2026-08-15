// ex-68 · heap-vs-stack · co-25
public final class Example68 { public static void main(String[] args){ Object value=new Object(); Object alias=value; System.out.println(value == alias); System.out.println(value.equals(alias)); } }

