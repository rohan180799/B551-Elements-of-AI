# Simple quintris program! v0.2
# D. Crandall, Sept 2021

# Akshay Tiwlekar [akstiwle], Rohan Mehta [mehtaro], Pramey Modi [pmmodi]

# Reference taken from channel:
# link: https://www.youtube.com/watch?v=jmLAx0jbPDc&t=184s

import copy
import math

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *

#
# Predefined Scores for best peice placement calculations
#
LINE_1 = 100
LINE_2 = 500
LINE_3 = 1000
LINE_4 = 10000
UNWANTED_LINE = -1000

# Weights for the criteria
HEIGHT_SIMPLE = -3  # Unit of height (overall)
HEIGHT_COEFF = 1.4  # For progressive weght of height i**coeff for each next row
WIDTH_COEFF = 3  # For regressive count of width on certain height (more for less effect)

HEIGHT_DIFFERENCE = -5  # Each step between neighbouring rows
HOLE = -500
OVERHEAD = -10  # Cells above the hole

DIVERSITY = 50  # Has a spot for all kinds of tetraminos
EXTRA_WELLS = -300  # More than one well (hole >2 deep)

HAS_LAST_COLUMN = -2000
PENULTIMATE_COLUMN_PROBLEM = -1000

mode = 2

show_scores = False


class HumanPlayer:
    def get_moves(self, quintris):
        print(
            "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands = {"b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right,
                        " ": quintris.down}
            commands[c]()


