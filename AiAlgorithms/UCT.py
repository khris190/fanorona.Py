import copy

from time import time, time_ns

import numpy as np

from Players import Player
from fanorona import Board
from Players import infinityEval, infinity
import AiAlgorithms.AlphaBeta
import time


class UCT:
    player: 'Player' = None

    startTime = 0.0
    maxTime = 2.0
    infinity = 32767

    def __init__(self, player):
        self.player = player

    def selectMove(self, depth: int, moves: list, board: Board):
        return self.UCTSearch(moves, board, depth)

    def UCTSearch(
            self,
            moves: list,
            board: 'Board',
            depth: int
    ):
        root = Node(board, self.player, None, None, moves)

        for i in range(depth):
            current = Node.treePolicy(root)
            reward = Node.defaultPolicy(current)
            Node.backup(current, reward)

        return Node.bestChild(root).move

class Node:
    player: 'Player' = None
    move: 'Move' = None
    board: 'Board' = None
    player: 'Player' = None

    results = {
        'win': 0,
        'lose': 0
    }

    children: list = []

    __numberOfVisits: int = 0
    __parent: 'Node' = None
    __untriedActions: list = []

    startTime = 0.0
    maxTime = 2.0
    infinity = 32767

    def __init__(
            self,
            player,
            board,
            move,
            parent,
            moves: list = None

    ):
        self.player = player
        self.board = board
        self.move = move
        self.__parent = parent

    def treePolicy(self) -> 'Node':
        self.startTime = time.process_time()
        while (time.process_time() - self.startTime) < self.maxTime:
            if self.isFullyExpanded() is False:
                return Node.expand(Node)
            else:
                node = Node.bestChild(self)
        return self

    def isFullyExpanded(self):
        return len(self.__untriedActions) == 0

    def v(self):
        return self.results['win'] - self.results['lose']

    def n(self):
        return self.__numberOfVisits

    def nIncrease(self):
        self.__numberOfVisits = self.__numberOfVisits + 1

    @classmethod
    def bestChild(cls, node: 'Node', cParam=0.2):
        choicesWeights = [
            (child.v() / child.n()) + cParam * np.sqrt((2 * np.log(node.n()) / child.n())) for child in node.children
        ]
        if len(choicesWeights):
            return node.children[np.argmax(choicesWeights)]

        return None


    def expand(self, node: 'Node'):
        child = Node(node.board, node.__untriedActions.pop(), node)
        node.children.append(child)

        return child

    def defaultPolicy(self) -> str:
        boardCopy = copy.deepcopy(self.board)
        current = self
        opponent = Player.GetEnemy(1)
        self.startTime = time.process_time()
        while (time.process_time() - self.startTime) < self.maxTime:
            childMove = Player.MakeMove(boardCopy, current.move)
            current = Node(opponent, boardCopy, childMove, self)

        return 'win' if boardCopy.GetPawnAmount(self.player.playerNumber) else 'lose'

    def getParent(self):
        return self.__parent

    @classmethod
    def backup(cls, node: 'Node', reward: str):
        while node is not None:
            node.nIncrease()
            node.results[reward] += 1
            node = node.getParent()
