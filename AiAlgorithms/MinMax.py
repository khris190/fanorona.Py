from Players import Player
from fanorona import Board
from Players import infinityEval, infinity


class MinMax:
    player: 'Player' = None

    def __init__(self, player):
        self.player = player

    def AI_MinMax(self, depth: int, board: 'Board'):
        movesList = board.GetAllPlayerMovements(self.player.playerNumber)

        value = -infinityEval
        winValue = value
        retBoard = Board()
        retBoard.fields = board.fields.copy()
        retChangePlayer = False

        for move in movesList:
            tmpBoard = Board()
            tmpBoard.fields = board.fields.copy()
            returnedBoard, allMoves = Player.MakeMove(tmpBoard, move)

            tmpBoard.fields = returnedBoard.copy()
            changePlayer = True

            # liczę kilkukrotne zbicia jako tą samą turę
            if allMoves != None and len(allMoves) > 0:
                value = max(value, self.MinMax(depth, tmpBoard, self.player.playerNumber, allMoves, True))
                changePlayer = False
            else:
                playerNum = 1
                if self.player.playerNumber == 1:
                    playerNum = 2
                movesListtmp = tmpBoard.GetAllPlayerMovements(playerNum)
                value = max(value, self.MinMax(depth - 1, tmpBoard, playerNum, movesListtmp, False))

            if winValue < value:
                winValue = value
                retBoard = tmpBoard
                retChangePlayer = changePlayer

        return winValue, retBoard.fields, retChangePlayer

    def MinMax(self, depth: int, board: Board, playerNumber: int, movesList: list, maximizing: bool):
        nodeVal = board.CalculatePlayerLead(playerNumber)
        if depth < 1 or infinity == nodeVal or infinity == -nodeVal:
            if not maximizing:
                nodeVal *= -1
            return nodeVal

        if maximizing == True:
            value = -infinityEval
            for move in movesList:
                tmpBoard = Board()
                tmpBoard.fields = board.fields.copy()
                returnedBoard, allMoves = Player.MakeMove(tmpBoard, move)
                tmpBoard.fields = returnedBoard.copy()

                # liczę kilkukrotne zbicia jako tą samą turę
                if allMoves != None and len(allMoves) > 0:
                    value = max(value, self.MinMax(depth, tmpBoard, playerNumber, allMoves, True))
                else:
                    playerNum = 1
                    if playerNumber == 1:
                        playerNum = 2
                    movesListtmp = tmpBoard.GetAllPlayerMovements(playerNum)
                    value = max(value, self.MinMax(depth - 1, tmpBoard, playerNum, movesListtmp, False))
            return value
        else:
            value = infinityEval
            for move in movesList:
                tmpBoard = Board()
                tmpBoard.fields = board.fields.copy()
                returnedBoard, allMoves = Player.MakeMove(tmpBoard, move)
                tmpBoard.fields = returnedBoard.copy()

                # liczę kilkukrotne zbicia jako tą samą turę
                if allMoves != None and len(allMoves) > 0:
                    value = min(value, self.MinMax(depth, tmpBoard, playerNumber, allMoves, False))
                else:
                    playerNum = 1
                    if playerNumber == 1:
                        playerNum = 2
                    movesListtmp = tmpBoard.GetAllPlayerMovements(playerNum)
                    value = min(value, self.MinMax(depth - 1, tmpBoard, playerNum, movesListtmp, True))
            return value