from dataclasses import dataclass, field


@dataclass
class TextEditor:
    text: str = ""
    undo_stack: list[str] = field(default_factory=list)
    redo_stack: list[str] = field(default_factory=list)

    def _perform_edit(self, text: str) -> None:
        self.undo_stack.append(self.text)
        self.text = text
        self.redo_stack = []
    
    def insert(self, text: str) -> None:
        self._perform_edit(self.text + text)

    def delete(self, num_chars: int) -> None:
        self._perform_edit(self.text[:-num_chars])

    def undo(self) -> None:
        if self.undo_stack:
            self.redo_stack.append(self.text)
            self.text = self.undo_stack.pop()

    def redo(self) -> None:
        if self.redo_stack:
            self.undo_stack.append(self.text)
            self.text = self.redo_stack.pop()

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
