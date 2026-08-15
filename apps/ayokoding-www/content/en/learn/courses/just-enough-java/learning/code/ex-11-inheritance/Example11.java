// ex-11 · inheritance · co-06
public final class Example11 { static class Task { String label(){return "task";} } static final class DoneTask extends Task { @Override String label(){return "done";} } public static void main(String[] args){ Task task=new DoneTask(); System.out.println(task.label()); } }

