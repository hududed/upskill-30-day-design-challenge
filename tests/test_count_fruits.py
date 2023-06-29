from after_v1 import count_fruits


def test_count_fruits_default() -> None:
    assert count_fruits(
        [
            "apple",
            "banana",
            "apple",
            "cherry",
            "banana",
            "cherry",
            "apple",
            "apple",
            "cherry",
            "banana",
            "cherry",
        ]
    ) == {"apple": 4, "banana": 3, "cherry": 4}

def test_count_fruits_empty() -> None:
    assert count_fruits([]) == {}