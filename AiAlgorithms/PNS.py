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
    parent: 'Node' = None
    children = []
    disproof: int = None
    proof: int = None
    evaluation: int = 0
    expanded = False
    value: int = 0
    player: int = 0
    type: Type

    def __init__(self, type: Type):
        self.type = type


    def generateChildren(self):
        boardList = []
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
        retBoards = []
        #movesList = board.GetAllPlayerMovements(self.player.playerNumber)
        for move in movesList:
            returnedFields, allMoves = Player.MakeMove(rootBoard, move)
            returnedBoard = Board()
            returnedBoard.fields = returnedFields.copy()
            if allMoves != None and len(allMoves) > 0:
                retBoards.extend(self.CutSubtree(returnedBoard, allMoves))
            else:
                retBoards.append(returnedBoard)
                
        return retBoards

#TODO jeszcze chyba nie wiem gdzie ustawiamy wygraną i czy dla aktualnego gracza czy dla roota
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


    def AIPNS(self,  Root: 'Board', maxTime: float = 60):
        self.maxTime = maxTime
        self.PNS(Root)
        return self.root.proof >= infinity, (time.process_time() - self.startTime)

    def PNS(self,  Root: 'Board'):
        self.root.board = Root
        self.Evaluate(self.root)
        self.SetProofAndDisproofNumbers(self.root)
        current = self.root
        self.startTime = time.process_time()
        while self.root.proof != 0 and self.root.disproof != 0 and (time.process_time() - self.startTime) < (self.maxTime):
            mostProving = self.SelectMostProvinNode(current)
            self.ExpandNode(mostProving)
            current = self.UpdateAncestors(mostProving, self.root)
        

    def SetProofAndDisproofNumbers(self, currNode: Node):
        if currNode.expanded:
            if currNode.type == Type.AND:
                currNode.proof = 0
                currNode.disproof = infinity
                for child in currNode.children:
                    if child.disproof is None or child.proof is None:
                        break
                    currNode.proof += child.proof
                    currNode.disproof = min(currNode.disproof, child.disproof)
            else:
                currNode.proof = infinity
                currNode.disproof = 0
                for child in currNode.children:
                    if child.disproof is None or child.proof is None:
                        break
                    currNode.disproof += child.disproof
                    currNode.proof = min(currNode.proof, child.proof)
        else:
            if  currNode.evaluation > 100:
                currNode.proof = 0
                currNode.disproof = infinity
            elif currNode.evaluation < -100:
                currNode.proof = infinity
                currNode.disproof = 0
            else:
                currNode.proof = 1
                currNode.disproof = 1

    def SelectMostProvinNode(self, node: Node):
        currNode = node
        best: 'Node'
        maxProofDisproof = 1000
        while currNode.expanded:
            value = infinity + 1
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
            #TODO poprawić, nie wiem jak to się dzieje
            if node.parent == None:
                return root
            if not hasattr(node, 'parent') and node != self.root:
                return root
            oldProof = node.proof
            oldDisproof = node.disproof
            self.SetProofAndDisproofNumbers(node)
            if node.proof == oldProof and node.disproof == oldDisproof:
                return node
            node = node.parent
        self.SetProofAndDisproofNumbers(root)
        return root
