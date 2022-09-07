# Minimax algorith for AI
# Copy for board => deepcopy for coping object itself
from game.stat_values import BLACK, WHITE

AI_color = BLACK
Player_color = WHITE if AI_color == BLACK else BLACK
wrongMoveChance = 0.2


# Minimax method + alpha-beta pruning => makes computing run faster
def minimax(position, depth, alpha, beta, max_player, game, turnChange=True):
    # position => current board position, object

    gameWinner, allMoves = game.tree.GenerateLevel(position, max_player, False)
    if depth == 0 or gameWinner is not None:
        return position.evaluate(), position

    if max_player:
        maxEvaluate = float('-inf')  # If we haven't found anything yet, it's -inf
        best_move = None  # Stores best move we can make
        for moveData in allMoves.values():
            move, turnChange = moveData
        # for move in get_all_moves(position, AI_color, game):  # For every move eval => calls minimax (recursive)
            evaluation = minimax(move, depth-1, alpha, beta, False, game, turnChange)[0]  # returns board and value
            maxEvaluate = max(maxEvaluate, evaluation)
            alpha = max(alpha, evaluation)
            if maxEvaluate == evaluation:
                best_move = move  # Sets current found best move in board as a best move
            if beta <= alpha:
                break

        # Chance to make a "wrong" move, so it doesnt always play the same
        import random
        if random.uniform(0, 1) < wrongMoveChance:
            best_move, ignored = list(allMoves.values())[random.randint(0, len(allMoves.values()) - 1)]

        return maxEvaluate, best_move

    else:
        minEvaluate = float('inf')  # If we haven't found anything yet, it's inf
        best_move = None  # Stores best move we can make
        for moveData in allMoves.values():
            move, turnChange = moveData
            # For every move eval => calls minimax (recursive)
            evaluation = minimax(move, depth-1, alpha, beta, True, game, turnChange)[0]  # returns board and value
            minEvaluate = min(minEvaluate, evaluation)
            beta = min(beta, evaluation)
            if minEvaluate == evaluation:
                best_move = move  # Sets current found best move in board as a best move
            if beta <= alpha:
                break

        # Chance to make a "wrong" move, so it doesnt always play the same
        import random
        if random.uniform(0, 1) < wrongMoveChance:
            best_move, ignored = list(allMoves.values())[random.randint(0, len(allMoves.values()) - 1)]

        return minEvaluate, best_move


def ChangeAIColor(color):
    global AI_color
    global Player_color
    AI_color = color
    Player_color = WHITE if AI_color == BLACK else BLACK
