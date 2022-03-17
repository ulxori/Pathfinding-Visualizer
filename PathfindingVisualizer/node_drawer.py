import time
from tkinter import Tk
from node import Node
from typing import List, Optional
from tkinter import Canvas
from node_status import NodeStatus


class NodeDrawer:
    INITIAL_DELAY: int = 20

    def __init__(self, canvas: Canvas, cell_size: int, window: Tk):
        self.canvas: Canvas = canvas
        self.node_size: int = cell_size
        self.rects: dict = {}
        self.window: Tk = window

    def draw_solution(self, visited: List[Node], path: List[Node]):
        delay: int = self.INITIAL_DELAY
        for node in visited:
            node.make_visited()
            if node in path:
                self.window.after(delay, self.draw, node, True, NodeStatus.PathNode)
            else:
                self.window.after(delay, self.draw, node)
            delay += self.INITIAL_DELAY

        for node in path:
            self.window.after(delay, self.draw, node)
            delay += self.INITIAL_DELAY

    def draw_grid(self, nodes: List[List[Node]]) -> None:
        [[self.draw(node) for node in row]for row in nodes]

    def draw_maze(self, maze: List[Node]) -> None:
        delay: int = self.INITIAL_DELAY
        for node in maze:
            node.make_obstacle()
            self.window.after(delay, self.draw, node)
            delay += self.INITIAL_DELAY

    def draw(self, node: Node, change_node_status: bool = False, status: Optional[NodeStatus] = None):
        x, y = node.get_position()
        color: str = node.status.value
        if (x, y) in self.rects:
            old_rect = self.rects[(x, y)]
            self.canvas.delete(old_rect)

        x_pos: int = x * self.node_size
        y_pos: int = y * self.node_size
        rect = self.canvas.create_rectangle(x_pos, y_pos, x_pos+self.node_size, y_pos + self.node_size, fill=color)
        self.rects[(x, y)] = rect
        if change_node_status:
            node.status = status

