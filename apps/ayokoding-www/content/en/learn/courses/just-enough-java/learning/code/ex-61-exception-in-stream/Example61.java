// ex-61 · exception-in-stream · co-24, co-18
public final class Example61 { static String read(boolean available) throws Exception { if(!available) throw new Exception("missing"); return "value"; } public static void main(String[] args){ try { System.out.println(read(false)); } catch(Exception problem) { System.out.println(problem.getMessage()); } } }

