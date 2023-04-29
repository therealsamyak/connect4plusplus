import pygame
import random
import numpy as np

random.seed(0)

ROW_COUNT = 6
COLUMN_COUNT = 7

class board:
    #Default Constructor (doesn't return )
    # def __init__(self):
    #     #creates 6 by 7 matrix
    #     self.board = [["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0", "0"]]
    #     self.game_over = False #game_over for this board
    
    def __init__(self, num_rows, num_columns):
        self.board = []
        column = []
        i = 0
        j = 0
        while (i < num_rows):
            while (j < num_columns):
                column.append("0")
                j += 1
            self.board.append(column)
            column = []
            j = 0
            i += 1
        
        self.game_over = False

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
        column -= 1
        row = self.get_first_empty_spot_in_column(column)
        if row < 0:
            print("Invalid Row")
            return
        else:
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
        for i in range(ROW_COUNT - 1, -1, -1):
            print("|", end="")
            for c in range(COLUMN_COUNT):
                print(self.board[i][c], end = " ")
            print("|")


    
    def check_tie(self):
        checker_Full = True
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                if self.board[i][j] == '0':
                    checker_Full = False
                    break
        return checker_Full
            


    def check_win(self,coin):

        r = 0
        #vertically bottom-up except while loop
        while (r + 3 < ROW_COUNT):
            for columns in range(COLUMN_COUNT):
                # print(r, c)
                if self.board[r][columns] == coin and self.board[r+1][columns] == coin and self.board[r+2][columns] == coin and self.board[r+3][columns] == coin:
                    return True
            r += 1
        #horizontally left-right except while loop
        c = 0
        while(c + 3 < COLUMN_COUNT):
            for rows in range(ROW_COUNT):
                if self.board[rows][c] == coin and self.board[rows][c+1] == coin and self.board[rows][c+2] == coin and self.board[rows][c+3] == coin:
                    return True
            c += 1
        
        #check for a positive slope diagnal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == coin and self.board[r+1][c+1] == coin and self.board[r+2][c+2] == coin and self.board[r+3][c+3] == coin:
                    return True
        
        #check for a negative slope
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == coin and self.board[r-1][c+1] == coin and self.board[r-2][c+2] == coin and self.board[r-3][c+3] == coin:
                    return True
        
        return False


def PvP():
    Board = board(6, 7)
    turn = 0
    print("Player 1 and Player 2 will enter a character symbol for their coin")
    player_one_symbol = input("Player 1: Please enter your symbol\n")
    player_two_symbol = input("Player 2: Please enter your symbol\n")
    
    while player_one_symbol == player_two_symbol and player_one_symbol != '0' and player_two_symbol != '0':
        print("Same symbols or one or more players' symbols are 0")
        player_one_symbol = input("Player 1: Please enter your symbol\n")
        player_two_symbol = input("Player 2: Please enter your symbol\n")
    
    running = True
    while (running):

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("What do you want to do with your coin\n")


        if userinput == "3":
            running = False
            break

        elif userinput == "1":
            col = input("Player 1: Select where to drop (1 - " + str(COLUMN_COUNT) + "): ")
            
            if (not col.isnumeric()):
                print("Error, invalid input")
            
            else:
                if turn % 2 == 0:
                    Board.place_coin(int(col), player_one_symbol)
                else:
                    Board.place_coin(int(col), player_two_symbol)
                turn += 1
        
        elif userinput == "2":
            col = input("Player 2: Select where to remove (1 - " + str(COLUMN_COUNT) + "): ")

            if (not col.isnumeric()):
                print("Error, invalid input")
                running = False
            else:
                Board.remove_Coin(int(col))
                running = False
    
        print()
        Board.print_board()
        print()
        #Change 2 and 6 to find wins
        if Board.check_win(player_one_symbol):
            print("Player 1 wins!!")
            running = False
        elif Board.check_win(player_two_symbol):
            print("Player 2 wins!!")
            running = False
        elif Board.check_tie():
            print("We have a tie")
            running = False

def PvC():
    Board = board(6, 7)
    turn = 0
    
    print("Player, Enter a Symbol")
    userinput = input()

    print("Player will enter a character symbol for their coin\n")
    player_symbol = input("Player: Please enter your symbol\n")
    AI_symbol = "A"
    
    while player_symbol == AI_symbol and player_symbol != '0':
        print("Same symbols or player's symbol is 0\n")
        player_symbol = input("Player: Please enter your symbol\n")

    running = True
    while (running):

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("What do you want to do with your coin\n")

        if userinput == "3":
            running = False
            break


        elif userinput == "1":
            col = input("Player: Select where to drop coin (1 - " + str(COLUMN_COUNT) + "): ")
            
            if (not col.isnumeric()):
                print("Error, invalid input")
            
        
        elif userinput == "2":
            col = input("Player: Select where to remove coin (1 - " + str(COLUMN_COUNT) + "): ")

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
        elif Board.check_tie():
            print("We have a tie")
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
        PvC()
    elif userInput == "2":
        PvP()


    



if __name__ == "__main__":
    main()
