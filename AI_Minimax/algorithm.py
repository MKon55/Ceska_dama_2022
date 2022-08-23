#Minimax algorith for AI

#Copy for board => deepcopy for coping object itself
from copy import deepcopy
from game.stat_values import BLACK, WHITE

#Minimax method
def minimax(position, depth, max_player, game):
    #position => current board position, object
    if depth == 0 or position.Winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEvaluate = float('-100') #If we haven't found anything yet, it's -inf
        best_move = None #Stores best move we can make
        for move in get_all_moves(position, BLACK, game): #For every move eval => calls minimax (reculsive)
            evaluation = minimax(move, depth-1, False, game)[0] #returns board and value
            maxEvaluate = max(maxEvaluate, evaluation)
            if maxEvaluate == evaluation:
                best_move = move #Sets current found best move in board as a best move

        return maxEvaluate, best_move
    else:
        minEvaluate = float('100') #If we haven't found anything yet, it's inf
        best_move = None #Stores best move we can make
        for move in get_all_moves(position, WHITE, game): #For every move eval => calls minimax (reculsive)
            evaluation = minimax(move, depth-1, True, game)[0] #returns board and value
            minEvaluate = min(minEvaluate, evaluation)
            if minEvaluate == evaluation:
                best_move = move #Sets current found best move in board as a best move

        return minEvaluate, best_move

#Method for move simulation on temp board
def possible_move(stone, move, board, game, skip):
    board.Movement(stone, move[0], move[1])
    if skip:
        board.Remove(skip)

    return board

#Method gets us all possible moves in current position, Method works with get_all_stones method in game_board
def get_all_moves(board, colour, game):
    moves = [] #Stores new board [[board, stone], [new_board, stone]]

    for stone in board.get_all_stones(colour):
        correct_moves = board.GetCorrectMoves(stone)
        for move, skip in correct_moves.items(): #Loop for all items (row, col): [stones] if correct
            temp_board = deepcopy(board)
            temp_stone = temp_board.GetStone(stone.row, stone.col)
            new_board = possible_move(temp_stone, move, temp_board, game, skip) #returns new board after move
            moves.append(new_board)

    return moves
