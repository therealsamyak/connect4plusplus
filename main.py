import time
import random
import copy

random.seed(time.time())  #seeding the random function to the current time

class board:
    
    def __init__(self, num_rows, num_columns):
        '''
        Default constructor
        '''
        self.num_rows = num_rows
        self.num_columns = num_columns
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
        self.AI_COIN = "A"
        self.PLAYER_COIN = "*"

    def copy(self):
        '''
        Copy constructor
        '''
        temp_class = board(self.num_columns, self.num_rows)
        temp_class.board = copy.deepcopy(self.board)
        temp_class.game_over = self.game_over

        return temp_class

        
    def valid(self, column):
        '''
        Checks whether the spot inputted is free or not 
        '''
        column -= 1
        for r in range(self.num_rows):
            if self.board[r][column] == "0":
                return True
        return False
    
    def place_coin(self, column, piece):
        '''
         Function that substitutes a 0 with a player's value
        '''
        if (column > self.num_columns or column <= 0):
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
        '''
        Removes the bottom most coin of the column inputted and brings down the coins above
        '''
        if (column > self.num_columns or column <= 0):
            print("Invalid Column")
            return
        column -= 1
        self.board[0][column] = 0
        for r in range(1, self.num_rows - 1):
            self.board[r - 1][column] = self.board[r][column]
        
        self.board[self.num_rows - 1][column] = "0"

    def get_first_empty_spot_in_column(self, column):
        '''
        Returns the first empty position going up the column
        '''
        for i in range(self.num_rows):
            if self.board[i][column] == "0":
                return i
        
        return -1
    
    #getter function for game_over
    def game_over(self):
        '''
        Returns state of game_over
        '''
        return self.game_over
    
    #getter function for print board
    def print_board(self):
        '''
        Prints out the current board 
        '''
        for i in range(self.num_rows - 1, -1, -1):
            print("║ ", end="")
            for c in range(self.num_columns):
                print(self.board[i][c], end = " ")
            print("║")


    
    def check_tie(self):
        '''
        Checks whether we had a tie or not
        '''
        checker_Full = True
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self.board[i][j] == "0":
                    checker_Full = False
                    break
        return checker_Full
            


    def check_win(self,coin):
        '''
        Checks conditions necessary for win: horizontal, vertical, positive slope, and negative slope
        '''
        r = 0
        #vertically bottom-up except while loop
        while (r + 3 < self.num_rows):
            for columns in range(self.num_columns):
                # print(r, c)
                if self.board[r][columns] == coin and self.board[r+1][columns] == coin and self.board[r+2][columns] == coin and self.board[r+3][columns] == coin:
                    return True
            r += 1
        #horizontally left-right except while loop
        c = 0
        while(c + 3 < self.num_columns):
            for rows in range(self.num_rows):
                if self.board[rows][c] == coin and self.board[rows][c+1] == coin and self.board[rows][c+2] == coin and self.board[rows][c+3] == coin:
                    return True
            c += 1
        
        #check for a positive slope diagnal
        for c in range(self.num_columns-3):
            for r in range(self.num_rows-3):
                if self.board[r][c] == coin and self.board[r+1][c+1] == coin and self.board[r+2][c+2] == coin and self.board[r+3][c+3] == coin:
                    return True
        
        #check for a negative slope
        for c in range(self.num_columns-3):
            for r in range(3, self.num_rows):
                if self.board[r][c] == coin and self.board[r-1][c+1] == coin and self.board[r-2][c+2] == coin and self.board[r-3][c+3] == coin:
                    return True
        
        return False
    #Helper Functions only for AI moderate difficulty
    def drop_piece(self,row,col,coin):
        '''
        Depending upon if it's player or ai inputs their symbol on that matrix location
        '''
        self.board[row][col] = coin

    def get_next_open_row(self,col):
        '''
        Returns the next empty row index up in the column inputted
        '''
        for r in range(self.num_rows-1):
            if self.board[r][col] == "0":
                return r
            
        return -1
        
        

    def is_valid_location(self,col):
        '''
        Returns whether the topmost position of the column is empty or not
        '''
        return self.board[self.num_rows-1][col] == "0"

    def get_valid_locations(self):
        '''
        Return array of possible columns free that AI can choose from
        '''
        valid_locations = []
        for col in range(self.num_columns):
            if self.valid(col):
                valid_locations.append(col)
        return valid_locations
    def update_coins(self, aiCoin,playerCoin):
        '''
        Updates the characters/ symbols used for the player and ai's turn
        '''
        AI_COIN = aiCoin
        PLAYER_COIN = playerCoin
    #Helper Function To find Score of player
    def evaluate_window(self, window, player_coin, ai_coin, coinType):
        '''
        Returns the score for 4 in a row, 3 in a row, 2 in a row, and finally opponent's score if they had 3 in a row. The score is used by the AI to determine the best possible column to drop its coin in
        '''
        EMPTY = 0
        score = 0
        opp_coin = player_coin
        if(coinType == player_coin):
            opp_coin = ai_coin
        if window.count(coinType) == 4:
            score += 10000
        elif window.count(coinType) == 3 and window.count(EMPTY) == 1:
            score += 1000
        elif window.count(coinType) == 2 and window.count(EMPTY) == 2:
            score += 250
        if window.count(opp_coin) == 3 and window.count(EMPTY) == 1:
            score -= 40

        return score

    def score_position(self,coinType):
        '''
        Calculates score similar to previous functions for moves done in the center, horizontal, vertical, and diagonals. Adding the score will determine the best possible move used by AI to act "intelligently"
        '''
        WINDOW_LENGTH = 4
        SCORE = 0
        EMPTY = "0"
        #score center column
        center_array = [i for i in list(self.board[0 : self.num_columns//2])]
        center_count = center_array.count(coinType)
        SCORE += center_count * 3
        #Score Horizontal
        for r in range(self.num_rows):
            row_array = [i for i in list(self.board[r : ])]
            for c in range(self.num_columns-3):
                window = row_array[c: c+WINDOW_LENGTH]
                #4 ina row winning
                if window.count(coinType) == 4:
                    SCORE += 100
                #3 in a row
                elif window.count(coinType) == 3 and window.count(EMPTY) == 1:
                    SCORE += 10
        #Score Vertical
        for c in range(self.num_columns):
            col_array = [i for i in list(self.board[0 : c])]
            for c in range(self.num_columns - 3):
                window = row_array[c : c + WINDOW_LENGTH]
                SCORE += self.evaluate_window(window, self.PLAYER_COIN, self.AI_COIN, coinType)
        
        #Score positive sloped diagonal
        for r in range(self.num_rows - 4):
            for c in range(self.num_columns - 4):
                window = [self.board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                SCORE += self.evaluate_window(window, self.PLAYER_COIN, self.AI_COIN, coinType)
        #Score negatively sloped diagonal
        for r in range(self.num_rows - 4):
            for c in range(self.num_columns - 4):
                window = [self.board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                SCORE = self.evaluate_window(window, self.PLAYER_COIN, self.AI_COIN, coinType)
        return SCORE

    def pick_best_move(self,coinType):
        '''
        Out of valid locations AI can put into and depending upon the best possible score choose that position for AI to put its coin there
        '''
        valid_locations = self.get_valid_locations()
        best_col = random.choice(valid_locations)
        best_score = 0
        for col in valid_locations:
            row = self.get_next_open_row(col)
            if (row != -1):
                
                temp_board = self.copy()
                temp_board.drop_piece(row,col,coinType)
                score = temp_board.score_position(coinType)
                if score > best_score:
                    best_score = score
                    best_col = col

        return best_col + 1
##
##
##  NOT IN CLASS AFTER THIS LINE!!!!!!!!!
##
##

def load_words():
    '''
    returns list of words that can be used by the AI to make game entertaining from a list of dialogues in Lines.txt generated from ChatGPT
    '''
    inFile = open("Lines.txt")
    wordlist = []
    for line in inFile:
        new_line = line.split("\n")
        wordlist.append(new_line[0])
    return wordlist



def PvP(num_rows, num_columns):
    '''
    Sets up player vs player game mode
    '''
    Board = board(num_rows, num_columns)
    turn = 2
    print("Player 1 and Player 2 will enter a character symbol for their coin")
    player_one_symbol = input("Player 1, please enter your symbol: ")
    player_two_symbol = input("Player 2, please enter your symbol: ")
    
    while player_one_symbol == player_two_symbol or player_one_symbol == "0" or player_two_symbol == "0":
        print("Both players have the same symbol, or one of the players has an invalid symbol.")
        player_one_symbol = input("Player 1, please enter your symbol: ")
        player_two_symbol = input("Player 2, please enter your symbol: ")

    
    running = True
    while (running):
        print()
        Board.print_board()
        print()


        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("Player " + str((turn % 2) + 1) + ", what do you want to do with your coin? ")
        print()

        if userinput in ["3", "Quit", "quit", "q","Q"]:
            running = False
            break

        elif userinput == "1":
            col = input("Player " + str((turn % 2) + 1) + ": Select where to place (1 - " + str(Board.num_columns) + "): ")
            
            if (not col.isnumeric()):
                print("Error, invalid input")
            
            else:
                if turn % 2 == 0:
                    Board.place_coin(int(col), player_one_symbol)
                else:
                    Board.place_coin(int(col), player_two_symbol)
                turn += 1
        
        elif userinput == "2":
            col = input("Player " + str((turn % 2) + 1) + ": Select where to remove (1 - " + str(Board.num_columns) + "): ")

            if (not col.isnumeric()):
                print("Error, invalid input")
            else:
                Board.remove_Coin(int(col))
    
    
        if Board.check_win(player_one_symbol):
            print()
            print("Player 1 wins!!")
            print()
            Board.print_board()
            print()
            Board.game_over = True
            running = False
        elif Board.check_win(player_two_symbol):
            print()
            print("Player 2 wins!!")
            print()
            Board.print_board()
            print()
            Board.game_over = True
            running = False
        elif Board.check_tie():
            print()
            print("We have a tie!")
            print()
            Board.print_board()
            print()
            Board.game_over = True
            running = False
        

def PvEasy(num_rows, num_columns):
    '''
    Sets up player vs easy ai game mode
    '''
    AI_voicelines = load_words()

    Board = board(num_rows, num_columns)
    print("Your Opponent: Random Robbie!!")
    print()

    print("Player will enter a character symbol for their coin\n")
    player_symbol = input("Player, please enter your symbol: ")
    AI_symbol = "A"
    
    while player_symbol == AI_symbol or player_symbol == "0":
        print("This symbol is not valid. Please enter another symbol. ")
        player_symbol = input("Player, please enter your symbol: ")

    running = True
    while (running):
        print()
        Board.print_board()
        print()

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("Player: What do you want to do with your coin? ")
        print()

        if userinput in ["3", "Quit", "quit", "q","Q"]:
            running = False
            break


        elif userinput == "1":
            col = input("Player : Select where to place (1 - " + str(Board.num_columns) + "): ")
            if (not col.isnumeric()):
                print("Error, invalid input")
            
            else:
                Board.place_coin(int(col), player_symbol)
            
        elif userinput == "2":
            col = input("Player: Select where to remove coin (1 - " + str(Board.num_columns) + "): ")

            if (not col.isnumeric()):
                print("Error, invalid input")
            else:
                Board.remove_Coin(int(col))
                running = False

        AI_column = random.randint(1, Board.num_columns)

        while (Board.get_first_empty_spot_in_column(AI_column - 1) == -1):
            AI_column = random.randint(1, Board.num_columns)
        
        Board.place_coin(AI_column, AI_symbol)
        print("Robbie Placed Coin in Column: " + str(AI_column) + ".")
        
        
        randomLine = random.randint(0, len(AI_voicelines) - 1)
        print("Robbie: \"" + str(AI_voicelines[randomLine]) + "\"")
        
        print()

                
        if Board.check_win(player_symbol):
            print()
            Board.print_board()
            print()
            print("The player wins!!")
            Board.game_over = True
            running = False
        elif Board.check_win(AI_symbol):
            print()
            Board.print_board()
            print()
            print("The computer wins!!")
            Board.game_over = True
            running = False
        elif Board.check_tie():
            print()
            Board.print_board()
            print()
            print("We have a tie")
            Board.game_over = True
            running = False
            print()


def PvMod(num_rows, num_columns):
    '''
    Sets up player vs moderate ai gamemode
    '''
    AI_voicelines = load_words()
    
    Board = board(num_rows, num_columns)
    
    print("Your Opponent: Mediocre Matthew!!")
    print()
    print("Player will enter a character symbol for their coin\n")
    player_symbol = input("Player, please enter your symbol: ")
    AI_symbol = "A"
    
    while player_symbol == AI_symbol or player_symbol == "0":
        print("This symbol is not valid. Please enter another symbol. ")
        player_symbol = input("Player, please enter your symbol: ")

    running = True
    while (running):

        print()
        Board.print_board()
        print()

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("Player, what do you want to do with your coin? ")
        print()
        col = ""

        if userinput in ["3", "Quit", "quit", "q","Q"]:
            running = False
            break


        elif userinput == "1":
            col = input("Player : Select where to place (1 - " + str(Board.num_columns) + "): ")
            if (not col.isnumeric()):
                print("Error, invalid input")
            
            else:
                Board.place_coin(int(col), player_symbol)
            
        elif userinput == "2":
            col = input("Player: Select where to remove coin (1 - " + str(Board.num_columns) + "): ")

            if (not col.isnumeric()):
                print("Error, invalid input")
            else:
                Board.remove_Coin(int(col))

        AI_column = Board.pick_best_move(AI_symbol)

        if (random.randint(1, 100) == 50):
            Board.remove_Coin(int(col))
            print("Matthew removed Coin in Column: " + str(AI_column) + ".")
        else:
            Board.place_coin(AI_column, AI_symbol)
            print("Matthew placed Coin in Column: " + str(AI_column) + ".")

        randomLine = random.randint(0, len(AI_voicelines) - 1)
        print("Matthew: \"" + str(AI_voicelines[randomLine]) + "\"")
        
        
        #Change 2 and 6 to find wins
        if Board.check_win(player_symbol):
            print()
            Board.print_board()
            print()
            print("The player wins!!")
            Board.game_over = True
            running = False
        elif Board.check_win(AI_symbol):
            print()
            Board.print_board()
            print()
            print("The computer wins!!")
            Board.game_over = True
            running = False
        elif Board.check_tie():
            print()
            Board.print_board()
            print()
            print("We have a tie")
            Board.game_over = True
            running = False
            print()
        

def main():
    '''
    main function implementation
    '''
    num_columns = 7
    num_rows = 6
    print()
    print("Welcome to Connect 4++!")
    print("Made by Samyak, Jay, Shrey")
    print()
    
    running = True
    while running:
        print("Settings: ")
        print("- Board Size: " + str(num_columns) + " x " + str(num_rows))
        print()
        print("Menu: ")
        print(" 1. Player vs Easy AI")
        print(" 2. Player vs Hard AI")
        print(" 3. Player vs Player")
        print(" 4. Change Board Size")
        print(" 5. Quit")
        userInput = input("Please select an option: ") #whatever user inputs will be stored in userInput

        if userInput == "1":
            PvEasy(num_rows, num_columns)
        
        elif userInput == "2":
            PvMod(num_rows, num_columns)

        elif userInput == "3":
            PvP(num_rows, num_columns)

        elif userInput == "4":
            
            new_column_num = input("Enter board width: ")
            num_columns = int(new_column_num)
            new_row_num = input("Enter board height: ")
            num_rows = int(new_row_num)
            
            while (num_columns * num_rows > 4000):
                print("Error. Board Size is too large. Please make the area of the board less than 4000")
                print()
                new_column_num = input("Enter board width: ")
                num_columns = int(new_column_num)
                new_row_num = input("Enter board height: ")
                num_rows = int(new_row_num)
                

            

        elif userInput in ["5", "Quit", "quit", "q","Q"]:
            break
 
        print()
    print()
    print("Thanks for playing Connect 4++!")
    print()

if __name__ == "__main__":
    main()
