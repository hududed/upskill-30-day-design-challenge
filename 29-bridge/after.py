from dataclasses import dataclass
from typing import Callable, Protocol


class MediaItem(Protocol):
    heading: str
    subheading: str
    text: str


@dataclass
class Movie:
    id: str
    title: str
    description: str
    director: str

    @property
    def heading(self) -> str:
        return self.title
    
    @property
    def subheading(self) -> str:
        return self.director
    
    @property
    def text(self) -> str:
        return self.description
    


@dataclass 
class Series:
    id: str
    title: str
    summary: str
    episodes: int

    @property
    def heading(self) -> str:
        return self.title
    
    @property
    def subheading(self) -> str:
        return f"{self.episodes} episodes"
    
    @property
    def text(self) -> str:
        return self.summary
    
MediaView = Callable[[MediaItem], None]

def view_list(item: MediaItem) -> None:
    print(item.heading)

def view_preview(item: MediaItem) -> None:
    print(item.heading)
    print(item.subheading)

def view_full(item: MediaItem) -> None:
    print(item.heading)
    print(item.subheading)
    print(item.text)

def view_teaser(item: MediaItem) -> None:
    print(item.heading)
    print(item.text[:10] + "...")


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
        view_list(item)
        view_preview(item)
        view_full(item)
        view_teaser(item)


if __name__ == "__main__":
    main()
