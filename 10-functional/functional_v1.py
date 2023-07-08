from math import pi
from typing import Callable

ShapeFn = Callable[..., float]
Shape = tuple[float, float, ShapeFn, ShapeFn]


def rectangle(width: float, height: float) -> Shape:
    def area() -> float:
        return width * height
    
    def perimeter() -> float:
        return 2 * (width + height)
    
    return (width, height, area, perimeter)

def square(side_length: float) -> Shape:
    def area() -> float:
        return side_length**2
    
    def perimeter() -> float:
        return 4 * side_length
    
    return (side_length, side_length, area, perimeter)

def circle(radius: float) -> Shape:
    def area() -> float:
        return pi * radius**2
    
    def perimeter() -> float:
        return 2 * pi * radius
    
    return (radius, radius, area, perimeter)

def total_area(shapes: list[Shape]) -> float:
    return sum(shape[2]() for shape in shapes)

def total_perimeter(shapes: list[Shape]) -> float:
    return sum(shape[3]() for shape in shapes)


def main() -> None:
    shapes: list[Shape] = [rectangle(4, 5), square(3), circle(2)]
    print("Total Area:", total_area(shapes))
    print("Total Perimeter:     ", total_perimeter(shapes))


if __name__ == "__main__":
    main()
