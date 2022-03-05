from enum import Enum


class NodeStatus(Enum):
    Unvisited = '#ffffff'
    Visited = '#ff00ff'
    Obstacle = '#000000'
    StartNode = '#00ff00'
    EndNode = '#ffff00'
    PathNode = '#0000ff'
