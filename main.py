import fanorona as game
from Players import *
import statistics
import time
from AiAlgorithms import AlphaBeta, MinMax, ABIterative, PNS


def PlayARandomGame():

    engine = game.Board()
    player1 = Player(PlayerTypeEnum.Human, "uno", 1)
    player2 = Player(PlayerTypeEnum.Human, "dos", 2)

    moveamount = []
    elapsed_time = []
    movecounter = 0
    player = player1
    allMoves = engine.GetAllPlayerMovements(player.playerNumber)
    movecount = len(allMoves)
    moveamount.append(movecount)

    while movecount > 0:
        movecounter += 1

        if player == player2:
            moveVal, board, changePlayer = player.AIRandom(engine)
            engine.fields = board
        else:
            t = time.process_time()
            pnsPlayer = ABIterative(player)
            moveVal, board, changePlayer = pnsPlayer.AI_ABIterative(engine, 1)

            engine.fields = board

        if engine.GetPawnAmount(player.playerNumber) < 3:
            pns = PNS(player1)
            pns.AIPNS(engine)


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
    timeOfMinMaxMove = []
    timeOfMinMaxGame = []
    MoveCountList = []
    meanPossibleMoveAmountList = []
    winsList = []

    for i in range(10):
        t = time.process_time()
        print(i)
        count, moveAmountList, wins = PlayARandomGame()
        MoveCountList.append(count)
        winsList.append(wins)
        meanPossibleMoveAmountList.append(statistics.mean(moveAmountList))
        timeOfMinMaxGame.append(time.process_time() - t)

    print(statistics.mean(meanPossibleMoveAmountList))
    print(statistics.mean(MoveCountList))
    print(statistics.mean(winsList))
    print(statistics.mean(timeOfMinMaxMove))
    print(statistics.mean(timeOfMinMaxGame))


main()
