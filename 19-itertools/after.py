import itertools
import operator
import random
from dataclasses import dataclass

from faker import Faker


@dataclass
class Person:
    name: str
    age: int
    city: str
    country: str


# Instantiate the Faker module
fake = Faker()

# List of possible countries
countries = [
    "UK",
    "USA",
    "Japan",
    "Australia",
    "France",
    "Germany",
    "Italy",
    "Spain",
    "Canada",
    "Mexico",
]

# Generate 1000 random Person instances
PERSON_DATA: list[Person] = [
    Person(fake.name(), random.randint(18, 70), fake.city(), random.choice(countries))
    for _ in range(1000)
]


def main() -> None:
    # Filter data with itertools.filterfalse()
    filtered_data = list(
        itertools.filterfalse(lambda person: person.age < 21, PERSON_DATA)
    )

    # Sort the filtered data based on country
    filtered_data.sort(key=operator.attrgetter("country"))

    # Group the filtered data by country with itertools.groupby()
    grouped_data = itertools.groupby(filtered_data, key=lambda person: person.country)

    # Create a summary dict from the grouped data
    summary = {country: len(list(group)) for country, group in grouped_data}

    print(summary)


if __name__ == "__main__":
    main()
