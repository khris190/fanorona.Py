from re import T
from typing import Match
from numpy import RAISE, empty, inf
from Players import Player
from fanorona import Board
import enum
import time
import copy
infinity = 2147483648


class Type(enum.IntEnum):
    AND = 0
    OR = 10


class Node:
    board: 'Board'
    parent: 'Node'
    children = []
    disproof: int = 0
    proof: int = 0
    evaluation: int = 0
    expanded = False
    value: int = 0
    player: int = 0
    type: Type

    def __init__(self, type: Type):
        self.type = type


    def generateChildren(self):
        boardList = [Board]
        movesList = self.board.GetAllPlayerMovements(self.player)
        tmpBoard = Board()
        tmpBoard.fields = self.board.fields.copy()
        boardList.extend(self.CutSubtree(tmpBoard, movesList))

        for board in boardList:

            newChild = Node(Type.AND)
            if self.type == Type.AND:
                newChild.type = Type.OR

            newChild.player = 1
            if self.player == 1:
                newChild.player = 2

            newChild.board = Board()
            newChild.board.fields = board.fields.copy()
            newChild.parent = self

            self.children.append(newChild)
            newChild.children = []
          

    def CutSubtree(self, rootBoard: 'Board', movesList) -> list[Board]:
        retBoards = [Board]
        #movesList = board.GetAllPlayerMovements(self.player.playerNumber)
        for move in movesList:
            returnedFields, allMoves = Player.MakeMove(rootBoard, move)
            returnedBoard = Board()
            returnedBoard.fields = returnedFields
            if allMoves != None and len(allMoves) > 0:
                retBoards.extend(returnedBoard)
            else:
                retBoards.extend(self.CutSubtree(returnedBoard, allMoves))
        return retBoards


class PNS:

    root: Node

    player: 'Player' = None

    resourcesAvailable = True
    startTime = 0.0
    maxTime = 2.0

    def __init__(self, player):
        self.player = player
        self.root = Node(Type.OR)
        self.root.player = player.playerNumber


    def AIPNS(self,  Root: 'Board'):
        pass

    def PNS(self,  Root: 'Board'):
        self.root.board = Root
        self.root.evaluation = self.root.board.CalculatePlayerLead(self.player.playerNumber)
        self.SetProofAndDisproofNumbers(self.root)
        current = self.root
        self.startTime = time.process_time()
        while self.root.proof != 0 and self.root.disproof != 0 and self.startTime - time.process_time() < self.maxTime*0.8:
            mostProving = self.SelectMostProvinNode(current)
            self.ExpandNode(mostProving)
            current = self.UpdateAncestors(mostProving, Root)
        return 'jebać ten przedmiot'
        

    def SetProofAndDisproofNumbers(self, currNode: Node):
        if currNode.expanded:
            if currNode.type == Type.AND:
                currNode.proof = 0
                currNode.disproof = infinity
                for child in currNode.children:
                    currNode.proof += child.proof
                    currNode.disproof = min(currNode.disproof, child.disproof)
            else:
                currNode.proof = infinity
                currNode.disproof = 0
                for child in currNode.children:
                    currNode.disproof += child.disproof
                    currNode.disproof = min(currNode.proof, child.proof)
        else:
            if currNode.value == 1:
                currNode.proof = 0
                currNode.disproof = infinity
            elif currNode.value == -1:
                currNode.proof = infinity
                currNode.disproof = 0
            else:
                currNode.proof = 1
                currNode.disproof = 1

    def SelectMostProvinNode(self, node: Node):
        currNode = node
        while currNode.expanded:
            value = infinity
            if currNode.type == Type.AND:
                for child in currNode.children:
                    if value > child.disproof:
                        best = child
                        value = child.disproof
            else:
                for child in currNode.children:
                    if value > child.proof:
                        best = child
                        value = child.proof
            currNode = best
        return currNode
                

    def ExpandNode(self, currNode: Node):
        currNode.generateChildren()
        for child in currNode.children:
            self.Evaluate(child)
            self.SetProofAndDisproofNumbers(child)
            if currNode.type == Type.AND:
                if child.disproof == 0:
                    break
            else:
                if child.proof == 0:
                    break
        currNode.expanded = True
    
    def Evaluate(self, node: Node):
        node.evaluation = node.board.CalculatePlayerLead(node.player)

    def UpdateAncestors(self, node: Node, root: Node):
        while node != root: 
            oldProof = node.proof
            oldDisproof = node.disproof
            self.SetProofAndDisproofNumbers(node)
            if node.proof == oldProof and node.disproof == oldDisproof:
                return node
            node = node.parent
        self.SetProofAndDisproofNumbers(root)
        return root
