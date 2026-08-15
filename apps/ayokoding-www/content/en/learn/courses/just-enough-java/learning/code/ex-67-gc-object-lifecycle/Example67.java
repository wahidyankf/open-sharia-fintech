// ex-67 · gc-object-lifecycle · co-25
public final class Example67 { public static void main(String[] args){ Object value=new Object(); Object alias=value; System.out.println(value == alias); System.out.println(value.equals(alias)); } }

