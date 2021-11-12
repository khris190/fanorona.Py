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
    moveVal = 0
    surrendered1 = False
    surrendered2 = False

    while movecount > 0:
        movecounter += 1

        if player == player2:
            moveVal, board, changePlayer = player.AIRandom(engine)
            engine.fields = board

        else:
            moveVal, board, changePlayer = player.AI_MinMax(2, engine)
            engine.fields = board

        if changePlayer:
            if player == player1:
                player = player2
            else:
                player = player1

        allMoves = engine.GetAllPlayerMovements(player.playerNumber)
        movecount = len(allMoves)
        moveamount.append(movecount)
    print(engine.fields[:][:])
    return movecounter, moveamount, engine.CalculatePlayerLead(1) > 0


def main():
    MoveCountList = []
    meanPossibleMoveAmountList = []
    winsList = []

    for i in range(500):
        print(i)
        count, moveAmountList, wins = PlayARandomGame()
        MoveCountList.append(count)
        winsList.append(wins)
        meanPossibleMoveAmountList.append(statistics.mean(moveAmountList))

    print(statistics.mean(meanPossibleMoveAmountList))
    print(statistics.mean(MoveCountList))
    print(statistics.mean(winsList))


main()
