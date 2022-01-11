
import copy
import random
import secrets
from abc import ABC
from time import time, time_ns
from Players import Player
from fanorona import Board
from Players import infinityEval, infinity
import AiAlgorithms.AlphaBeta
import time


class MonteCarlo:
    player: 'Player' = None

    def __init__(self, player):
        self.player = player

    def selectMove(self, depth : int, moves: list, board: Board):
        return self.monteCarloSearch(moves, board)

    def AIMonteCarlo(self, board: Board, depth: int):
        moves = board.GetAllPlayerMovements(self.player.playerNumber)
        #its gonna be a hack
        while len(moves) != 0:
            bestMove = self.MontecarloSearch(depth, moves, board)
            retBoard, moves = Player.MakeMove(board, bestMove)
            board.fields = retBoard
            if depth > 1:
                depth -= 1
        
        return 0, retBoard, 1

    def MontecarloSearch(self, depth : int, moves: list, board: Board):
        boardCopy = copy.deepcopy(board)
        bestChild = None
        bestProbabality = -1
        opponent = self.player.playerNumber
        for move in moves:
            r = 0
            for i in range(depth):
                # 5 lines just to make a move
                retBoard, retMoves = Player.MakeMove(board, move)


                boardCopy.fields = retBoard
                if len(retMoves) == 0:
                    opponent = Player.GetEnemy(opponent)
                    retMoves = boardCopy.GetAllPlayerMovements(opponent)
                
                

                while not self.isEndMove(boardCopy, opponent):
                    retBoard, retMoves = Player.MakeMove(boardCopy, retMoves[random.randint(0, len(retMoves) - 1)])
                    boardCopy.fields = retBoard
                    if len(retMoves) == 0:
                        opponent = Player.GetEnemy(opponent)
                        retMoves = boardCopy.GetAllPlayerMovements(opponent)
                
                if self.isWinMove(boardCopy, self.player.playerNumber):
                    r += 1
            probability = r / depth
            if probability > bestProbabality:  
                bestChild = move
                bestProbabality = probability
        return bestChild




    def isEndMove(self, board : 'Board', player_num : int) -> bool:
        return not (-100 < board.CalculatePlayerLead(player_num) < 100)

    def isWinMove(self, board : 'Board', player_num : int) -> bool:
        return not (board.CalculatePlayerLead(player_num) < 100)
