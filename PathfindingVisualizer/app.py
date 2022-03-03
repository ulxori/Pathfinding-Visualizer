from abc import ABC, abstractmethod
from typing import Optional
from tkinter import Tk, Canvas
from menu import Menu
from node_drawer import NodeDrawer
from grid import Grid


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
    CELL_SIZE: int = 25

    def __init__(self, height: str, width: str, title: str, background: str,
                 path_algorithms: dict, maze_algorithms: dict):

        super().__init__(height, width, title, background)
        self.path_algorithms: dict = path_algorithms
        self.maze_algorithms: dict = maze_algorithms
        self.grid = Grid(int(width), int(height) - self.MENU_HEIGHT, self.CELL_SIZE)
        self.menu: Menu = None
        self.drawer: NodeDrawer = None

    def on_solve_maze_button_click(self):
        print("solve_button")

    def on_generate_maze_button_click(self):
        print("generate_button")

    def add_ui(self) -> None:
        path_algorithms_names = list(self.path_algorithms.keys())
        maze_algorithms_names = list(self.maze_algorithms.keys())
        self.menu = Menu(path_algorithms_names, maze_algorithms_names, self.window)

        self.menu.add_button("Solve", self.on_solve_maze_button_click)
        self.menu.add_button("Generate", self.on_generate_maze_button_click)

        grid_canvas = Canvas(self.window, height=int(self.height)-self.MENU_HEIGHT, width=int(self.width))
        grid_canvas.place(x=0, y=50)
        self.drawer = NodeDrawer(grid_canvas, self.CELL_SIZE, self.window)
        self.drawer.draw_grid(self.grid.nodes)

    def update(self) -> None:
        self.window.mainloop()


