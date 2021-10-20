import enum
import numpy
from enum import Enum

class Board:
    fields = numpy.zeros((5, 9))

    def __init__(self) -> None:
        self.fields[:2][:] = 1
        self.fields[2][:4:2] = 1
        self.fields[2][1:4:2] = 2

        self.fields[2][5::2] = 1
        self.fields[2][6::2] = 2
        self.fields[3:][:] = 2

    # if x + y %2 == 0 to ruchy 8 ruchów else 4

    def CheckPossibleMoves(self, x: int, y: int):
        tmpX = x
        tmpY = y
        res = numpy.zeros((3, 3))

        if (x + y) % 2 == 0:
            for i in range(3):
                for j in range(3):
                    res[i][j] = self.IsEmpty(y+i-1, x+j-1)
        else:
            res[1][2] = self.IsEmpty(y, x+1)
            res[1][0] = self.IsEmpty(y, x-1)
            res[2][1] = self.IsEmpty(y+1, x)
            res[0][1] = self.IsEmpty(y-1, x)
        print(res[:][:])
        return res

    def IsEmpty(self, y, x) -> bool:
        if 0 <= x < 9 and 0 <= y < 5:
            return self.fields[y][x] == 0
        else:
            return False

    # def move(self, x, y, xDest, yDest) -> bool:

class Vector:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.SetValues(x, y)
    
    def SetValues(self, x: int, y: int):
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
    x : int
    y : int

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class PlayerType(Enum):
    Human = 1
    Computer = 2

class Player:
    playerType : PlayerType
    Name : str
    lastMoveDirection : Vector
    lastMove : Point

    def __init__(self, type : PlayerType, name : str) -> None:
        self.playerType = PlayerType
        self.Name = name

    def MakeMove(self, fromLoc : Point, toLoc : Point) -> bool:
        pass

    def AI(self) -> bool:
        pass


class env:
    board : Board


