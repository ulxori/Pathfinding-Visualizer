import random
from grid import Grid
from enum import Enum
from node import Node
from typing import List
from abc import ABC, abstractmethod


class Direction(Enum):
    horizontal = (1, 0)
    vertical = (0, 1)


class MazeAlgorithm(ABC):
    @abstractmethod
    def generate(self, grid: Grid) -> List[Node]:
        pass


class RecursiveDivision(MazeAlgorithm):
    def generate(self, grid: Grid) -> List[Node]:
        rows_num: int = grid.rows_num
        cols_num: int = grid.cols_num
        obstacles: List[Node] = []

        def divide2(x_start: int, x_end: int, y_start: int, y_end: int) -> None:
            height = y_end - y_start + 1
            width = x_end - x_start + 1
            if height <= 1 or width <= 1:
                return

            direction: Direction = self.get_direction(width, height)
            if direction is Direction.vertical:
                wall_x = random.randint(x_start, x_end)
                even_spot_wall = wall_x % 2 == 0

                if even_spot_wall:
                    offset: int = -1 if wall_x == x_end else 1
                    wall_x += offset

                hole_y = random.randint(y_start, y_end)
                even_spot_hole = hole_y % 2 == 0
                if not even_spot_hole:
                    offset = -1 if hole_y == y_end else 1
                    hole_y += offset

                for y in range(y_start, y_end+1):
                    if y == hole_y:
                        continue
                    obstacles.append(grid.get_node(wall_x, y))

                divide2(x_start, wall_x-1, y_start, y_end)
                divide2(wall_x+1, x_end, y_start, y_end)
            else:
                wall_y = random.randint(y_start, y_end)
                hole_x = random.randint(x_start, x_end)
                even_spot_wall = wall_y % 2 == 0
                if even_spot_wall:
                    offset = -1 if wall_y == y_end else 1
                    wall_y += offset

                even_spot_hole = hole_x % 2 == 0
                if not even_spot_hole:
                    offset = -1 if hole_x == x_end else 1
                    hole_x += offset

                for x in range(x_start, x_end+1):
                    if x == hole_x:
                        continue

                    obstacles.append(grid.get_node(x, wall_y))
                divide2(x_start, x_end, y_start, wall_y-1)
                divide2(x_start, x_end, wall_y+1, y_end)

        divide2(0, cols_num-1, 0, rows_num-1)

        return obstacles

    def get_direction(self, width: int, height: int) -> Direction:
        if width > height:
            return Direction.vertical
        elif width < height:
            return Direction.horizontal
        else:
            random.choice([Direction.vertical, Direction.horizontal])


class RecursiveDivisionVerticalSkew(RecursiveDivision):
    def get_direction(self, width: int, height: int) -> Direction:
        directions = [Direction.vertical, Direction.horizontal]
        directions_weights = (1, 4)
        selected = random.choices(directions, weights=directions_weights, k=2)[0]
        return selected


class RecursiveDivisionHorizontalSkew(RecursiveDivision):
    def get_direction(self, width: int, height: int) -> Direction:
        directions = [Direction.vertical, Direction.horizontal]
        directions_weights = (4, 1)
        selected = random.choices(directions, weights=directions_weights, k=2)[0]
        return selected


class MidPointCircle(MazeAlgorithm):
    RADIUS_GROWTH: int = 3
    INITIAL_RADIUS: int = 4

    def generate(self, grid: Grid) -> List[Node]:
        rows_num: int = grid.rows_num
        cols_num: int = grid.cols_num
        max_radius: int = rows_num//2 if rows_num < cols_num else cols_num//2
        current_radius: int = self.INITIAL_RADIUS
        x_center: int = cols_num//2
        y_center: int = rows_num//2
        obstacles: List[Node] = []

        while current_radius < max_radius:
            circle_cords = self.get_circle_cords(current_radius, x_center, y_center)
            # remove a random point that doesn't touch the border  to go through the maze
            while True:
                random_cord_index = random.randint(0, len(circle_cords)-1)
                selected_point = circle_cords.pop(random_cord_index)
                x, y = selected_point
                is_x_cord_correct = x != 0 and x != cols_num-1
                is_y_cord_correct = y != 0 and y != rows_num-1
                if is_x_cord_correct and is_y_cord_correct:
                    break

            for cord in circle_cords:
                x, y = cord
                obstacle = grid.nodes[y][x]
                obstacles.append(obstacle)

            current_radius += self.RADIUS_GROWTH

        return obstacles

    def get_circle_cords(self, radius: int, offset_x: int, offset_y: int) -> List[tuple[int, int]]:
        cords: List[tuple[int, int]] = []
        p = 1 - radius
        x = radius
        y = 0
        cords.append((offset_x, offset_y + radius))
        cords.append((offset_x, offset_y - radius))
        cords.append((offset_x + radius, offset_y))
        cords.append((offset_x - radius, offset_y))
        while x > y:
            y += 1
            if p <= 0:
                p = p + 2*y + 1
            else:
                x -= 1
                p = p + 2*y - 2*x + 1

            if x < y:
                break
            cords += self.get_symmetric_points(x, y, offset_x, offset_y)
            if x != y:
                cords += self.get_symmetric_points(y, x, offset_x, offset_y)

        return cords

    def get_symmetric_points(self, x, y, offset_x, offset_y) -> List[tuple[int, int]]:
        points: List[tuple[int,int]] = []
        points.append((x + offset_x, y + offset_y))
        points.append((x + offset_x, -y + offset_y))
        points.append((-x + offset_x, y + offset_y))
        points.append((-x + offset_x, -y + offset_y))

        return points


class MazeAlgorithmFactory:

    def get_maze_algorithm(self, algorithm: str = "Recursion division"):
        algorithms = {
            "Recursive division": RecursiveDivision,
            "Recursive division vertical skew": RecursiveDivisionVerticalSkew,
            "Recursive division horizontal skew": RecursiveDivisionHorizontalSkew,
            "Midpoint": MidPointCircle
        }
        return algorithms[algorithm]

