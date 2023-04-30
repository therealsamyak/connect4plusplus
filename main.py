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
        Returns 
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
            print("| ", end="")
            for c in range(self.num_columns):
                print(self.board[i][c], end = " ")
            print("|")


    
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
    #Helper Functions
    def drop_piece(self,row,col,coin):
        self.board[row][col] = coin

    def get_board(self):
        return self.board

    def get_next_open_row(self,col):
        for r in range(self.num_rows-1):
            if self.board[r][col] == "0":
                return r

    def is_valid_location(self,col):
        return self.board[self.num_rows-1][col] == "0"

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.num_columns):
            if self.valid(self,col):
                valid_locations.append(col)
        return valid_locations
    def update_coins(self, aiCoin,playerCoin):
        AI_COIN = aiCoin
        PLAYER_COIN = playerCoin
    #Helper Function To find Score of player
    def evaluate_window(self, window, player_coin, ai_coin, coinType):
        EMPTY = 0
        score = 0
        opp_coin = player_coin
        if(coinType == player_coin):
            opp_coin = ai_coin
        if window.count(coinType) == 4:
            score += 100
        elif window.count(coinType) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(coinType) == 2 and window.count(EMPTY) == 2:
            score += 2
        if window.count(opp_coin) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(self,coinType):
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
        return SCORE

    def pick_best_move(self,coinType):
        valid_locations = self.get_valid_locations()
        best_col = random.choice(valid_locations)
        best_score = 0
        for col in valid_locations:
            row = self.get_next_open_row(col)
            temp_board = self.copy()
            temp_board.drop_piece(row,col,coinType)
            score = temp_board.score_position(coinType)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col + 1
##
##
##                  NOT IN CLASS AFTER THIS LINE!!!!!!!!!
##
##
def load_words():
    inFile = open("Lines.txt")
    wordlist = []
    for line in inFile:
        new_line = line.split("\n")
        wordlist.append(new_line[0])
    return wordlist



def PvP(num_rows, num_columns):
    Board = board(num_rows, num_columns)
    turn = 2
    print("Player 1 and Player 2 will enter a character symbol for their coin")
    player_one_symbol = input("Player 1: Please enter your symbol\n")
    player_two_symbol = input("Player 2: Please enter your symbol\n")
    
    while player_one_symbol == player_two_symbol and player_one_symbol != "0" and player_two_symbol != "0":
        print("Same symbols or one or more players' symbols are 0")
        player_one_symbol = input("Player 1: Please enter your symbol\n")
        player_two_symbol = input("Player 2: Please enter your symbol\n")

        player_one_symbol = " " + player_one_symbol + " "
        player_two_symbol = " " + player_two_symbol + " "
    
    running = True
    while (running):

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("Player " + str((turn % 2) + 1) + ": What do you want to do with your coin?\n")

        if userinput == "3":
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
        

def PvEasy(num_rows, num_columns):
    AI_voicelines = load_words()

    Board = board(num_rows, num_columns)
    print("Your Opponent: Random Robbie!!")
    print()

    print("Player will enter a character symbol for their coin\n")
    player_symbol = input("Player: Please enter your symbol\n")
    AI_symbol = "A"
    
    while player_symbol == AI_symbol or player_symbol == "0":
        print("Same symbols or player's symbol is 0\n")
        player_symbol = input("Player: Please enter your symbol\n")

    running = True
    while (running):

        Board.print_board()
        print()

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("Player: What do you want to do with your coin?\n")

        if userinput == "3":
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

        #Change 2 and 6 to find wins
        if Board.check_win(player_symbol):
            print("The player wins!!", end=" ")
            print("Thanks for playing!")
            running = False
        elif Board.check_win(AI_symbol):
            print("The computer wins!!", end=" ")
            print("Thanks for playing!")
            running = False
        elif Board.check_tie():
            print("We have a tie", end=" ")
            print("Thanks for playing!")
            running = False

def PvMod(num_rows, num_columns):
    Board = board(num_columns, num_rows)
    

    print("Player will enter a character symbol for their coin\n")
    player_symbol = input("Player: Please enter your symbol\n")
    AI_symbol = "A"
    
    while player_symbol == AI_symbol or player_symbol == "0":
        print("Same symbols or player's symbol is 0\n")
        player_symbol = input("Player: Please enter your symbol\n")

    running = True
    while (running):

        print()
        Board.print_board()
        print()

        print("Options:")
        print("1. Place coin")
        print("2. Pop coin")
        print("3. Quit")
        userinput = input("Player: What do you want to do with your coin?\n")
        col = ""

        if userinput == "3":
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
            print("AI removed Coin in Column: " + str(AI_column) + ".")
        else:
            Board.place_coin(AI_column, AI_symbol)
            print("AI Placed Coin in Column: " + str(AI_column) + ".")
        
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

def main():
    num_columns = 6
    num_rows = 7

    print("Welcome to Connect 4++!")
    
    running = True
    while running:
        print("1. Player vs Easy AI")
        print("2. Player vs Hard AI")
        print("3. Player vs Player")
        print("4. Change Board Size")
        print("5. Quit")
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

        elif userInput in ["5", "Quit", "quit", "q","Q"]:
            print("Thanks for playing!")
            break
 
        print()

if __name__ == "__main__":
    main()
