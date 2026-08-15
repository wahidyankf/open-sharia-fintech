// ex-24 · checked-exception · co-24
public final class Example24 { static String read(boolean available) throws Exception { if(!available) throw new Exception("missing"); return "value"; } public static void main(String[] args){ try { System.out.println(read(false)); } catch(Exception problem) { System.out.println(problem.getMessage()); } } }

