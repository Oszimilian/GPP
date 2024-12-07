from node import Node
from position import Position
from typing import List
from enum import Enum



class Grid:
    def __init__(self, x_size : float, y_size : float, x_steps : float, y_steps : float, z : float):
        self.x_grid : float = x_size / x_steps
        self.y_grid : float = y_size / y_steps

        self.x_size : float = x_size
        self.y_size : float = y_size
        self.x_steps : float = x_steps
        self.y_steps : float = y_steps

        self.nodes : List[Node] = []


        self.create_nodes(z=z)
        self.connect_neighbours()

    def get_node_from_position(self, position : Position) -> Node:
        for node in self.nodes:
            if node.get_position() == position:
                return node
        return None

    def get_path(self, start_node : Node, dest_node : Node) -> List[Node]:
        all_paths : List[List[Node]] = start_node.dfs_path(dest_node=dest_node)       
        all_paths = list(filter(lambda a : len(a) > 0, all_paths))
        shortest_path = min(all_paths, key=len)
        return shortest_path 
            

    def create_nodes(self, z : float):
        for x in range(self.x_steps + 1):
            for y in range(self.y_steps + 1):
                position : Position = Position(x * self.x_grid, y * self.y_grid, z)
                node : Node = Node(position=position)
                self.nodes.append(node)

    def connect_neighbours(self):
        for node in self.nodes:
            neighbours : List[Node] = self.get_neighbours(node=node, epsilon=0.01)
            #print(node.get_position())
            for neighbour in neighbours:
                angle = node.get_position().get_angle(neighbour.get_position())
                match angle:
                    case 0.0:
                        node.set_right_node(neighbour)
                    case 90.0:
                        node.set_up_node(neighbour)
                    case 180.0:
                        node.set_left_node(neighbour)
                    case 270.0:
                        node.set_down_node(neighbour)
                    case _:
                        pass

    def get_neighbours(self, node : Node, epsilon : float) -> List[Node]:
        neighbours : List[Node] = []
        for tmp in self.nodes:
            if node.get_position().is_grid_neighbour(tmp.get_position()):
                angle : float = node.get_position().get_angle(tmp.get_position())
                distance : float = node.get_position().get_distance(tmp.get_position())
                if angle == 0.0 or angle == 180:
                    if distance > (self.x_grid - epsilon) and distance < (self.x_grid + epsilon):
                        neighbours.append(tmp)
                elif angle == 90.0 or angle == 270.0:
                    if distance > (self.y_grid - epsilon) and distance < (self.y_grid + epsilon):
                        neighbours.append(tmp)
        return neighbours


    def __str__(self):
        output_str : str = ''
        for node in self.nodes:
            output_str += f"{node} \n"
        return output_str
            

grid : Grid = Grid(x_size=3.8, y_size=3.8, x_steps=19, y_steps=19, z=0.5)

start_node : Node = grid.get_node_from_position(Position(x=0.0, y=0.0, z=0.5))
dest_node: Node = grid.get_node_from_position(Position(x=2.0, y=1.4, z=0.5))

path = grid.get_path(start_node=start_node, dest_node=dest_node)
path = list(map(lambda a : a.get_position(), path))
for pos in path:
    print(pos)


#print(grid)