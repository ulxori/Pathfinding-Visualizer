from tkinter import StringVar, OptionMenu, Button, LEFT, NW


class Menu:
    PADDING: int = 5

    def __init__(self, path_algorithms: list[str], maze_algorithms: list[str], window):
        self.window = window
        self.clicked_path_algorithm = StringVar()
        self.clicked_maze_algorithm = StringVar()

        self.clicked_path_algorithm.set(path_algorithms[0])
        self.clicked_maze_algorithm.set(maze_algorithms[0])

        self.drop_path = OptionMenu(window, self.clicked_path_algorithm, *path_algorithms)
        self.drop_maze = OptionMenu(window, self.clicked_maze_algorithm, *maze_algorithms)

        self.drop_path.pack(padx=self.PADDING, pady=self.PADDING, side=LEFT, anchor=NW)
        self.drop_maze.pack(padx=self.PADDING, pady=self.PADDING, side=LEFT, anchor=NW)

    def add_button(self, text: str, func) -> None:
        Button(self.window, text=text, command=func).pack(padx=self.PADDING, pady=self.PADDING, side=LEFT, anchor=NW)

    def get_selected_path_algorithm_name(self) -> str:
        return self.clicked_path_algorithm.get()

    def get_selected_maze_algorithm_name(self) -> str:
        return self.clicked_maze_algorithm.get()
