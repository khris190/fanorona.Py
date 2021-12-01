from Players import Player
from fanorona import Board
from Players import infinityEval, infinity
import AiAlgorithms.AlphaBeta
import time


class ABIterative:
    player: 'Player' = None

    def __init__(self, player):
        self.player = player

    def AI_ABIterative(self, board: 'Board', maxTime: float = 1.0):

        t = time.process_time()
        for i in range(2, infinity):
            alphaBeta = AiAlgorithms.AlphaBeta(self.player)
            moveVal, retBoard, changePlayer = alphaBeta.AI_AlphaBeta(i, board)
            if time.process_time() - t > (maxTime/2):
                print(i)
                break

        return moveVal, retBoard, changePlayer