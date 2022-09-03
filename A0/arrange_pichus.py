#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Rohan Mehta, mehtaro]
#
# Based on skeleton code in CSCI B551, Fall 2021.
#
#Discussed logic with Akshay Tiwlekar and Krutik Oza

#https://www.tutorialspoint.com/How-can-we-return-a-list-from-a-Python-function
#https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/
# https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
#https://numpy.org/doc/stable/reference/generated/numpy.diagonal.html


import sys
import numpy as np


# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]


#def valid(board,r,c):
 #   return(valid_row(board,r,c) and valid_column(board,r,c))

# Count total # of pichus on house_map
# def count_pichus(house_map):
#     return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(new_house_map):
    return "\n".join(["".join(row) for row in new_house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(new_house_map):
    while True:
        rand_r = np.random.randint(0,len(new_house_map))
        rand_c = np.random.randint(0,len(new_house_map[0]))
        if new_house_map[rand_r][rand_c] not in 'X@p':
            new_house_map[rand_r][rand_c]='p'
            return new_house_map
    # return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# For checking the row, column and diagonal to see if any other pichu is not placed there, so as to avoid clashing.
def check_row_col_diag(new_house_map,i,j):
    new_house_map[i,j] = 'c'
    clashing_pos = 0
    same_row_other_p_position = [x for x,value in enumerate(new_house_map[i,:]) if value=='p']
    row_right_flag = 0
    row_left_flag = 0
    for k in same_row_other_p_position:
        if k > j and row_right_flag==0:
            if 'X' not in new_house_map[i,j:k]:
                clashing_pos+=1
                row_right_flag=1
        elif k < j and row_left_flag==0:
            if 'X' not in new_house_map[i,k:j]:
                clashing_pos+=1
                row_left_flag=1

    same_col_other_p_position = [x for x,value in enumerate(new_house_map[:,j]) if value=='p']
    col_up_flag = 0
    col_down_flag = 0
    for k in same_col_other_p_position:
        if k > i and col_down_flag==0:
            if 'X' not in new_house_map[i:k,j]:
                clashing_pos+=1
                col_down_flag=1
        elif k < i and col_up_flag==0:
            if 'X' not in new_house_map[k:i,j]:
                clashing_pos+=1
                col_up_flag=1

    right_top_to_left_bottom_diag = np.array(new_house_map.diagonal(j-i))
    left_bottom_to_right_top_diag = np.array(new_house_map[::-1,:].diagonal((1+i+j)-new_house_map.shape[0]))
    c_position_diag = int(np.argwhere(right_top_to_left_bottom_diag=='c'))
    c_position_opp_diag = int(np.argwhere(left_bottom_to_right_top_diag=='c'))
    other_p_positions_diag = np.argwhere(right_top_to_left_bottom_diag=='p')
    other_p_positions_opp_diag = np.argwhere(left_bottom_to_right_top_diag=='p')
    m_greater_c_diag = 0
    m_smaller_c_diag = 0
    m_greater_c_opp_diag = 0
    m_smaller_c_opp_diag = 0
    if len(other_p_positions_diag) > 0:
        for m in other_p_positions_diag:
            if int(m)>c_position_diag and m_greater_c_diag==0:
                if 'X' not in right_top_to_left_bottom_diag[c_position_diag:int(m)]:
                    clashing_pos+=1
                    m_greater_c_diag=1
            elif int(m)<c_position_diag and m_smaller_c_diag==0:
                if 'X' not in right_top_to_left_bottom_diag[int(m):c_position_diag]:
                    clashing_pos+=1
                    m_smaller_c_diag=1
    if len(other_p_positions_opp_diag) > 0:
        for m in other_p_positions_opp_diag:
            if int(m)>c_position_opp_diag and m_greater_c_opp_diag==0:
                if 'X' not in left_bottom_to_right_top_diag[c_position_opp_diag:int(m)]:
                    clashing_pos+=1
                    m_greater_c_opp_diag=1
            elif int(m)<c_position_opp_diag and m_smaller_c_opp_diag==0:
                if 'X' not in left_bottom_to_right_top_diag[int(m):c_position_opp_diag]:
                    clashing_pos+=1
                    m_smaller_c_opp_diag=1
    new_house_map[i,j] = 'p'
    return clashing_pos

def inspect_zero_index(new_house_map):
    zero_index = []
    for i in range(len(new_house_map)):
        for j in range(len(new_house_map[0])):
            if new_house_map[i][j] == 0:
                zero_index.append([i,j])
    return np.array(zero_index)

def changing_map(new_house_map):
    for i in range(len(new_house_map)):
        for j in range(len(new_house_map[0])):
            if str(new_house_map[i,j]) not in '@pX':
                new_house_map[i,j] = '.'
    return new_house_map

# Get list of successors of given house_map state
def successors(new_house_map):
    try:
        new_house_map = np.array(new_house_map, dtype='object')
        p_position = [[row,col] for row in range(len(new_house_map)) for col in range(len(new_house_map[0])) if new_house_map[row,col]=='p']
        for k in range(len(p_position)):
            new_house_map[p_position[k][0],p_position[k][1]] = 'P'
            for i in range(len(new_house_map)):
                for j in range(len(new_house_map[0])):
                    if str(new_house_map[i,j]) not in '@Xp':
                        try:
                            new_house_map[i,j] = check_row_col_diag(new_house_map,i,j)
                        except:
                            return (new_house_map, False)
            if new_house_map[p_position[k][0],p_position[k][1]] == 0:
                new_house_map[p_position[k][0]][p_position[k][1]] = 'p'
            else:
                zero_index = inspect_zero_index(new_house_map)
                rand_0 =np.random.randint(0,len(zero_index))
                new_house_map[zero_index[rand_0][0],zero_index[rand_0][1]] = 'p'
                new_house_map[p_position[k][0]][p_position[k][1]] = '.'
            new_house_map = changing_map(new_house_map)
        return (new_house_map, True)           
    except:
        return (new_house_map, False)

# For checking all the diagonals while placing a pichu
# def rud(house_map,r,c):
#     rupd= []
#     while r!=0 in len(house_map):
#         r=r-1
#         c=c+1
#     return rupd.append(r,c)
# def lud(house_map,r,c):
#     lupd=[]
#     while r!=0:
#         r=r-1
#         c=c-1
#     return lupd.append(r,c)
#
# def rdd(house_map,r,c):
#     rdod=[]
#     while c!=7:
#         r=r+1
#     return rdod.append(r,c)
#
# def ldd(house_map,r,c):
#     ldod=[]
#     while c!=0:
#         r=r+1
#         c=c-1
#     return ldod.append(r,c)

#For finding walls, i.e. "X" on the house map
# def wall_loc(house_map):
#     wall=set()
#     for c in range(len(house_map[0])):
#         for r in range(len(house_map)):
#             if house_map[r][c] == "X":
#                 wall.add(house_map[r][c])
#     return (wall)

# For finding the locations of already placed pichus
# def pichu_location(house_map):
#     p_loc= []
#     for c in range(len(house_map[0])):
#         for r in range(len(house_map)):
#             if house_map[r][c] == "p":
#                 p_loc.append(house_map)
#     return (p_loc)


# check if house_map is a goal state, i.e. if we have reached our final house map or not.
def is_goal(new_house_map):
    for i in range(len(new_house_map)):
        for j in range(len(new_house_map[0])):
            if new_house_map[i, j] == 'p':
                if check_row_col_diag(new_house_map, i, j) == 0:
                    return True
                else:
                    return False


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    Max_tries = 50
    for count in range(Max_tries):
        initial_added_pichus = initial_house_map.copy()
        for _ in range(k - 1):
            initial_added_pichus = add_pichu(initial_added_pichus)
        final_house_map = successors(initial_added_pichus)
        if final_house_map[1]:
            if is_goal(final_house_map[0]):
                return (final_house_map[0], True)
            else:
                pass
        else:
            pass
    return (-1, False)

# Main Function
if __name__ == "__main__":

    house_map = parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n\nRandomly placed pichus")
    solution = solve(np.array(house_map, dtype='object'), k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")

