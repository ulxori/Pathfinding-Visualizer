from app import PathFindingApp
from colors import Color

WIDTH = "720"
HEIGHT = "480"
TITLE = "Pathfinding-Visualizer"
BACKGROUND_COLOR = Color.Brown.value
PATH_ALGORITHMS = {'A*': 'A*'}
MAZE_ALGORITHMS = {'Recursive Division': 'Recursive Division'}


def main():
    app = PathFindingApp(HEIGHT, WIDTH, TITLE, BACKGROUND_COLOR, PATH_ALGORITHMS, MAZE_ALGORITHMS)
    app.run()


if __name__ == '__main__':
    main()

