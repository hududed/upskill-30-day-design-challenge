import unittest
from collections import Counter


def count_fruits(fruits: list[str]) -> dict[str, int]:
    return dict(Counter(fruits))

class TestCountFruits(unittest.TestCase):
    def test_count_fruits_default(self):
        self.assertEqual(
            count_fruits(
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
            ),
            {"apple": 4, "banana": 3, "cherry": 4},
        )

    def test_count_fruits_empty(self):
        self.assertEqual(count_fruits([]), {})


if __name__ == "__main__":
    unittest.main()