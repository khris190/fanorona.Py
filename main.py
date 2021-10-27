from numpy import true_divide
import fanorona as game
from primitives import *
from Players import *
import random
import statistics



def PlayARandomGame():

    engine = game.Board()
    player1 = Player(PlayerTypeEnum.Human, "uno", 1)
    player2 = Player(PlayerTypeEnum.Human, "dos", 2)

    moveamount = []
    movecounter = 0
    player = player1
    allMoves = engine.GetAllPlayerMovements(player.playerNumber)
    movecount = len(allMoves)
    moveamount.append(movecount)

    while movecount > 0:
        movecounter += 1


        moveVal, board, changePlayer = player.AI_MinMax(3, engine)
        engine.fields = board
        print(engine.fields[:][:])

        if changePlayer:
            if player == player1:
                player = player2
            else:
                player = player1

        allMoves = engine.GetAllPlayerMovements(player.playerNumber)
        movecount = len(allMoves)
        moveamount.append(movecount)
    return movecounter, moveamount


def main():
    MoveCountList = []
    meanPossibleMoveAmountList = []

    for i in range(1):
        print(i)
        count, moveAmountList = PlayARandomGame()
        MoveCountList.append(count)
        meanPossibleMoveAmountList.append(statistics.mean(moveAmountList))

    print(statistics.mean(meanPossibleMoveAmountList))
    print(statistics.mean(MoveCountList))

main()
