from node_status import NodeStatus
from typing import List


class Node:
    def __init__(self, col_num, row_num):
        self.status = NodeStatus.Unvisited.value
        self.col_num = col_num
        self.row_num = row_num
        self.neighbors = []

    def get_position(self) -> tuple[int, int]:
        return self.row_num, self.col_num

    def set_neighbors(self, neighbors: List['Node']) -> None:
        self.neighbors = neighbors

    def make_visited(self) -> None:
        self.status = NodeStatus.Visited.value

    def make_unvisited(self) -> None:
        self.status = NodeStatus.Unvisited.value

    def make_obstacle(self) -> None:
        self.status = NodeStatus.Obstacle.value

    def make_start_node(self) -> None:
        self.status = NodeStatus.StartNode.value

    def make_end_node(self) -> None:
        self.status = NodeStatus.EndNode.value