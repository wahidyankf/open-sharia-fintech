// ex-66 · interface-default-method · co-05
public final class Example66 { enum Priority { LOW(1), HIGH(2); final int score; Priority(int score){this.score=score;} } public static void main(String[] args){ System.out.println(Priority.HIGH.score); } }

