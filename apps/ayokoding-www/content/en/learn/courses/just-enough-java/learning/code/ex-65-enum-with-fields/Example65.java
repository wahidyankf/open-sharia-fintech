// ex-65 · enum-with-fields · co-09
public final class Example65 { enum Status { TODO, DONE } public static void main(String[] args){ Status status=Status.DONE; String message=switch(status){case TODO -> "open"; case DONE -> "closed";}; System.out.println(message); } }

