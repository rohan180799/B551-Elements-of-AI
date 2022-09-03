#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Rohan Mehta, mehtaro]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.
#
#Discussed logic with Pramey Modi and Akshay Tiwlekar
#https://www.geeksforgeeks.org/args-kwargs-python/

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")

        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def move_str(move, curr_move, move_string):
        if move[0] == curr_move[0]+1:
                move_string += "D"
        elif move[0] == curr_move[0] -1:
                move_string += "U"
        elif move[1] == curr_move[1]+1:
                move_string += "R"
        elif move[1] == curr_move[1]-1:
                move_string += "L"
        return move_string


def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0,"")]

        alr_visited = [] #already visited locations

        while fringe:
                (curr_move, curr_dist, move_string)=fringe.pop(0)
                #curr_move=(5,0)
                #curr_dist=0
                for move in moves(house_map, *curr_move):
                        if move in alr_visited:
                                continue
                        if house_map[move[0]][move[1]]=="@":
                                return (curr_dist+1, move_str(move, curr_move, move_string))  # return a dummy answer
                        else:
                                fringe.append((move, curr_dist + 1, move_str(move, curr_move, move_string)))
        return (-1,"")    # -1 for getting no route to reach the goal

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + str(solution[1]))

