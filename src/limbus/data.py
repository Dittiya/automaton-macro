from dataclasses import dataclass
from enum import Enum

@dataclass
class Config:
    x_start: int = 690
    y_start: int = 370
    width: int = 80
    height: int = 80
    x_stride: int = 160
    y_stride: int = 130

@dataclass
class Node:
    id: int
    name: str
    type: int
    x: int 
    y: int 
    width: int 
    height: int 
    connection: list["Node"]

    def get_center(self) -> list:
        return [int(self.x+self.width/2), int(self.y+self.height/2)]
    
    def add_connection(self, node: "Node"):
        return self.connection.append(node)

@dataclass
class Encounter:
    name: str
    type: int
    descriptor: list

class Encounters(Enum):
    EVENT = 0
    ELITE = 1
    FOCUSED = 2
    REGULAR = 3

class Deviations(Enum):
    TOP = -1
    MIDDLE = 0
    BOTTOM = 1