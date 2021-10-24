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

    # TODO dla pewności blokować przejścia na nie puste miejsca(ale ruchy powinny być robione z listy dostępnych więc wyjebane)
    #zwraca nową planszę, boola informującego czy pionek zbił i kierunek bicia
    def MakeMove(self, board: Board, move: Move, beatingDirection: BeatingDirectionEnum):
        boardCopy = board.fields.copy()

        currentPos = move.position

        nextPos = move.GetNextPosition()

        # result bool that shows if something was beaten
        wasBeaten = False

        #get enemy and player number
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
        if beatingDirection == BeatingDirectionEnum.forward:
            while (tmpX < 8 and tmpY < 8 and tmpX > 0 and tmpY > 0):
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
            while (tmpX < 8 and tmpY < 8 and tmpX > 0 and tmpY > 0):
                tmpX -= move.direction.x
                tmpY -= move.direction.y
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True

        return boardCopy, wasBeaten, move.direction

    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)
