from abc import ABC, abstractmethod
from typing import Optional
from tkinter import Tk


class App(ABC):
    def __init__(self, height: str, width: str, title: str, background: str):
        self.height: str = height
        self.width: str = width
        self.title: str = title
        self.background: str = background
        self.window: Optional[Tk] = None

    def run(self) -> None:
        self.window = Tk()
        self.window.geometry(self.width+"x"+self.height)
        self.window.title(self.title)
        self.window.configure(bg=self.background)
        self.add_ui()
        self.update()

    @abstractmethod
    def add_ui(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class PathFindingApp(App):
    MENU_HEIGHT: int = 50

    def __init__(self, height: str, width: str, title: str, background: str,
                 path_algorithms: dict, maze_algorithms: dict):

        super().__init__(height, width, title, background)
        self.path_algorithms = path_algorithms
        self.maze_algorithms = maze_algorithms
        self.menu = None

    def add_ui(self) -> None:
        pass

    def update(self) -> None:
        self.window.mainloop()


