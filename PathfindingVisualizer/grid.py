from math import floor
from node import Node
from typing import Optional
from node_status import NodeStatus


class Grid:
    def __init__(self, width: int, height: int, cell_size: int):
        self.width: int = width
        self.height: int = height
        self.rows_num: int = floor(height/cell_size)
        self.cols_num: int = floor(width/cell_size)
        self.start_node: Optional[Node] = None
        self.end_node: Optional[Node] = None
        self.nodes: [[Node]] = [[Node(x, y) for x in range(self.cols_num)] for y in range(self.rows_num)]
        # add neighbors to every node
        [list(map(self.add_neighbors, row)) for row in self.nodes]

    def add_neighbors(self, node: Node) -> None:
        x, y = node.get_position()
        neighbors = []
        is_left_available = x - 1 >= 0
        is_right_available = x + 1 < self.cols_num
        is_up_available = y - 1 >= 0
        is_down_available = y + 1 < self.rows_num

        if is_left_available:
            neighbors.append(self.nodes[y][x - 1])
        if is_right_available:
            neighbors.append(self.nodes[y][x + 1])
        if is_up_available:
            neighbors.append(self.nodes[y - 1][x])
        if is_down_available:
            neighbors.append(self.nodes[y + 1][x])

        self.nodes[y][x].set_neighbors(neighbors)

    def reset_grid(self) -> None:
        [[node.make_unvisited() for node in row] for row in self.nodes]

    def remove_solution(self) -> None:
        visited = NodeStatus.Visited.value
        path = NodeStatus.Solution.value
        to_remove = [visited, path]
        nodes_to_remove = list([filter(lambda node: node.status in to_remove, row) for row in self.nodes])
        [[node.make_unvisited() for node in row]for row in nodes_to_remove]

    def is_valid(self) -> bool:
        return self.start_node is not None and self.end_node is not None

    def is_position_within(self, x, y) -> bool:
        is_x_pos_within: bool = 0 <= x <= self.width
        is_y_pos_within: bool = 0 <= y <= self.height
        return is_x_pos_within and is_y_pos_within

    def add_start_node(self, x, y) -> None:
        selected_node = self.get_node(x, y)
        if selected_node is None:
            return
        if selected_node is self.start_node:
            selected_node.make_unvisited()
            self.start_node = None
            return

        self.start_node.make_unvisited()
        selected_node.make_start_node()
        self.start_node = selected_node

    def add_end_node(self, x, y):
        selected_node = self.get_node(x, y)
        if selected_node is None:
            return
        if selected_node is self.end_node:
            selected_node.make_unvisited()
            self.start_node = None

        self.end_node.make_unvisited()
        selected_node.make_end_node()
        self.end_node = selected_node

    def add_obstacle(self, x, y):
        selected_node = self.get_node(x, y)
        is_end_node = selected_node is self.end_node
        is_start_node = selected_node is self.start_node

        if selected_node is None or is_start_node or is_end_node:
            return
        if selected_node.status == NodeStatus.Obstacle.value:
            selected_node.make_unvisited()
            return

        selected_node.make_obstacle()

    def get_node(self, x, y):
        if not self.is_position_within(x, y):
            return None
        x_index = floor((x / self.width) * self.cols_num)
        y_index = floor((y / self.height) * self.rows_num)
        return self.nodes[y_index][x_index]


