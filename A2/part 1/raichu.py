#
# raichu.py : Play the game of Raichu
#
# Pramey Modi [pmmodi], Akshay Tiwlekar [akstiwle], Rohan Mehta [mehtaro]
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import heapq
import sys
import time
import numpy as np
from copy import deepcopy

def board_to_string(board, N):
    board1 = "\n".join(board[i:i + N] for i in range(0, len(board), N))
    return board1


class Board:
    def __init__(self,a,max):
        self.W_left = 0  # just initializing
        self.w_left = 0  # this all will get updated in cheak function
        self.B_left = 0  # length of the set
        self.b_left = 0  # ends here
        self.WR_left = 0 # number of white richu left
        self.BR_left = 0 # number of black richu left
        self.board = a # the board in terms of matrix has been passed
        self.ROWS = N # takes the number of row and column form the board
        self.COLS = N
        self.max_player = max # get the value of max player
        self.Whitesu = []
        self.Blacksu = []


    # def evaluate(self):
    #     self.white = self.W_left + self.w_left # return the number of white pieces on the board
    #     self.black = self.B_left + self.b_left # return the number of black pieces on the board
    #     self.Richu = self.WR_left * 0.5 - self.BR_left * 0.5
    #     return self.white - self.black +(self.Richu)
    # def validmoves(self):
    #
    """lcoations of all the pices in the set """
    def cheakwhitepichu(self):
        whitepichu = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'w':
                        whitepichu[i, j] = self.board[i][j]
        w = set()
        for i,j in whitepichu.items():
            w.add(i)
        self.w_left = len(w)
        return w
    def cheakwhitepikachu(self):   # this will add the lications of white pikachu to the set
        whitepikachu = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'W':
                        whitepikachu[i, j] = self.board[i][j]
        W = set()
        for i,j in whitepikachu.items():
            W.add(i)
        self.W_left = len(W)
        return W

    def cheakblackpichu(self):   # this will add the lications of blck pichu to the set
        blackpichu= {} # wtore both location as key and valeu
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'b':
                        blackpichu[i, j] = self.board[i][j]
        b = set()
        for i,j in blackpichu.items():
            b.add(i)
        self.b_left = len(b)
        return b

    def cheakblackpikachu(self):   # this will add the lications of black pikachu to the set
        blackpikachu = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'B':
                        blackpikachu[i, j] = self.board[i][j]
        B = set()
        for i,j in blackpikachu.items():
            B.add(i)
        self.B_left = len(B)
        return B
    def cheakdot(self): # this will cheak the location of dots
        dots = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == '.':
                    dots[i, j] = self.board[i][j]
        dot = set()
        for i, j in dots.items():
            dot.add(i)
        self.B_left = len(dot)
        return dot
    """"stores all the pices location in the set """

    def movewhitepichu(self):
        w = self.cheakwhitepichu()
        b = self.cheakblackpichu()
        dot = self.cheakdot()
        blacklist = []
        blacklist2 = []
        rightmov = set()
        leftmov = set()
        for i,j in w:
            #b1=self.list_cpy(b)
            print(i,j)
            if i>= 0 and j> 0 and i< N and j< N - 1 : # location of w is inner box this will work
                mov1 = (i + 1,j + 1)
                mov2 = (i + 1,j - 1)
                # if mov1 in b:
                #     mov1 = (i, j)
                if mov1 in b:
                    # if i >= 0 and j > 1 and i <= N and j < N - 2: # when land on b and will skip the balck b
                        blacklist.append(mov1)
                        mov1 = (i + 2,j + 2)
                        if mov1 not in dot: # ther is other b so it will return to the main point
                            mov1 = (i ,j )
                            blacklist.remove(mov1)
                else:
                    blacklist.append(())
                # if mov2 in b :
                #     mov2 = (i, j)
                if mov2 in b:
                    #if i >= 0 and j > 1 and i <= N and j < N - 2:
                        blacklist2.append((mov2))
                        mov2 = (i + 2,j - 2)
                        if mov2 not in dot:
                            mov2 = (i , j )
                            blacklist2.remove(mov2)
                else:
                    blacklist2.append(())
                rightmov.add(mov1)
                leftmov.add(mov2)
                #return mov1,mov2
            elif i>=0 and j==0: # when w location is on the border of the box
                mov1 = (i + 1, j + 1)
                if mov1 in b:# when land on b and will skip the balck b
                    blacklist.append(mov1)
                    mov1 = (i + 2, j + 2)
                    if mov1 not in dot:# ther is other b so it will return to the main point
                        mov1 = (i , j)
                        blacklist.remove(mov1)
                else:
                    blacklist.append(())
                rightmov.add(mov1)
                #return mov1

            elif i<=N-1 and j==N-1:
                mov2 = (i + 1,j - 1)
                if mov2 in b:# when land on b and will skip the balck b
                    blacklist2.append(mov2)
                    mov2 = (i + 2, j - 2)
                    if  mov2 not in dot:# ther is other b so it will return to the main point
                        mov2 = (i ,j)
                        blacklist2.remove(mov2)
                else:
                    blacklist2.append(())
                leftmov.add(mov2)
                #return mov2

        return rightmov,leftmov,blacklist,blacklist2 # got the vlaue of all the move location

    def moveblackpichu(self):
        w = self.cheakwhitepichu()
        b = self.cheakblackpichu()
        rightmov = set()
        leftmov = set()
        blacklist = []
        blacklist2 = []
        for i, j in b:
            print(i, j)
            if i >= 0 and j > 0 and i < N and j < N - 1:  # location of w is inner box this will work
                mov1 = (i - 1, j + 1)
                mov2 = (i - 1, j - 1)
                # if mov1 in w:
                #     mov1 = (i, j)
                if mov1 in w:
                    # eif i >= 0 and j > 1 and i <= N and j < N - 2: # when land on b and will skip the balck b
                    blacklist.append(mov1)
                    mov1 = (i - 2, j + 2)
                    if mov1 in b:  # ther is other b so it will return to the main point
                        mov1 = (i, j)
                        blacklist.remove(mov1)
                else:
                    blacklist.append(())
                #
                if mov2 in w:
                    # if i >= 0 and j > 1 and i <= N and j < N - 2:
                    blacklist2.append(mov2)
                    mov2 = (i - 2, j - 2)

                    if mov2 in b:
                        mov2 = (i, j)
                        blacklist2.remove(mov2)
                else:
                    blacklist2.append(())
                rightmov.add(mov1)
                leftmov.add(mov2)
                # return mov1,mov2
            elif i >= 0 and j == 0:  # when w location is on the border of the box
                mov1 = (i - 1, j + 1)
                if mov1 in w:  # when land on b and will skip the balck b
                    blacklist.append(mov1)
                    mov1 = (i - 2, j + 2)
                    if mov1 in w:  # ther is other b so it will return to the main point
                        mov1 = (i, j)
                        blacklist.remove(mov1)
                else:
                    blacklist.append(())
                rightmov.add(mov1)
                # return mov1

            elif i <= N - 1 and j == N - 1:
                mov2 = (i - 1, j - 1)
                if mov2 in w:  # when land on b and will skip the balck b
                    blacklist2.append(mov2)
                    mov2 = (i - 2, j - 2)
                    if mov2 in w:  # ther is other b so it will return to the main point
                        mov2 = (i, j)
                        blacklist2.remove(mov2)
                else:
                    blacklist2.append(())
                leftmov.add(mov2)
                # return mov2

        return rightmov, leftmov, blacklist, blacklist2  # got the vlaue of all the move lon


    def movewhitepikahcu(self):
        W = self.cheakwhitepikachu()
        B = self.cheakblackpikachu()
        b = self.cheakblackpichu()
        dot = self.cheakdot()
        moveup1 = set() # store pikachu up +1 and +2 both
        moveup2 = set()
        moveright1 = set()
        moveright2 = set()
        moveleft1 = set()
        moveleft2 = set()
        blklist1 = []
        blklist2 = []
        blklist3 = []
        blklist4 = []
        blklist5 = []
        blklist6 = []
        # for moveup1 ......1111.....
        for i, j in W:
            if i < N-1:
                #print('true')
                movup1 = (i + 1, j)
                if movup1 in B :
                    blklist1.append(movup1)
                    movup1 = (i + 2, j)
                    if movup1 not in dot:
                        movup1 = (i,j)
                        blklist1.remove(movup1)
                elif movup1 in b:
                    #print('true')
                    blklist1.append(movup1)
                    movup1 = (i + 2, j)
                    if movup1 not in dot:
                        movup1 = (i,j)
                        blklist1.remove(movup1)
                else:
                    blklist1.append(())
                # if j +2 or j+1 or i +1 or i +2>= N-1:
                #     movup1 = (i, j)
                moveup1.add(movup1)
            elif i == N - 1:
                movup1 = (i, j)
                moveup1.add(movup1)
        # for moveup 2 ..........222
        for i, j in W:
            if i < N-2:
                movup2 = (i + 2 , j)
                if movup2 in B :
                    blklist2.append(movup2)
                    movup2 = (i + 3, j)
                    if movup2 not in dot:
                        movup2 = (i,j)
                        blklist2.remove(movup2)
                elif movup2 in b:
                    movup2 = (i + 3, j)
                    if movup2 not in dot:
                        movup2 = (i,j)
                        blklist2.remove(movup2)
                else:
                    blklist2.append(())
                moveup2.add(movup2)
                # if i + 2 >= N - 1:
                #     movup2 = (i, j)


            elif i == N - 2:
                movup2 = (i+1,j)
                moveup2.add(movup2)
        # # for movedown1 ......1111.....
        # for i, j in W:
        #     if i > 0:
        #         movdown1 = (i - 1, j)
        #         if movdown1 in B:
        #             movdown1 = (i - 2, j)
        #         elif movdown1 in b:
        #             movdown1 = (i - 2, j)
        #         if movdown1 in B:
        #             movdown1 = (i, j)
        #         elif movdown1 in b:
        #             movdown1 = (i, j)
        #         if j +2 or j+1 or i +1 or i +2>= N-1:
        #             movdown1 = (i, j)
        #         movedown1.add(movdown1)
        #     elif i == 0:
        #         movdown1 = (i,j)
        #         movedown1.add(movdown1)
        # # for movedown 2 ..........222
        # for i, j in W:
        #     if j > 1:
        #         movdown2 = (i - 1, j)
        #         if movdown2 in B:
        #             movdown2 = (i - 2, j)
        #         elif movdown2 in b:
        #             movdown2 = (i - 3, j)
        #         if movdown2 in B:
        #             movdown2 = (i, j)
        #         elif movdown2 in b:
        #             movdown2 = (i, j)
        #         movedown2.add(movdown2)
        #         if j +2 or j+1 or i +1 or i +2>= N-1:
        #             movdown2 = (i, j)
        #     elif i == 1:
        #         movdown2 = (i - 1,j)
        #         movedown2.add(movdown2)
        #move right 1........1..1......
        for i, j in W:
            if j < N-1:
                #print('true')
                movright1 = (i, j +1)
                if movright1 in B :
                    blklist3.append(movright1)
                    movright1 = (i, j + 2)
                    if movright1 not in dot:
                        movright1 = (i,j)
                        blklist3.remove(movright1)
                elif movright1 in b:
                    blklist3.append(movright1)
                    movright1 = (i, j + 2)
                    if movright1 not in dot:
                        movright1 = (i,j)
                        blklist3.remove(movright1)
                else:
                    blklist3.append(())
                moveright1.add(movright1)
                if j >= N - 1:
                    movright1 = (i, j)
                if movright1 not in dot:
                    movright1 = (i,j)
                if j +2 or j+1 or i +1 or i +2>= N-1:
                    movright1 = (i, j)
                    #moveright1.add(movright1)
                    if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                        movright1 = (i, j)
            elif j == N - 1:
                movright1 = (i, j)
                moveright1.add(movright1)
        # for moveright 2 ..........222
        for i, j in W:
            if j < N-1:
                movright2 = (i, j + 2)
                if movright2 in B :
                    blklist4.append(movright2)
                    movright2 = (i, j + 3)
                    if movright2 not in dot:
                        movright2 = (i,j)
                        blklist4.remove(moveright2)
                elif movright2 in b:
                    blklist4.append(moveright2)
                    movright2 = (i, j + 3)
                    if movright2 not in dot:
                        movright2 = (i,j)
                        blklist4.remove(movright2)
                else:
                    blklist4.append(())
                moveright2.add(movright2)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movright2 = (i, j)
            elif j == N - 2:
                movright2 = (i,j + 1)
                moveright2.add(movright2)
        # for moveleft1 ......1111.....
        for i, j in W:
            if j > 0:
                movleft1 = (i, j -1)
                if movleft1 in B:
                    blklist5.append(movleft1)
                    movleft1 = (i - 2, j)
                    if movleft1 not in dot:
                        movleft1 = (i,j)
                        blklist5.remove((movleft1))
                elif movleft1 in b:
                    blklist5.append(movleft1)
                    movleft1 = (i, j - 2)
                    if movleft1 not in dot:
                        movleft1 = (i,j)
                        blklist5.remove(movleft1)
                else:
                    blklist5.append(())

                moveleft1.add(movleft1)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movleft1 = (i, j)
            elif j == 0:
                movleft1 = (i,j)
                moveleft1.add(movleft1)
                blklist5.append(())
        # for moveleft 2 ..........222
        for i, j in W:
            if j > 1:
                movleft2 = (i, j - 2)
                if movleft2 in B:
                    blklist6.append(movleft2)
                    movleft2 = (i, j -3)
                    if movleft2 not in dot:
                        movleft2 = (i,j)
                        blklist6.remove(movleft2)
                        blklist6.append(())
                elif movleft2 in b:
                    blklist6.append(movleft2)
                    movleft2 = (i, j - 3)
                    if movleft2 not in dot:
                        movleft2 = (i,j)
                        blklist6.remove(movleft2)
                        blklist6.append(())
                else:
                    blklist6.append(())

                moveleft2.add(movleft2)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movleft2 = (i, j)
            elif j == 1:
                movleft2 = (i,j - 1)
                moveleft2.add(movleft2)
            elif j == 0:
                movleft2 = (i,j)
                moveleft2.add(movleft2)
                blklist6.append(())
        return moveup1,moveup2,moveright1,moveright2,moveleft1,moveleft2,blklist1,blklist2,blklist3,blklist4,blklist5,blklist6

    def moveblackpikahcu(self):
        W = self.cheakwhitepikachu()
        B = self.cheakblackpikachu()
        w = self.cheakwhitepichu()
        dot = self.cheakdot()
        movedown1 = set()  # store pikachu down -1 and -2 both
        movedown2 = set()
        moveright1 = set()
        moveright2 = set()
        moveleft1 = set()
        moveleft2 = set()
        blklist1 = []
        blklist2 = []
        blklist3 = []
        blklist4 = []
        blklist5 = []
        blklist6 = []
        # for moveup1 ......1111.....
        # for i, j in B:
        #     if i < N - 1:
        #         # print('true')
        #         movup1 = (i + 1, j)
        #         if movup1 in W:
        #             movup1 = (i + 2, j)
        #         elif movup1 in w:
        #             # print('true')
        #             movup1 = (i + 2, j)
        #         if movup1 in W:
        #             movup1 = (i, j)
        #         elif movup1 in w:
        #             movup1 = (i, j)
        #         moveup1.add(movup1)
        #         if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
        #             movup1 = (i, j)
        #     elif i == N - 1:
        #         movup1 = (i, j)
        #         moveup1.add(movup1)
        # for moveup 2 ..........222
        # for i, j in B:
        #     if i < N - 2:
        #         movup2 = (i + 2, j)
        #         if movup2 in W:
        #             movup2 = (i + 3, j)
        #         elif movup2 in w:
        #             movup2 = (i + 3, j)
        #         if movup2 in W:
        #             movup2 = (i, j)
        #         elif movup2 in w:
        #             movup2 = (i, j)
        #         moveup2.add(movup2)
        #         if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
        #             movup2 = (i, j)
        #     elif i == N - 2:
        #         movup2 = (i + 1, j)
        #         moveup2.add(movup2)
        # for movedown1 ......1111.....
        for i, j in B:
            if i > 0:
                movdown1 = (i - 1, j)
                if movdown1 in W:
                    blklist1.append(movdown1)
                    movdown1 = (i - 2, j)
                    if movdown1 not in dot:
                        movdown1 = (i,j)
                        blklist1.remove(movdown1)
                elif movdown1 in w:
                    blklist1.append(movdown1)
                    movdown1 = (i - 2, j)
                    if movdown1 not in dot:
                        movdown1 = (i,j)
                        blklist1.remove(movdown1)
                if movdown1 in W:
                    movdown1 = (i, j)
                elif movdown1 in w:
                    movdown1 = (i, j)
                else:
                    blklist1.append(())
                movedown1.add(movdown1)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movdown1 = (i, j)
            elif i == 0:
                movdown1 = (i, j)
                movedown1.add(movdown1)
                blklist1.append(())
        # for movedown 2 ..........222
        for i, j in B:
            if j > 1:
                movdown2 = (i - 1, j)
                if movdown2 in W:
                    blklist2.append(movdown2)
                    movdown2 = (i - 2, j)
                    if movdown2 not in dot:
                        movdown2 = (i,j)
                        blklist2.remove(movdown2)
                elif movdown2 in w:
                    blklist2.append(movdown2)
                    movdown2 = (i - 3, j)
                    if movdown2 not in dot:
                        movdown2 = (i,j)
                        blklist2.remove(movdown2)
                else :
                    blklist2.append(())
                movedown2.add(movdown2)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movdown2 = (i, j)
            elif i == 1:
                movdown2 = (i - 1, j)
                movedown2.add(movdown2)
                blklist2.append(())

        # move right 1........1..1......
        for i, j in B:
            if j < N - 1:
                # print('true')
                movright1 = (i, j + 1)
                if movright1 in W:
                    blklist3.append(movright1)
                    movright1 = (i, j + 2)
                    if movright1 not in dot:
                        movright1 = (i,j)
                        blklist3.remove(movright1)
                elif movright1 in w:
                    blklist3.append(movright1)
                    movright1 = (i, j + 2)
                    if movright1 not in dot:
                        movright1 = (i,j)
                        blklist3.remove(movright1)
                else:
                    blklist3.append(())
                moveright1.add(movright1)
                if j >= N - 1:
                    movright1 = (i, j)
                    if movright1 not in dot:
                        movright1 = (i,j)
                    moveright1.add(movright1)
                    if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                        movright1 = (i, j)
            elif j == N - 1:
                movright1 = (i, j)
                moveright1.add(movright1)
                blklist3.append(())
        # for moveright 2 ..........222
        for i, j in B:
            if j < N - 2:
                movright2 = (i, j + 2)
                if movright2 in W:
                    blklist4.append(movright2)
                    movright2 = (i, j + 3)
                    if movright2 not in dot:
                        movright2 = (i,j)
                        blklist3.remove(movright2)
                elif movright2 in w:
                    blklist3.append(movright2)
                    movright2 = (i, j + 3)
                    if movright2 not in dot:
                        movright2 = (i,j)
                        blklist3.remove(movright2)
                else:
                    blklist4.append(())
                moveright2.add(movright2)
                # if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                #     movright2 = (i, j)
            elif j == N - 2:
                movright2 = (i, j + 1)
                moveright2.add(movright2)
                blklist4.append(())
        # for moveleft1 ......1111.....
        for i, j in B:
            if j > 0:
                movleft1 = (i, j - 1)
                if movleft1 in W:
                    blklist5.append(movleft1)
                    movleft1 = (i - 2, j)
                    if movleft1 not in dot:
                        movleft1 = (i,j)
                        blklist5.remove(movleft1)
                elif movleft1 in w:
                    blklist5.append(movleft1)
                    movleft1 = (i, j - 2)
                    if movleft1 not in dot:
                        movleft1 = (i,j)
                        blklist5.remove(movleft1)
                else:
                    blklist5.append(())
                moveleft1.add(movleft1)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movleft1 = (i, j)
            elif j == 0:
                movleft1 = (i, j)
                moveleft1.add(movleft1)
                blklist5.append(())
        # for moveleft 2 ..........222
        for i, j in B:
            if j > 1:
                movleft2 = (i, j - 2)
                if movleft2 in W:
                    blklist6.append(movleft2)
                    movleft2 = (i, j - 3)
                    if movleft2 not in dot:
                        movleft2 = (i,j)
                        blklist6.remove(movleft2)
                elif movleft2 in w:
                    blklist6.append(movleft2)
                    movleft2 = (i, j - 3)
                    if movleft2 not in dot:
                        movleft2 = (i,j)
                        blklist6.remove(movleft2)
                else:
                    blklist6.append(())
                moveleft2.add(movleft2)
                if j + 2 or j + 1 or i + 1 or i + 2 >= N - 1:
                    movleft2 = (i, j)
            elif j == 1:
                movleft2 = (i, j - 1)
                moveleft2.add(movleft2)
            elif j == 0:
                movleft2 = (i, j)
                moveleft2.add(movleft2)
                blklist6.append(())
        return  movedown1, movedown2, moveright1, moveright2, moveleft1, moveleft2,blklist1,blklist2,blklist3,blklist4,blklist5,blklist6

    def creat_board_wpichu(self): # this will creat all the borads for white pichi moves
        """all the variabel in between store the list of orignal locations of pichu and pikachu"""
        self.origw = self.cheakwhitepichu()
        self.origw = list(self.origw)  # store the valuse of white pichu
        self.origw.sort()
        self.a = []
        """ends hear orignal"""
        """store the location of all themove pichu pikachu locations"""
        wrig,wlef,blacklsit1,blacklist2 = self.movewhitepichu()
        wright_move = list(wrig)
        wleft_move = list(wlef)
        wright_move.sort()
        for i in range(len(wright_move)):
            lst1=self.list_cpy(self.origw)
            temp=wright_move[i]
            lst1[i]=temp
            dead_bp = blacklsit1[i]
            #print(dead_bp)
            temp1 = self.make_board(lst1,self.cheakwhitepikachu(),self.cheakblackpichu(),self.cheakblackpikachu())
            #print('before dead',temp1)
            if(dead_bp!=()):
                temp1[dead_bp[0]][dead_bp[1]]='.'
            #print('aftear dead',temp1)
            self.Whitesu.append(temp1)
        for i in range(len(wleft_move)):
            lst1=self.list_cpy(self.origw)
            temp=wleft_move[i]
            lst1[i]=temp
            dead_bp = blacklist2[i]
            temp2 = self.make_board(lst1,self.cheakwhitepikachu(),self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_bp != ()):
                temp2[dead_bp[0]][dead_bp[1]] = '.'
           # print(temp2)
            self.Whitesu.append(temp2)
        return self.Whitesu
    def creat_board_bpichu(self):
        orgib = self.cheakblackpichu()
        orgib = list(orgib)
        brig,blef,blacklist1,blacklist2 = self.moveblackpichu()
        bright_move = list(brig)
        bleft_move = list(blef)
        bright_move.sort()
        bleft_move.sort()
        for i in range(len(bright_move)):
            lst2=self.list_cpy(orgib)
            temp = bright_move[i]
            lst2[i] = temp
            dead_wp = blacklist1[i]
            temp1 = self.make_board(self.cheakwhitepichu(),self.cheakwhitepikachu(),lst2,self.cheakblackpikachu())
            #print('before',temp1)
            if (dead_wp != ()):
                temp1[dead_wp[0]][dead_wp[1]] = '.'
            #print('aftear dead', temp1)
            self.Blacksu.append(temp1)
        for i in range(len(bleft_move)):
            lst2=self.list_cpy(orgib)
            temp=bleft_move[i]
            lst2[i] = temp
            dead_wp = blacklist2[i]
            temp2 = self.make_board(self.cheakwhitepichu(),self.cheakwhitepikachu(),lst2,self.cheakblackpikachu())
            if (dead_wp != ()):
                temp2[dead_wp[0]][dead_wp[1]] = '.'
            #print('aftear dead', temp2)
            self.Blacksu.append(temp2)
        return self.Blacksu
    # draw board for white pikachu
    def creat_board_wpikachu(self):
        orgiW = self.cheakwhitepikachu()
        orgiW = list(orgiW)
        up1,up2,right1,right2,left1,left2,blklist1,blklist2,blklist3,blklist4,blklist5,blklist6 = self.movewhitepikahcu()
        up1 = list(up1)
        up2 = list(up2)
        # down1 = list(down1)
        # down2 = list(down2)
        right1 = list (right1)
        right2 = list(right2)
        left1 = list(left1)
        left2 = list(left2)
        up1.sort(),up2.sort(),left1.sort(),left2.sort(),right1.sort(),right2.sort()
        #print(blklist3)
        #draw borad for up movement
        for i in range(len(up1)):
            lst2=self.list_cpy(orgiW)
            temp = up1[i]
            lst2[i] = temp
            dead_bp = blklist1[i]
            temp1 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_bp != ()):
                temp1[dead_bp[0]][dead_bp[1]] = '.'
            #print(temp1)
            self.Whitesu.append(temp1)
            #print(temp1)
        # draw board for up2 movement movement
        for i in range(len(up2)):
            lst2=self.list_cpy(orgiW)
            temp = up2[i]
            dead_Bp = blklist2[i]
            lst2[i] = temp
            temp2 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_Bp != ()):
                temp2[dead_Bp[0]][dead_Bp[1]] = '.'
            #print(temp2)
            self.Whitesu.append(temp2)
            #print(temp2)
        # draw board for right1
        for i in range(len(right1)):
            lst2=self.list_cpy(orgiW)
            temp = right1[i]
            dead_bp = blklist3[i]
            lst2[i] = temp
            temp3 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_bp != ()):
                temp3[dead_bp[0]][dead_bp[1]] = '.'
            #print(temp3)
            self.Whitesu.append(temp3)
        #draw board for right 2 movement
        for i in range(len(right2)):
            lst2=self.list_cpy(orgiW)
            temp = right2[i]
            dead_Bp = blklist4[i]
            lst2[i] = temp
            temp4 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_Bp != ()):
                temp4[dead_Bp[0]][dead_Bp[1]] = '.'
            print(temp4)
            self.Whitesu.append(temp4)
        # draw board for left 1 movement
        for i in range(len(left1)):
            lst2=self.list_cpy(orgiW)
            temp = up2[i]
            dead_bp = blklist5[i]
            lst2[i] = temp
            temp5 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_bp != ()):
                temp5[dead_bp[0]][dead_bp[1]] = '.'
            print(temp5)
            self.Whitesu.append(temp5)
        # draw board for left 2 movemnet
        for i in range(len(left2)):
            lst2 = self.list_cpy(orgiW)
            temp = up2[i]
            dead_Bp = blklist6[i]
            lst2[i] = temp
            temp6 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_Bp != ()):
                temp6[dead_Bp[0]][dead_Bp[1]] = '.'
            print(temp6)
            self.Whitesu.append(temp6)
        return self.Whitesu
    #creat board foe black pikachu
    def creat_board_bpikachu(self):
        orgiW = self.cheakwhitepikachu()
        orgiW = list(orgiW)
        down1,down2,right1,right2,left1,left2,blklist1,blklist2,blklist3,blklist4,blklist5,blklist6 = self.movewhitepikahcu()
        # up1 = list(up1)
        # up2 = list(up2)
        down1 = list(down1)
        down2 = list(down2)
        right1 = list (right1)
        right2 = list(right2)
        left1 = list(left1)
        left2 = list(left2)
        down1.sort(),down2.sort(),left1.sort(),left2.sort(),right1.sort(),right2.sort()
       # draw borad for up movement
        for i in range(len(down1)):
            lst2=self.list_cpy(orgiW)
            temp = down1[i]
            lst2[i] = temp
            dead_wp = blklist1[i]
            temp1 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_wp != ()):
                temp1[dead_wp[0]][dead_wp[1]] = '.'
            print(temp1)
            self.Blacksu.append(temp1)
        # draw board for up2 movement movement
        for i in range(len(down2)):
            lst2=self.list_cpy(orgiW)
            temp = down2[i]
            lst2[i] = temp
            dead_Wp = blklist2[i]
            temp2 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_Wp != ()):
                temp2[dead_Wp[0]][dead_Wp[1]] = '.'
            print(temp2)
            self.Blacksu.append(temp2)
        #draw board for right1
        for i in range(len(right1)):
            lst2=self.list_cpy(orgiW)
            temp = right1[i]
            dead_wp = blklist4[i]
            lst2[i] = temp
            temp3 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_wp != ()):
                temp3[dead_wp[0]][dead_wp[1]] = '.'
            print(temp3)
            self.Blacksu.append(temp3)
        #draw board for right 2 movement
        for i in range(len(right2)):
            lst2=self.list_cpy(orgiW)
            temp = right2[i]
            dead_Wp = blklist5[i]
            lst2[i] = temp
            temp4 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_Wp != ()):
                temp4[dead_Wp[0]][dead_Wp[1]] = '.'
            print(temp4)
            self.Blacksu.append(temp4)
        # draw board for left 1 movement
        for i in range(len(left1)):
            lst2=self.list_cpy(orgiW)
            temp = left1[i]
            dead_wp = blklist5[i]
            lst2[i] = temp
            temp5 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_wp != ()):
                temp5[dead_wp[0]][dead_wp[1]] = '.'
            print(temp5)
            self.Blacksu.append(temp5)
        # draw board for left 2 movemnet
        for i in range(len(left2)):
            lst2 = self.list_cpy(orgiW)
            temp = left2[i]
            dead_Wp = blklist6[i]
            lst2[i] = temp
            temp6 = self.make_board(self.cheakwhitepichu(),lst2,self.cheakblackpichu(),self.cheakblackpikachu())
            if (dead_Wp != ()):
                temp6[dead_Wp[0]][dead_Wp[1]] = '.'
            print(temp6)
            self.Blacksu.append(temp6)
        return self.Blacksu
    def list_cpy(self,lst): # create the list
        lst1=[]
        for i in lst:
            lst1.append(i)
        return lst1

    def make_board(self,w,W,b,B):
        # W = self.cheakwhitepikachu()
        # b = self.origb
        # B = self.cheakblackpikachu()
        Rw = []
        Rb = []
        lst = [[0 for i in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                if ((i, j) in w):
                    lst[i][j] = "w"
                elif ((i, j) in W):
                    lst[i][j] = "W"
                elif ((i, j) in b):
                    lst[i][j] = "b"
                elif ((i, j) in B):
                    lst[i][j] = "B"
                elif ((i, j) in Rw):
                    lst[i][j] = "@"
                elif ((i, j) in Rb):
                    lst[i][j] = "$"
                else:
                    lst[i][j] = "."
        return lst

    def getall_board(self):
        White_list = self.creat_board_bpikachu()
        Black_list = self.creat_board_bpikachu()
        return White_list,Black_list
class Minmax(Board):
    def __init__(self, a, max):
        Board.__init__(self, a, max)

    def get_sucessor(self,player):
        if player == 'w':
            return self.Whitesu
        else :
            return self.Blacksu

    def game_over(self):
        if (self.W_left + self.w_left <= 0):
            return True, 'Black'
        elif (self.B_left + self.b_left <= 0):
            return True, 'White'
        return False
    def eval_board(self, a):
        listscore_w = []
        listscore_b = []
        #print(len(a))
        for i in range(len(a)) :
            board_matrix = a[i]
        # end, winner = self.game_over()
        # if (end):
        #     if (winner == self.max_player):
        #         return +2222
        #     else:
        #         return -2222
            N = len(board_matrix)
            score = 0
            for i in board_matrix:
                print(i)
                for j in i:
                    if (j == '.'):
                        continue
                    elif (j == 'w'):
                        #self.w_left += 1
                        score += 1
                    elif (j == 'W'):
                        #self.W_left += 1
                        score += 2
                    elif (j == '@'):
                        score += N
                    elif (j == 'b'):
                        #self.b_left += 1
                        score -= 1
                    elif (j == 'B'):
                        #self.B_left += 1
                        score -= 2
                    elif (j == '$'):
                        score -= N
            if (self.max_player == 'b'):
                listscore_w.append(-1 * score)
            else:
                listscore_w.append(score)
        # for i in range(len(b)):
        #     board_matrix = a[i]
        #     end, winner = self.game_over()
        #     if (end):
        #         if (winner == self.max_player):
        #             return +2222
        #         else:
        #             return -2222
        #     N = len(board_matrix)
        #     score = 0
        #     for i in board_matrix:
        #         print(i)
        #         for j in i:
        #             if (j == '.'):
        #                 continue
        #             elif (j == 'w'):
        #                 # self.w_left += 1
        #                 score += 1
        #             elif (j == 'W'):
        #                 # self.W_left += 1
        #                 score += 2
        #             elif (j == '@'):
        #                 score += N
        #             elif (j == 'b'):
        #                 # self.b_left += 1
        #                 score -= 1
        #             elif (j == 'B'):
        #                 # self.B_left += 1
        #                 score -= 2
        #             elif (j == '$'):
        #                 score -= N
        #     if (self.max_player == 'b'):
        #         listscore_b.append(-1 * score)
        #     else:
        #         listscore_b.append(score)
        # print (len(listscore_b))
        return listscore_w

    def getsucessor(self,a):
        sucessor = []
        #Black_sucessor = []
        for i in range(len(a)):
            subboard = a[i]
            Board(subboard, player)
            sucessor=self.getall_board()
        # for j in range(len(b)):
        #     subboard = b[j]
        #     Board(subboard, player)
        #     Black_sucessor=self.getall_board()

        return sucessor
    '''starting the min max algorithm with alpha beta pruning'''

'''' dicuss the code with Dinesh Dchalla redy and get some portion of the code also get dsome of the code from Geeks for geeks
    # lisnk: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
'''
# computes the minimum value among the successors of a given state
def min_play(self, successor, alpha, beta, depth, player, depthlimit, N):
    depth += 1
    if depth == depthlimit or self.game_over()[0]:
        return self.eval_board(successor)
    else:
        if (player == "w"):
            other_player = "b"
        else:
            other_player = "w"
        maxsuccessors = self.getsucessor(successor)
        for (r, c), maxsucc in maxsuccessors:
            beta = min(beta, self.max_play(maxsucc, alpha,
                                           beta, depth, player, depthlimit, N))
            if alpha >= beta:
                return beta
        return beta

# computes the maximum value among the successors of a given state
def max_play(self, successor, alpha, beta, depth, player, depthlimit, N):
    depth += 1

    if depth >= depthlimit or self.game_over()[0]:
        return self.eval_board(successor)
    else:
        minsuccessors = self.getsucessor(successor)
        for (r, c), minsucc in minsuccessors:
            alpha = max(alpha, self.min_play(minsucc, alpha,
                                             beta, depth, player, depthlimit, N))
            if alpha >= beta:
                return alpha
        return alpha

def min_max(self, board, player, N, depth):
    succs = self.getsucessor(board)
    init_beta, init_alpha = float("inf"), float('-inf')
    max_heap = []
    for (r,c), minsucc in succs:
        heapq.heappush(max_heap, (self.min_play(
            minsucc, init_alpha, init_beta, 0, player, depth, N) * -1, minsucc))
    return heapq.heappop(max_heap)[1]
# refrence ends here



def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    asss = board_to_string(board, N)
    templist = [] # this is just ot convert the string in terms of matrix
    board1 = list((board[i:i + N] for i in range(0, len(board), N)))
    m = list()
    for i in range(len(board1)):
        m.append(list(board1[i]))
    #print(m)
    obj = Board(m, player)
    obj2 = Minmax(m, player)
    a = obj.getall_board()
    #obj2.getsucessor(a,b)

    #print(obj2.getsucessor(a,b))
    print(obj2.min_max(m,N, player, timelimit))

    # def getsucessor(a):
    #     for i in a:
    #         subboard = a[i]
    #         aobj = Board(subboard, player)
    #
    #     print(aobj.getall_board())
    #print(m)
    #print(obj2.eval_board(a))
    #print(obj.creat_board_wpikachu())


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)


