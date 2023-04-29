import pygame
import random
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
EVEN = 0
ODD = 1

class board:
    #Default Constructor (doesn't return )
    def __init__(self):
        #creates 6 by 7 matrix
        self.board = np.zeros((6, 7))
        self.game_over = False #game_over for this board

    def valid(self, board, column):
        column -= 1
        for r in range(ROW_COUNT):
            if self.board[r][column] == 0:
                return True
        return False
    
    def place_coin(self, column, piece):
        
        if (column > COLUMN_COUNT or column <= 0):
            print("Invalid Column")
            return

        row = self.get_first_empty_spot_in_column(column)
        if row < 0:
            print("Invalid Row")
            return
        else:
            column -= 1
            self.board[self.get_first_empty_spot_in_column(column)][column] = piece

    def remove_Coin(self, column):
        if (column > COLUMN_COUNT or column <= 0):
            print("Invalid Column")
            return
        column -= 1
        self.board[0][column] = 0
        for r in range(1, ROW_COUNT - 1):
            self.board[r - 1][column] = self.board[r][column]
        
        self.board[ROW_COUNT - 1][column] = 0

    def get_first_empty_spot_in_column(self, column):
        for i in range(ROW_COUNT):
            if self.board[i][column] == 0:
                return i
        
        return -1
    
    #getter function for game_over
    def game_over(self):
        return self.game_over
    #getter function for print board
    def print_board(self):
        for index in range(len(self.board)-1, -1, -1):
            print(self.board[index])
    
    def check_win(self,coin):
        #check horizontally
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == coin and self.board[r][c+1] == coin and self.board[r][c+2] == coin and self.board[r][c+3] == coin:
                    return True
        
def PvP():
    Board = board()
    turn = 0


    running = True
    while (running):

        userinput = input("pop or place? ")

        if userinput == "q":
            running = False
            break


        elif userinput == "place":
            col = input("Player 1: Select where to drop (1 - " + str(COLUMN_COUNT) + "):")
            
            if (not col.isnumeric()):
                print("Error, invalid input")
            
            else:
                if turn % 2 == 0:
                    Board.place_coin(int(col), 2)
                else:
                    Board.place_coin(int(col), 6)
                turn += 1
        
        elif userinput == "pop":
            col = input("Player 1: Select where to remove (1 - " + str(COLUMN_COUNT) + "):")

            if (not col.isnumeric()):
                print("Error, invalid input")
                running = False
            else:
                Board.remove_Coin(int(col))
                running = False
    
        
        Board.print_board()
        #Change 2 and 6 to find wins
        if Board.check_win(2):
            print("Player 1 wins!!")
            running = False
        elif Board.check_win(6):
            print("Player 2 wins!!")
            running = False
    

def print_menu():
    print("Welcome to Connect 4++!")
    
    running = True

    while running:
    
        print("User Menu:")
        print("1. Player vs AI")
        print("2. Player vs Player")
        userInput = input("Please select an option: ") #whatever user inputs will be stored in userInput

        if userInput == "1" or userInput == "2":
            running = False
            break
        
        print()

    return userInput
    

def main():

    userInput = print_menu()

    if userInput == "1":
        pass
    elif userInput == "2":
        PvP()


    



if __name__ == "__main__":
    main()
