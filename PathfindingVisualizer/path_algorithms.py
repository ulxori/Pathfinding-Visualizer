from abc import ABC, abstractmethod
from node import Node
from grid import Grid
from node_status import NodeStatus
from typing import List
from queue import PriorityQueue
from helper import calculate_manhattan_distance, calculate_euclidean_distance, calculate_chebyshev_distance,\
    restore_path, INF


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
                obstacle: bool = neighbor.status is NodeStatus.Obstacle
                if neighbor not in visited and not obstacle:
                    queue.append(neighbor)
                    previous_node[neighbor] = current_node
                    visited.append(neighbor)

        visited.remove(grid.start_node)
        if grid.end_node in visited:
            visited.remove(grid.end_node)

        path: List[Node] = []

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
            for neighbor in current_node.neighbors:
                obstacle: bool = neighbor.status is NodeStatus.Obstacle
                if neighbor not in visited and not obstacle:
                    if neighbor is grid.end_node:
                        return True
                    path.append(neighbor)
                    visited.append(neighbor)
                    is_found = helper(neighbor, is_found)
                if is_found:
                    return True
            if len(path) != 0:
                path.pop()
            return False

        helper(grid.start_node, False)
        visited.remove(grid.start_node)

        return visited, path


class AStar(PathFindingAlgorithm):
    def solve(self, grid: Grid) -> tuple[List[Node], List[Node]]:
        visited: List[Node] = [grid.start_node]
        path: List[Node] = []
        open: PriorityQueue = PriorityQueue()
        in_open = {grid.start_node}
        counter = 0
        previous_node: dict = {}
        g_score: dict[Node, int] = {node: INF for row in grid.nodes for node in row}
        f_score: dict[Node, int] = {node: INF for row in grid.nodes for node in row}

        g_score[grid.start_node] = 0
        f_score[grid.start_node] = self.calculate_heuristic(grid.start_node, grid.end_node)

        open.put((f_score[grid.start_node], counter, grid.start_node))

        while not open.empty():
            current_node = open.get()[2]
            in_open.remove(current_node)
            if current_node is grid.end_node:
                break

            for neighbor in current_node.neighbors:
                obstacle: bool = neighbor.status is NodeStatus.Obstacle
                if not obstacle:

                    tmp_g_score = g_score[current_node] + 1
                    if tmp_g_score < g_score[neighbor]:
                        g_score[neighbor] = tmp_g_score
                        tmp_f_score = tmp_g_score + self.calculate_heuristic(neighbor, grid.end_node)
                        f_score[neighbor] = tmp_f_score
                        if neighbor not in in_open:
                            counter += 1
                            open.put((tmp_f_score, counter, neighbor))
                            previous_node[neighbor] = current_node
                            in_open.add(neighbor)
                            visited.append(neighbor)

        visited.remove(grid.start_node)

        if grid.end_node in visited:
            visited.remove(grid.end_node)

        if grid.end_node in previous_node:
            prev_node = previous_node[grid.end_node]
            while prev_node is not grid.start_node:
                path.append(prev_node)
                prev_node = previous_node[prev_node]

        return visited, path

    @abstractmethod
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        pass


class AStarManhattan(AStar):
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        return calculate_manhattan_distance(*start_node.get_position(), *end_node.get_position())


class AStarEuclidean(AStar):
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        return calculate_euclidean_distance(*start_node.get_position(), *end_node.get_position())


class AStarChebyshev(AStar):
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        return calculate_chebyshev_distance(*start_node.get_position(), *end_node.get_position())


class BestFirstSearch(PathFindingAlgorithm):
    def solve(self, grid: Grid) -> tuple[List[Node], List[Node]]:
        visited: List[Node] = [grid.start_node]
        path: List[Node] = []
        previous_node: dict[Node, Node] = {}
        counter: int = 0
        pq: PriorityQueue = PriorityQueue()
        pq.put((0, counter, grid.start_node))
        while not pq.empty():
            current_node = pq.get()[2]
            if current_node is grid.end_node:
                break

            for neighbor in current_node.neighbors:
                obstacle: bool = neighbor.status is NodeStatus.Obstacle
                if neighbor not in visited and not obstacle:
                    counter += 1
                    visited.append(neighbor)
                    pq.put((self.calculate_heuristic(neighbor, grid.end_node), counter, neighbor))
                    previous_node[neighbor] = current_node

        visited.remove(grid.start_node)

        if grid.end_node in visited:
            visited.remove(grid.end_node)
        path = restore_path(previous_node, grid.end_node, grid.start_node)
        return visited, path

    @abstractmethod
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        pass


class BestFirstSearchManhattan(BestFirstSearch):
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        return calculate_manhattan_distance(*start_node.get_position(), *end_node.get_position())


class BestFirstSearchEuclidean(BestFirstSearch):
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        return calculate_euclidean_distance(*start_node.get_position(), *end_node.get_position())


class BestFirstSearchChebyshev(BestFirstSearch):
    def calculate_heuristic(self, start_node: Node, end_node: Node) -> int:
        return calculate_chebyshev_distance(*start_node.get_position(), *end_node.get_position())


class Dijkstra(PathFindingAlgorithm):
    def solve(self, grid: Grid) -> tuple[List[Node], List[Node]]:
        visited: List[Node] = []
        path: List[Node] = []
        previous_node: dict[Node, Node] = {}
        unvisited = {node: INF for row in grid.nodes for node in row if node.status is not NodeStatus.Obstacle}
        unvisited[grid.start_node] = 0

        while unvisited:
            current_node = min(unvisited, key=unvisited.get)
            tmp_distance = unvisited[current_node]
            if current_node is grid.end_node or tmp_distance == INF:
                break

            visited.append(current_node)
            for neighbor in current_node.neighbors:
                obstacle: bool = neighbor.status is NodeStatus.Obstacle
                if neighbor not in visited and not obstacle:
                    new_distance = unvisited[current_node] + 1
                    old_distance = unvisited[neighbor]
                    if new_distance < old_distance:
                        unvisited[neighbor] = new_distance
                        previous_node[neighbor] = current_node

            unvisited.pop(current_node)

        visited.remove(grid.start_node)
        path = restore_path(previous_node, grid.end_node, grid.start_node)
        return visited, path


class PathAlgorithmFactory:

    def get_path_algorithm(self, algorithm_name: str = "Bfs"):
        path_algorithms = {
            "Bfs": Bfs,
            "Dfs": Dfs,
            "Dijkstra": Dijkstra,
            "A star manhattan distance": AStarManhattan,
            "A star euclidean distance": AStarEuclidean,
            "A star chebyshev distance": AStarChebyshev,
            "Best first search manhattan distance": BestFirstSearchManhattan,
            "Best first search euclidean distance": BestFirstSearchEuclidean,
            "Best first search chebyshev distance": BestFirstSearchChebyshev
        }
        return path_algorithms[algorithm_name]
