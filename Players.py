import random

from typing import Tuple

from primitives import *
from fanorona import Board
import random

infinityEval = 2147483648
infinity = 32767


class Player:
    playerType: PlayerTypeEnum
    Name: str
    playerNumber: int
    lastMoveDirection: Vector
    lastMove: Point

    def __init__(self, type: PlayerTypeEnum, name: str, playerNumber: int) -> None:
        self.playerType = PlayerTypeEnum
        self.Name = name
        self.playerNumber = playerNumber

    @classmethod
    def MakeMove(cls, board: Board, move: Move) -> Tuple[numpy.ndarray, list]:
        boardCopy = board.fields.copy()

        currentPos = move.position

        nextPos = move.GetNextPosition()

        # result bool that shows if something was beaten
        wasBeaten = False

        # get enemy and player number
        player = 2
        enemy = 1
        if boardCopy[currentPos.y][currentPos.x] == 1:
            player = 1
            enemy = 2

        # remove current pos
        boardCopy[currentPos.y][currentPos.x] = 0
        # add new pos
        boardCopy[nextPos.y][nextPos.x] = player

        tmpX = nextPos.x
        tmpY = nextPos.y
        if move.beatType == BeatingDirectionEnum.forward:
            tmpX += move.direction.x
            tmpY += move.direction.y
            while (tmpX <= 8 and tmpY <= 4 and tmpX >= 0 and tmpY >= 0):
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True
                tmpX += move.direction.x
                tmpY += move.direction.y
        # beat backward
        else:
            tmpX = currentPos.x
            tmpY = currentPos.y
            tmpX -= move.direction.x
            tmpY -= move.direction.y
            while (tmpX <= 8 and tmpY <= 4 and tmpX >= 0 and tmpY >= 0):
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True
                tmpX -= move.direction.x
                tmpY -= move.direction.y

        # sprawdzić czy wszystkie ruchy są bez bicia
        nextMoves = []
        if wasBeaten:
            tmpBoard = Board()
            tmpBoard.fields = boardCopy
            # print(boardCopy[:][:])
            nextmove = tmpBoard.GetEmptyPlacesForMovement(nextPos.x, nextPos.y)

            nextmove[move.direction.y + 1][move.direction.x + 1] = 0
            nextmove[-move.direction.y + 1][-move.direction.x + 1] = 0

            tmpBoard.FindBeatingPossibleMoves(player, nextPos.x, nextPos.y, nextmove)
            tmpBoard.RefineMoves(nextmove)
            tmpMoves = Move.CreateMovesListFromPositionMoves(PositionMoves(nextPos.x, nextPos.y, nextmove))

            if tmpBoard.RefineMoves(nextmove) and tmpMoves != None:
                tmpMoves = Move.CreateMovesListFromPositionMoves(PositionMoves(nextPos.x, nextPos.y, nextmove))
                for tmpmove in tmpMoves:
                    if tmpmove.beatType != BeatingDirectionEnum.noBeat:
                        nextMoves.append(tmpmove)
                        if tmpmove.beatType == BeatingDirectionEnum.noBeat:
                            nextMoves = []
                            break
            else:
                nextMoves = []

        return boardCopy, nextMoves

    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)

    # random move
    def AIRandom(self, board: Board):

        allMoves = board.GetAllPlayerMovements(self.playerNumber)
        movecount = len(allMoves)
        retChangePlayer = True

        if movecount != 0:
            board1, allMoves = self.MakeMove(
                board, allMoves[random.randint(0, movecount - 1)])
            if allMoves != None and len(allMoves) > 0:
                retChangePlayer = False

        return 0, board1, retChangePlayer
