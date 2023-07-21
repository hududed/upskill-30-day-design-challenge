import unittest


def count_fruits(fruits: list[str]) -> dict[str, int]:
    fruits_dict: dict[str, int] = {}
    for i in range(len(fruits)):
        if fruits[i] not in fruits_dict:
            count = 0
            for j in range(i, len(fruits)):
                if fruits[j] == fruits[i]:
                    count += 1
            fruits_dict[fruits[i]] = count
    return fruits_dict


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