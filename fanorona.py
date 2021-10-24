import enum

import board as board
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

    def FindAllPossibleMovesForPlayer(self, player: int):
        moves = numpy.zeros((5, 9, 3, 3), numpy.int8)
        for i in range(5):
            for j in range(9):
                if self.fields[i][j] == player:
                    moves[i][j] = self.CheckPossibleMoves(j, i)
        return moves

    # TODO funkcja sprawdzająca czy któryś z możliwych ruchów zbija pionki przeciwnika
    # na wejściu x, y - pole planszy, typ playera typu int
    # int[3][3] - możliwe ruchy bez uwzględnienia czy któryś zbija czy nie
    # na wyściu int[3][3] gdzie 0 brak ruchu, 1 ruch zbijający na zbiżeniu 2 zbijający na oddaleniu i 3 obie typy zbicia

    # [mk] Wydaje mi się że powinno działać, ale nie sprawdzałem, bo nie chciało mi się wyciągać tych pól z biciem

    def FindBeatingPossibleMoves(self, player: int, x: int, y: int, board):
        tmpX = x
        tmpY = y
        focusOn = False
        focusOut = False
        beatingmoves = numpy.zeros((3, 3), numpy.int8)
        if self.fields[x][y] == player:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 1:
                        directionX = (i - 1)
                        directionY = (j - 1)
                        while not (tmpX == 9 or tmpX == -1 or tmpY == 5 or tmpY == -1):
                            tmpX += directionX
                            tmpY += directionY
                            if (self.fields[tmpX][tmpY] != player and self.fields[tmpX][tmpY]) != 0:
                                focusOn = True
                        directionX *= -1
                        directionY *= -1
                        tmpX = x
                        tmpY = y
                        while not (tmpX == 9 or tmpX == -1 or tmpY == 5 or tmpY == -1):
                            tmpX += directionX
                            tmpY += directionY
                            if (self.fields[tmpX][tmpY] != player and self.fields[tmpX][tmpY]) != 0:
                                focusOut = True
                        if (focusOn == True and focusOut == True):
                            beatingmoves[i][j] = 3
                        elif (focusOn == False and focusOut == True):
                            beatingmoves[i][j] = 2
                        elif (focusOn == True and focusOut == False):
                            beatingmoves[i][j] = 1
                        elif (focusOn == False and focusOut == False):
                            beatingmoves[i][j] = 0
                        focusOut = False
                        focusOn = False
                    else:
                        beatingmoves[i][j] = 0
        return beatingmoves

    def CheckPossibleMoves(self, x: int, y: int):
        tmpX = x
        tmpY = y
        res = numpy.zeros((3, 3))

        if (x + y) % 2 == 0:
            for i in range(3):
                for j in range(3):
                    res[i][j] = self.IsEmpty(y + i - 1, x + j - 1)
        else:
            res[1][2] = self.IsEmpty(y, x + 1)
            res[1][0] = self.IsEmpty(y, x - 1)
            res[2][1] = self.IsEmpty(y + 1, x)
            res[0][1] = self.IsEmpty(y - 1, x)
        # print(res[:][:])
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


class env:
    board: Board
    player1 = Player(PlayerTypeEnum.Human, "1")
    player2 = Player(PlayerTypeEnum.Human, "2")

    def __init__(self) -> None:
        pass
