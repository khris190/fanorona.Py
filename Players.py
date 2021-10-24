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
    def MakeMove(self, move: Move, board: Board) -> None:
        pass



    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)
