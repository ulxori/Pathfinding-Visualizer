from app import PathFindingApp
from colors import Color

WIDTH: str = "720"
HEIGHT: str = "480"
TITLE: str = "Pathfinding-Visualizer"
BACKGROUND_COLOR: str = Color.Brown.value
PATH_ALGORITHMS: list[str] = ["Bfs", "Dfs", "Dijkstra", "A star manhattan distance", "A star euclidean distance",
                              "A star chebyshev distance", "Best first search manhattan distance",
                              "Best first search euclidean distance", "Best first search chebyshev distance"]
MAZE_ALGORITHMS: list[str] = ["Recursive division", "Recursive division vertical skew",
                              "Recursive division horizontal skew", "Midpoint"]


def main():
    app = PathFindingApp(HEIGHT, WIDTH, TITLE, BACKGROUND_COLOR, PATH_ALGORITHMS, MAZE_ALGORITHMS)
    app.run()


if __name__ == '__main__':
    main()

