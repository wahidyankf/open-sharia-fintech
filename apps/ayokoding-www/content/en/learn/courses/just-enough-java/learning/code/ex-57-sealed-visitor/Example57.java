// ex-57 · sealed-visitor · co-08, co-11
public final class Example57 { sealed interface Result permits Ok, Missing {} record Ok(String value) implements Result {} record Missing() implements Result {} static String render(Result result){ return switch(result){ case Ok ok -> ok.value(); case Missing missing -> "missing"; }; } public static void main(String[] args){ System.out.println(render(new Ok("ready"))); } }

