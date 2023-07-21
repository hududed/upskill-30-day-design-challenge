from dataclasses import dataclass, field
from typing import List


@dataclass
class TextEditorMemento:
    text: str

@dataclass
class TextEditor:
    text: str = ""
    undo_stack: List[TextEditorMemento] = field(default_factory=list)
    redo_stack: List[TextEditorMemento] = field(default_factory=list)

    def insert(self, text: str) -> None:
        memento = TextEditorMemento(self.text)
        self.undo_stack.append(memento)
        self.text += text
        self.redo_stack.clear()

    def delete(self, num_chars: int) -> None:
        memento = TextEditorMemento(self.text)
        self.undo_stack.append(memento)
        self.text = self.text[:-num_chars]
        self.redo_stack.clear()

    def undo(self) -> None:
        if not self.undo_stack:
            return
        memento = self.undo_stack.pop()
        self.redo_stack.append(TextEditorMemento(self.text))
        self.text = memento.text

    def redo(self) -> None:
        if not self.redo_stack:
            return
        memento = self.redo_stack.pop()
        self.undo_stack.append(TextEditorMemento(self.text))
        self.text = memento.text

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
