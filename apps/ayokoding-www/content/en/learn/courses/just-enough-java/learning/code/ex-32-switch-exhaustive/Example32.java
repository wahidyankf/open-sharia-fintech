// ex-32 · switch-exhaustive · co-12
public final class Example32 { sealed interface Shape permits Circle, Square {} record Circle(int radius) implements Shape {} record Square(int side) implements Shape {} static int measure(Shape shape){ return switch(shape){case Circle c -> c.radius(); case Square s -> s.side();};} public static void main(String[] args){System.out.println(measure(new Circle(2)));} }

