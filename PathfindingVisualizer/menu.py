from tkinter import  StringVar, OptionMenu, Button, LEFT, NW


class Menu:
    PADDING: int = 5

    def __init__(self, path_algorithms_names, maze_algorithms_names, window):
        self.window = window
        self.clicked_path_algorithm = StringVar()
        self.clicked_maze_algorithm = StringVar()

        self.clicked_path_algorithm.set(path_algorithms_names[0])
        self.clicked_maze_algorithm.set(maze_algorithms_names[0])

        self.drop_path = OptionMenu(window, self.clicked_path_algorithm, *path_algorithms_names)
        self.drop_maze = OptionMenu(window, self.clicked_maze_algorithm, *maze_algorithms_names)

        self.drop_path.pack(padx=self.PADDING, pady=self.PADDING, side=LEFT, anchor=NW)
        self.drop_maze.pack(padx=self.PADDING, pady=self.PADDING, side=LEFT, anchor=NW)

    def add_button(self, text, func):
        Button(self.window, text=text, command=func).pack(padx=5, pady=5, side=LEFT, anchor=NW)

    def get_selected_path_algorithm_key(self) -> str:
        return self.clicked_path_algorithm.get()

    def get_selected_maze_algorithm_key(self) -> str:
        return self.clicked_maze_algorithm.get()
