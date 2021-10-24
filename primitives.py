from enum import Enum
import numpy


class Vector:
    x: int
    y: int
    value: int

    def __init__(self, x: int, y: int, value: int) -> None:
        self.SetValues(x, y, value)

    def SetValues(self, x: int, y: int, value: int):
        self.value = value
        self.x = x
        self.y = y
        if x < 0:
            self.x = -1
        elif x > 0:
            self.x = 1
        if y < 0:
            self.y = -1
        elif y > 0:
            self.y = 1

    def GetMovement(self):
        return self.x*self.value, self.y*self.value


class Point:
    x: int
    y: int

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class PlayerTypeEnum(Enum):
    Human = 1
    Computer = 2

class BeatingDirectionEnum(Enum):
    noBeat = 1
    forward = 2
    backward = 3


class PositionMoves:
    x: int
    y: int
    moves = numpy.zeros((3, 3))

    def __init__(self, x, y, moves):
        self.x = x
        self.y = y
        self.moves = moves


class Move:
    position: Point
    direction: Vector

    def __init__(self, point: Point, movement: Vector):
        self.position = point
        self.direction = movement

    def GetNextPosition(self):
        return Point(self.position.x + self.direction.x, self.position.y + self.direction.y)
