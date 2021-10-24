from primitives import *
from fanorona import Board


class Player:
    playerType: PlayerTypeEnum
    Name: str
    lastMoveDirection: Vector
    lastMove: Point

    def __init__(self, type: PlayerTypeEnum, name: str) -> None:
        self.playerType = PlayerTypeEnum
        self.Name = name

    #TODO sprawdzić czy działa
    def MakeMove(self, board: Board, move: Move) -> None:
        boardCopy = board.fields.copy()

        currentPosX = move.x
        currentPosY = move.y

        nextPosX = currentPosX + move.vectorX
        nextPosY = currentPosY + move.vectorY

        #remove current pos
        boardCopy[currentPosX][currentPosY] = 0
        #add new pos
        boardCopy[nextPosX][nextPosY] = self.playerType

        tmpX = nextPosX
        tmpY = nextPosY

        while not (tmpX < 9 and tmpY < 9 and tmpX >= 0 and tmpY >= 0):
            tmpX += move.vectorX
            tmpY += move.vectorY
            if (boardCopy[tmpX][tmpY] != self.playerType and boardCopy[tmpX][tmpY] != 0 ):
                break
            boardCopy[tmpX][tmpY] = 0

        return boardCopy





    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)
