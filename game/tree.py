from game.stat_values import ROW, COL, WHITE, BLACK
from game.tree_node import Node
from game.piece_normal import PieceNormal
from game.piece_queen import PieceQueen
import copy


class Tree:
    def __init__(self, headData):
        self.head = Node(None, headData, False, None, True)
        self.lastMove = self.head
        self.lastSelected = None
        self.boardReference = None

    def AddSelectableStones(self, board, turn):
        self.boardReference = board
        acceptForcedMovesOnly = False
        for row in range(ROW):
            for col in range(COL):
                stone = board.GameBoard[row][col]
                # Check if its a stone
                if stone != 0:
                    # Check if its color is the same as turn
                    if stone.color == turn:
                        # Get all moves
                        moves, turnStays, movesWereForced = board.GetCorrectMoves(stone)
                        # Has availible moves
                        if len(moves) != 0:
                            if movesWereForced and not acceptForcedMovesOnly:
                                # If any of the moves are forced, they are the only moves we can play
                                self._PruneUnforcedMoves()
                                acceptForcedMovesOnly = True
                            if acceptForcedMovesOnly and not movesWereForced:
                                continue
                            selectedBoard = copy.deepcopy(board.GameBoard)
                            selectedBoard[row][col].selected = True
                            selectable = Node(self.lastMove, selectedBoard, False, None, True)
                            self.lastMove.AddChild(selectable)
                            idx = -1
                            for move, killedPiece in moves.items():
                                idx += 1
                                moveBoard = copy.deepcopy(board.GameBoard)
                                moveRow, moveCol = move
                                moveBoard[moveRow][moveCol] = moveBoard[row][col]
                                moveBoard[moveRow][moveCol].selected = True
                                moveBoard[row][col] = 0
                                # Telling the stone it moved
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
                                moveNode = Node(selectable, moveBoard, turnBool, kp, movesWereForced, move)
                                selectable.AddChild(moveNode)
                                # Once the GetCorrectMoves is changed to return one killedPiece
                                # Add code to remove piece from here

    def SelectNode(self, board):
        for selectableNode in self.lastMove.children:
            testBoard = selectableNode.data
            if self._AreBoardsIdentical(board, testBoard):
                self.lastSelected = selectableNode
                # self._PrintBoard(board, selectableNode.data)

    def UnselectNode(self):
        self.lastSelected = None

    def GetMovesForSelected(self):
        if self.lastSelected is None:
            return {}
        moves = {}
        for move in self.lastSelected.children:
            moves[move.move] = []
        return moves
        # {(row, col) = [], (row,col) = []}

    def _PruneUnforcedMoves(self):
        for selected in self.lastMove.children:
            for move in selected.children:
                print(move)

    def _PrintBoard(self, board, board2=None):
        c = 1
        if board2 is not None:
            c = 2
        for i in range(c):
            s = ""
            for i in range(ROW):
                for j in range(COL):
                    if board[i][j] != 0:
                        if board[i][j].color == WHITE:
                            s += "\033[91m"
                        else:
                            s += "\033[92m"
                        s += str("Y" if board[i][j].selected else "N") + ", "
                        s += "\033[00m"
                    else:
                        s += str(board[i][j]) + ", "
                s += "\n"
            print(s)
            print("\n")
            board = board2

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
        if a.color == b.color:
            if (isinstance(a, PieceNormal) and isinstance(b, PieceNormal)) or (isinstance(a, PieceQueen) and isinstance(b, PieceQueen)):
                if (a.selected and b.selected) or (not a.selected and not b.selected):
                    return True
        return False

    def Move(self, move):
        if self.lastSelected is None:
            return False, False
        board = self._GetBoardWithMove(self.lastSelected.data, move)
        # self._PrintBoard(board)
        if board is None:
            return False, False
        for moveNode in self.lastSelected.children:
            testBoard = moveNode.data
            if self._AreBoardsIdentical(board, testBoard):
                moveSelected = self._GetSelectedStone(moveNode.data)
                # Check for queen upgrade
                moveNode.data = self._UpgradeQueen(moveNode.data, moveSelected)
                # Unselect moved piece
                moveNode.data = self._DeselectPiece(moveNode.data, moveSelected)

                self.lastMove = moveNode
                # If a piece was killed, remove it
                if moveNode.killedPiece is not None:
                    moveNode.data = self._GetBoardWithKill(moveNode)
                self.boardReference.GameBoard = moveNode.data
                return True, moveNode.turnChange
        return False, False

    def _UpgradeQueen(self, board, selected):
        if isinstance(selected, PieceNormal):
            if selected.row == 0 or selected.row == ROW - 1:
                queen = PieceQueen.fromPiece(selected)
                board[queen.row][queen.col] = queen
            # if selected.color == WHITE and selected.row == 0:
            #     # normal white piece at the top edge
            #     queen = PieceQueen.fromPiece(selected)
            #     board[queen.row][queen.col] = queen
            # if selected.color == BLACK and selected.row == ROW - 1:
            #     # normal black piece at the bottom edge
            #     queen = PieceQueen.fromPiece(selected)
            #     board[queen.row][queen.col] = queen
        return board

    def _DeselectPiece(self, board, selected):
        board[selected.row][selected.col].selected = False
        return board

    def _GetBoardWithMove(self, board, move):
        if board is None:
            return None
        selected = self._GetSelectedStone(board)
        if selected is not None:
            selRow, selCol = selected.pos
            moveRow, moveCol = move
            boardCopy = copy.deepcopy(board)
            boardCopy[moveRow][moveCol] = boardCopy[selRow][selCol]
            # boardCopy[moveRow][moveCol].selected = True
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
