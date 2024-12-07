from grid import Grid
from node import Node
from typing import List


class Path:
    def __init__(self, grid : Grid):
        self.path : List[Node] = []
