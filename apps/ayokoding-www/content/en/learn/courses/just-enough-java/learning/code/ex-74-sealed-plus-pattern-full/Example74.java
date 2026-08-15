// ex-74 · sealed-plus-pattern-full · co-08, co-12
public final class Example74 { sealed interface Result permits Ok, Missing {} record Ok(String value) implements Result {} record Missing() implements Result {} static String render(Result result){ return switch(result){ case Ok ok -> ok.value(); case Missing missing -> "missing"; }; } public static void main(String[] args){ System.out.println(render(new Ok("ready"))); } }

