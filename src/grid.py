from node import Node
from position import Position
from typing import List, Dict
from enum import Enum
import collections



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
    
    def get_path(self, start_node: Node, dest_node: Node) -> List[Node]:
        q = collections.deque([start_node])

        visited: List[Dict] = []
        for node in self.nodes:
            visited.append({'node': node, 'visit': False})

        for entry in visited:
            if entry['node'] == start_node:
                entry['visit'] = True

        prev: List[Dict] = []
        for node in self.nodes:
            prev.append({'node': node, 'prev': None})

        while len(q) > 0:
            node = q.popleft()
            for next in [node.get_up_node(), node.get_right_node(), node.get_down_node(), node.get_left_node()]:
                for vis in visited:
                    if vis['node'] == next:
                        if vis['visit'] == False:
                            q.append(next)
                            vis['visit'] = True
                            for p in prev:
                                if p['node'] == next:
                                    p['prev'] = node
        #for p in prev:
        #    print(f"{p['node'].get_position() if p['prev'] != None else 'None'} - {p['prev'].get_position() if p['prev'] != None else 'None'}")

        path : List[Node] = []
        at = dest_node
        while at != None:
            path.append(at)
            for p in prev:
                if p['node'] == at:
                    at = p['prev']

        path.reverse()

        return path



            
    def remove_node_by_position(self, position : Position):
        for node in self.nodes:
            if node.get_position() == position:
                node.disconnect()

    def create_nodes(self, z : float):
        for x in range(self.x_steps + 1):
            for y in range(self.y_steps + 1):
                position : Position = Position(x * self.x_grid, y * self.y_grid, z)
                node : Node = Node(position=position)
                self.nodes.append(node)

    def connect_neighbours(self):
        for node in self.nodes:
            neighbours : List[Node] = self.get_neighbours(node=node, epsilon=0.01)
            for neighbour in neighbours:
                angle = node.get_position().get_angle(neighbour.get_position())
                match angle:
                    case 0.0:
                        node.set_left_node(neighbour)
                    case 90.0:
                        node.set_down_node(neighbour)
                    case 180.0:
                        node.set_right_node(neighbour)
                    case 270.0:
                        node.set_up_node(neighbour)
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
            

grid : Grid = Grid(x_size=0.8, y_size=0.8, x_steps=8, y_steps=8, z=0.5)

start_node : Node = grid.get_node_from_position(Position(x=0.0, y=0.0, z=0.5))
dest_node: Node = grid.get_node_from_position(Position(x=0.7, y=0.6, z=0.5))

grid.remove_node_by_position(position=Position(x=0.0, y=0.1, z=0.5))
grid.remove_node_by_position(position=Position(x=0.1, y=0.5, z=0.5))
path = grid.get_path(start_node=start_node, dest_node=dest_node)



path = list(map(lambda a : a.get_position(), path))
for pos in path:
    print(pos)

