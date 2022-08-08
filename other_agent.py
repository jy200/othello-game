"""
An AI player for Othello.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache_dict = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    a = get_score(board)
    if color == 1: ## 1 for dark, 2 for light
        return a[0] - a[1]
    else:
        return a[1] - a[0]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    if color == 1:
        opp_color = 2
    else:
        opp_color = 1

    a = get_possible_moves(board, color)
    b = get_possible_moves(board, opp_color)

    if len(b) == 0:
        curr_score = get_score(board)
        if color == 1:
            if curr_score[0] >= curr_score[1]:
                return 10000
        else:
            if curr_score[1] >= curr_score[0]:
                return 100000

    score = len(a) - len(b)


    if(board[0][0] == color):
        score += 20
    if(board[0][len(board)-1] == color):
        score += 20
    if(board[len(board)-1][0] == color):
        score += 20
    if(board[len(board)-1][len(board)-1] == color):
        score += 20

    for y in range(len(board)):
        for x in range(len(board)):
            if x == 0 or x == len(board) - 1 or y == 0 or y == len(board) - 1:
                if board[x][y] == color:
                    score += 5

    return score

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT
    if caching == 1:
        if (board, color) in cache_dict:
            return cache_dict[(board, color)]

    if color == 1:
        opp_color = 2
    else:
        opp_color = 1

    possible_moves = get_possible_moves(board, opp_color)
    if len(possible_moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))

    next_move = None
    next_move_val = float('inf')
    for move in possible_moves:
        new_board = play_move(board, opp_color, move[0], move[1])
        new_val = minimax_max_node(new_board, color, limit - 1, caching)[1]
        if new_val < next_move_val:
            next_move = move
            next_move_val = new_val

    if caching == 1:
        cache_dict[(board, color)] = (next_move, next_move_val)

    return (next_move, next_move_val)

    #return ((0,0),0)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT
    if caching == 1:
        if (board, color) in cache_dict:
            return cache_dict[(board, color)]

    possible_moves = get_possible_moves(board, color)
    if len(possible_moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))

    next_move = None
    next_move_val = float('-inf')
    for move in possible_moves:
        new_board = play_move(board, color, move[0], move[1])
        new_val = minimax_min_node(new_board, color, limit - 1, caching)[1]
        if new_val > next_move_val:
            next_move = move
            next_move_val = new_val

    if caching == 1:
        cache_dict[(board, color)] = (next_move, next_move_val)

    return (next_move, next_move_val)



    #return ((0,0),0)

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
    #IMPLEMENT
    cache_dict.clear()
    return minimax_max_node(tuple([tuple(row) for row in board]), color, limit, caching)[0]
    #return (0,0) #change this!

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    if caching == 1:
        if (board, color) in cache_dict:
            return cache_dict[(board, color)]

    if color == 1:
        opp_color = 2
    else:
        opp_color = 1

    possible_moves = get_possible_moves(board, opp_color)
    if len(possible_moves) == 0 or limit == 0:
        # return (None, compute_utility(board, color))
        return (None, compute_heuristic(board, color))

    if ordering == 1:
        move_value = {}
        for move in possible_moves:
            new_board = play_move(board, opp_color, move[0], move[1])
            # move_value[move] = compute_utility(new_board, color)
            move_value[move] = compute_heuristic(new_board, color)
        possible_moves.sort(key=lambda x: move_value[x])

    next_move = None
    next_move_val = float('inf')
    for move in possible_moves:
        new_board = play_move(board, opp_color, move[0], move[1])
        if beta > alpha:
            new_val = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
            if new_val < next_move_val:
                next_move = move
                next_move_val = new_val
                beta = new_val

    if caching == 1:
        cache_dict[(board, color)] = (next_move, next_move_val)

    return (next_move, next_move_val)
    # return ((0,0),0) #change this!

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    if caching == 1:
        if (board, color) in cache_dict:
            return cache_dict[(board, color)]

    possible_moves = get_possible_moves(board, color)
    if len(possible_moves) == 0 or limit == 0:
        # return (None, compute_utility(board, color))
        return (None, compute_heuristic(board, color))


    if ordering == 1:
        move_value = {}
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            # move_value[move] = compute_utility(new_board, color)
            move_value[move] = compute_heuristic(new_board, color)

        possible_moves.sort(key=lambda x: move_value[x], reverse=True)


    next_move = None
    next_move_val = float('-inf')
    for move in possible_moves:
        new_board = play_move(board, color, move[0], move[1])
        if beta > alpha:
            new_val = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
            if new_val > next_move_val:
                next_move = move
                next_move_val = new_val
                alpha = new_val

    if caching == 1:
        cache_dict[(board, color)] = (next_move, next_move_val)

    return (next_move, next_move_val)

    # return ((0,0),0) #change this!

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
    #IMPLEMENT
    cache_dict.clear()
    return alphabeta_max_node(tuple([tuple(row) for row in board]), color, float('-inf'), float('inf'), limit, caching, ordering)[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Other agent") # First line is the name of this AI
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

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
