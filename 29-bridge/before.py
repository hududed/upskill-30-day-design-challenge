from dataclasses import dataclass


@dataclass
class Movie:
    id: str
    title: str
    description: str
    director: str


@dataclass
class Series:
    id: str
    title: str
    summary: str
    episodes: int


def view(item: Movie | Series, view_type: str) -> None:
    if view_type == "list":
        heading = item.title
        print(heading)
    elif view_type == "preview":
        heading = item.title
        if isinstance(item, Movie):
            subheading = item.director
        else:
            subheading = f"{item.episodes} episodes"
        print(heading)
        print(subheading)

    elif view_type == "full":
        heading = item.title
        if isinstance(item, Movie):
            subheading = item.director
            text = item.description
        else:
            subheading = f"{item.episodes} episodes"
            text = item.summary
        print(heading)
        print(subheading)
        print(text)


def main() -> None:
    media = [
        Movie(
            id="1",
            title="Spirited Away",
            description="Chihiro ...",
            director="Hayao Miyazaki",
        ),
        Series(
            id="2",
            title="Fullmetal Alchemist: Brotherhood",
            summary="Edward ...",
            episodes=64,
        ),
    ]

    for item in media:
        view(item, "list")
        view(item, "preview")
        view(item, "full")


if __name__ == "__main__":
    main()
