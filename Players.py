import random

from primitives import *
from fanorona import Board


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

    # TODO dla pewności blokować przejścia na nie puste miejsca(ale ruchy powinny być robione z listy dostępnych więc wyjebane)
    # zwraca nową planszę, boola informującego czy pionek zbił i kierunek bicia
    def MakeMove(self, board: Board, move: Move):
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
            while (tmpX < 8 and tmpY < 4 and tmpX > 0 and tmpY > 0):
                tmpX += move.direction.x
                tmpY += move.direction.y
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True
        # beat backward
        else:
            tmpX = currentPos.x
            tmpY = currentPos.y
            while (tmpX < 8 and tmpY < 4 and tmpX > 0 and tmpY > 0):
                tmpX -= move.direction.x
                tmpY -= move.direction.y
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True

        nextMoves = []
        if wasBeaten:
            tmpBoard = Board()
            tmpBoard.fields = boardCopy
            # print(boardCopy[:][:])
            nextmove = tmpBoard.GetEmptyPlacesForMovement(nextPos.x, nextPos.y)

            nextmove[move.direction.y + 1][move.direction.x + 1] = 0
            nextmove[-move.direction.y + 1][-move.direction.x + 1] = 0

            tmpMoves = tmpBoard.FindBeatingPossibleMoves(player, nextPos.x, nextPos.y, nextmove)
            if tmpBoard.RefineMoves(nextmove):
                tmpMoves = Move.CreateMovesListFromPositionMoves(PositionMoves(nextPos.x, nextPos.y, nextmove))
                for tmpmove in tmpMoves:
                    if tmpmove.beatType != BeatingDirectionEnum.noBeat:
                        nextMoves.append(tmpmove)

        return boardCopy, nextMoves

    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)

    # random move
    def AIRandom(self, board: Board):

        allMoves = board.GetAllPlayerMovements(self.playerNumber)
        movecount = len(allMoves)

        if movecount != 0:
            board1, allMoves = self.MakeMove(
                board, allMoves[random.randint(0, movecount - 1)])
            Board.fields = board1

            while allMoves != None and len(allMoves) > 0:
                movecount = len(allMoves)

                board1, allMoves = self.MakeMove(
                    board, allMoves[random.randint(0, movecount - 1)])
                Board.fields = board1
