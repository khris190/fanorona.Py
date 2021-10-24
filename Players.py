from primitives import *


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
