import time
from abc import ABC, abstractmethod
from node import Node
from node_drawer import NodeDrawer
from typing import List
from grid import Grid
from node_status import NodeStatus
from typing import List

class PathFindingAlgorithm(ABC):
    @abstractmethod
    def solve(self, grid: Grid) -> None:
        pass


class Bfs(PathFindingAlgorithm):
    def solve(self, grid: Grid) -> tuple[List[Node], List[Node]]:
        previous_node: dict = {}
        queue: List[Node] = []
        visited: List[Node] = []
        queue.append(grid.start_node)
        visited.append(grid.start_node)

        while len(queue) > 0:
            current_node: Node = queue.pop(0)
            if current_node is grid.end_node:
                break
            for neighbor in current_node.neighbors:
                obstacle: bool = neighbor.status == NodeStatus.Obstacle.value
                if neighbor not in visited and not obstacle:
                    queue.append(neighbor)
                    previous_node[neighbor] = current_node
                    visited.append(neighbor)

        visited.remove(grid.start_node)
        visited.remove(grid.end_node)
        path: Node = []

        if grid.end_node in previous_node:
            prev_node = previous_node[grid.end_node]
            while prev_node is not grid.start_node:
                path.append(prev_node)
                prev_node = previous_node[prev_node]

        path.reverse()
        return visited, path


class Dfs(PathFindingAlgorithm):
    def solve(self, grid: Grid) -> tuple[List[Node], List[Node]]:
        visited: List[Node] = [grid.start_node]
        path: List[Node] = []

        def helper(current_node: Node, is_found: bool) -> bool:
            if current_node is grid.end_node:
                return True
            for neighbor in current_node.neighbors:
                obstacle: bool = neighbor.status == NodeStatus.Obstacle.value
                if neighbor not in visited and not obstacle:
                    path.append(neighbor)
                    visited.append(neighbor)
                    is_found = helper(neighbor, is_found)
                if is_found:
                    return True
            path.pop()
            return False

        helper(grid.start_node, False)
        visited.remove(grid.end_node)

        return visited, path


class AStar(PathFindingAlgorithm):
    def solve(self, grid: Grid) -> tuple[List[Node], List[Node]]:
        pass






