from typing import ForwardRef
import numpy
from primitives import *


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

    def GetAllPlayerMovements(self, player: int):
        moves = []
        for i in range(5):
            for j in range(9):
                if self.fields[i][j] == player:
                    move = self.GetEmptyPlacesForMovement(j, i)
                    if any(1 in sublist for sublist in move):
                        self.FindBeatingPossibleMoves(player, j, i, move)
                        self.RefineMoves(move)
                        moves.append(Move(j, i, move))
        return moves

    def RefineMoves(self, moves: list):
        doRefine = False
        for move in moves:
            for x in move:
                if x > 1:
                    doRefine = True
        if doRefine:
            for move in moves:
                for x in move:
                    if x == 1:
                        x = 0

    def FindBeatingPossibleMoves(self, player: int, x: int, y: int, moves):
        dirX = 0
        dirY = 0
        resMoves = numpy.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                dirX = j - 1
                dirY = i - 1
                if moves[i][j] == 1:
                    resMoves[i][j] = self.CheckFrontandBackForBeat(
                        player, x, y, dirX, dirY)
        return resMoves

    # returns 1 if movement is possible without beating
    # 2 if movement is possible with forward beat
    # 3 if movement is possible with backward beat and
    # 4 if movement is possible with both forward and backward

    def CheckFrontandBackForBeat(self, player, x, y, dirX, dirY) -> int:
        enemy = 1
        if player == 1:
            enemy = 2
        forward = False
        backward = False
        # check front
        tmpX = x + 2 * dirX
        tmpY = y + 2 * dirY
        if tmpX < 9 and tmpY < 9 and tmpX >= 0 and tmpY >= 0:
            forward = (self.fields[tmpY][tmpX] == enemy)
        # check back
        tmpX = x - dirX
        tmpY = y - dirY
        if tmpX < 9 and tmpY < 9 and tmpX >= 0 and tmpY >= 0:
            backward = (self.fields[tmpY][tmpX] == enemy)
        if forward and backward:
            return 4
        if backward:
            return 3
        if forward:
            return 2
        return 1

    def GetEmptyPlacesForMovement(self, x: int, y: int):
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


#class env:
#    board: Board
#    player1 = Player(PlayerTypeEnum.Human, "1")
#    player2 = Player(PlayerTypeEnum.Human, "2")
#
#    def __init__(self) -> None:
#        pass
