''' This module is a computer module.'''

from unicodedata import name
from player_module import Player
from round_module import round_module
import random

class Computer(Player):
    '''
    Class Computer initializes computer
    '''
    def make_a_move(self, cover_squares_available, uncover_squares_available, hint):
        '''
            Function Name: make_a_move
            Purpose: Computer either makes a move or suggests a move
            Parameters: cover_squares_available, uncover_squares_available, hint
            Return Value: Return the best move, to_cover_or_to_uncover, and the hint message
            Algorithm:
                    1) Determines which move optimizes the chances of winning and makes the move
                    2) If hint is True, suggests the player to make a move that optimizes the chances of winning
        '''

        def get_best_move(self, squares_moves):
            '''
            Function Name: get_best_move
            Purpose: Get the best move
            Parameters: squares_moves
            Return Value: Return the best move
            Algorithm:
                    1) Compare all the possible moves and return the move that has the highest number
            '''
            best_move = 0
            max_square = 0

            for move in squares_moves:
                if type(move) == int:
                    best_move = move
                    break
                else:
                    for square in move:
                        if square > max_square:
                            max_square = square
                            best_move = move
            return best_move


        def to_cover_or_to_uncover(self):
            '''
                Function Name: get_best_move
                Purpose: Get the best move
                Parameters: squares_moves
                Return Value: true for cover, false otherwise
                Algorithm:
                        1) If the opponent has more uncovered squares than self covered, cover own squares
                        2) If the opponent has more covered squares than self uncovered, uncover their squares
                        3) If the number of self covered squares equal the number of opponent's uncovered,
                            choose the side that gives more number of squares
            '''
            reason = ""

            if self.round_module.current_player == self.Player.player1_name:
                self_covered_squares = self.Player.covered_squares_player1(self)
                self_covered_squares_len = len(self_covered_squares)
                self_uncovered_squares = self.Player.uncovered_squares_player1(self)
                self_uncovered_squares_len = len(self_uncovered_squares)

                opp_covered_squares = self.Player.covered_squares_player2(self)
                opp_covered_squares_len = len(opp_covered_squares)
                opp_uncovered_squares = self.Player.uncovered_squares_player2(self)
                opp_uncovered_squares_len = len(opp_uncovered_squares)

            elif self.round_module.current_player == self.Player.player2_name:
                self_covered_squares = self.Player.covered_squares_player2(self)
                self_covered_squares_len = len(self_covered_squares)
                self_uncovered_squares = self.Player.uncovered_squares_player2(self)
                self_uncovered_squares_len = len(self_uncovered_squares)

                opp_covered_squares = self.Player.covered_squares_player1(self)
                opp_covered_squares_len = len(opp_covered_squares)
                opp_uncovered_squares = self.Player.uncovered_squares_player1(self)
                opp_uncovered_squares_len = len(opp_uncovered_squares)

            if opp_uncovered_squares_len <= 3 and self_uncovered_squares_len > 3:
                reason = " to minimize oppnonent's chances of winning"
                return "False", reason

            if opp_covered_squares_len > self_uncovered_squares_len:
                reason = " to maximize the number of covered squares"
                return "True", reason

            # if opp has more uncovered squares than self covered
            # cover the squares
            elif opp_uncovered_squares_len > self_covered_squares_len:
                reason = " to maximize the number of uncovered squares"
                return "False", reason

            # if cover and uncover in both sides are equal
            # check which sides gives more number of squares
            else:
                #reason = " because it gives more number of uncovered squares."
                max_square = 1
                if self_uncovered_squares:
                    for square in self_covered_squares:
                        max_square = max(square, max_square)
                if opp_uncovered_squares:
                    for square in opp_uncovered_squares:
                        if square > max_square:
                            reason = " to maximize uncovered squares"
                            return "False", reason
            # cover
                reason = " to maximize covered squares and minimize opponents score"
                return "True", reason

        moves = ()
        ## True for cover, False for uncover
        cov_or_uncov = True 
        message = ""
        # check to see if squares are only available for covers
        if len(cover_squares_available) > 0 and len(uncover_squares_available) <= 0:
            moves = get_best_move(self, cover_squares_available)
            cov_or_uncov = True
            cover_option = "True"
            if hint:
                message += "Suggestion to cover "
                if type(moves) is int:
                    message += str(moves)
                else:
                    for move in moves:
                        message += str(move) + " " 
                message += " as there are no squares left to uncover "
            message = " as there are no squares left to uncover "

        # check to see if squares are only available for uncovers
        elif len(uncover_squares_available)> 0 and len(cover_squares_available) <= 0:
            moves = get_best_move(self, uncover_squares_available)
        # check to see if squares are available for both covers and uncovers
            cov_or_uncov = False
            cover_option = "False"
            if hint:
                message += "Suggestion to uncover "
                if type(moves) is int:
                    message += str(moves)
                else:    
                    for move in moves:
                        message += str(move) + " "    
                message += " as there are no squares left to cover "
            message += " as there are no squares left to cover"
            
        elif uncover_squares_available and uncover_squares_available:
            cover_option, reason = to_cover_or_to_uncover(self)
            message += reason
            if cover_option == "True":
                moves = get_best_move(self, cover_squares_available)
                cov_or_uncov = True
                if hint:
                    message += "Suggestion to cover " 
                    if type(moves) is int:
                        message += str(moves)
                    else:
                        for move in moves:
                            message += str(move) + " "
                    message += reason    
            else:
                moves = get_best_move(self, uncover_squares_available)
                cov_or_uncov = False

                if hint:
                    message += "Suggestion to uncover " 
                    if type(moves) is int:
                        message += str(moves)
                    else:
                        for move in moves:
                            message += str(move) + " "
                    message += reason    
            
        return moves, cov_or_uncov, message

    def roll(self):
        '''
                Function Name: roll
                Purpose: To roll the dice and get values
                Parameters: self
                Return Value: die1, die2
                Algorithm:
                        1) Randomly generate 2 numbers between 1 and 6
                        2) Return those numbers
        '''
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        return die1, die2
