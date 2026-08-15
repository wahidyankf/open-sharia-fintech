// ex-23 · try-catch · co-24
public final class Example23 { static String read(boolean available) throws Exception { if(!available) throw new Exception("missing"); return "value"; } public static void main(String[] args){ try { System.out.println(read(false)); } catch(Exception problem) { System.out.println(problem.getMessage()); } } }

