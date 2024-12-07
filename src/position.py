import math

class Position:
    def __init__(self, x : float, y : float, z : float):
        self.x : float = x
        self.y : float = y
        self.z : float = z

        self.epsilon : float = 0.01

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"
    
    def get_x(self) -> float:
        return self.x
    
    def get_y(self) -> float:
        return self.y
    
    def get_z(self) -> float:
        return self.z
    
    def get_distance(self, position : "Position") -> float:
        x_diff : float = abs(self.x - position.get_x())
        y_diff : float = abs(self.y - position.get_y())
        z_diff : float = abs(self.z - position.get_z())

        distance : float = math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2) + math.pow(z_diff, 2))

        return distance
    
    def is_grid_neighbour(self, position : "Position") -> bool:
        x_diff : float = abs(self.x - position.get_x())
        y_diff : float = abs(self.y - position.get_y())

        is_grid_neighbour : bool = ((x_diff == 0 and y_diff != 0) or (x_diff != 0 and y_diff == 0))

        return is_grid_neighbour
    
    def get_angle(self, position : "Position") -> bool:
        x_diff : float = self.x - position.get_x()
        y_diff : float = self.y - position.get_y()

        angle : float = 0
        is_grid_neighbour : bool = self.is_grid_neighbour(position=position)

        if is_grid_neighbour == True:
            if x_diff == 0:
                angle = 90.0 if y_diff > 0 else 270.0
            else:
                angle = 0.0 if x_diff > 0 else 180.0
        else:
            angle = math.atan(y_diff / x_diff) * 180 / 3.1415

        return angle
    
    def __eq__(self, position : "Position"):
        if abs(position.get_x() - self.x) > self.epsilon:
            return False
        if abs(position.get_y() - self.y) > self.epsilon:
            return False
        if abs(position.get_z() - self.z) > self.epsilon:
            return False
        return True
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
