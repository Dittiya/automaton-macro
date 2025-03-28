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
    name: str
    type: int
    x: int 
    y: int 
    width: int 
    height: int 
    connection: list["Node"]

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
