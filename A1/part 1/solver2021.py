#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np
ROWS = 5
COLS = 5

goal = np.arange(1, (ROWS*COLS)+1)
goal = goal.reshape(ROWS, COLS)
print (goal.tolist())

def printable_board(board):
    return [('%3d ') * COLS % board[j:(j + COLS)] for j in range(0, ROWS * COLS, COLS)]


# goal = ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25])


# return a list of possible successor states
def successors(state):
    return True


# row 1-5 movement code
def move_left(board, r):
    fe = board[r][0]
    for i in range(len(board)):
        if i == len(board) - 1:
            board[r][i] = fe
        else:
            board[r][i] = board[r][i + 1]
    return board


def move_right(board, r):
    le = board[r][len(board) - 1]
    for i in range(len(board) - 1, 0, -1):
        board[r][i] = board[r][i - 1]
    board[r][0] = le
    return board


def move_up(board, c):
    fe = board[0][c]
    for i in range(len(board[0])):
        if i == len(board[0]) - 1:
            board[i][c] = fe
        else:
            board[i][c] = board[i + 1][c]
    print(board)
    return board


def move_down(board, c):
    le = board[len(board[0]) - 1][c]
    for i in range(len(board[0]) - 1, 0, -1):
        board[i][c] = board[i - 1][c]
    board[0][c] = le
    print(board)
    return board


def tp_to_mat(board):
    m = list(board)
    # print(*M, sep="\n")
    return [m[c:c + COLS] for c in range(0, len(m), ROWS)]


def get_map_as_list(map_):
    # Converts list of list into a single list for map
    map_out = []
    for row in map_:
        map_out.extend(row)
    return map_out


# def get_pos(current_state, element):
#     for row in range(len(current_state)):
#         if element in current_state[row]:
#             return (row, current_state[row].index(element))
#
# def euclidianCost(current_state):
#     cost = 0
#     for row in range(len(current_state)):
#         for col in range(len(current_state[0])):
#             pos = get_pos(goal, current_state[row][col])
#             cost += abs(row - pos[0]) + abs(col - pos[1])
#     return cost

# check if we've reached the goal
def is_goal(state):
    return False


def solve(initial_board):
    ##print(initial_board)
    matrix_board = tp_to_mat(initial_board)
    # move_left(matrix_board, 2)
    # move_right(matrix_board, 1)
    # move_up(matrix_board, 2)
    # matrix_board = new_board
    ##move_down(matrix_board, 3)
    ##changed_board = get_map_as_list(matrix_board)
    ##print("mid state: \n" + "\n".join(printable_board(tuple(changed_board))))
    # gboard = get_map_as_list(goal)
    # print("Goal state: \n" + "\n".join(printable_board(tuple(gboard))))
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    return ["Oc", "L2", "Icc", "R4"]


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != ROWS * COLS:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
