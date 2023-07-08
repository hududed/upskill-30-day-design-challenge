from functools import partial
from math import pi
from typing import Callable


def rectangle_area(width: float, height: float) -> float:
    return width * height

def rectangle_perimeter(width: float, height: float) -> float:
    return 2 * (width + height)

def square_area(side_length: float) -> float:
    return side_length**2

def square_perimeter(side_length: float) -> float:
    return 4 * side_length

def circle_area(radius: float) -> float:
    return pi * radius**2

def circle_circumference(radius: float) -> float:
    return 2 * pi * radius

def calculate_total(*args: Callable[[], float]) -> float:
    return sum(arg() for arg in args)


def main() -> None:
    print(
        "Total Area:",
        calculate_total(
            partial(rectangle_area, 4, 5),
            partial(square_area, 3),
            partial(circle_area, 2),
        ),
    )
    print(
        "Total Perimeter:",
        calculate_total(
            partial(rectangle_perimeter, 4, 5),
            partial(square_perimeter, 3),
            partial(circle_circumference, 2),
        ),
    )

if __name__ == "__main__":
    main()
