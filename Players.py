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

    #TODO zaimplementować ruch i zbijanie w metodzie MakeMove zbijanie przód tył na parametr funkcji
    def MakeMove(self, point: Point, board: Board, vector: Vector) -> None:
        boardCopy = board.fields.copy()

        currentPosX = point.x
        currentPosY = point.y

        nextPosX = currentPosX + vector.x
        nextPosY = currentPosY + vector.y

        #remove current pos
        boardCopy[currentPosX][currentPosY] = 0
        #add new pos
        boardCopy[nextPosX][nextPosY] = self.playerType

        tmpX = nextPosX
        tmpY = nextPosY

        while not (tmpX < 9 and tmpY < 9 and tmpX >= 0 and tmpY >= 0):
            tmpX += vector.x
            tmpY += vector.y
            if (boardCopy[tmpX][tmpY] != self.playerType and boardCopy[tmpX][tmpY] != 0 ):
                break
            boardCopy[tmpX][tmpY] = 0

        return boardCopy





    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)
