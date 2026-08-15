// ex-33 · switch-guard · co-11
// Java 25 guard syntax is intentionally shown as a comment so this file remains compilable on JDK 21.
public final class Example33 { public static void main(String[] args){ int radius=2; System.out.println(radius > 0 ? "positive circle" : "other"); } }
// Java 25 form: case Circle(var radius) when radius > 0 -> "positive circle";

