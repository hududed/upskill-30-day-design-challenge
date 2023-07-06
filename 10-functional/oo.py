from dataclasses import dataclass
from math import pi
from typing import Protocol


class Shape(Protocol):
    def area(self) -> float:
        ...

    def perimeter(self) -> float:
        ...


@dataclass
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Square(Rectangle):
    def __init__(self, side_length: float):
        self.side_length = side_length
        super().__init__(self.side_length, self.side_length)


@dataclass
class Circle:
    radius: float

    def area(self) -> float:
        return pi * self.radius**2

    def perimeter(self) -> float:
        return 2 * pi * self.radius


@dataclass
class ShapeCalculator:
    shapes: list[Shape]

    def total_area(self) -> float:
        return sum(shape.area() for shape in self.shapes)

    def total_perimeter(self) -> float:
        return sum(shape.perimeter() for shape in self.shapes)


def main() -> None:
    shapes: list[Shape] = [Rectangle(4, 5), Square(3), Circle(2)]
    calculator = ShapeCalculator(shapes)
    print("Total Area:", calculator.total_area())
    print("Total Perimeter:", calculator.total_perimeter())


if __name__ == "__main__":
    main()
