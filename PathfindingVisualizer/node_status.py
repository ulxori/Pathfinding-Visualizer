from enum import Enum


class NodeStatus(Enum):
    Unvisited = '#ffffff'
    Visited = '#0000ff'
    Obstacle = '#000000'
    StartNode = '#00ff00'
    EndNode = '#ff00ff'
    Path = '#0f0f0f'
