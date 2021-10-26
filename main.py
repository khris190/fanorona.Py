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

        #print(board[:][:])

        board, wasbeat, direction, allMoves = player.MakeMove(
            engine, allMoves[random.randint(0, movecount - 1)])
        engine.fields = board

        #zrobić resztę ruchów i nie wiem czy je liczyć i jak więc idc
        while allMoves != None and len(allMoves) > 0:
            movecount = len(allMoves)
            moveamount.append(movecount) 
            movecounter += 1

            board, wasbeat, direction, allMoves = player.MakeMove(
                engine, allMoves[random.randint(0, movecount - 1)])
            engine.fields = board


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

    for i in range(5000):
        print(i)
        count, moveAmountList = PlayARandomGame()
        MoveCountList.append(count)
        meanPossibleMoveAmountList.append(statistics.mean(moveAmountList))

    print(statistics.mean(meanPossibleMoveAmountList))
    print(statistics.mean(MoveCountList))




main()
