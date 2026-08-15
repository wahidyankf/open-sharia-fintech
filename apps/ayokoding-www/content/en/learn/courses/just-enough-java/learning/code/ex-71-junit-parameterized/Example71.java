// ex-71 · junit-parameterized · co-26
// The executable JUnit 6 test lives in learning/capstone/code; this source demonstrates a testable assertion boundary.
public final class Example71 { static int add(int left,int right){return left+right;} public static void main(String[] args){ if(add(2,3)!=5) throw new AssertionError("expected five"); System.out.println("assertion passed"); } }

