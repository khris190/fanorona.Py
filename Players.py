from primitives import *
from fanorona import Board
import random
infinityEval = 2147483648
infinity = 32767


class Player:
    playerType: PlayerTypeEnum
    Name: str
    playerNumber: int
    lastMoveDirection: Vector
    lastMove: Point

    def __init__(self, type: PlayerTypeEnum, name: str,playerNumber: int) -> None:
        self.playerType = PlayerTypeEnum
        self.Name = name
        self.playerNumber = playerNumber

    # TODO dla pewności blokować przejścia na nie puste miejsca(ale ruchy powinny być robione z listy dostępnych więc wyjebane)
    #zwraca nową planszę, boola informującego czy pionek zbił i kierunek bicia
    @classmethod
    def MakeMove(cls, board: Board, move: Move):
        boardCopy = board.fields.copy()

        currentPos = move.position

        nextPos = move.GetNextPosition()

        # result bool that shows if something was beaten
        wasBeaten = False

        #get enemy and player number
        player = 2
        enemy = 1
        if boardCopy[currentPos.y][currentPos.x] == 1:
            player = 1
            enemy = 2

        # remove current pos
        boardCopy[currentPos.y][currentPos.x] = 0
        # add new pos
        boardCopy[nextPos.y][nextPos.x] = player

        tmpX = nextPos.x
        tmpY = nextPos.y
        if move.beatType == BeatingDirectionEnum.forward:
            tmpX += move.direction.x
            tmpY += move.direction.y
            while (tmpX <= 8 and tmpY <= 4 and tmpX >= 0 and tmpY >= 0):
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True
                tmpX += move.direction.x
                tmpY += move.direction.y
        # beat backward
        else:
            tmpX = currentPos.x
            tmpY = currentPos.y
            tmpX -= move.direction.x
            tmpY -= move.direction.y
            while (tmpX <= 8 and tmpY <= 4 and tmpX >= 0 and tmpY >= 0):
                if (boardCopy[tmpY][tmpX] != enemy):
                    break
                boardCopy[tmpY][tmpX] = 0
                wasBeaten = True
                tmpX -= move.direction.x
                tmpY -= move.direction.y
    

        #sprawdzić czy wszystkie ruchy są bez bicia
        nextMoves = []
        if wasBeaten:
            tmpBoard = Board()
            tmpBoard.fields = boardCopy
            #print(boardCopy[:][:])
            nextmove = tmpBoard.GetEmptyPlacesForMovement(nextPos.x, nextPos.y)

            nextmove[move.direction.y + 1][move.direction.x + 1] = 0
            nextmove[-move.direction.y + 1][-move.direction.x + 1] = 0


            tmpMoves = tmpBoard.FindBeatingPossibleMoves(player, nextPos.x, nextPos.y, nextmove)
            if tmpBoard.RefineMoves(nextmove) and tmpMoves != None:
                tmpMoves = Move.CreateMovesListFromPositionMoves(PositionMoves(nextPos.x, nextPos.y, nextmove))
                for tmpmove in tmpMoves:
                    if tmpmove.beatType != BeatingDirectionEnum.noBeat:
                        nextMoves.append(tmpmove)
                        if tmpmove.beatType == BeatingDirectionEnum.noBeat:
                            nextMoves = []
                            break
            else:
                nextMoves = []


        return boardCopy, nextMoves

    def AI(self, playerType: PlayerTypeEnum, board: Board) -> bool:
        moves = board.GetAllPlayerMovements(playerType)

    def AI_MinMax(self, depth: int, board: Board):
        movesList = board.GetAllPlayerMovements(self.playerNumber)

        value = -infinityEval
        winValue = value
        retBoard = Board()
        retBoard.fields = board.fields.copy()


        for move in movesList:
            tmpBoard = Board()
            tmpBoard.fields = board.fields.copy()
            returnedBoard, allMoves = self.MakeMove(tmpBoard, move)

            tmpBoard.fields = returnedBoard.copy()

            #liczę kilkukrotne zbicia jako tą samą turę
            if allMoves != None and len(allMoves) > 0:
                value = max(value, self.MinMax(depth, tmpBoard, self.playerNumber, True))
            else:
                if self.playerNumber == 1:
                    value = max(value, self.MinMax(depth - 1, tmpBoard, 2, False))
                else:
                    value = max(value, self.MinMax(depth - 1, tmpBoard, 1, False))


            if winValue < value:
                winValue = value
                retBoard = tmpBoard

        return  winValue, retBoard.fields, not(allMoves != None and len(allMoves) > 0)
        

    def MinMax(self, depth: int, board: Board, playerNumber: int, maximizing: bool = True):
        nodeVal = board.CalculatePlayerLead(playerNumber)
        if depth < 1 or infinityEval == nodeVal or infinityEval == -nodeVal:
            return nodeVal
        movesList = board.GetAllPlayerMovements(playerNumber)

        if maximizing == True:
            value = -infinityEval
            for move in movesList:
                tmpBoard = Board()
                returnedBoard, allMoves = self.MakeMove(tmpBoard, move)
                tmpBoard.fields = returnedBoard.copy()

                #liczę kilkukrotne zbicia jako tą samą turę
                if allMoves != None and len(allMoves) > 0:
                    value = max(value, self.MinMax(depth, tmpBoard, playerNumber, True))
                else:
                    if playerNumber == 1:
                        value = max(value, self.MinMax(depth - 1, tmpBoard, 2, False))
                    else:
                        value = max(value, self.MinMax(depth - 1, tmpBoard, 1, False))
        else:
            value = infinityEval
            for move in movesList:
                tmpBoard = Board()
                returnedBoard, allMoves = self.MakeMove(tmpBoard, move)
                tmpBoard.fields = returnedBoard.copy()

                #liczę kilkukrotne zbicia jako tą samą turę
                if allMoves != None and len(allMoves) > 0:
                    value = min(value, self.MinMax(depth, tmpBoard, playerNumber, True))
                else:
                    if playerNumber == 1:
                        value = min(value, self.MinMax(depth - 1, tmpBoard, 2, False))
                    else:
                        value = min(value, self.MinMax(depth - 1, tmpBoard, 1, False))

        
        return value

            





    
