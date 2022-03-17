from node_status import NodeStatus
from typing import List


class Node:
    def __init__(self, col_num: int, row_num: int):
        self.status = NodeStatus.Unvisited
        self.col_num: int = col_num
        self.row_num: int = row_num
        self.neighbors: List['Node'] = []

    def get_position(self) -> tuple[int, int]:
        return self.col_num, self.row_num

    def set_neighbors(self, neighbors: List['Node']) -> None:
        self.neighbors = neighbors

    def make_visited(self) -> None:
        self.status = NodeStatus.Visited

    def make_unvisited(self) -> None:
        self.status = NodeStatus.Unvisited

    def make_obstacle(self) -> None:
        self.status = NodeStatus.Obstacle

    def make_start_node(self) -> None:
        self.status = NodeStatus.StartNode

    def make_end_node(self) -> None:
        self.status = NodeStatus.EndNode

    def make_path_node(self) -> None:
        self.status = NodeStatus.PathNode
