// ex-15 · enum-switch · co-09, co-11
public final class Example15 { enum Status { TODO, DONE } public static void main(String[] args){ Status status=Status.DONE; String message=switch(status){case TODO -> "open"; case DONE -> "closed";}; System.out.println(message); } }

