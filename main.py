import pygame
import random
import numpy as np

random.seed(0)

ROW_COUNT = 6
COLUMN_COUNT = 7

class board:
    #Default Constructor (doesn't return )
    def __init__(self):
        #creates 6 by 7 matrix
        self.board = [["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"]]
        self.game_over = False #game_over for this board

    def valid(self, board, column):
        column -= 1
        for r in range(ROW_COUNT):
            if self.board[r][column] == "0":
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
        
        self.board[ROW_COUNT - 1][column] = "0"

    def get_first_empty_spot_in_column(self, column):
        for i in range(ROW_COUNT):
            if self.board[i][column] == "0":
                return i
        
        return -1
    
    #getter function for game_over
    def game_over(self):
        return self.game_over
    #getter function for print board
    def print_board(self):
        for i in range(len(ROW_COUNT)-1, -1, -1):
            for c in range(len(COLUMN_COUNT)):
                print(self.board[i][c], end=" ")
            print("\n")
    
    def check_win(self,coin):
        #check horizontally
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-4):
                if self.board[r][c] == coin and self.board[r][c+1] == coin and self.board[r][c+2] == coin and self.board[r][c+3] == coin:
                    return True
        #check vertically
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT-4):
                if self.board[r][c] == coin and self.board[r+1][c] == coin and self.board[r+2][c] == coin and self.board[r+3][c] == coin:
                    return True
        #check for a positive slope diagnal
        for c in range(COLUMN_COUNT-4):
            for r in range(ROW_COUNT-4):
                if self.board[r][c] == coin and self.board[r+1][c+1] == coin and self.board[r+2][c+2] == coin and self.board[r+3][c+3] == coin:
                    return True
        #check for a negative slope
        for c in range(COLUMN_COUNT-4):
            for r in range(ROW_COUNT-4):
                if self.board[r][c] == coin and self.board[r-1][c+1] == coin and self.board[r-2][c+2] == coin and self.board[r-3][c+3] == coin:
                    return True
        
        
def PvP():
    Board = board()
    turn = 0
    print("Player 1 and Player 2 will enter a character symbol for their coin\n")
    player_one_symbol = input("Player 1: Please enter your symbol\n")
    player_two_symbol = input("Player 2: Please enter your symbol\n")
    
    while player_one_symbol == player_two_symbol:
        print("Same symbols\n")
        player_one_symbol = input("Player 1: Please enter your symbol\n")
        player_two_symbol = input("Player 2: Please enter your symbol\n")
    
    running = True
    while (running):

        userinput = input("What do you want to do with your coin\n")
        print("1. Place coin\n")
        print("2. Pop coin\n")
        print("3. Quit\n")


        if userinput == "Quit":
            running = False
            break

        elif userinput == "Place coin":
            col = input("Player 1: Select where to drop (1 - " + str(COLUMN_COUNT) + "):")
            
            if (not col.isnumeric()):
                print("Error, invalid input")
            
            else:
                if turn % 2 == 0:
                    Board.place_coin(int(col), player_one_symbol)
                else:
                    Board.place_coin(int(col), player_two_symbol)
                turn += 1
        
        elif userinput == "Pop coin":
            col = input("Player 1: Select where to remove (1 - " + str(COLUMN_COUNT) + "):")

            if (not col.isnumeric()):
                print("Error, invalid input")
                running = False
            else:
                Board.remove_Coin(int(col))
                running = False
    
        
        Board.print_board()
        #Change 2 and 6 to find wins
        if Board.check_win(player_one_symbol):
            print("Player 1 wins!!")
            running = False
        elif Board.check_win(player_two_symbol):
            print("Player 2 wins!!")
            running = False

def PvC():
    Board = board()
    turn = 0
    
    print("Player, Enter a Symbol")
    userinput = input()

    print("Player will enter a character symbol for their coin\n")
    player_symbol = input("Player: Please enter your symbol\n")
    AI_symbol = "I"
    
    while player_symbol == AI_symbol:
        print("Same symbols\n")
        player_symbol = input("Player: Please enter your symbol\n")

    running = True
    while (running):

        userinput = input("What do you want to do with your coin\n")
        print("1. Place coin\n")
        print("2. Pop coin\n")
        print("3. Quit\n")

        if userinput == "Quit":
            running = False
            break


        elif userinput == "Place coin":
            col = input("Player: Select where to drop coin (1 - " + str(COLUMN_COUNT) + "):")
            
            if (not col.isnumeric()):
                print("Error, invalid input")
            
        
        elif userinput == "Pop coin":
            col = input("Player: Select where to remove coin (1 - " + str(COLUMN_COUNT) + "):")

            if (not col.isnumeric()):
                print("Error, invalid input")
            else:
                Board.remove_Coin(int(col))
                running = False
    
        
        Board.print_board()
        #Change 2 and 6 to find wins
        if Board.check_win(player_symbol):
            print("The player wins!!")
            running = False
        elif Board.check_win(AI_symbol):
            print("The computer wins!!")
            running = False
    
def print_menu():
    print("Welcome to Connect 4++!")
    
    running = True

    while running:
    
        print("User Menu:")
        print("1. Player vs AI")
        print("2. Player vs Player")
        userInput = input("Please select an option: ") #whatever user inputs will be stored in userInput

        if userInput == "Player vs AI" or userInput == "Player vs Player":
            running = False
            break
        
        print()

    return userInput


def main():

    userInput = print_menu()

    if userInput == "Player vs AI":
        PvC()
    elif userInput == "Player vs Player":
        PvP()


    



if __name__ == "__main__":
    main()
