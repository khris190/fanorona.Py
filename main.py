import fanorona as game
from Players import *
import statistics
import time
from AiAlgorithms import AlphaBeta, MinMax, ABIterative, PNS, MonteCarlo


def PlayARandomGame():

    engine = game.Board()
    player1 = Player(PlayerTypeEnum.Human, "uno", 1)
    player2 = Player(PlayerTypeEnum.Human, "dos", 2)

    moveamount = []
    WinFindTimes = []
    FoundWinAmount = []
    movecounter = 0
    player = player1
    allMoves = engine.GetAllPlayerMovements(player.playerNumber)
    movecount = len(allMoves)
    moveamount.append(movecount)
    doLoop = True
    while movecount > 0 and doLoop:
        movecounter += 1

        if player == player2:
            moveVal, board, changePlayer = player.AIRandom(engine)
            engine.fields = board
        else:
            play = MonteCarlo(player)
            moveVal, board, changePlayer = play.AIMonteCarlo(engine, 5)
            engine.fields = board



        if changePlayer:
            print(engine.fields[:][:])
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
    timeOfMinMaxGame = []
    MoveCountList = []
    meanPossibleMoveAmountList = []
    P1WonAmount = []
    for i in range(20):
        t = time.process_time()
        print(i)
        count, moveAmountList, P1Won = PlayARandomGame()
        MoveCountList.append(count)
        meanPossibleMoveAmountList.append(statistics.mean(moveAmountList))
        P1WonAmount.append(P1Won)
        timeOfMinMaxGame.append(time.process_time() - t)
    
    print(statistics.mean(meanPossibleMoveAmountList))
    print(statistics.mean(MoveCountList))
    print(statistics.mean(timeOfMinMaxGame))
    print(statistics.mean(P1WonAmount))


main()
