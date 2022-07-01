from round_module import round_module
''' Player module'''
class Player:

    '''Player Class initialized methods for cover and uncover'''

    def __init__(self, player1_name, player1_score, player1_last_round_score,
                 player1_first_turn,
                 player2_name, player2_score,
                 player2_last_round_score, player2_first_turn,
                first_roll, player1_total, player2_total
                 ):
        '''
        Function Name: __init__
        Purpose: Initialize a Player Class
        Parameters: self, player1_name, player1_score, player1_last_round_score,
                 player1_first_turn,
                 player2_name, player2_score,
                 player2_last_round_score, player2_first_turn,
                first_roll, player1_total, player2_total
        Return Value: None
        Algorithm: Initialize members with default values
        '''
        self.player1_score = player1_score
        self.player1_last_round_score = player1_last_round_score
        self.player1_first_turn = player1_first_turn
        #self.player1_advantage_score = player1_advantage_score
        self.player1_board_squares = []
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player2_score = player2_score
        self.player2_last_round_score = player2_last_round_score
        self.player2_first_turn = player2_first_turn
        #self.player2_advantage_score = player2_advantage_score
        self.player2_board_squares = []
        #self.first_roll = first_roll
        self.player1_total = player1_total
        self.player2_total = player2_total
        self.player1_last_round_first_turn =  False
        self.player2_last_round_first_turn = False
        #self.combinations = []

    def covered_squares_player1(self):
        '''
        Function Name: covered_squares_player1
        Purpose: To get a list of all covered squares for player1
        Parameters: self
        Return Value: Return the list of covered squares for player1
        Algorithm:
                1) Append the square in the squares_covered list if its
                  value is True
        '''
        squares_covered = []
        length_board_squares = self.round_module.squares
        i = length_board_squares -1
        #print(self.round_module.player1_squares)
        for square in self.round_module.player1_squares:
            if square:
                squares_covered.append(length_board_squares - i)
            i -= 1
        #print(squares_covered)
        return squares_covered

    def covered_squares_player2(self):
        '''
        Function Name: covered_squares_player2
        Purpose: To get a list of all covered squares for player2
        Parameters: self
        Return Value: Return the list of covered squares for player2
        Algorithm:
                1) Append the square in the squares_covered list if its
                  value is True
        '''
        squares_covered = []
        length_board_squares = self.round_module.squares
        i = length_board_squares - 1
        #print(self.round_module.player2_squares)
        for square in self.round_module.player2_squares:
            if square:
                squares_covered.append(length_board_squares - i)
            i -= 1
        #print(squares_covered)
        return squares_covered

    def uncovered_squares_player1(self):
        '''
        Function Name: uncovered_squares_player1
        Purpose: To get a list of all uncovered squares for player1
        Parameters: self
        Return Value: Return the list of uncovered squares for player1
        Algorithm:
                1) Append the square in the uncovered_squares list if its
                  value is True
        '''
        uncovered_squares = []
        length_board_squares = self.round_module.squares
        i = length_board_squares - 1
        #print(self.round_module.player1_squares)
        for square in self.round_module.player1_squares:
            if not square:
                uncovered_squares.append(length_board_squares - i)
            i -= 1
        #print(uncovered_squares)
        return uncovered_squares


    def uncovered_squares_player2(self):
        '''
        Function Name: uncovered_squares_player2
        Purpose: To get a list of all uncovered squares for player2
        Parameters: self
        Return Value: Return the list of uncovered squares for player2
        Algorithm:
                1) Append the square in the uncovered_squares list if its
                  value is True
        '''
        uncovered_squares = []
        length_board_squares = self.round_module.squares
        i = length_board_squares - 1
        #print(self.round_module.player2_squares)
        for square in self.round_module.player2_squares:
            if not square:
                uncovered_squares.append(length_board_squares - i)
            i -= 1
        #print(uncovered_squares)
        return uncovered_squares

    def isCovered_player1(self):
        '''
        Function Name: isCovered_player1
        Purpose: To check if all the squares of player1 is covered
        Parameters: self
        Return Value: True if all squares covered, False otherwise
        Algorithm:
                1) Check all the values of the squares,
                 return False if any of the squares is False
        '''
        for square in self.round_module.player1_squares:
            if square == False:
                return False
        return True

    def isCovered_player2(self):
        '''
        Function Name: isCovered_player2
        Purpose: To check if all the squares of player2 is covered
        Parameters: self
        Return Value: True if all squares covered, False otherwise
        Algorithm:
                1) Check all the values of the squares,
                 return False if any of the squares is False
        '''
        for square in self.round_module.player2_squares:
            if square == False:
                return False
        return True

    def isUncovered_player1(self):
        '''
        Function Name: isUncovered_player1
        Purpose: To check if all the squares of player1 is uncovered
        Parameters: self
        Return Value: True if all squares uncovered, False otherwise
        Algorithm:
                1) Check all the values of the squares,
                 return False if any of the squares is True
        '''
        for square in self.round_module.player1_squares:
            if square == True:
                return False
        return True

    def isUncovered_player2(self):
        '''
        Function Name: isUncovered_player2
        Purpose: To check if all the squares of player2 is uncovered
        Parameters: self
        Return Value: True if all squares uncovered, False otherwise
        Algorithm:
                1) Check all the values of the squares,
                 return False if any of the squares is True
        '''
        for square in self.round_module.player2_squares:
            if square == True:
                return False
        return True

    def is7Up(self, player, covered_squares):
        '''
        Function Name: is7Up
        Purpose: To check if all the squares from 7 to n is covered
        Parameters: player, covered_squares
        Return Value: True if all squares from 7 to n is covered, False otherwise
        Algorithm:
                1) Check all the values of the squares,
                 return False if any of the squares is True
        '''
        check = []
        check_flag = False

        for i in range(7, self.round_module.squares + 1):
            check.append(i)

        if player == "player1":
            for items in check:
                    if items not in covered_squares:
                        check_flag = True

        elif player == "player2":
            for items in check:
                    if items not in covered_squares:
                        check_flag = True
        if check_flag == True:     
            return False
        else:
            return True
