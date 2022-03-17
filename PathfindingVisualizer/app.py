from abc import ABC, abstractmethod
from typing import Optional
from tkinter import Tk, Canvas
from menu import Menu
from node_drawer import NodeDrawer
from grid import Grid
from maze_algorithms import MazeAlgorithmFactory
from path_algorithms import PathAlgorithmFactory


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
    MENU_HEIGHT: int = 40
    CELL_SIZE: int = 20

    def __init__(self, height: str, width: str, title: str, background: str,
                 path_algorithms: list[str], maze_algorithms: list[str]):

        super().__init__(height, width, title, background)
        self.path_algorithms: dict = path_algorithms
        self.maze_algorithms: dict = maze_algorithms
        self.grid = Grid(int(width), int(height) - self.MENU_HEIGHT, self.CELL_SIZE)
        self.menu: Menu = None
        self.drawer: NodeDrawer = None

    def on_solve_maze_button_click(self) -> None:
        if not self.grid.is_valid():
            return

        path_algorithm_factory: PathAlgorithmFactory = PathAlgorithmFactory()
        algorithm_name: str = self.menu.get_selected_path_algorithm_name()
        algorithm = path_algorithm_factory.get_path_algorithm(algorithm_name)
        self.grid.remove_solution()
        self.drawer.draw_grid(self.grid.nodes)
        visited, path = algorithm().solve(self.grid)
        self.drawer.draw_solution(visited, path)

    def on_generate_maze_button_click(self) -> None:
        maze_algorithm_factory: MazeAlgorithmFactory = MazeAlgorithmFactory()
        algorithm_name: str = self.menu.get_selected_maze_algorithm_name()
        algorithm = maze_algorithm_factory.get_maze_algorithm(algorithm_name)
        self.grid.reset_grid()
        self.drawer.draw_grid(self.grid.nodes)
        obstacles = algorithm().generate(self.grid)
        self.drawer.draw_maze(obstacles)

    def on_reset_button_click(self) -> None:
        self.grid.reset_grid()
        self.drawer.draw_grid(self.grid.nodes)

    def on_remove_solution_button_click(self) -> None:
        self.grid.remove_solution()
        self.drawer.draw_grid(self.grid.nodes)

    def on_lef_button_motion(self, event) -> None:
        x, y = event.x, event.y
        new_obstacle = self.grid.add_obstacle(x, y)
        if new_obstacle is not None:
            self.drawer.draw(new_obstacle)

    def on_right_button_click(self, event) -> None:
        x, y = event.x, event.y
        self.grid.add_start_node(x, y)
        self.drawer.draw_grid(self.grid.nodes)

    def on_middle_button_click(self, event) -> None:
        x, y = event.x, event.y
        self.grid.add_end_node(x, y)
        self.drawer.draw_grid(self.grid.nodes)

    def add_ui(self) -> None:
        self.menu = Menu(self.path_algorithms, self.maze_algorithms, self.window)

        self.menu.add_button("Solve", self.on_solve_maze_button_click)
        self.menu.add_button("Generate", self.on_generate_maze_button_click)
        self.menu.add_button("Reset", self.on_reset_button_click)
        self.menu.add_button("Remove solution", self.on_remove_solution_button_click)

        grid_canvas = Canvas(self.window, height=int(self.height)-self.MENU_HEIGHT, width=int(self.width))
        grid_canvas.place(x=0, y=50)
        self.drawer = NodeDrawer(grid_canvas, self.CELL_SIZE, self.window)
        self.drawer.draw_grid(self.grid.nodes)

        grid_canvas.bind('<B1-Motion>', self.on_lef_button_motion)
        grid_canvas.bind('<ButtonPress-2>', self.on_middle_button_click)
        grid_canvas.bind('<ButtonPress-3>', self.on_right_button_click)

    def update(self) -> None:
        self.window.mainloop()
