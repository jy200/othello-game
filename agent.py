"""
Custom Heuristic description:
If opponent has no more moves prioritize pieces you can gain.
Else: Use a mobility heuristic + focus on corners. Deduct C,X moves if
    board is large enough. Assign positive value to other edge spots.
"""

"""
An AI player for Othello.
"""
import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
cached_moves = dict()


def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    dark_score, light_score = get_score(board)
    return [dark_score - light_score, light_score - dark_score][color == 2]


# Better heuristic value of board
def compute_heuristic(board, color):
    opposite_color = [1, 2][color == 1]
    opposite = get_possible_moves(board, opposite_color)

    # Opponent no longer has moves; prioritize coin gain
    if not opposite:
        dark_score, light_score = get_score(board)
        if color == 1 and dark_score >= light_score:
            return 25000
        elif color == 2 and light_score >= dark_score:
            return 25000
    player = get_possible_moves(board, color)

    # mobility calculation
    moves = len(player) + len(opposite)
    if moves != 0:
        score = 100 * (len(player) - len(opposite)) / moves
    else:
        score = 0

    # corners
    b_length = len(board)
    for corner in [board[0][0], board[0][b_length-1], board[b_length-1][0],
                   board[b_length-1][b_length-1]]:
        if corner == color:
            score += 100

    # deduct C and X moves if sufficient board size.
    # edge pieces are somewhat attractive
    if b_length >= 4:
        x_moves = [(0, 1), (0, b_length - 2), (1, 0),
                   (1, b_length - 1), (b_length - 2, 0),
                   (b_length - 2, b_length - 1), (b_length - 1, 1),
                   (b_length - 1, b_length - 2)]
        c_moves = [(1, 1), (1, b_length - 2), (b_length - 2, 1),
                   (b_length - 2, b_length - 2)]
        for x in range(b_length):
            for y in range(b_length):
                if (x, y) in x_moves or (x, y) in c_moves:
                    if board[x][y] == color:
                        score -= 10
                elif x == 0 or x == b_length - 1 or y == 0 or y == b_length - 1: # edge pieces
                    if board[x][y] == color:
                        score += 25
    else:
        for x in range(b_length):
            for y in range(b_length):
                if x == 0 or x == b_length - 1 or y == 0 or y == b_length - 1:
                    if board[x][y] == color:
                        score += 30
    return score


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if caching and (board, color) in cached_moves:
        return cached_moves[(board, color)]
    best_move = None
    opposite_color = [1, 2][color == 1]
    moves = get_possible_moves(board, opposite_color)
    if not moves or limit == 0:
        result = best_move, compute_utility(board, color)
        return result
    best_move, best_value = moves[0], float("inf")
    for move in moves:
        new_board = play_move(board, opposite_color, move[0], move[1])
        new_value = minimax_max_node(new_board, color, limit - 1, caching)[1]
        if new_value < best_value:
            best_move, best_value = move, new_value
    if caching:     # cache unknown moves
        cached_moves[(board, color)] = (best_move, best_value)
    return best_move, best_value


def minimax_max_node(board, color, limit, caching = 0):
    if caching and (board, color) in cached_moves:
        return cached_moves[(board, color)]
    best_move = None
    moves = get_possible_moves(board, color)
    if not moves or limit == 0:
        result = best_move, compute_utility(board, color)
        return result
    best_move, best_value = moves[0], float("-inf")
    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        new_value = minimax_min_node(new_board, color, limit - 1, caching)[1]
        if new_value > best_value:
            best_move, best_value = move, new_value
    if caching:     # cache unknown moves
        cached_moves[(board, color)] = (best_move, best_value)
    return best_move, best_value


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    move = minimax_max_node(board, color, limit, caching)[0]
    return move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if caching and (board, color) in cached_moves:
        return cached_moves[(board, color)]
    best_move = None
    opposite_color = [1, 2][color == 1]
    moves = get_possible_moves(board, opposite_color)
    if not moves or limit == 0:
        result = best_move, compute_utility(board, color)
        return result
    best_value = float("inf")
    if ordering:
        new_moves = dict()
        for move in moves:
            new_board = play_move(board, opposite_color, move[0], move[1])
            new_moves[move] = compute_utility(new_board, color)
        moves.sort(key=new_moves.get)
    best_move = moves[0]
    for move in moves:
        new_board = play_move(board, opposite_color, move[0], move[1])
        new_value = alphabeta_max_node(new_board, color,alpha, beta, limit-1, caching, ordering)[1]
        if new_value < best_value:
            best_move, best_value = move, new_value
        beta = min(beta, best_value)
        if beta <= alpha:
            break
    if caching:     # cache unknown moves
        cached_moves[(board, color)] = (best_move, best_value)
    return best_move, best_value


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if caching and (board, color) in cached_moves:
        return cached_moves[(board, color)]
    best_move = None
    moves = get_possible_moves(board, color)
    if not moves or limit == 0:
        result = best_move, compute_utility(board, color)
        return result
    best_value = float("-inf")
    if ordering:
        new_moves = dict()
        for move in moves:
            new_board = play_move(board, color, move[0], move[1])
            new_moves[move] = compute_utility(new_board, color)
        moves.sort(key=new_moves.get, reverse=True)
    best_move = moves[0]
    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        new_value = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
        if new_value > best_value:
            best_move, best_value = move, new_value
        alpha = max(alpha, best_value)
        if beta <= alpha:
            break
    if caching:     # cache unknown moves
        cached_moves[(board, color)] = (best_move, best_value)
    return best_move, best_value


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    move = alphabeta_max_node(board, color, float("-inf"), float("inf"),
                              limit, caching, ordering)[0]
    return move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
            board = tuple(tuple(row) for row in board)
            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