#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    # checks that the row is empty or not
    def is_empty_line(self, field, n):
        for i in range(25):
            if field[i][n] != ' ':
                return False
        return True

    # Rotates the piece in 270 degree and returns the list of rotated piece
    def get_rotations(self, piece, temp_quintris):
        rotations = []
        for i in [0, 90, 180, 270]:
            rotations.append(temp_quintris.rotate_piece(piece[0], i))
        return rotations

    # checks if piece is going out of board
    def is_legit_position(self, piece, position):
        ''' See if the piece seps out of the field'''
        if position + len(max(piece[0])) > 15:
            return False
        return True

    # function for combining piece and the existing piece
    # got a bug with piece placement, hence used down instead
    #
    def get_new_floor(self, floor, orig_piece, orig_position, obj):
        # piece = orig_piece.copy()
        col = orig_position
        row = 0
        score = 0

        if self.is_empty_line(floor, col):
            print(self.is_empty_line(floor, col))
            new_floor = obj.place_piece(floor, score, orig_piece, len(floor) - len(orig_piece), col)
            return new_floor[0]
        else:
            print("................i am here..................")
            for j in range(25):
                if floor[j][col] != ' ':
                    row = j - len(orig_piece)
                    # print(row)
                    new_floor = floor[0:row] + \
                                [(floor[i + row][0:col] + obj.combine(r, floor[i + row][col:col + len(r)]) +
                                  floor[i + row][col + len(r):]) for (i, r) in enumerate(orig_piece)] + \
                                  floor[row + len(orig_piece):]
                    # print(new_floor)
                    for i in new_floor:
                        print(i)
                    return new_floor[0]

    # used to check completion of lines in checking every possible outcome with the current floor
    def collapse_floor(self, floor):
        # cell_counts = np.sum(floor, axis=0)
        cell_counts = []
        for i in range(len(floor)):
            cell_counts.append(len(floor[i]) - floor[i].count(' '))
        new_floor = floor.copy()
        lines = 0
        for i in range(len(cell_counts))[::-1]:
            if cell_counts[i] == 15:
                lines += 1
                # new_floor = np.delete(new_floor, i, 1)
        return lines

    # gets number of holes in the current row
    def get_holes(self, floor):
        holes = 0
        overhead = 0
        for i in range(25):
            found_cell = False
            over_in_row = 0
            for j in range(len(floor[0])):
                if floor[i][j] == 'x':
                    found_cell = True
                    over_in_row += 1
            if found_cell:
                holes += floor[i].count(' ')
                overhead += over_in_row

        # print('Holes: ',holes)
        return holes, overhead

    # gives height of every column, checks column wise and returns maximum
    def get_height(self, floor):
        heights = []
        for i in range(len(floor[0])):
            c = []
            d = 0
            for j in range(len(floor)):
                c.append(floor[j][i])
            d = len(c)
            for k in range(len(c)):
                if c[k] == 'x':
                    break
                else:
                    d = len(c) - (k + 1)
            heights.append(d)
        return max(heights)

    # gives height according to the row count
    def get_height_adv(self, floor):
        cell_counts = []
        for i in range(len(floor)):
            cell_counts.append(len(floor[i]) - floor[i].count(' '))
        return cell_counts

    # check height difference of the adjacent column and gives their difference
    def get_hgt_differences(self, floor):
        h_diffs = 0
        heights = []
        for i in range(len(floor[0])):
            c = []
            d = 0
            for j in range(len(floor)):
                c.append(floor[j][i])
            d = len(c)
            for k in range(len(c)):
                if c[k] == 'x':
                    break
                else:
                    d = len(c) - (k + 1)
            heights.append(d)

        for i in range(1, 15):
            h_diffs += abs(heights[i] - heights[i - 1])
        return h_diffs

    # gives diversity for checking if the pieces are not pilling up
    def get_diversity(self, floor):
        a, b, c = False, False, False
        heights = []
        for i in range(len(floor[0])):
            hlist = []
            d = 0
            for j in range(len(floor)):
                hlist.append(floor[j][i])
            d = len(hlist)
            for k in range(len(hlist)):
                if hlist[k] == 'x':
                    break
                else:
                    d = len(hlist) - (k + 1)
            heights.append(d)

        for i in range(1, 15):
            if heights[i] - heights[i - 1] == 0:
                a = True
            if heights[i] - heights[i - 1] == 1:
                b = True
            if heights[i] - heights[i - 1] == -1:
                c = True
        return a and b and c

    # checks if the pieces are not forming big wells
    def count_wells(self, floor):
        wells = 0

        heights = []
        for i in range(len(floor[0])):
            c = []
            d = 0
            for j in range(len(floor)):
                c.append(floor[j][i])
            d = len(c)
            for k in range(len(c)):
                if c[k] == 'x':
                    break
                else:
                    d = len(c) - (k + 1)
            heights.append(d)

        if heights[1] - heights[0] > 2:
            wells += 1
        if mode != 2 and heights[8] - heights[9] > 2:
            wells += 1
        for i in range(1, 8):
            if heights[i - 1] - heights[i] > 2 and heights[i + 1] - heights[i] > 2:
                wells += 1
        return wells

    # not working but the purpose was to keep the last column empty so that if straight piece
    # appears then it will complete more than 2 lines
    def last_column(self, floor):
        len(floor[14])
        b = []
        for i in range(len(floor)):
            b.append(floor[i][14])
            c = len(b) - b.count(' ')
        if c > 0:
            return True
        return False

    # gives score for every piece placements according to height, number of holes, diversity, height differences
    def get_score(self, orig_floor):

        score = 0
        sc_lines = 0
        sc_height = 0
        sc_diverse = 0
        sc_wells = 0

        # Check for full lines
        lines = self.collapse_floor(orig_floor)

        # Completed lines
        if mode != 2:
            if lines == 1:
                sc_lines = LINE_1
            if lines == 2:
                sc_lines = LINE_2
            if lines == 3:
                sc_lines = LINE_3
            if lines == 4:
                sc_lines = LINE_4
        elif lines > 0:
            score += UNWANTED_LINE
        score += sc_lines

        # # Holes (less is better)
        holes, overhead = self.get_holes(orig_floor)
        sc_holes = holes * HOLE
        sc_overhead = overhead * OVERHEAD
        score += sc_holes
        score += sc_overhead

        # Height (less is beter)
        # ......code for height........
        # score += self.get_height(orig_floor) * HEIGHT_SIMPLE

        height_list = self.get_height_adv(orig_floor)
        for i in range(len(orig_floor[0])):
            if height_list[-i - 1] > 0:

                # print (i, height_list[-i-1], HEIGHT_SIMPLE*HEIGHT_COEFF**i, math.log(height_list[-i-1],WIDTH_COEFF)+1)
                height_score = height_list[-i - 1] * HEIGHT_SIMPLE * (HEIGHT_COEFF ** i) * (
                        math.log(height_list[-i - 1], WIDTH_COEFF) + 1)
                if mode == 2:
                    sc_height += height_score / 2
                else:
                    sc_height += height_score
        score += sc_height

        # # Height differences
        sc_diff = self.get_hgt_differences(orig_floor) * HEIGHT_DIFFERENCE
        score += sc_diff

        # .........code for diversity and count wells........

        if self.get_diversity(orig_floor):
            sc_diverse = DIVERSITY
            score += sc_diverse

        wells = self.count_wells(orig_floor)
        if wells > 0:
            sc_wells = wells * EXTRA_WELLS
            score += sc_wells

        # Has stuff in last column (only for hole-less situation)
        if mode == 2:
            if self.last_column(orig_floor):
                score += HAS_LAST_COLUMN
            heights = []
            for i in range(len(orig_floor[0])):
                c = []
                d = 0
                for j in range(len(orig_floor)):
                    c.append(orig_floor[j][i])
                d = len(c)
                for k in range(len(c)):
                    if c[k] == 'x':
                        break
                    else:
                        d = len(c) - (k + 1)
                heights.append(d)

            if heights[12] - heights[13] > 2:
                score += PENULTIMATE_COLUMN_PROBLEM

        if show_scores:
            print("Lines:", sc_lines, "Holes:", sc_holes, "Overhead", sc_overhead, "Height:", sc_height)
            print("Diff:", sc_diff, "Divers:", sc_diverse, "Wells", sc_wells)

        # Add dither
        score -= random.random()
        return score

    #
    # will first move the piece to the starting position, then it will rotate and move to the right and place
    # the piece on the board
    #
    def do_permutations(self, copy_quintris):
        curr_piece = copy_quintris.get_piece()
        rotations = self.get_rotations(copy_quintris.get_piece(), copy_quintris)
        # for rotation in range(4):  # rotation option off a piece
        #     rotated_piece = rotations[rotation]
        current_position = curr_piece[2]
        best_position = -1000000
        best_rotation = -1000000
        best_score = -1000000
        while current_position != 0:
            copy_quintris.left()
            current_position -= 1

        end_col = False

        while current_position < 15:
            rotation = 1
            temp_quintris = copy.deepcopy(copy_quintris)
            # rotations = self.get_rotations(temp_quintris.get_piece(), temp_quintris)
            for i in range(current_position + 1):
                copy_quintris.left()

            while rotation < 5:
                piece_place_quintris = copy.deepcopy(temp_quintris)
                rotated_piece = []
                for i in range(rotation):
                    if end_col and rotation == 1:
                        rotated_piece = piece_place_quintris.get_piece()
                        rotation += 1
                    else:
                        piece_place_quintris.rotate()
                        rotated_piece = piece_place_quintris.get_piece()

                    if end_col and rotation > 2:
                        rotated_piece = piece_place_quintris.rotate_piece(piece_place_quintris.get_piece()[0], 180)
                        rotation += 1

                if self.is_legit_position(rotated_piece, current_position):
                    # new_floor = self.get_new_floor(floor, rotated_piece, current_poistion, quin_obj)
                    piece_place_quintris.down()
                    new_floor = piece_place_quintris.get_board()
                    score = self.get_score(new_floor)
                    if show_scores:
                        print("Pos:", current_position, "Rot:", rotation, "Score:", score)
                        print("-" * 40)
                    if score > best_score:
                        best_score = score
                        best_position = current_position
                        best_rotation = rotation
                rotation += 1
            for i in range(current_position + 1):
                before_right = copy_quintris.get_piece()[2]
                copy_quintris.right()
                after_right = copy_quintris.get_piece()[2]

                if before_right == after_right:
                    copy_quintris.rotate()
                    copy_quintris.right()
                    end_col = True
            current_position += 1

        # commented code for flip and rotation, but was not ready to push to the git
        #
        # flipped_piece = quin_obj.hflip_piece(curr_piece[0])
        # rotations = self.get_rotations(flipped_piece)
        # for position in range(0, 14):  # position of a piece
        #     for rotation in range(4):  # rotation option off a piece
        #         rotated_piece = rotations[rotation]
        #         # print(rotated_piece)
        #         if self.is_legit_position(rotated_piece, position):
        #
        #             new_floor = self.get_new_floor(floor, rotated_piece, position, quin_obj)
        #             score = self.get_score(new_floor)
        #             if show_scores:
        #                 # print(new_floor)
        #                 print("Pos:", position, "Rot:", rotation, "Score:", score)
        #                 print("-" * 40)
        #
        #             if score > best_score:
        #                 best_score = score
        #                 best_position = position
        #                 best_rotation = rotation

        print("Best pos:", best_position, "Best rot:", best_rotation, "Best score:", best_score)
        return best_position, best_rotation

    # changes the mode according to the piece it want to place
    def set_mode(self, floor):
        global mode

        holes, _ = self.get_holes(floor)
        if holes > 0:
            mode = 0  # fix a hole
            return
        heights = []
        for i in range(len(floor[0])):
            c = []
            d = 0
            for j in range(len(floor)):
                c.append(floor[j][i])
            d = len(c)
            for k in range(len(c)):
                if c[k] == 'x':
                    break
                else:
                    d = len(c) - (k + 1)
            heights.append(d)
        if heights.count(0) == 1:
            heights.remove(0)
            if min(heights) > 3:
                mode = 1  # ready for a stick
                return
        mode = 2  # building a thing

    # returns a sequence of moves that the piece has to take to get to the best possible piece placement
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        temp = copy.deepcopy(quintris)
        floor = temp.get_board()
        move = ''
        left = 'b'
        right = 'm'
        rotate = 'n'
        h_flip = 'h'

        self.set_mode(floor)
        print(mode)

        best_position, best_rotation = self.do_permutations(temp)
        piece = quintris.get_piece()
        print(piece)
        curr_position = piece[2]
        print(best_position, best_rotation)
        if best_position == curr_position:
            # the piece will stay at the same position and only rotation will be applied
            if best_rotation > 0:
                move += ''.join([char * best_rotation for char in rotate])

        elif best_position < curr_position:

            # rotation if any
            if best_rotation > 0:
                move += ''.join([char * best_rotation for char in rotate])

            # we will have to move the piece to the left
            perfect_position = curr_position - best_position
            move += ''.join([char * perfect_position for char in left])

        elif best_position > curr_position:

            # rotation if any
            if best_rotation > 0:
                move += ''.join([char * best_rotation for char in rotate])

            perfect_position = best_position - curr_position
            move += ''.join([char * perfect_position for char in right])

        # return random.choice("mnbh") * random.randint(1, 10)
        return move

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column

        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [min([r for r in range(len(board) - 1, 0, -1) if board[r][c] == "x"] + [100, ]) for c in
                              range(0, len(board[0]))]
            index = column_heights.index(max(column_heights))

            # best_position, best_rotation = self.do_permutations(temp)
            moves = self.get_moves(quintris)

            for move in moves:
                if move == 'n':
                    quintris.rotate()
                elif move == 'b':
                    quintris.left()
                elif move == 'm':
                    quintris.right()
                elif move == 'h':
                    quintris.rotate()
                    quintris.rotate()
            quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)
