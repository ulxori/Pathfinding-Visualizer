from math import sqrt
from node import Node
from typing import List

def calculate_manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1-y2)


def calculate_euclidean_distance(x1: int, x2: int, y1: int, y2: int) -> int:
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def restore_path(previous_node: dict[Node, Node], end_node: Node, start_node: Node) -> List[Node]:
    path: List[Node] = []
    if end_node in previous_node:
        prev_node = previous_node[end_node]
        while prev_node is not start_node:
            path.append(prev_node)
            prev_node = previous_node[prev_node]

    return path
