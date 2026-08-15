// ex-31 · switch-pattern · co-11
public final class Example31 { sealed interface Shape permits Circle, Square {} record Circle(int radius) implements Shape {} record Square(int side) implements Shape {} static int measure(Shape shape){ return switch(shape){case Circle c -> c.radius(); case Square s -> s.side();};} public static void main(String[] args){System.out.println(measure(new Circle(2)));} }

