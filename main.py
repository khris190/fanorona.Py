from numpy import true_divide
import fanorona as game
from primitives import *
from Players import *

engine = game.Board()


def main():
    print(engine.fields[:][:])
    player = Player(PlayerTypeEnum.Human, 'play')
    test = engine.GetAllPlayerMovements(2)
    board, wasbeat, direction = player.MakeMove(engine, Move(Point(4,3),Vector(0,-1,1)), BeatingDirectionEnum.forward)
    engine.fields = board
    print(board[:][:])
    board, wasbeat, direction = player.MakeMove(engine, Move(Point(4,2),Vector(0,-1,1)), BeatingDirectionEnum.forward)
    engine.fields = board
    print(board[:][:])
    board, wasbeat, direction = player.MakeMove(engine, Move(Point(5,3),Vector(-1,-1,1)), BeatingDirectionEnum.forward)
    engine.fields = board
    print(board[:][:])
    board, wasbeat, direction = player.MakeMove(engine, Move(Point(4,1),Vector(-1,0,1)), BeatingDirectionEnum.backward)
    print(board[:][:])
main()  