from tkinter import Tk
from node import Node
from typing import List
from tkinter import Canvas


class NodeDrawer:
    DELAY: int = 1

    def __init__(self, canvas: Canvas, cell_size: int, window: Tk):
        self.canvas: Canvas = canvas
        self.node_size: int = cell_size
        self.rects: dict = {}
        self.window: Tk = window

    def wait_and_draw(self, node: Node):
        self.window.after(self.DELAY, self.draw, node)

    def draw_grid(self, nodes: List[List[Node]]):
        [[self.draw(node) for node in row]for row in nodes]

    def draw(self, node: Node):
        x, y = node.get_position()
        color: str = node.status
        if (x, y) in self.rects:
            old_rect = self.rects[(x, y)]
            self.canvas.delete(old_rect)

        x_pos: int = x * self.node_size
        y_pos: int = y * self.node_size
        rect = self.canvas.create_rectangle(x_pos, y_pos, x_pos+self.node_size, y_pos + self.node_size, fill=color)
        self.rects[(x, y)] = rect
