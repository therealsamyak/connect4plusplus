import pygame
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

    def valid(self, board, position):
        for r in range(ROW_COUNT):
            if self.board[r][position] == 0:
                return True
        return False
    
    def place_coin(self, column, piece):
        self.board[self.get_first_empty_spot_in_column(column)][column] = piece

    def get_first_empty_spot_in_column(self, column):
        for i in range(ROW_COUNT):
            if self.board[i][column] == 0:
                return i
    
    #getter function for game_over
    def game_over(self):
        return self.game_over
    #getter function for print board
    def print_board(self):
        print(self.board)

def main():
    Board = board()
    turn = 0
    Board.print_board()
    print("Hihi")
    


if __name__ == "__main__":
    main()

