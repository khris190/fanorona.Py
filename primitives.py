from enum import Enum


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


class Point:
    x: int
    y: int

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class PlayerTypeEnum(Enum):
    Human = 1
    Computer = 2


class Player:
    playerType: PlayerTypeEnum
    Name: str
    lastMoveDirection: Vector
    lastMove: Point

    def __init__(self, type: PlayerTypeEnum, name: str) -> None:
        self.playerType = PlayerTypeEnum
        self.Name = name

    def MakeMove(self, fromLoc: Point, toLoc: Point) -> bool:
        pass

    def AI(self) -> bool:
        pass
