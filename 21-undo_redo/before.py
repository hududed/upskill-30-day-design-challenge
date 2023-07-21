from dataclasses import dataclass


@dataclass
class TextEditor:
    text: str = ""

    def insert(self, text: str) -> None:
        self.text += text

    def delete(self, num_chars: int) -> None:
        self.text = self.text[:-num_chars]

    def undo(self) -> None:
        pass

    def redo(self) -> None:
        pass

    def print_text(self) -> None:
        print(self.text)


def main() -> None:
    # Test the text editor
    editor = TextEditor()

    # Since there is no text, these commands should do nothing
    editor.undo()
    editor.redo()

    editor.insert("Hello")
    editor.insert(" World!")
    editor.print_text()  # Output: Hello World!

    editor.delete(6)
    editor.print_text()  # Output: Hello

    editor.undo()
    editor.print_text()  # Output: Hello World!

    editor.redo()
    editor.print_text()  # Output: Hello

    editor.insert("!!!")
    editor.print_text()  # Output: Hello!!!

    editor.undo()
    editor.undo()
    editor.print_text()  # Output: Hello World!


if __name__ == "__main__":
    main()
