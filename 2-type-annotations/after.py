from typing import Iterable, Sized


def filter_odd_numbers(numbers: Iterable[int]) -> list[int]:
    """Filters odd numbers from a sequence of numbers."""
    result: list[int] = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num)
    return result 


def square_numbers(numbers: Iterable[int | float]) -> list[float]:
    """Square numbers in a sequence."""
    result: list[float] = []
    for num in numbers:
        result.append(num**2)
    return result


def count(words: Iterable[Sized]) -> list[int]:
    """Counts the number of characters in a sequence of words."""
    result: list[int] = []
    for word in words:
        result.append(len(word))
    return result


def process_data(
    data,
    filter_func=None,
    process_func=None,
):
    """Applies filter_func and process_func on a data sequence."""
    if filter_func is None:
        filter_func = lambda x: x
    filtered_data = filter_func(data)
    if process_func is None:
        process_func = lambda x: x
    return process_func(filtered_data)


def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    result = process_data(numbers, filter_func=filter_odd_numbers, process_func=square_numbers)
    print(result)

    words = ["apple", "banana", "cherry"]
    result2 = process_data(words, process_func=count)
    print(result2)


if __name__ == "__main__":
    main()
