// ex-78 · capstone-java-primer · co-07, co-08, co-11, co-18, co-01, co-26
// The executable JUnit 6 test lives in learning/capstone/code; this source demonstrates a testable assertion boundary.
public final class Example78 { static int add(int left,int right){return left+right;} public static void main(String[] args){ if(add(2,3)!=5) throw new AssertionError("expected five"); System.out.println("assertion passed"); } }

