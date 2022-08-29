from game.stat_values import ROW, COL
from game.tree_node import Node
from game.piece_normal import PieceNormal
from game.piece_queen import PieceQueen
import copy


class Tree:
    def __init__(self, headData):
        self.head = Node(None, headData, False, None)
        self.lastMove = self.head
        self.lastSelected = None
        self.boardReference = None

    def AddSelectableStones(self, board, turn):
        self.boardReference = board
        for row in range(ROW):
            for col in range(COL):
                stone = board.GameBoard[row][col]
                # Check if its a stone
                if stone != 0:
                    # Check if its color is the same as turn
                    if stone.color == turn:
                        # Get all moves
                        moves, turnStays = board.GetCorrectMoves(stone)
                        # Has availible moves
                        if len(moves) != 0:
                            selectedBoard = copy.deepcopy(board.GameBoard)
                            selectedBoard[row][col].selected = True
                            selectable = Node(self.lastMove, selectedBoard, False, None)
                            self.lastMove.AddChild(selectable)
                            idx = -1
                            for move, killedPiece in moves.items():
                                idx += 1
                                moveBoard = copy.deepcopy(board.GameBoard)
                                moveRow, moveCol = move
                                moveBoard[moveRow][moveCol] = moveBoard[row][col]
                                moveBoard[row][col] = 0
                                moveBoard[moveRow][moveCol].Move(moveRow, moveCol)
                                kp = None
                                if len(killedPiece) == 1:
                                    kp = killedPiece[0].pos
                                    # killRow, killCol = kp
                                    # moveBoard[killRow][killCol] = 0

                                # No turnstays, assume we should change turn
                                turnBool = True
                                if len(turnStays) != 0:
                                    turnBool = not list(turnStays.values())[idx]
                                moveNode = Node(selectable, moveBoard, turnBool, kp)
                                selectable.AddChild(moveNode)
                                # Once the GetCorrectMoves is changed to return one killedPiece
                                # Add code to remove piece from here

    def SelectNode(self, board):
        for selectableNode in self.lastMove.children:
            testBoard = selectableNode.data
            if self._AreBoardsIdentical(board, testBoard):
                self.lastSelected = selectableNode

    def UnselectNode(self):
        self.lastSelected = None

    def _PrintBoard(self, board):
        s = ""
        for i in range(ROW):
            for j in range(COL):
                if board[i][j] != 0:
                    s += str(board[i][j].selected) + ", "
                else:
                    s += str(board[i][j]) + ", "
            s += "\n"
        print(s)

    def _AreBoardsIdentical(self, a, b):
        for i in range(ROW):
            for j in range(COL):
                if not self._ArePiecesTheSame(a[i][j], b[i][j]):
                    return False
        return True

    def _ArePiecesTheSame(self, a, b):
        if a == 0 and b == 0:
            return True
        if (a == 0 and b != 0) or (a != 0 and b == 0):
            return False
        return (a.color == b.color) and (
            (
                isinstance(a, PieceNormal) and isinstance(b, PieceNormal)
            ) or (
                isinstance(a, PieceQueen) and isinstance(b, PieceQueen)
            )
        )

    def Move(self, move):
        if self.lastSelected is None:
            return False, False
        board = self._GetBoardWithMove(self.lastSelected.data, move)
        if board is None:
            return False, False
        for moveNode in self.lastSelected.children:
            testBoard = moveNode.data
            if self._AreBoardsIdentical(board, testBoard):
                self.lastMove = moveNode
                if moveNode.killedPiece is not None:
                    moveNode.data = self._GetBoardWithKill(moveNode)
                self.boardReference.GameBoard = moveNode.data
                return True, moveNode.turnChange
        return False, False

    def _GetBoardWithMove(self, board, move):
        if board is None:
            return None
        selected = self._GetSelectedStone(board)
        if selected is not None:
            selRow, selCol = selected.pos
            moveRow, moveCol = move
            boardCopy = copy.deepcopy(board)
            boardCopy[moveRow][moveCol] = boardCopy[selRow][selCol]
            boardCopy[selRow][selCol] = 0
            return boardCopy
        return None

    def _GetBoardWithKill(self, node):
        if node.killedPiece is not None:
            board = copy.deepcopy(node.data)
            killRow, killCol = node.killedPiece
            board[killRow][killCol] = 0
            return board

    def _GetSelectedStone(self, board):
        for row in range(ROW):
            for col in range(COL):
                stone = board[row][col]
                if stone != 0 and stone.selected is True:
                    return stone
        return None

    def GetPossibleMoves(self, board):
        print("Not working")
        return
        for selectableNode in self.lastMove.children:
            testBoard = selectableNode.data
            if testBoard == board:
                # Build the list of moves
                for moveNode in testBoard.children:
                    ...
        # "board" is not in our selectable boards
        return None
