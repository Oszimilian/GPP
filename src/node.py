from position import Position
from typing import List
from functools import lru_cache

def memoize_dfs(func):
    """
    Ein Dekorator, um DFS-Ergebnisse zu memoizieren.
    """
    cache = {}  # Ein Cache, um berechnete Ergebnisse zu speichern

    def wrapper(node, path, all_paths, visited_cache):
        # Wenn wir den Knoten schon besucht haben, geben wir den gespeicherten Wert zurück
        cache_key = (id(node), tuple(path))  # Einfache Möglichkeit, den Pfad als Cache-Schlüssel zu verwenden

        if cache_key in cache:
            return cache[cache_key]

        result = func(node, path, all_paths, visited_cache)
        cache[cache_key] = result
        return result

    return wrapper

class Node:
    def __init__ (self, position : Position):
        self.position = position

        self.up_node : Node = None
        self.right_node : Node = None
        self.down_node : Node = None
        self.left_node : Node = None

        self.visit : bool = False

    def get_visit(self) -> bool:
        return self.visit

    def set_visit(self, val : bool):
        self.visit = val

    
    def __eq__(self, other: "Node") -> bool:
        return self.position == other.position

    def __hash__(self) -> int:
        return hash(self.position)
    
    def dfs_path(self, dest_node : "Node", path : List["Node"] = [], all_paths : List[List["Node"]] = [[]], visited : List["Node"] = []) -> List[List["Node"]]:
        path.append(self)
        if self == dest_node:
            all_paths.append(path[:])
        else:
            for neighbor in [self.up_node, self.right_node, self.down_node, self.left_node]:
                if neighbor:
                    if neighbor not in visited:
                        if neighbor not in path:
                            neighbor.dfs_path(dest_node, path, all_paths, visited=visited)
                        else:             
                            for i in range(path.index(neighbor), len(path)):
                                visited.append(path[i])
        path.pop()
        return all_paths

    def __str__(self) -> str: 
        output_str : str = ''
        output_str += f"{self.get_position()} \n"
        output_str += f"UP \t {self.up_node.get_position()} \n" if self.up_node != None else "UP \t Boarder \n"
        output_str += f"RIGHT \t {self.right_node.get_position()} \n" if self.right_node != None else "UP \t Boarder \n"
        output_str += f"DOWN \t {self.down_node.get_position()} \n" if self.down_node != None else "UP \t Boarder \n"
        output_str += f"LEFT \t {self.left_node.get_position()} \n" if self.left_node != None else "UP \t Boarder \n"
        return output_str
    
    def disconnect(self):
        if self.up_node:
            self.up_node.set_down_node(None)
        if self.right_node:
            self.right_node.set_left_node(None)
        if self.down_node:
            self.down_node.set_up_node(None)
        if self.left_node:
            self.left_node.set_right_node(None)


    def get_position(self) -> Position:
        return self.position

    def set_up_node(self, node : "Node"):
        self.up_node = node

    def set_right_node(self, node : "Node"):
        self.right_node = node

    def set_down_node(self, node : "Node"):
        self.down_node = node

    def set_left_node(self, node : "Node"):
        self.left_node = node

    def get_up_node(self) -> "Node":
        return self.up_node
    
    def get_right_node(self) -> "Node":
        return self.right_node
    
    def get_down_node(self) -> "Node":
        return self.down_node
    
    def get_left_node(self) -> "Node":
        return self.left_node

